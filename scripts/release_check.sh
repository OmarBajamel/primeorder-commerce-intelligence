#!/usr/bin/env bash
set -euo pipefail
export DATA_MODE=public-demo
cd "$(dirname "$0")/.."
node scripts/run_python.mjs scripts/release_check.py
