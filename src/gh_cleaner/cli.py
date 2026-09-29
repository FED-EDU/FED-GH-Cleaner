"""Click command-line interface for gh-cleaner."""

from __future__ import annotations

import os

import click

from . import __version__
from .api import GitHubAPI, GitHubAPIError
from .cleaner import clean
from .reporting import load_plan, write_plan, write_report
from .utils import parse_duration, setup_logging

STATUSES = ["completed", "in_progress", "queued", "requested", "waiting", "pending"]


def _apply_plan(api: GitHubAPI, repo: str, entries: list[dict]) -> tuple[int, int, int]:
    """Apply only the explicit IDs in a reviewed plan file."""
    runs = artifacts = caches = 0
    for entry in entries:
        kind, item_id = entry.get("kind"), int(entry["id"])
        if kind == "run":
            api.delete_run(repo, item_id)
            runs += 1
        elif kind == "artifact":
            api.delete_artifact(repo, item_id)
            artifacts += 1
        elif kind == "cache":
            api.delete_cache(repo, item_id)
            caches += 1
    return runs, artifacts, caches


@click.command(name="gh-cleaner")
@click.option("--token", required=False, help="Token value; prefer --token-env for local use.")
@click.option(
    "--token-env",
    default="GITHUB_TOKEN",
    show_default=True,
    help="Environment variable containing the token.",
)
@click.option("--repo", required=True, help="Repository in owner/name form.")
@click.option("--dry-run/--no-dry-run", default=True, show_default=True)
@click.option("--yes", is_flag=True, help="Required confirmation for destructive local mode.")
@click.option("--keep-latest", default=10, show_default=True, type=click.IntRange(min=0))
@click.option("--older-than", default="30d", show_default=True)
@click.option("--cache-older-than", default=None)
@click.option("--workflow")
@click.option("--status", type=click.Choice(STATUSES))
@click.option("--branch")
@click.option("--event")
@click.option("--exclude-workflow", multiple=True)
@click.option("--exclude-branch", multiple=True)
@click.option("--exclude-name-prefix", multiple=True)
@click.option("--exclude-tags/--include-tags", default=True, show_default=True)
@click.option(
    "--protect-default-branch/--allow-default-branch-success", default=True, show_default=True
)
@click.option("--default-branch", default=None)
@click.option("--delete-runs/--no-delete-runs", default=True)
@click.option("--delete-artifacts/--no-delete-artifacts", default=True)
@click.option("--delete-caches/--no-delete-caches", default=False, show_default=True)
@click.option("--max-deletions", default=None, type=click.IntRange(min=1))
@click.option("--artifact-name")
@click.option("--plan-out", type=click.Path(dir_okay=False, writable=True))
@click.option("--apply-plan", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--report-out", type=click.Path(dir_okay=False, writable=True))
@click.option(
    "--report-format", type=click.Choice(["json", "csv"]), default="json", show_default=True
)
@click.option("--diagnose-permissions", is_flag=True)
@click.option(
    "--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]), default="INFO"
)
@click.version_option(__version__)
def cli(
    token,
    token_env,
    repo,
    dry_run,
    yes,
    keep_latest,
    older_than,
    cache_older_than,
    workflow,
    status,
    branch,
    event,
    exclude_workflow,
    exclude_branch,
    exclude_name_prefix,
    exclude_tags,
    protect_default_branch,
    default_branch,
    delete_runs,
    delete_artifacts,
    delete_caches,
    max_deletions,
    artifact_name,
    plan_out,
    apply_plan,
    report_out,
    report_format,
    diagnose_permissions,
    log_level,
):
    """Scan, plan, and safely remove old GitHub Actions data."""
    token = token or os.getenv(token_env)
    if not token:
        raise click.UsageError(f"set ${token_env} or pass --token")
    if not dry_run and not yes and not apply_plan:
        raise click.UsageError("destructive mode requires --yes; use --dry-run to preview")
    try:
        setup_logging(log_level)
        api = GitHubAPI(token)
        if protect_default_branch and not default_branch:
            default_branch = api.repository_permissions(repo).get("default_branch")
        if diagnose_permissions:
            metadata = api.repository_permissions(repo)
            permissions = metadata.get("permissions", {})
            click.echo(f"Repository: {metadata.get('full_name', repo)}")
            click.echo(f"Token repository permissions: {permissions or 'not exposed by API'}")
            click.echo("Required for deletion: Actions write permission.")
            return
        if apply_plan:
            payload = load_plan(apply_plan)
            if payload.get("repo") != repo:
                raise ValueError("plan repository does not match --repo")
            if not yes:
                raise ValueError("applying a plan requires --yes")
            runs, artifacts, caches = _apply_plan(api, repo, payload["entries"])
            click.echo(
                f"Applied plan: deleted {runs} runs, {artifacts} artifacts, {caches} caches."
            )
            return
        stats = clean(
            api,
            repo,
            dry_run=dry_run,
            keep_latest=keep_latest,
            older_than=parse_duration(older_than),
            cache_older_than=parse_duration(cache_older_than) if cache_older_than else None,
            workflow=workflow,
            status=status,
            branch=branch,
            event=event,
            delete_runs=delete_runs,
            delete_artifacts=delete_artifacts,
            artifact_name=artifact_name,
            delete_caches=delete_caches,
            max_deletions=max_deletions,
            exclude_workflows=tuple(exclude_workflow),
            exclude_branches=tuple(exclude_branch),
            exclude_tags=exclude_tags,
            protect_default_branch_success=protect_default_branch,
            default_branch=default_branch,
            exclude_name_prefixes=tuple(exclude_name_prefix),
        )
        if plan_out:
            write_plan(plan_out, repo, stats.plan)
        if report_out:
            write_report(report_out, repo, stats, report_format)
        click.echo(
            f"Deleted {stats.runs_deleted} runs, {stats.artifacts_deleted} artifacts, "
            f"and {stats.caches_deleted} caches (dry-run: {dry_run})."
        )
        click.echo(
            f"Skipped/would delete: {stats.runs_skipped} runs, {stats.artifacts_skipped} artifacts, "
            f"and {stats.caches_skipped} caches; failures: {stats.failures}."
        )
        summary = os.getenv("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as handle:
                handle.write("## gh-cleaner summary\n\n")
                handle.write("| Category | Deleted | Skipped / preview |\n|---|---:|---:|\n")
                handle.write(f"| Runs | {stats.runs_deleted} | {stats.runs_skipped} |\n")
                handle.write(
                    f"| Artifacts | {stats.artifacts_deleted} | {stats.artifacts_skipped} |\n"
                )
                handle.write(f"| Caches | {stats.caches_deleted} | {stats.caches_skipped} |\n")
                handle.write(f"\nFailures: **{stats.failures}**\n")
    except (ValueError, GitHubAPIError) as exc:
        raise click.ClickException(str(exc)) from exc


main = cli
if __name__ == "__main__":
    main()
