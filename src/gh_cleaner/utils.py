"""Small, dependency-light helpers used by the CLI and configuration layer."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta, timezone

_DURATION = re.compile(r"^(?P<amount>\d+)(?P<unit>[smhdw])$")


def parse_duration(value: str) -> timedelta:
    """Parse a duration such as 30d, 12h, 45m, 20s, or 2w."""
    match = _DURATION.fullmatch(value.strip().lower())
    if not match:
        raise ValueError("duration must look like 30d, 12h, 45m, 20s, or 2w")
    amount = int(match.group("amount"))
    seconds = amount * {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}[match.group("unit")]
    if seconds <= 0:
        raise ValueError("duration must be positive")
    return timedelta(seconds=seconds)


def format_duration(value: timedelta) -> str:
    """Format a timedelta as the largest useful whole unit."""
    seconds = int(value.total_seconds())
    for size, suffix in ((604800, "w"), (86400, "d"), (3600, "h"), (60, "m")):
        if seconds % size == 0 and seconds >= size:
            return f"{seconds // size}{suffix}"
    return f"{seconds}s"


def setup_logging(level: str) -> None:
    """Configure concise timestamped logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper()), format="%(asctime)s [%(levelname)s] %(message)s"
    )


def parse_github_repo(repo: str) -> tuple[str, str]:
    """Validate and split an owner/name repository identifier."""
    parts = repo.strip().strip("/").split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("repository must be in owner/name form")
    return parts[0], parts[1]


def utcnow() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)
