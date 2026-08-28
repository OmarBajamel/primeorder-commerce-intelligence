$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path
$Targets = @(
    (Join-Path $ProjectRoot 'apps\web\.next'),
    (Join-Path $ProjectRoot 'apps\web\out'),
    (Join-Path $ProjectRoot 'analytics\target'),
    (Join-Path $ProjectRoot 'analytics\logs'),
    (Join-Path $ProjectRoot 'playwright-report'),
    (Join-Path $ProjectRoot 'test-results')
)
foreach ($Target in $Targets) {
    $Full = [System.IO.Path]::GetFullPath($Target)
    if (-not $Full.StartsWith($ProjectRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove path outside project: $Full"
    }
    if (Test-Path -LiteralPath $Full) { Remove-Item -LiteralPath $Full -Recurse -Force }
}
