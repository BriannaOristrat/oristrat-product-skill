[CmdletBinding()]
param(
    [ValidateSet("Check", "Update")]
    [string]$Mode = "Check",
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$SourceCatalog = "catalog/external-skill-sources.json",
    [string]$ReportPath = "catalog/skill-dashboard-status.md",
    [switch]$NoFetch,
    [switch]$OpenReport
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$catalogPath = if ([IO.Path]::IsPathRooted($SourceCatalog)) { $SourceCatalog } else { Join-Path $repo $SourceCatalog }
$report = if ([IO.Path]::IsPathRooted($ReportPath)) { $ReportPath } else { Join-Path $repo $ReportPath }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git executable was not found."
}
if (-not (Test-Path -LiteralPath $catalogPath)) {
    throw "External source catalog was not found: $catalogPath"
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string]$WorkTree,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $previousErrorAction = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $output = @(& git -C $WorkTree @Arguments 2>&1 | ForEach-Object { [string]$_ })
        $gitExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorAction
    }
    [pscustomobject]@{
        ExitCode = $gitExitCode
        Output = $output
        Text = ($output -join "`n").Trim()
    }
}

function Escape-MarkdownCell {
    param([AllowNull()][string]$Value)
    if ($null -eq $Value) { return "-" }
    return $Value.Replace('|', '\|').Replace("`r", ' ').Replace("`n", ' ')
}

function Get-LatestFileTime {
    param([string]$Path)
    $latest = Get-ChildItem -LiteralPath $Path -Recurse -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($latest) { return $latest.LastWriteTime.ToString("yyyy-MM-dd HH:mm") }
    return "-"
}

function Normalize-RepositoryUrl {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return "" }
    return (($Value.Trim().TrimEnd('/') -replace '\.git$', '').ToLowerInvariant())
}

$sourceCatalogData = Get-Content -LiteralPath $catalogPath -Raw -Encoding utf8 | ConvertFrom-Json
$externalRoot = [IO.Path]::GetFullPath((Join-Path $repo "external-skills")).TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
$disabledHooksPath = Join-Path $repo "tools/no-git-hooks"
$selfResults = @()

foreach ($directory in @(Get-ChildItem -LiteralPath (Join-Path $repo "skills") -Directory | Sort-Object Name)) {
    $skillFile = Join-Path $directory.FullName "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) { continue }

    $relative = "skills/$($directory.Name)"
    $trackedResult = Invoke-Git -WorkTree $repo -Arguments @("ls-files", "--", $relative)
    $tracked = $trackedResult.ExitCode -eq 0 -and -not [string]::IsNullOrWhiteSpace($trackedResult.Text)
    $dirtyResult = Invoke-Git -WorkTree $repo -Arguments @("status", "--porcelain", "--", $relative)
    $dirty = -not [string]::IsNullOrWhiteSpace($dirtyResult.Text)

    $commit = "-"
    $commitDate = "-"
    if ($tracked) {
        $logResult = Invoke-Git -WorkTree $repo -Arguments @("log", "-1", "--format=%h|%cI", "--", $relative)
        if ($logResult.ExitCode -eq 0 -and $logResult.Text) {
            $parts = $logResult.Text -split "\|", 2
            $commit = $parts[0]
            if ($parts.Count -gt 1) {
                $commitDate = ([DateTimeOffset]::Parse($parts[1])).ToString("yyyy-MM-dd HH:mm")
            }
        }
    }

    $status = if (-not $tracked) {
        "UNCOMMITTED"
    }
    elseif ($dirty) {
        "LOCAL_CHANGES"
    }
    else {
        "CLEAN"
    }

    $selfResults += [pscustomobject]@{
        Name = $directory.Name
        SubmittedVersion = if ($tracked) { $commit } else { "NOT_COMMITTED" }
        LastCommit = $commitDate
        LastLocalUpdate = Get-LatestFileTime -Path $directory.FullName
        Status = $status
    }
}

