[CmdletBinding()]
param(
    [int]$FrontendPort,
    [int[]]$ExpectedClosedPorts = @(),
    [string[]]$FrontendUrls = @(),
    [string[]]$ProxyUrls = @(),
    [string[]]$BackendUrls = @(),
    [int]$TimeoutSec = 15
)

$ErrorActionPreference = "Stop"
$checks = @()

function Add-Check([string]$Layer, [string]$Target, [string]$Status, [object]$Evidence) {
    $script:checks += [ordered]@{
        layer = $Layer
        target = $Target
        status = $Status
        evidence = $Evidence
    }
}

if ($FrontendPort -gt 0) {
    $listeners = @(Get-NetTCPConnection -LocalPort $FrontendPort -State Listen -ErrorAction SilentlyContinue)
    $owners = @($listeners | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object {
        $process = Get-Process -Id $_ -ErrorAction SilentlyContinue
        [ordered]@{ pid = $_; process = if ($process) { $process.ProcessName } else { $null } }
    })
    Add-Check "process" "port:$FrontendPort" $(if ($listeners.Count -gt 0) { "PASS" } else { "FAIL" }) $owners
}

foreach ($port in $ExpectedClosedPorts) {
    $listeners = @(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
    Add-Check "process" "closed-port:$port" $(if ($listeners.Count -eq 0) { "PASS" } else { "FAIL" }) @($listeners | Select-Object LocalAddress, LocalPort, OwningProcess)
}

function Test-Urls([string]$Layer, [string[]]$Urls) {
    foreach ($url in $Urls) {
        $watch = [Diagnostics.Stopwatch]::StartNew()
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec $TimeoutSec
            $watch.Stop()
            Add-Check $Layer $url "PASS" ([ordered]@{ httpStatus = [int]$response.StatusCode; durationMs = $watch.ElapsedMilliseconds })
        }
        catch {
            $watch.Stop()
            $statusCode = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { $null }
            Add-Check $Layer $url "FAIL" ([ordered]@{ httpStatus = $statusCode; durationMs = $watch.ElapsedMilliseconds; error = $_.Exception.Message })
        }
    }
}

Test-Urls "frontend" $FrontendUrls
Test-Urls "proxy" $ProxyUrls
Test-Urls "backend" $BackendUrls

$failed = @($checks | Where-Object { $_.status -eq "FAIL" })
$missingBusinessProof = $ProxyUrls.Count -gt 0 -or $BackendUrls.Count -gt 0
$notTested = $checks.Count -eq 0
[ordered]@{
    status = if ($notTested) { "NOT_TESTED" } elseif ($failed.Count -gt 0) { "FAIL" } elseif ($missingBusinessProof) { "PARTIAL" } else { "PASS" }
    failed = $failed.Count
    note = if ($notTested) { "No runtime target was provided." } elseif ($missingBusinessProof -and $failed.Count -eq 0) { "Reachability passed. Business success and end-to-end state still require a feature-specific probe." } else { $null }
    checks = $checks
} | ConvertTo-Json -Depth 7

if ($notTested -or $failed.Count -gt 0) { exit 2 }
exit 0
