# BigStream OSLoop API 503-storm gate (tech#205, R2339 seed).
# Gap anchor: the 2026-10-18 00:52 round burned its full 25min budget inside
# a backend Gemini 503 storm (round_20261018_005202.err: 15x "503" hits + 5x
# "Error generating JSON content via API" reports), launcher-killed with ZERO
# accounting. The launcher had no backend health preflight, so storm slots
# kept igniting rounds straight into the retry wall.
# Two verbs (caller = iteration_loop.ps1; exactly one decision line each):
#   Arm  - after a TIMEOUT-KILLED round only: scan the round stderr for the
#          storm signature; hits >= threshold -> write the storm flag, arming
#          the next slots. Missing/unreadable err -> noarm (fail-open).
#   Gate - before igniting a round:
#            no flag            -> ignite (fast path, zero overhead)
#            flag older than cap -> clear + ignite (a stuck probe can never
#                                   starve the loop; a storm that outlives the
#                                   cap costs one canary round per cap window)
#            armed + fresh flag -> one tiny headless probe call:
#              probe pass  -> clear flag + ignite (disarm)
#              probe fail  -> defer: ledger line + "decision=defer" (caller
#                             pulses state ts and exits 0; budget conserved)
#              probe timeout -> kill probe tree + defer
#          Any machinery crash -> ignite (fail-open; flag kept for next slot).
# Output: exactly one line "decision=armed|noarm|ignite|defer ...".
# Pure ASCII (see iteration_loop.ps1 ENCODING RULE). No exit - caller parses.
param(
    [Parameter(Mandatory = $true)][ValidateSet('Arm', 'Gate')][string]$Verb,
    [string]$FlagPath = '',
    [string]$ErrFile = '',
    [string]$ProbeExe = '',
    [string]$ProbeArgs = '-y -p "Reply with the single word OK"',
    [string]$WorkDir = '',
    [string]$OutDir = '',
    [string]$LedgerFile = '',
    [int]$HitsThreshold = 5,
    [int]$ProbeTimeoutSec = 120,
    [int]$FlagMaxAgeMinutes = 90
)
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'

function Invoke-Arm {
    $hits = 0
    try {
        if ($ErrFile -and $FlagPath -and (Test-Path $ErrFile)) {
            $hits = @(Select-String -Path $ErrFile -Pattern '503|gemini-client-error-generateJson' -ErrorAction SilentlyContinue).Count
        }
    } catch { }
    if ($hits -ge $HitsThreshold -and $FlagPath) {
        try {
            Set-Content -Path $FlagPath -Value "$stamp armed hits=$hits" -Encoding ASCII
            Write-Output "decision=armed hits=$hits threshold=$HitsThreshold"
        } catch { Write-Output "decision=noarm hits=$hits threshold=$HitsThreshold flag-write-failed" }
        return
    }
    Write-Output "decision=noarm hits=$hits threshold=$HitsThreshold"
}

function Invoke-Defer([string]$reason, $probePid) {
    if ($LedgerFile) {
        try {
            Add-Content -Path $LedgerFile -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | API_STORM_DEFER $reason probe_pid=$probePid" -Encoding UTF8
        } catch { }
    }
    Write-Output "decision=defer reason=$reason probe_pid=$probePid"
}

function Invoke-Gate {
    if (-not $FlagPath -or -not (Test-Path $FlagPath)) {
        Write-Output 'decision=ignite reason=no-flag'
        return
    }
    $ageMin = 0.0
    try { $ageMin = ((Get-Date) - (Get-Item $FlagPath).LastWriteTime).TotalMinutes } catch { }
    if ($ageMin -gt $FlagMaxAgeMinutes) {
        try { Remove-Item -Force -ErrorAction SilentlyContinue $FlagPath } catch { }
        Write-Output "decision=ignite reason=flag-expired age=$([int]$ageMin)"
        return
    }
    if (-not $ProbeExe -or -not (Test-Path $ProbeExe)) {
        # fail-open: cannot probe -> ignite anyway; flag stays for the next slot
        Write-Output 'decision=ignite reason=fail-open probe-exe-missing'
        return
    }
    $probeOut = ''
    $probeErr = ''
    if ($OutDir) {
        New-Item -ItemType Directory -Force $OutDir | Out-Null
        $probeOut = Join-Path $OutDir "stormprobe_$stamp.out"
        $probeErr = Join-Path $OutDir "stormprobe_$stamp.err"
    }
    $p = $null
    try {
        if ($probeOut) {
            $p = Start-Process -FilePath $ProbeExe -ArgumentList $ProbeArgs -WorkingDirectory $WorkDir -PassThru -NoNewWindow -RedirectStandardOutput $probeOut -RedirectStandardError $probeErr
        } else {
            $p = Start-Process -FilePath $ProbeExe -ArgumentList $ProbeArgs -WorkingDirectory $WorkDir -PassThru -NoNewWindow
        }
    } catch {
        Write-Output 'decision=ignite reason=fail-open probe-spawn-crashed'
        return
    }
    $null = $p.Handle
    if (-not $p.WaitForExit($ProbeTimeoutSec * 1000)) {
        try {
            Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)" -ErrorAction SilentlyContinue |
                ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        } catch { }
        Invoke-Defer 'probe-timeout' $p.Id
        return
    }
    $p.Refresh()
    if ($p.ExitCode -eq 0) {
        try { Remove-Item -Force -ErrorAction SilentlyContinue $FlagPath } catch { }
        Write-Output 'decision=ignite reason=probe-pass disarm=1'
    } else {
        Invoke-Defer ("probe-fail exit=" + $p.ExitCode) $p.Id
    }
}

try {
    if ($Verb -eq 'Arm') { Invoke-Arm } else { Invoke-Gate }
} catch {
    Write-Output 'decision=ignite reason=fail-open gate-crashed'
}
