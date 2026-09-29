from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from gh_cleaner.cleaner import clean, select_runs_to_delete


def item(days, id=1, status="completed"):
    return {
        "id": id,
        "status": status,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=days))
        .isoformat()
        .replace("+00:00", "Z"),
    }


def test_select_runs_keeps_latest_and_cutoff():
    runs = [item(1, 1), item(40, 2), item(50, 3)]
    result = select_runs_to_delete(runs, 1, datetime.now(timezone.utc) - timedelta(days=30))
    assert [x["id"] for x in result] == [2, 3]


def test_dry_run_does_not_delete():
    api = MagicMock()
    api.list_runs.return_value = [item(40, 1)]
    api.list_artifacts.return_value = []
    stats = clean(api, "o/r", dry_run=True, keep_latest=0)
    api.delete_run.assert_not_called()
    assert stats.runs_skipped == 1


def test_real_run_deletes():
    api = MagicMock()
    api.list_runs.return_value = [item(40, 1)]
    api.list_artifacts.return_value = []
    stats = clean(api, "o/r", dry_run=False, keep_latest=0)
    api.delete_run.assert_called_once_with("o/r", 1)
    assert stats.runs_deleted == 1
