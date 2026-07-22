[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$ValidatorPath = "",
    [switch]$IncludeRuntimeDependencies
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$skillRoot = Join-Path $repo "skills"
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }

if (-not $ValidatorPath) {
    $ValidatorPath = Join-Path $codexHome "skills\.system\skill-creator\scripts\quick_validate.py"
}
if (-not (Test-Path -LiteralPath $ValidatorPath)) {
    throw "Skill validator not found: $ValidatorPath"
}

$previousUtf8 = $env:PYTHONUTF8
$previousBytecode = $env:PYTHONDONTWRITEBYTECODE
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"

$results = @()
try {
    foreach ($directory in @(Get-ChildItem -LiteralPath $skillRoot -Directory | Sort-Object Name)) {
        $skillFile = Join-Path $directory.FullName "SKILL.md"
        if (-not (Test-Path -LiteralPath $skillFile)) { continue }

        $output = @(& python $ValidatorPath $directory.FullName 2>&1)
        $exitCode = $LASTEXITCODE
        $results += [ordered]@{
            name = $directory.Name
            origin = "repo"
            status = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
            exitCode = $exitCode
            output = @($output | ForEach-Object { [string]$_ })
        }
    }

    if ($IncludeRuntimeDependencies) {
        $lockPath = Join-Path $repo "catalog\runtime-skill-lock.json"
        if (-not (Test-Path -LiteralPath $lockPath)) { throw "Runtime skill lock not found: $lockPath" }
        $lock = Get-Content -LiteralPath $lockPath -Raw -Encoding utf8 | ConvertFrom-Json
        foreach ($item in @($lock.externalDependencies)) {
            $runtimePath = Join-Path (Join-Path $codexHome "skills") ([string]$item.installName)
            if (-not (Test-Path -LiteralPath $runtimePath)) { continue }
            $output = @(& python $ValidatorPath $runtimePath 2>&1)
            $exitCode = $LASTEXITCODE
            $results += [ordered]@{
                name = [string]$item.name
                origin = "runtime-external"
                status = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
                exitCode = $exitCode
                output = @($output | ForEach-Object { [string]$_ })
            }
        }
    }
}
finally {
    $env:PYTHONUTF8 = $previousUtf8
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
}

$failed = @($results | Where-Object { $_.status -eq "FAIL" })
[ordered]@{
    repo = $repo
    checked = $results.Count
    failed = $failed.Count
    status = if ($failed.Count -eq 0) { "PASS" } else { "FAIL" }
    results = $results
} | ConvertTo-Json -Depth 6

if ($failed.Count -gt 0) { exit 2 }
exit 0
