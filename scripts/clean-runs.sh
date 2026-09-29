#!/usr/bin/env bash
set -euo pipefail
# Compatibility entry point: the maintained implementation lives in delete-runs.sh.
# Usage: scripts/clean-runs.sh --repo owner/name --older-than 30 --keep-latest 10 --dry-run
REPO=""
OLDER_THAN=30
KEEP_LATEST=10
DRY_RUN=true
DELETE_ARTIFACTS=false
while (($#)); do
  case "$1" in
    --repo) REPO="$2"; shift 2;;
    --older-than) OLDER_THAN="$2"; shift 2;;
    --keep-latest) KEEP_LATEST="$2"; shift 2;;
    --dry-run) DRY_RUN=true; shift;;
    --no-dry-run) DRY_RUN=false; shift;;
    --delete-artifacts) DELETE_ARTIFACTS=true; shift;;
    -h|--help) sed -n '2,4p' "$0"; exit 0;;
    *) echo "Unknown argument: $1" >&2; exit 2;;
  esac
done
: "${REPO:?--repo owner/name is required}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DIR/delete-runs.sh"
source "$DIR/delete-artifacts.sh"
delete_old_runs "$REPO" "$OLDER_THAN" "$KEEP_LATEST" "$DRY_RUN"
if [[ "$DELETE_ARTIFACTS" == true ]]; then delete_old_artifacts "$REPO" "$OLDER_THAN" "$DRY_RUN"; fi
