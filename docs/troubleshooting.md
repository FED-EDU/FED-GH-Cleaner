# Troubleshooting

## The workflow never runs

**Cause:** the file is in the wrong folder, not on the default branch, or Actions are disabled. **Fix:** verify the exact path `.github/workflows/cleanup.yml`, commit it to the default branch, and check Settings → Actions → General. GitHub may pause scheduled workflows after long repository inactivity; a new commit or manual run reactivates it.

## 403 Forbidden

**Cause:** the token cannot delete Actions data. **Fix:** retain top-level `permissions: actions: write` and check organization policy.

## It ran but deleted nothing

**Cause:** no completed items are older than the cutoff, or the keep-minimum value protects them. **Fix:** inspect the printed cutoff and run manually with a conservative test value.

## Some deletions failed

Runs can change state while the job is processing. The loop continues intentionally; inspect the log for the specific ID.

## I want to see what it did

Open **Actions → workflow name → latest run**, expand each step, and read the echoed cutoff and IDs.

## I want to undo

Deleted run history and artifacts cannot be restored. The workflow does not delete code or workflow files, which remain in Git history.

## The manual button is missing

`workflow_dispatch:` must be present and the workflow file must be on the default branch.

## The permission check fails

The repository metadata endpoint does not expose write permission for the token. Confirm `actions: write` is declared and that repository or organization Actions policy allows it. Classic PATs need repository access; fine-grained tokens need Actions write access on the target repository.

## The plan does not apply

The plan is bound to its repository. Use the same `owner/name` with `--apply-plan`, and include `--yes`. If the resource was already removed, the API failure is recorded and the other entries continue.

## Storage is still high

Workflow runs, artifacts, and Actions caches are separate categories. Cache cleanup is opt-in with `--delete-caches`; other storage such as packages or releases is outside this project.