$externalResults = @()
foreach ($source in @($sourceCatalogData.sources)) {
    $localPath = Join-Path $repo ([string]$source.localDirectory)
    $result = [ordered]@{
        Name = [string]$source.name
        Repository = [string]$source.repository
        Category = [string]$source.category
        LocalDirectory = [string]$source.localDirectory
        UpdateMode = [string]$source.updateMode
        Branch = "-"
        LocalCommit = "-"
        CommitDate = "-"
        Ahead = 0
        Behind = 0
        Status = "SOURCE_RECORD_ONLY"
        Action = "OPEN_UPSTREAM"
        Error = ""
    }

    $fullLocalPath = [IO.Path]::GetFullPath($localPath)
    if (-not $fullLocalPath.StartsWith($externalRoot, [StringComparison]::OrdinalIgnoreCase)) {
        $result.Status = "OUT_OF_SCOPE"
        $result.Action = "SKIPPED_INVALID_PATH"
        $externalResults += [pscustomobject]$result
        continue
    }

    if (-not (Test-Path -LiteralPath $localPath)) {
        $result.Status = "LOCAL_MISSING"
        $externalResults += [pscustomobject]$result
        continue
    }

    if ([string]$source.updateMode -ne "git" -or -not (Test-Path -LiteralPath (Join-Path $localPath ".git"))) {
        $externalResults += [pscustomobject]$result
        continue
    }

    $originResult = Invoke-Git -WorkTree $localPath -Arguments @("remote", "get-url", "origin")
    if ($originResult.ExitCode -ne 0 -or (Normalize-RepositoryUrl $originResult.Text) -ne (Normalize-RepositoryUrl ([string]$source.repository))) {
        $result.Status = "REMOTE_MISMATCH"
        $result.Action = "SKIPPED_REMOTE_MISMATCH"
        $externalResults += [pscustomobject]$result
        continue
    }

    $branchResult = Invoke-Git -WorkTree $localPath -Arguments @("branch", "--show-current")
    $branch = $branchResult.Text
    if ([string]::IsNullOrWhiteSpace($branch)) {
        $result.Status = "DETACHED_HEAD"
        $result.Action = "MANUAL_REVIEW"
        $externalResults += [pscustomobject]$result
        continue
    }
    $result.Branch = $branch

    $dirtyResult = Invoke-Git -WorkTree $localPath -Arguments @("status", "--porcelain")
    $dirty = -not [string]::IsNullOrWhiteSpace($dirtyResult.Text)

    if (-not $NoFetch) {
        $fetchResult = Invoke-Git -WorkTree $localPath -Arguments @("-c", "submodule.recurse=false", "fetch", "--no-recurse-submodules", "--prune", "origin")
        if ($fetchResult.ExitCode -ne 0) {
            $result.Status = "FETCH_FAILED"
            $result.Action = "CHECK_NETWORK_OR_REMOTE"
            $result.Error = $fetchResult.Text
        }
    }

    $remoteRef = "origin/$branch"
    $remoteResult = Invoke-Git -WorkTree $localPath -Arguments @("rev-parse", "--verify", $remoteRef)
    if ($remoteResult.ExitCode -ne 0) {
        if ($result.Status -ne "FETCH_FAILED") {
            $result.Status = "NO_REMOTE_BRANCH"
            $result.Action = "MANUAL_REVIEW"
        }
    }
    else {
        $countResult = Invoke-Git -WorkTree $localPath -Arguments @("rev-list", "--left-right", "--count", "HEAD...$remoteRef")
        if ($countResult.ExitCode -eq 0) {
            $counts = @($countResult.Text -split "\s+")
            if ($counts.Count -ge 2) {
                $result.Ahead = [int]$counts[0]
                $result.Behind = [int]$counts[1]
            }
        }

        if ($Mode -eq "Update" -and -not $NoFetch -and -not $dirty -and $result.Ahead -eq 0 -and $result.Behind -gt 0) {
            $mergeResult = Invoke-Git -WorkTree $localPath -Arguments @("-c", "core.hooksPath=$disabledHooksPath", "-c", "submodule.recurse=false", "merge", "--ff-only", $remoteRef)
            if ($mergeResult.ExitCode -eq 0) {
                $result.Action = "FAST_FORWARDED"
                $result.Behind = 0
            }
            else {
                $result.Status = "UPDATE_FAILED"
                $result.Action = "MANUAL_REVIEW"
                $result.Error = $mergeResult.Text
            }
        }

        if ($result.Status -notin @("FETCH_FAILED", "UPDATE_FAILED")) {
            if ($dirty) {
                $result.Status = "DIRTY"
                $result.Action = "SKIPPED_LOCAL_CHANGES"
            }
            elseif ($result.Ahead -gt 0 -and $result.Behind -gt 0) {
                $result.Status = "DIVERGED"
                $result.Action = "SKIPPED_DIVERGED"
            }
            elseif ($result.Ahead -gt 0) {
                $result.Status = "AHEAD"
                $result.Action = "SKIPPED_LOCAL_AHEAD"
            }
            elseif ($result.Behind -gt 0) {
                $result.Status = "UPDATE_AVAILABLE"
                $result.Action = if ($Mode -eq "Update") { "NOT_UPDATED" } else { "SAFE_FAST_FORWARD" }
            }
            else {
                $result.Status = "UP_TO_DATE"
                if ($result.Action -ne "FAST_FORWARDED") { $result.Action = "NO_ACTION" }
            }
        }
    }

    $headResult = Invoke-Git -WorkTree $localPath -Arguments @("rev-parse", "--short", "HEAD")
    if ($headResult.ExitCode -eq 0) { $result.LocalCommit = $headResult.Text }
    $dateResult = Invoke-Git -WorkTree $localPath -Arguments @("log", "-1", "--format=%cs")
    if ($dateResult.ExitCode -eq 0) { $result.CommitDate = $dateResult.Text }
    $externalResults += [pscustomobject]$result
}

