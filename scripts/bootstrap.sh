#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pnpm install --frozen-lockfile
node scripts/run_python.mjs -m pip install --require-hashes -r requirements.lock
node scripts/run_python.mjs scripts/generate_demo_data.py
