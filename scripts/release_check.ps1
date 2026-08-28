$ErrorActionPreference = 'Stop'
$env:DATA_MODE = 'public-demo'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
node scripts/run_python.mjs scripts/release_check.py
