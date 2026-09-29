#!/usr/bin/env bash
set -euo pipefail
# Set REPO and optional WORKFLOW, BRANCH, STATUS before running this example.
: "${REPO:?Set REPO=owner/name}"
query="?per_page=100"
[[ -n "${WORKFLOW:-}" ]] && query+="&workflow_id=$WORKFLOW"
[[ -n "${BRANCH:-}" ]] && query+="&branch=$BRANCH"
[[ -n "${STATUS:-}" ]] && query+="&status=$STATUS"
echo "Would query repos/$REPO/actions/runs$query"
# Examples:
# REPO=owner/name WORKFLOW=build.yml bash examples/custom-filters.sh
# REPO=owner/name BRANCH=main bash examples/custom-filters.sh
# REPO=owner/name STATUS=completed bash examples/custom-filters.sh
