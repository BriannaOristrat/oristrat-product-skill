[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string[]]$ScopePrefixes = @()
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path

function Invoke-GitLines([string[]]$Arguments) {
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = @(& git -C $repo @Arguments 2>$null)
        $exitCode = $LASTEXITCODE
        if ($exitCode -ne 0) { $errorOutput = @(& git -C $repo @Arguments 2>&1) }
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }
    if ($exitCode -ne 0) { throw "git $($Arguments -join ' ') failed: $($errorOutput -join [Environment]::NewLine)" }
    return @($output | ForEach-Object { [string]$_ })
}

function Test-InScope([string]$Path) {
    if ($ScopePrefixes.Count -eq 0) { return $true }
    $normalized = $Path.Replace('\', '/').TrimStart('/')
    foreach ($prefix in $ScopePrefixes) {
        $candidate = $prefix.Replace('\', '/').Trim('/')
        if ($normalized.Equals($candidate, [StringComparison]::OrdinalIgnoreCase) -or
            $normalized.StartsWith("$candidate/", [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

$branch = (Invoke-GitLines @("branch", "--show-current") | Select-Object -First 1)
$head = (Invoke-GitLines @("rev-parse", "HEAD") | Select-Object -First 1)
$upstreamOutput = @(& git -C $repo rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>$null)
$upstream = if ($LASTEXITCODE -eq 0) { [string]($upstreamOutput | Select-Object -First 1) } else { $null }

$staged = Invoke-GitLines @("diff", "--cached", "--name-only")
$unstaged = Invoke-GitLines @("diff", "--name-only")
$untracked = Invoke-GitLines @("ls-files", "--others", "--exclude-standard")
$ignored = Invoke-GitLines @("ls-files", "--others", "--ignored", "--exclude-standard")
$unmerged = Invoke-GitLines @("diff", "--name-only", "--diff-filter=U")
$stash = Invoke-GitLines @("stash", "list", "--format=%gd %H %s")

$result = [ordered]@{
    repo = $repo
    branch = $branch
    head = $head
    upstream = $upstream
    scopePrefixes = $ScopePrefixes
    staged = @($staged | Where-Object { Test-InScope $_ })
    unstaged = @($unstaged | Where-Object { Test-InScope $_ })
    untracked = @($untracked | Where-Object { Test-InScope $_ })
    ignored = @($ignored | Where-Object { Test-InScope $_ })
    unmerged = @($unmerged | Where-Object { Test-InScope $_ })
    stash = $stash
}
$result["status"] = if ($result.unmerged.Count -gt 0) { "UNMERGED" } elseif (
    $result.staged.Count + $result.unstaged.Count + $result.untracked.Count + $result.ignored.Count -gt 0
) { "DIRTY" } else { "CLEAN" }
$result | ConvertTo-Json -Depth 6
exit 0
