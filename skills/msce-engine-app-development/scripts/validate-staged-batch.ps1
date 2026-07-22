[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string]$ProjectPath = ".",
    [ValidateSet("auto", "always", "never")]
    [string]$BuildMode = "auto",
    [switch]$FullLint,
    [string]$LogRoot = ""
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$project = (Resolve-Path -LiteralPath (Join-Path $repo $ProjectPath)).Path
if (-not $LogRoot) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $LogRoot = Join-Path $env:TEMP "oristrat-msce-gates\$stamp"
}
[void](New-Item -ItemType Directory -Path $LogRoot -Force)

$repoUri = [Uri]($repo.TrimEnd('\') + '\')
$projectUri = [Uri]$project
$projectPrefix = [Uri]::UnescapeDataString($repoUri.MakeRelativeUri($projectUri).ToString()).Trim('.')
if ($projectPrefix) { $projectPrefix = $projectPrefix.TrimEnd('/') + '/' }

$staged = @(git -C $repo diff --cached --name-only --diff-filter=ACMR)
if ($LASTEXITCODE -ne 0) { throw "Unable to read staged files." }
if ($staged.Count -eq 0) {
    [ordered]@{
        stagedCount = 0
        logRoot = $LogRoot
        status = "NOT_TESTED"
        reason = "No staged files were found. Define and stage the approved batch before staged validation."
        results = @()
    } | ConvertTo-Json -Depth 5
    exit 2
}
$projectFiles = @($staged | Where-Object { -not $projectPrefix -or $_.Replace('\', '/').StartsWith($projectPrefix) })
$sourceFiles = @($projectFiles | Where-Object { $_ -match '\.(js|jsx|ts|tsx)$' } | ForEach-Object {
    if ($projectPrefix) { $_.Replace('\', '/').Substring($projectPrefix.Length) } else { $_ }
})

$eslint = Join-Path $project 'node_modules\.bin\eslint.cmd'
$tsc = Join-Path $project 'node_modules\.bin\tsc.cmd'
if (-not (Test-Path -LiteralPath $eslint)) { throw "ESLint is missing. Run npm install in $project." }

$buildRequired = $BuildMode -eq 'always'
if ($BuildMode -eq 'auto') {
    $buildRequired = @($projectFiles | Where-Object {
        $path = $_.Replace('\', '/')
        $path -match '(^|/)app/' -or $path -match '(^|/)dsl/' -or
        $path -match 'Msc(Web|Server)Env\.(ts|tsx)$' -or
        $path -match '(^|/)package(-lock)?\.json$' -or $path -match '(^|/)next\.config\.'
    }).Count -gt 0
}

$results = @()
function Invoke-Recorded([string]$Name, [string]$Executable, [string[]]$Arguments) {
    $safeName = $Name -replace '[^a-zA-Z0-9_.-]', '-'
    $log = Join-Path $LogRoot "$safeName.log"
    $watch = [Diagnostics.Stopwatch]::StartNew()
    & $Executable @Arguments *> $log
    $exitCode = $LASTEXITCODE
    $watch.Stop()
    return [ordered]@{
        name = $Name
        command = "$Executable $($Arguments -join ' ')"
        exitCode = $exitCode
        durationMs = $watch.ElapsedMilliseconds
        status = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
        log = $log
    }
}

Push-Location $project
try {
    if ($FullLint) {
        $results += Invoke-Recorded "full-lint" "npm.cmd" @("run", "lint", "--", "--quiet")
    }
    elseif ($sourceFiles.Count -gt 0) {
        for ($index = 0; $index -lt $sourceFiles.Count; $index += 10) {
            $end = [Math]::Min($index + 9, $sourceFiles.Count - 1)
            $chunk = @($sourceFiles[$index..$end])
            $results += Invoke-Recorded "target-lint-$([int]($index / 10) + 1)" $eslint $chunk
        }
    }

    if ($projectFiles.Count -gt 0 -and (Test-Path -LiteralPath $tsc)) {
        $results += Invoke-Recorded "typecheck" $tsc @("--noEmit")
    }
    if ($buildRequired) {
        $results += Invoke-Recorded "build" "npm.cmd" @("run", "build")
    }
}
finally {
    Pop-Location
}

$failed = @($results | Where-Object { $_.status -eq "FAIL" })
[ordered]@{
    stagedCount = $staged.Count
    projectFileCount = $projectFiles.Count
    lintedSourceCount = $sourceFiles.Count
    fullLint = [bool]$FullLint
    build = $buildRequired
    logRoot = $LogRoot
    status = if ($failed.Count -eq 0) { "TARGET_PASS" } else { "NEW_REGRESSION_OR_UNATTRIBUTED" }
    results = $results
} | ConvertTo-Json -Depth 7

if ($failed.Count -gt 0) { exit 2 }
exit 0
