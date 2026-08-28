#!/usr/bin/env bash
set -euo pipefail
export DATA_MODE=public-demo
cd "$(dirname "$0")/.."
pnpm build
