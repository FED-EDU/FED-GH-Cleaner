#!/usr/bin/env bash
set -euo pipefail
failed=0
for f in assets/images/favicon.ico assets/images/logo.svg assets/images/logo-192.png assets/images/social-preview.png; do
  if [[ -f "$f" ]]; then echo "PASS $f"; else echo "WARN missing $f"; failed=1; fi
done
exit "$failed"
