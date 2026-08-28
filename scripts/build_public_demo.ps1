$ErrorActionPreference = 'Stop'
$env:DATA_MODE = 'public-demo'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
pnpm build
