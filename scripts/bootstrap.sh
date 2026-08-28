#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pnpm install
node scripts/run_python.mjs -m pip install -r requirements.txt
node scripts/run_python.mjs scripts/generate_demo_data.py
