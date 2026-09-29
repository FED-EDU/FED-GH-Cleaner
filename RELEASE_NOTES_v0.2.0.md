# gh-cleaner v0.2.0

## Highlights

`gh-cleaner` 0.2.0 is a safety-focused release for managing GitHub Actions storage without deleting workflow YAML files or source code.

### Safety changes

- Scheduled cleanup runs in **preview-only mode** by default.
- Destructive local CLI runs require `--yes`.
- Manual deletion supports reviewed JSON plans with `--plan-out` and `--apply-plan`.
- Protected-run rules can preserve release workflows, tags, selected branches, name prefixes, and successful default-branch runs.
- Every execution has a configurable maximum deletion cap.
- Workflow runs use a per-repository concurrency group.

### Storage coverage

- Workflow-run history cleanup.
- Artifact cleanup.
- Optional Actions cache cleanup with `--delete-caches`.
- JSON and CSV audit reports.
- GitHub Actions Step Summary output.

### Operations

- Permission diagnostics with `--diagnose-permissions`.
- Retry behavior for transient GitHub API failures.
- Pagination for runs, artifacts, and caches.
- 17 automated tests, shell validation, YAML validation, and package-build verification.

## Important behavior change from 0.1.x

Scheduled workflows no longer delete by default. They print a preview. To perform a scheduled destructive cleanup, a maintainer must deliberately change the workflow configuration. For local deletion, use `--no-dry-run --yes` or apply a reviewed plan with `--apply-plan ... --yes`.

## Safe upgrade path

1. Replace the old workflow with the 0.2.0 `.github/workflows/cleanup.yml`.
2. Run it manually with the default dry-run input.
3. Review the Actions Step Summary and any generated plan/report.
4. Keep release workflows and production branches protected.
5. Only then run a deliberately destructive cleanup.

## Recovery warning

Deleted workflow runs, artifacts, and caches cannot be restored by this project. Test with dry-run first.
