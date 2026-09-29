"""Small GitHub REST API client with pagination, retries, and permission diagnostics."""

from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from typing import Any

import requests

LOG = logging.getLogger(__name__)


class GitHubAPIError(RuntimeError):
    """An unexpected GitHub API response."""

    def __init__(self, status_code: int, message: str):
        super().__init__(f"GitHub API error {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class AuthenticationError(GitHubAPIError):
    """The token was missing or invalid."""


class PermissionDeniedError(GitHubAPIError):
    """The token is valid but cannot perform the operation."""


class GitHubAPI:
    """Requests-session wrapper for Actions runs, artifacts, and caches."""

    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "gh-cleaner/0.2.0",
            }
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Make a request, retrying transient failures and mapping auth errors."""
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        for attempt in range(4):
            LOG.debug("GitHub %s %s", method, url)
            try:
                response = self.session.request(method, url, timeout=30, **kwargs)
            except requests.RequestException as exc:
                if attempt == 3:
                    raise GitHubAPIError(0, str(exc)) from exc
                time.sleep(2**attempt)
                continue
            if response.status_code >= 500 and attempt < 3:
                time.sleep(2**attempt)
                continue
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                reset = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                time.sleep(max(0, reset - int(time.time())) + 1)
            if response.status_code == 401:
                raise AuthenticationError(401, "token is missing or invalid")
            if response.status_code == 403:
                raise PermissionDeniedError(403, response.text or "permission denied")
            if response.status_code >= 400:
                try:
                    message = response.json().get("message", response.text)
                except ValueError:
                    message = response.text
                raise GitHubAPIError(response.status_code, message)
            return response
        raise GitHubAPIError(500, "request failed after retries")

    def _paged(
        self, path: str, params: dict[str, Any] | None = None, item_keys: tuple[str, ...] = ()
    ) -> Iterator[dict[str, Any]]:
        """Yield items from GitHub list responses by following Link headers."""
        next_url = path
        first = True
        while next_url:
            response = self._request("GET", next_url, params=params if first else None)
            first = False
            data = response.json()
            keys = item_keys or ("workflow_runs", "artifacts", "actions_caches")
            for key in keys:
                if key in data:
                    yield from data[key]
                    break
            next_url = None
            for part in response.headers.get("Link", "").split(","):
                if 'rel="next"' in part:
                    next_url = part.split("<", 1)[1].split(">", 1)[0]
                    break

    def list_runs(
        self,
        repo: str,
        workflow: str | None = None,
        branch: str | None = None,
        status: str | None = None,
        event: str | None = None,
        per_page: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """List workflow runs, optionally filtered by workflow, branch, status, or event."""
        path = (
            f"/repos/{repo}/actions/runs"
            if not workflow
            else f"/repos/{repo}/actions/workflows/{workflow}/runs"
        )
        params: dict[str, Any] = {"per_page": per_page}
        if branch:
            params["branch"] = branch
        if status:
            params["status"] = status
        if event:
            params["event"] = event
        yield from self._paged(path, params, ("workflow_runs",))

    def delete_run(self, repo: str, run_id: int) -> None:
        """Delete one workflow run."""
        self._request("DELETE", f"/repos/{repo}/actions/runs/{run_id}")

    def list_artifacts(self, repo: str, name: str | None = None) -> Iterator[dict[str, Any]]:
        """List repository artifacts, optionally filtering by exact name."""
        for artifact in self._paged(
            f"/repos/{repo}/actions/artifacts", {"per_page": 100}, ("artifacts",)
        ):
            if name is None or artifact.get("name") == name:
                yield artifact

    def delete_artifact(self, repo: str, artifact_id: int) -> None:
        """Delete one artifact."""
        self._request("DELETE", f"/repos/{repo}/actions/artifacts/{artifact_id}")

    def list_caches(self, repo: str, ref: str | None = None) -> Iterator[dict[str, Any]]:
        """List Actions caches, optionally for a particular ref."""
        params: dict[str, Any] = {"per_page": 100}
        if ref:
            params["ref"] = ref
        yield from self._paged(
            f"/repos/{repo}/actions/caches", params, ("actions_caches",)
        )

    def delete_cache(self, repo: str, cache_id: int) -> None:
        """Delete one Actions cache entry."""
        self._request("DELETE", f"/repos/{repo}/actions/caches/{cache_id}")

    def repository_permissions(self, repo: str) -> dict[str, Any]:
        """Return repository metadata useful for diagnosing token permissions."""
        return self._request("GET", f"/repos/{repo}").json()
