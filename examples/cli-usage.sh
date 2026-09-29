#!/usr/bin/env bash
set -euo pipefail
# Examples for the Python CLI. Export a token before running these commands.
export GITHUB_TOKEN="${GITHUB_TOKEN:-YOUR_TOKEN}"

# Safe preview: retain the latest five runs and inspect what is old enough.
gh-cleaner --repo owner/repo --dry-run --older-than 30d --keep-latest 5

# Preview artifact cleanup filtered by artifact name.
gh-cleaner --repo owner/repo --dry-run --no-delete-runs --delete-artifacts --artifact-name my-artifact

# Preview runs from a particular workflow and status.
gh-cleaner --repo owner/repo --dry-run --workflow build.yml --status completed

# Real deletion requires the explicit opt-out from dry-run.
# gh-cleaner --repo owner/repo --no-dry-run --older-than 30d --keep-latest 10
