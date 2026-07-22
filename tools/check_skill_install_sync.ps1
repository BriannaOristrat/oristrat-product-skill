[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$LockFile = "catalog/runtime-skill-lock.json",
    [string]$CodexHome = ""
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$lockPath = if ([IO.Path]::IsPathRooted($LockFile)) { $LockFile } else { Join-Path $repo $LockFile }
if (-not (Test-Path -LiteralPath $lockPath)) { throw "Skill lock not found: $lockPath" }
if (-not $CodexHome) { $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" } }

$lock = Get-Content -LiteralPath $lockPath -Raw -Encoding utf8 | ConvertFrom-Json

function Get-TreeManifest([string]$Root) {
    $resolved = (Resolve-Path -LiteralPath $Root).Path
    $manifest = @{}
    foreach ($file in @(Get-ChildItem -LiteralPath $resolved -Recurse -File | Where-Object {
        $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -ne '.pyc'
    })) {
        $relative = $file.FullName.Substring($resolved.Length).TrimStart([char[]]@('\', '/')).Replace('\', '/')
        $manifest[$relative] = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
    }
    return $manifest
}

function Compare-Tree([string]$Source, [string]$Installed) {
    $sourceManifest = Get-TreeManifest $Source
    $installedManifest = Get-TreeManifest $Installed
    $paths = @($sourceManifest.Keys + $installedManifest.Keys | Sort-Object -Unique)
    $different = @($paths | Where-Object { $sourceManifest[$_] -ne $installedManifest[$_] })
    return [ordered]@{
        sourceFileCount = $sourceManifest.Count
        installedFileCount = $installedManifest.Count
        differenceCount = $different.Count
        differences = $different
    }
}

$selfResults = @()
foreach ($item in @($lock.selfDeveloped)) {
    $source = Join-Path $repo ([string]$item.source)
    $installed = Join-Path (Join-Path $CodexHome "skills") ([string]$item.installName)
    $sourceExists = Test-Path -LiteralPath $source
    $installedExists = Test-Path -LiteralPath $installed
    $status = "PASS"
    $comparison = $null

    if (-not $sourceExists) {
        $status = "SOURCE_MISSING"
    }
    elseif (-not $installedExists) {
        $status = if ([bool]$item.installRequired) { "INSTALL_MISSING" } else { "REPO_ONLY" }
    }
    else {
        $comparison = Compare-Tree $source $installed
        if ($comparison.differenceCount -gt 0) { $status = "DRIFT" }
    }

    $selfResults += [ordered]@{
        name = [string]$item.name
        status = $status
        source = [string]$item.source
        installName = [string]$item.installName
        installRequired = [bool]$item.installRequired
        comparison = $comparison
    }
}

$externalResults = @()
foreach ($item in @($lock.externalDependencies)) {
    $recordExists = if ($item.sourceRecord) { Test-Path -LiteralPath (Join-Path $repo ([string]$item.sourceRecord)) } else { $null }
    $installedExists = Test-Path -LiteralPath (Join-Path (Join-Path $CodexHome "skills") ([string]$item.installName))
    $status = if ([bool]$item.installRequired -and -not $installedExists) {
        "INSTALL_MISSING"
    }
    elseif ($installedExists) {
        "INSTALLED"
    }
    else {
        "UNAVAILABLE_OPTIONAL"
    }
    if ($item.sourceRecord -and -not $recordExists) { $status = "SOURCE_RECORD_MISSING" }

    $externalResults += [ordered]@{
        name = [string]$item.name
        status = $status
        sourceRecord = [string]$item.sourceRecord
        sourceRecordExists = $recordExists
        installName = [string]$item.installName
        installRequired = [bool]$item.installRequired
        executionPolicy = [string]$item.executionPolicy
    }
}

$blockingSelf = @($selfResults | Where-Object { $_.status -in @("SOURCE_MISSING", "INSTALL_MISSING", "DRIFT") })
$blockingExternal = @($externalResults | Where-Object { $_.status -in @("INSTALL_MISSING", "SOURCE_RECORD_MISSING") })
$failed = $blockingSelf.Count + $blockingExternal.Count

[ordered]@{
    schemaVersion = $lock.schemaVersion
    repo = $repo
    codexHome = $CodexHome
    status = if ($failed -eq 0) { "PASS" } else { "FAIL" }
    failed = $failed
    selfDeveloped = $selfResults
    externalDependencies = $externalResults
} | ConvertTo-Json -Depth 8

if ($failed -gt 0) { exit 2 }
exit 0
