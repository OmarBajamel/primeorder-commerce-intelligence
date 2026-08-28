#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "$0")/.." && pwd)"
for rel in apps/web/.next apps/web/out analytics/target analytics/logs playwright-report test-results; do
  target="$project_root/$rel"
  case "$target" in "$project_root"/*) rm -rf -- "$target" ;; *) exit 2 ;; esac
done
