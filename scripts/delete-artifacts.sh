#!/usr/bin/env bash
set -euo pipefail
# Source this file, then call delete_old_artifacts REPO RETAIN_DAYS DRY_RUN.
delete_old_artifacts() {
  local repo="$1" retain_days="$2" dry_run="${3:-true}" cutoff id count=0
  cutoff=$(date -u -d "$retain_days days ago" +%Y-%m-%dT%H:%M:%SZ)
  mapfile -t ids < <(gh api "repos/$repo/actions/artifacts?per_page=100" --paginate --jq ".artifacts[] | select(.created_at < \\"$cutoff\\") | .id")
  for id in "${ids[@]}"; do
    if [[ "$dry_run" == true ]]; then echo "[dry-run] would delete artifact $id"; else gh api -X DELETE "repos/$repo/actions/artifacts/$id" || true; ((count+=1)) || true; fi
  done
  echo "Artifacts deleted: $count"
}
export -f delete_old_artifacts
