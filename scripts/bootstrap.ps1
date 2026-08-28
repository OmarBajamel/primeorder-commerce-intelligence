$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

pnpm install
if ($LASTEXITCODE -ne 0) { throw 'pnpm install failed' }

node scripts/run_python.mjs -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed' }
node scripts/run_python.mjs scripts/generate_demo_data.py
if ($LASTEXITCODE -ne 0) { throw 'Public-demo data generation failed' }
