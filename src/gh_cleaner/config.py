"""Configuration helpers for CLI and composite-action environments."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import timedelta

from .utils import parse_duration


@dataclass
class Config:
    token: str
    repo: str
    dry_run: bool = True
    keep_latest: int = 10
    older_than: timedelta = timedelta(days=30)
    workflow: str | None = None
    status: str | None = None
    branch: str | None = None
    delete_runs: bool = True
    delete_artifacts: bool = True
    artifact_name: str | None = None

    def __post_init__(self):
        if self.repo.count("/") != 1 or not all(self.repo.split("/")):
            raise ValueError("repo must be owner/name")
        if self.keep_latest < 0:
            raise ValueError("keep_latest cannot be negative")
        if self.older_than <= timedelta(0):
            raise ValueError("older_than must be positive")

    @classmethod
    def from_env(cls) -> Config:
        """Build configuration from GitHub Action INPUT_* variables."""

        def flag(name: str, default: bool) -> bool:
            return os.getenv(name, str(default)).strip().lower() not in {"0", "false", "no", "off"}

        repo = os.getenv("GITHUB_REPOSITORY", "")
        return cls(
            os.getenv("GITHUB_TOKEN", ""),
            repo,
            flag("INPUT_DRY_RUN", True),
            int(os.getenv("INPUT_KEEP_LATEST", "10")),
            parse_duration(os.getenv("INPUT_OLDER_THAN", "30d")),
            os.getenv("INPUT_WORKFLOW") or None,
            os.getenv("INPUT_STATUS") or None,
            os.getenv("INPUT_BRANCH") or None,
            flag("INPUT_DELETE_RUNS", True),
            flag("INPUT_DELETE_ARTIFACTS", True),
            os.getenv("INPUT_ARTIFACT_NAME") or None,
        )
