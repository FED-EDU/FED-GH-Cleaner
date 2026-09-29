# Migrating from 0.1.x to 0.2.0

## Behavior change

Version 0.1.x could be configured to delete on a schedule. Version 0.2.0 makes scheduled cleanup **preview-only by default**. This is intentional because workflow runs, artifacts, and caches cannot be restored after deletion.

## Required changes

- Replace the old cleanup workflow with the 0.2.0 version.
- Use `--yes` for destructive local CLI runs.
- Use `--plan-out` and `--apply-plan` when an approval/review step is desired.
- Add `--delete-caches` only if Actions cache cleanup is explicitly wanted.

## Recommended upgrade test

```bash
python -m gh_cleaner --token-env GITHUB_TOKEN --repo owner/name \
  --dry-run --older-than 3650d --plan-out cleanup-plan.json
```

Review the plan, then use the exact same repository with:

```bash
python -m gh_cleaner --token-env GITHUB_TOKEN --repo owner/name \
  --apply-plan cleanup-plan.json --yes --report-out cleanup-report.json
```

## Compatibility

The 0.2.0 CLI remains compatible with the existing flag-based invocation. It does not require a database, web server, Streamlit application, or external cleanup action.
