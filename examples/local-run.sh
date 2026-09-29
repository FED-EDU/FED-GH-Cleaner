#!/usr/bin/env bash
set -euo pipefail
# Usage: examples/local-run.sh owner/name [days] [--dry-run]
REPO="${1:?Usage: $0 owner/name [days] [--dry-run]}"
DAYS="${2:-30}"
DRY_RUN="${3:---dry-run}"
gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first." >&2; exit 1; }
cutoff=$(date -u -d "$DAYS days ago" +%Y-%m-%dT%H:%M:%SZ)
  mapfile -t ids < <(gh api "repos/$repo/actions/runs?per_page=100" --paginate --jq ".workflow_runs[] | select(.status == \"completed\" and .created_at < \"$cutoff\") | .id" | tail -n +$((keep_minimum + 1)))
for id in "${ids[@]}"; do
  if [[ "$DRY_RUN" == "--dry-run" ]]; then echo "[dry-run] $id"; else gh api -X DELETE "repos/$REPO/actions/runs/$id"; fi
done
echo "Considered ${#ids[@]} old runs."
