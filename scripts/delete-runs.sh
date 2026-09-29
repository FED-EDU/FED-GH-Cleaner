#!/usr/bin/env bash
set -euo pipefail
# Source this file, then call delete_old_runs REPO RETAIN_DAYS KEEP_MINIMUM DRY_RUN.
delete_old_runs() {
  local repo="$1" retain_days="$2" keep_minimum="$3" dry_run="${4:-true}"
  local cutoff id count=0
  [[ -n "$repo" && "$retain_days" =~ ^[0-9]+$ && "$keep_minimum" =~ ^[0-9]+$ ]] || { echo "invalid run cleanup arguments" >&2; return 2; }
  cutoff=$(date -u -d "$retain_days days ago" +%Y-%m-%dT%H:%M:%SZ)
  mapfile -t ids < <(gh api "repos/$repo/actions/runs?per_page=100" --paginate --jq ".workflow_runs[] | select(.status == \"completed\" and .created_at < \"$cutoff\") | .id" | tail -n +$((keep_minimum + 1)))
  for id in "${ids[@]}"; do
    if [[ "$dry_run" == true ]]; then echo "[dry-run] would delete run $id"; else gh api -X DELETE "repos/$repo/actions/runs/$id" || true; ((count+=1)) || true; fi
  done
  echo "Runs deleted: $count"
}
export -f delete_old_runs
