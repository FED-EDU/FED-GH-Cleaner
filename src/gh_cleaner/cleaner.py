"""Retention policy, protected-run rules, cache cleanup, and plan generation."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from .api import GitHubAPI

LOG = logging.getLogger(__name__)


@dataclass
class CleanStats:
    """Counts and audit entries produced by a cleanup."""

    runs_deleted: int = 0
    artifacts_deleted: int = 0
    caches_deleted: int = 0
    runs_skipped: int = 0
    artifacts_skipped: int = 0
    caches_skipped: int = 0
    failures: int = 0
    plan: list[dict[str, Any]] = field(default_factory=list)


def _created(item: dict[str, Any]) -> datetime:
    value = item.get("created_at") or item.get("updated_at") or item.get("last_accessed_at")
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _branch(item: dict[str, Any]) -> str:
    return str(item.get("head_branch") or item.get("branch") or "")


def is_protected(
    run: dict[str, Any],
    *,
    exclude_workflows: tuple[str, ...] = (),
    exclude_branches: tuple[str, ...] = (),
    exclude_tags: bool = True,
    protect_default_branch_success: bool = True,
    default_branch: str | None = None,
    exclude_name_prefixes: tuple[str, ...] = (),
) -> bool:
    """Return true when a run should never be selected for deletion."""
    name = str(run.get("name") or "")
    branch = _branch(run)
    if any(value.lower() in name.lower() for value in exclude_workflows):
        return True
    if any(value.endswith("*") and branch.startswith(value[:-1]) or value == branch for value in exclude_branches):
        return True
    if exclude_tags and not branch and run.get("event") in {"push", "release"}:
        return True
    if any(name.startswith(prefix) for prefix in exclude_name_prefixes):
        return True
    return bool(
        protect_default_branch_success
        and default_branch
        and branch == default_branch
        and run.get("conclusion") == "success"
    )


def select_runs_to_delete(
    runs: list[dict[str, Any]],
    keep_latest: int,
    cutoff: datetime,
    **protection: Any,
) -> list[dict[str, Any]]:
    """Return old completed runs after retaining the newest N and protected runs."""
    ordered = sorted(runs, key=_created, reverse=True)
    candidates = [
        item
        for item in ordered[keep_latest:]
        if _created(item) < cutoff
        and item.get("status") == "completed"
        and not is_protected(item, **protection)
    ]
    return candidates


def select_artifacts_to_delete(
    artifacts: list[dict[str, Any]], keep_latest: int, cutoff: datetime
) -> list[dict[str, Any]]:
    """Return old artifacts after retaining the newest N entries."""
    ordered = sorted(artifacts, key=_created, reverse=True)
    return [item for item in ordered[keep_latest:] if _created(item) < cutoff]


def _entry(kind: str, item: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "kind": kind,
        "id": item.get("id"),
        "name": item.get("name"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "size_in_bytes": item.get("size_in_bytes") or item.get("size_in_bytes", 0),
        "reason": reason,
    }


def clean(
    api: GitHubAPI,
    repo: str,
    dry_run: bool = True,
    keep_latest: int = 10,
    older_than: timedelta = timedelta(days=30),
    workflow: str | None = None,
    status: str | None = None,
    branch: str | None = None,
    event: str | None = None,
    delete_runs: bool = True,
    delete_artifacts: bool = True,
    artifact_name: str | None = None,
    delete_caches: bool = False,
    cache_older_than: timedelta | None = None,
    max_deletions: int | None = None,
    exclude_workflows: tuple[str, ...] = (),
    exclude_branches: tuple[str, ...] = (),
    exclude_tags: bool = True,
    protect_default_branch_success: bool = True,
    default_branch: str | None = None,
    exclude_name_prefixes: tuple[str, ...] = (),
) -> CleanStats:
    """Apply a retention policy while continuing after individual failures."""
    stats = CleanStats()
    cutoff = datetime.now(timezone.utc) - older_than
    remaining = max_deletions
    protection = {
        "exclude_workflows": exclude_workflows,
        "exclude_branches": exclude_branches,
        "exclude_tags": exclude_tags,
        "protect_default_branch_success": protect_default_branch_success,
        "default_branch": default_branch,
        "exclude_name_prefixes": exclude_name_prefixes,
    }

    def allowed() -> bool:
        return remaining is None or remaining > 0

    def used() -> None:
        nonlocal remaining
        if remaining is not None:
            remaining -= 1

    if delete_runs:
        runs = list(api.list_runs(repo, workflow=workflow, branch=branch, status=status, event=event))
        for item in select_runs_to_delete(runs, keep_latest, cutoff, **protection):
            entry = _entry("run", item, f"older than {older_than}")
            stats.plan.append(entry)
            if not allowed():
                stats.runs_skipped += 1
                continue
            if dry_run:
                stats.runs_skipped += 1
                LOG.info("would delete run %s", item.get("id"))
                continue
            try:
                api.delete_run(repo, int(item["id"]))
                stats.runs_deleted += 1
                used()
            except Exception as exc:  # noqa: BLE001
                stats.failures += 1
                stats.runs_skipped += 1
                entry["error"] = str(exc)
                LOG.error("run %s failed: %s", item.get("id"), exc)

    if delete_artifacts:
        artifacts = list(api.list_artifacts(repo, name=artifact_name))
        for item in select_artifacts_to_delete(artifacts, keep_latest, cutoff):
            entry = _entry("artifact", item, f"older than {older_than}")
            stats.plan.append(entry)
            if not allowed():
                stats.artifacts_skipped += 1
                continue
            if dry_run:
                stats.artifacts_skipped += 1
                LOG.info("would delete artifact %s", item.get("id"))
                continue
            try:
                api.delete_artifact(repo, int(item["id"]))
                stats.artifacts_deleted += 1
                used()
            except Exception as exc:  # noqa: BLE001
                stats.failures += 1
                stats.artifacts_skipped += 1
                entry["error"] = str(exc)
                LOG.error("artifact %s failed: %s", item.get("id"), exc)

    if delete_caches:
        cache_cutoff = datetime.now(timezone.utc) - (cache_older_than or older_than)
        caches = sorted(api.list_caches(repo), key=_created, reverse=True)
        for item in [cache for cache in caches if _created(cache) < cache_cutoff]:
            entry = _entry("cache", item, f"older than {cache_older_than or older_than}")
            stats.plan.append(entry)
            if not allowed():
                stats.caches_skipped += 1
                continue
            if dry_run:
                stats.caches_skipped += 1
                LOG.info("would delete cache %s", item.get("id"))
                continue
            try:
                api.delete_cache(repo, int(item["id"]))
                stats.caches_deleted += 1
                used()
            except Exception as exc:  # noqa: BLE001
                stats.failures += 1
                stats.caches_skipped += 1
                entry["error"] = str(exc)
                LOG.error("cache %s failed: %s", item.get("id"), exc)
    return stats
