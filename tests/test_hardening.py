from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import responses
from click.testing import CliRunner

from gh_cleaner.api import GitHubAPI
from gh_cleaner.cleaner import clean, is_protected
from gh_cleaner.cli import cli
from gh_cleaner.reporting import load_plan, write_plan


def old_item(kind_id=1, **extra):
    value = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat().replace("+00:00", "Z")
    return {"id": kind_id, "created_at": value, "status": "completed", **extra}


def test_protected_release_and_default_success():
    assert is_protected(old_item(name="Release", head_branch="dev"), exclude_workflows=("release",))
    assert is_protected(
        old_item(name="Build", head_branch="main", conclusion="success"),
        default_branch="main",
    )


def test_cache_cleanup_is_opt_in():
    api = MagicMock()
    api.list_runs.return_value = []
    api.list_artifacts.return_value = []
    api.list_caches.return_value = [old_item(9, last_accessed_at=old_item()["created_at"])]
    stats = clean(api, "o/r", dry_run=False, delete_runs=False, delete_artifacts=False, delete_caches=True)
    api.delete_cache.assert_called_once_with("o/r", 9)
    assert stats.caches_deleted == 1


def test_plan_round_trip(tmp_path):
    path = tmp_path / "plan.json"
    write_plan(path, "o/r", [{"kind": "run", "id": 4}])
    assert load_plan(path)["entries"][0]["id"] == 4


def test_cli_requires_yes_for_destructive_mode():
    result = CliRunner().invoke(cli, ["--token", "x", "--repo", "o/r", "--no-dry-run"])
    assert result.exit_code != 0
    assert "requires --yes" in result.output


@responses.activate
def test_list_and_delete_cache():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/actions/caches",
        json={"actions_caches": [{"id": 5}]},
        status=200,
    )
    responses.add(
        responses.DELETE,
        "https://api.github.com/repos/o/r/actions/caches/5",
        status=204,
    )
    api = GitHubAPI("secret")
    assert next(iter(api.list_caches("o/r")))["id"] == 5
    api.delete_cache("o/r", 5)
