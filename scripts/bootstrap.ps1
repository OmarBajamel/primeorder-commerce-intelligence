$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

pnpm install --frozen-lockfile
if ($LASTEXITCODE -ne 0) { throw 'pnpm install failed' }

node scripts/run_python.mjs -m pip install --require-hashes -r requirements.lock
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed' }
node scripts/run_python.mjs scripts/generate_demo_data.py
if ($LASTEXITCODE -ne 0) { throw 'Public-demo data generation failed' }
