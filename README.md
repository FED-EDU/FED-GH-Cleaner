# gh-cleaner

A self-contained tool for safely scanning and deleting **old GitHub Actions workflow runs, artifacts, and optional caches**. The primary automation is a plain GitHub Actions workflow that uses GitHub's preinstalled `gh` CLI and API. It does **not** delete workflow files in `.github/workflows/`.

> **Recipe versus cooked meals:** a workflow file is the recipe; a workflow run is one cooked meal made from that recipe. `gh-cleaner` removes old meals and their generated artifacts, never the recipe.

## Quick start (the version that needs no installation)

1. Copy `.github/workflows/cleanup.yml` into the repository you want to clean.
2. Commit it to the repository's default branch.
3. Open **Actions → Cleanup old workflow runs and artifacts → Run workflow**.

The default is a **dry-run** with a 30-day retention window and at least 10 recent runs. Scheduled executions preview only; destructive mode requires an explicit manual choice. The schedule runs daily at 02:00 UTC. The first manual test can use `retain_days: 3650` to confirm permissions without deleting normal history.

## What it deletes

- Completed workflow-run history older than the retention cutoff, while preserving the newest `keep_minimum` runs.
- Artifacts older than the same cutoff.

It never edits, deletes, or commits repository files, workflow YAML, branches, releases, issues, pull requests, source code, or in-progress runs. Cache cleanup is separate and disabled by default.

## Why this repository has its own implementation

The cleanup workflow is intentionally auditable: the destructive operations are visible `gh api -X DELETE` commands, with no third-party action in the core cleanup workflow. The Python CLI is optional for people who prefer structured configuration, logging, and tests.

## Configuration

| Setting | Default | Meaning |
|---|---:|---|
| `retain_days` / `RETAIN_DAYS` | `30` | Delete items older than this many days. |
| `keep_minimum` / `KEEP_MINIMUM` | `10` | Preserve at least this many newest runs. |
| `MAX_DELETE` | `200` | Safety cap per category in the workflow. |
| cron | `0 2 * * *` | Daily at 02:00 UTC; edit the YAML to change it. |

## Local usage

Requires the GitHub CLI and an authenticated account:

```bash
gh auth login
REPO=owner/name RETAIN_DAYS=30 KEEP_MINIMUM=10 DRY_RUN=true \
  bash scripts/cleanup-all.sh
```

Use `DRY_RUN=false` only after reviewing the IDs printed by a dry run. The standalone Python CLI is also available:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
export GITHUB_TOKEN=YOUR_TOKEN
python -m gh_cleaner --repo owner/name --dry-run --older-than 30d
python -m gh_cleaner --repo owner/name --no-dry-run --older-than 30d
```


## Safeguards in 0.2.0

- Protected-run rules can exclude release workflows, branches, tags, name prefixes, and successful default-branch runs.
- Local destructive mode requires `--yes`; preview first.
- `--plan-out cleanup-plan.json` writes exact candidate IDs for review, and `--apply-plan cleanup-plan.json --yes` applies only that reviewed plan.
- `--report-out report.json` or `.csv` creates an audit report with IDs, dates, sizes, reasons, and failures.
- `--delete-caches` is opt-in because Actions caches are a separate storage category.
- `--diagnose-permissions` checks what repository permissions the token exposes.

Example:

```bash
python -m gh_cleaner --token-env GITHUB_TOKEN --repo owner/repo --dry-run \
  --exclude-workflow Release --exclude-branch main --plan-out cleanup-plan.json
python -m gh_cleaner --token-env GITHUB_TOKEN --repo owner/repo --no-dry-run --yes \
  --apply-plan cleanup-plan.json --report-out cleanup-report.json
```

## Permissions

The workflow requests `actions: write` and `contents: read`. Deleting a workflow run can also remove artifacts associated with that run. The workflow performs an early permission check and scheduled runs default to preview mode. A local token needs permission to read and delete Actions data. Keep tokens in environment variables or GitHub secrets, never in committed files.

## Troubleshooting

See [`docs/troubleshooting.md`](docs/troubleshooting.md) for 403 errors, missing manual buttons, schedules that do not run, and safe testing. For the internal design, see [`docs/how-it-works.md`](docs/how-it-works.md).

## Release documentation

- [v0.2.0 release notes](RELEASE_NOTES_v0.2.0.md)
- [Migration guide](docs/migration-0.2.0.md)
- [Compatibility matrix](docs/compatibility.md)
- [Public release checklist](RELEASE_CHECKLIST.md)

## License

MIT. Free software, community funded, and no in-app telemetry.
