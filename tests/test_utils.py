from datetime import timedelta, timezone

import pytest

from gh_cleaner.utils import parse_duration, parse_github_repo, utcnow


def test_parse_duration():
    assert parse_duration("2w") == timedelta(days=14)
    assert parse_duration("30d") == timedelta(days=30)


def test_bad_duration():
    with pytest.raises(ValueError):
        parse_duration("tomorrow")


def test_repo():
    assert parse_github_repo("owner/name") == ("owner", "name")
    with pytest.raises(ValueError):
        parse_github_repo("bad")


def test_utcnow_is_aware():
    assert utcnow().tzinfo == timezone.utc
