# Usage guide

## GitHub Action

Copy `.github/workflows/cleanup.yml` to the repository you want to clean, commit it to the default branch, then open **Actions → Cleanup old workflow runs and artifacts → Run workflow**. For a safe first test, enter `3650` days. The normal default is 30 days.

| Input | Meaning | Example |
|---|---|---|
| `retain_days` | Age threshold | `30` |
| `keep_minimum` | Newest runs to preserve | `10` |
| cron | Schedule in UTC | `0 2 * * *` |

Cron examples: `0 */6 * * *` every six hours; `0 2 * * 0` Sundays; `0 2 1 * *` monthly.

## Local Bash

```bash
gh auth login
REPO=owner/name RETAIN_DAYS=7 KEEP_MINIMUM=3 DRY_RUN=true bash scripts/cleanup-all.sh
```

Set `DRY_RUN=false` only after reviewing output. To clean only runs, call `scripts/delete-runs.sh`; to clean only artifacts, call `scripts/delete-artifacts.sh`.

## Python CLI

```bash
pip install -e '.[dev]'
export GITHUB_TOKEN=your-token
python -m gh_cleaner --repo owner/name --dry-run --older-than 30d --keep-latest 5
python -m gh_cleaner --repo owner/name --no-dry-run --no-delete-runs --delete-artifacts
```

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| 403 | Missing `actions: write` | Keep the permissions block. |
| Workflow not found | File is not on default branch | Commit the YAML to the default branch. |
| Nothing runs | Actions disabled | Settings → Actions → General → enable Actions. |
| Nothing deleted | Nothing is older than cutoff | This is expected; lower the test threshold carefully. |

## Safe plans and reports

The CLI defaults to dry-run. Generate a plan without deleting anything:

```bash
python -m gh_cleaner --token "$GITHUB_TOKEN" --repo owner/name --dry-run \
  --exclude-workflow Release --exclude-branch main --plan-out cleanup-plan.json
```

Review the IDs, then apply exactly that file with explicit confirmation:

```bash
python -m gh_cleaner --token "$GITHUB_TOKEN" --repo owner/name --no-dry-run --yes \
  --apply-plan cleanup-plan.json --report-out cleanup-report.json
```

Use `--report-format csv` for a spreadsheet-friendly report. A report records failures, but it cannot restore deleted data.

## Caches

Caches are not artifacts. They are cleaned only when `--delete-caches` is supplied, and are selected by last-access time. The GitHub workflow exposes this as an opt-in manual input.

## Permission diagnostics

Run `python -m gh_cleaner --token "$GITHUB_TOKEN" --repo owner/name --diagnose-permissions` before a destructive run. The workflow requires `actions: write`; organization or repository policy can still restrict the token.