$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$selfUncommitted = @($selfResults | Where-Object { $_.Status -eq "UNCOMMITTED" }).Count
$selfChanged = @($selfResults | Where-Object { $_.Status -eq "LOCAL_CHANGES" }).Count
$upToDate = @($externalResults | Where-Object { $_.Status -eq "UP_TO_DATE" }).Count
$available = @($externalResults | Where-Object { $_.Status -eq "UPDATE_AVAILABLE" }).Count
$blockedStates = @("DIRTY", "DIVERGED", "FETCH_FAILED", "UPDATE_FAILED", "NO_REMOTE_BRANCH", "DETACHED_HEAD", "OUT_OF_SCOPE", "REMOTE_MISMATCH")
$blocked = @($externalResults | Where-Object { $_.Status -in $blockedStates }).Count

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("# Skill Dashboard Machine Status")
$lines.Add("")
$lines.Add("> [!info] Generated status")
$lines.Add("> Generated: $generatedAt | mode: $Mode | Only clean fast-forward external caches can be updated.")
$lines.Add("")
$lines.Add("## Self-developed Skill versions")
$lines.Add("")
$lines.Add("| Skill | Submitted version | Last commit | Last local update | Status |")
$lines.Add("|---|---|---|---|---|")
foreach ($item in $selfResults) {
    $link = "../skills/$($item.Name)/SKILL.md"
    $lines.Add("| [$($item.Name)]($link) | $(Escape-MarkdownCell $item.SubmittedVersion) | $(Escape-MarkdownCell $item.LastCommit) | $(Escape-MarkdownCell $item.LastLocalUpdate) | **$(Escape-MarkdownCell $item.Status)** |")
}
$lines.Add("")
$lines.Add("> Self summary: uncommitted $selfUncommitted; committed with local changes $selfChanged.")
$lines.Add("")
$lines.Add("## External GitHub source status")
$lines.Add("")
$lines.Add("| Source | Category | Local version | Branch | Ahead / Behind | Status | Action |")
$lines.Add("|---|---|---|---|---:|---|---|")
foreach ($item in $externalResults) {
    $name = "[$($item.Name)]($($item.Repository))"
    $version = if ($item.LocalCommit -eq "-") { "-" } else { "$($item.LocalCommit) / $($item.CommitDate)" }
    $lines.Add("| $name | $(Escape-MarkdownCell $item.Category) | $version | $(Escape-MarkdownCell $item.Branch) | $($item.Ahead) / $($item.Behind) | **$(Escape-MarkdownCell $item.Status)** | $(Escape-MarkdownCell $item.Action) |")
}
$lines.Add("")
$lines.Add("> Git source summary: up-to-date $upToDate; update available $available; manual attention $blocked. SOURCE_RECORD_ONLY entries are never overwritten automatically.")
$lines.Add("")
$lines.Add("## Status glossary")
$lines.Add("")
$lines.Add("- CLEAN: submitted and no local change in the Skill directory.")
$lines.Add("- LOCAL_CHANGES: a submitted version exists, with newer local changes.")
$lines.Add("- UNCOMMITTED: the Skill has no submitted Git version yet.")
$lines.Add("- UP_TO_DATE: the external cache matches origin/current-branch.")
$lines.Add("- UPDATE_AVAILABLE: a clean fast-forward update is available.")
$lines.Add("- DIRTY or DIVERGED: automatic update was skipped to preserve local state.")
$lines.Add("- SOURCE_RECORD_ONLY: selected source files, not a pullable full clone.")

$reportDirectory = Split-Path -Parent $report
if (-not (Test-Path -LiteralPath $reportDirectory)) {
    New-Item -ItemType Directory -Path $reportDirectory | Out-Null
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllLines($report, $lines, $utf8NoBom)

$summary = [ordered]@{
    mode = $Mode
    generatedAt = $generatedAt
    report = $report
    selfDeveloped = [ordered]@{
        checked = $selfResults.Count
        uncommitted = $selfUncommitted
        localChanges = $selfChanged
    }
    external = [ordered]@{
        checked = $externalResults.Count
        upToDate = $upToDate
        updateAvailable = $available
        requiresAttention = $blocked
    }
}
$summary | ConvertTo-Json -Depth 4

if ($OpenReport) {
    $encodedPath = [Uri]::EscapeDataString($report)
    try {
        Start-Process "obsidian://open?path=$encodedPath"
    }
    catch {
        Start-Process $report
    }
}

if ($blocked -gt 0) { exit 2 }
exit 0
