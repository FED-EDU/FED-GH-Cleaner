from click.testing import CliRunner

from gh_cleaner.cli import cli


def test_help():
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0 and "--dry-run" in result.output


def test_missing_repo():
    result = CliRunner().invoke(cli, ["--token", "x"])
    assert result.exit_code != 0
