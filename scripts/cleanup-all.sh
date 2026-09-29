#!/usr/bin/env bash
set -euo pipefail
# Usage: REPO=owner/name RETAIN_DAYS=30 KEEP_MINIMUM=10 DRY_RUN=true bash scripts/cleanup-all.sh
trap 'echo "Interrupted" >&2; exit 130' INT TERM
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DIR/delete-runs.sh"
source "$DIR/delete-artifacts.sh"
: "${REPO:?Set REPO=owner/name}"
RETAIN_DAYS="${RETAIN_DAYS:-30}"
KEEP_MINIMUM="${KEEP_MINIMUM:-10}"
DRY_RUN="${DRY_RUN:-true}"
echo "Cleaning $REPO; older than ${RETAIN_DAYS} days; keeping ${KEEP_MINIMUM}; dry-run=${DRY_RUN}"
delete_old_runs "$REPO" "$RETAIN_DAYS" "$KEEP_MINIMUM" "$DRY_RUN"
delete_old_artifacts "$REPO" "$RETAIN_DAYS" "$DRY_RUN"
echo "Cleanup complete."
