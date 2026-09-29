"""Plan and audit-report serialization helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .cleaner import CleanStats


def write_plan(path: str | Path, repo: str, entries: list[dict[str, Any]]) -> None:
    """Write an explicit deletion plan that can be reviewed before applying."""
    payload = {"version": 1, "repo": repo, "entries": entries}
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_plan(path: str | Path) -> dict[str, Any]:
    """Load and minimally validate a JSON plan file."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("version") != 1 or not isinstance(payload.get("entries"), list):
        raise ValueError("unsupported or malformed plan file")
    return payload


def report_payload(repo: str, stats: CleanStats) -> dict[str, Any]:
    """Build a stable JSON-compatible audit payload."""
    return {
        "version": 1,
        "repo": repo,
        "summary": {
            "runs_deleted": stats.runs_deleted,
            "artifacts_deleted": stats.artifacts_deleted,
            "caches_deleted": stats.caches_deleted,
            "runs_skipped": stats.runs_skipped,
            "artifacts_skipped": stats.artifacts_skipped,
            "caches_skipped": stats.caches_skipped,
            "failures": stats.failures,
        },
        "items": stats.plan,
    }


def write_report(path: str | Path, repo: str, stats: CleanStats, fmt: str = "json") -> None:
    """Write an audit report as JSON or CSV."""
    target = Path(path)
    if fmt == "csv" or target.suffix.lower() == ".csv":
        rows = stats.plan
        fields = ["kind", "id", "name", "created_at", "updated_at", "size_in_bytes", "reason", "error"]
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        target.write_text(json.dumps(report_payload(repo, stats), indent=2, sort_keys=True) + "\n", encoding="utf-8")
