# How it works

## Two things called “workflow”

A **workflow file** is the YAML recipe in `.github/workflows/`. A **workflow run** is one execution of that recipe. This project deletes old run records, not the recipe. Think of a recipe card and the meals cooked from it: old meals can be discarded without burning the recipe.

## What is deleted

- `GET /repos/{owner}/{repo}/actions/runs` lists run history.
- `DELETE /repos/{owner}/{repo}/actions/runs/{run_id}` deletes one run record.
- `GET /repos/{owner}/{repo}/actions/artifacts` lists generated artifacts.
- `DELETE /repos/{owner}/{repo}/actions/artifacts/{artifact_id}` deletes one artifact.

The workflow never writes to the repository, so YAML, branches, source, issues, pull requests, and releases are untouched.

## Pagination and cutoff

`gh api --paginate` follows GitHub's next-page links. The runner computes a UTC cutoff with `date -u -d "30 days ago"`. Only completed runs older than that timestamp are candidates.

## Why `|| true` appears

One run may be temporarily unavailable or have a dependent in-progress operation. `|| true` records the failure and lets later IDs continue instead of abandoning the entire cleanup.

## Rate limits

Authenticated GitHub API clients generally have a generous hourly allowance. This job makes one list request per page plus one delete per item, so the `MAX_DELETE` cap prevents an unexpectedly large cleanup from consuming the budget.

## Protected records and caches

The Python implementation can exclude release workflow names, branch patterns such as `release/*`, tag-like runs, name prefixes, and successful runs on the default branch. Caches use separate list and delete endpoints and are opt-in.

## Token safety

Use `GITHUB_TOKEN` in Actions or an environment variable for local use. Do not place tokens in command history, committed files, or pull-request output. Never run a write-permission cleanup workflow on untrusted fork code. Deletion is permanent; GitHub retention settings affect future cleanup behavior but do not restore objects already removed.
