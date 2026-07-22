[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string[]]$AllowedPrefixes = @(),
    [string[]]$AdditionalForbiddenPatterns = @(),
    [switch]$RequireStaged,
    [switch]$AllowTests,
    [switch]$AllowScripts,
    [switch]$AllowGenerated,
    [switch]$AllowLocalEnv,
    [switch]$FailOnMixedFiles,
    [switch]$FailOnRelevantIgnored
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$staged = @(git -C $repo diff --cached --name-only --diff-filter=ACMRDT)
if ($LASTEXITCODE -ne 0) { throw "Unable to read staged files." }

$patterns = @($AdditionalForbiddenPatterns)
if (-not $AllowTests) {
    $patterns += '(^|/)(test|tests|__tests__|fixtures)(/|$)'
    $patterns += '\.(test|spec)\.[^/]+$'
    $patterns += '(^|/)vitest\.setup\.[^/]+$'
}
if (-not $AllowScripts) { $patterns += '(^|/)scripts?(/|$)' }
if (-not $AllowGenerated) {
    $patterns += '(^|/)next-env\.d\.ts$'
    $patterns += '(^|/)(\.next|dist|coverage)(/|$)'
    $patterns += '\.(log|tmp|cache)$'
}
if (-not $AllowLocalEnv) { $patterns += '(^|/)\.env(\..+)?$' }

$forbidden = @($staged | Where-Object {
    $path = $_ -replace '\\', '/'
    @($patterns | Where-Object { $path -match $_ }).Count -gt 0
})

$normalizedPrefixes = @($AllowedPrefixes | ForEach-Object { ($_ -replace '\\', '/').TrimEnd('/') + '/' })
function Test-InScope([string]$Path) {
    if ($normalizedPrefixes.Count -eq 0) { return $true }
    $normalized = ($Path -replace '\\', '/').TrimStart('/')
    return @($normalizedPrefixes | Where-Object { $normalized.StartsWith($_, [StringComparison]::OrdinalIgnoreCase) }).Count -gt 0
}

$outOfScope = @($staged | Where-Object { -not (Test-InScope $_) })
$unstaged = @(git -C $repo diff --name-only)
if ($LASTEXITCODE -ne 0) { throw "Unable to read unstaged files." }
$unstagedSet = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$unstaged | ForEach-Object { [void]$unstagedSet.Add($_) }
$mixed = @($staged | Where-Object { $unstagedSet.Contains($_) })

$ignored = @(git -C $repo ls-files --others --ignored --exclude-standard)
if ($LASTEXITCODE -ne 0) { throw "Unable to read ignored files." }
$relevantIgnored = @($ignored | Where-Object { Test-InScope $_ })

$diffCheck = @(git -C $repo diff --cached --check 2>&1)
$diffCheckPassed = $LASTEXITCODE -eq 0
$failed = (-not $diffCheckPassed) -or $forbidden.Count -gt 0 -or $outOfScope.Count -gt 0
if ($RequireStaged -and $staged.Count -eq 0) { $failed = $true }
if ($FailOnMixedFiles -and $mixed.Count -gt 0) { $failed = $true }
if ($FailOnRelevantIgnored -and $relevantIgnored.Count -gt 0) { $failed = $true }

[ordered]@{
    repo = $repo
    status = if ($failed) { "FAIL" } else { "PASS" }
    stagedCount = $staged.Count
    staged = $staged
    forbidden = $forbidden
    outOfScope = $outOfScope
    mixedFiles = $mixed
    relevantIgnored = $relevantIgnored
    diffCheckPassed = $diffCheckPassed
    diffCheckOutput = $diffCheck
} | ConvertTo-Json -Depth 6

if ($failed) { exit 2 }
exit 0
