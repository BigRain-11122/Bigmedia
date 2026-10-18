# BigStream round liveness-budget guard (tech#217, OS round R2359).
# v2 activity-gated kill recipe ported from the BigMoney canonical
# iteration_loop v2 (quant/bigmoney 945c3f60, 2026-10-18 fleet-ops root
# cure, CEO order "solve it at the root"): a headless round is killed
# ONLY on EVIDENCE - $SilenceMinutes of zero output activity (true hang)
# or the $HardCapMinutes hard cap. The 2026-09-23 port carried the
# MiniGame 25-min wall-clock guillotine; every legitimate long round
# crossing it was tree-killed mid-flight (the fleet-wide "dead window"
# epidemic, "died pre-closeout" family). A productive long round that
# streams tool output continuously is never killed by wall clock alone.
#
# Extracted monitor unit (lock_guard.ps1 precedent): the launcher
# (iteration_loop.ps1) starts the round body, then hands the PID plus
# its stdout/stderr redirect files to this guard, which polls in
# $PollMillis slices and reports ONE verdict line. Extraction keeps the
# launcher preflight topology (cloud-cap / storm-gate / pulse / lock)
# zero-touch and makes the silence-gate / hard-cap pair directly
# testable (tests/test_round_budget_guard.py drives this file with a
# fake streaming/hanging child and tiny windows).
#
# Verdict lines (caller parses the line; matching exit code for CLI use):
#   budget=finished                       round body exited on its own   (rc 0)
#   budget=silence-kill silent=N total=M  tree killed, N min zero output (rc 3)
#   budget=hard-cap-kill total=M           tree killed, age over the cap  (rc 4)
#   budget=guard-error <msg>               guard machinery fault          (rc 1)
# "Activity" = the round's stdout/stderr redirect files gaining bytes
# (same evidence face as the BM v2 monitor). Pure ASCII (ENCODING RULE
# in iteration_loop.ps1).
param(
    [Parameter(Mandatory = $true)][int]$ProcId,
    [Parameter(Mandatory = $true)][string]$OutFile,
    [Parameter(Mandatory = $true)][string]$ErrFile,
    [double]$SilenceMinutes = 25,
    [double]$HardCapMinutes = 240,
    [int]$PollMillis = 30000
)
$ErrorActionPreference = 'Continue'

function Get-RedirectBytes {
    # Total bytes currently held by the round's stdout+stderr redirect files.
    $n = 0L
    foreach ($f in @($OutFile, $ErrFile)) {
        try {
            $fi = Get-Item -LiteralPath $f -ErrorAction SilentlyContinue
            if ($fi) { $n += $fi.Length }
        } catch { }
    }
    return $n
}

function Stop-RoundTree([int]$TargetPid) {
    # One-level child sweep + self, same kill face as the BM v2 monitor and
    # the retired v1 wall-clock path (codely job-objects its own children,
    # so the sweep is belt-and-braces; grandchildren ride the job object).
    try {
        Get-CimInstance Win32_Process -Filter "ParentProcessId=$TargetPid" -ErrorAction SilentlyContinue |
            ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
        Stop-Process -Id $TargetPid -Force -ErrorAction SilentlyContinue
    } catch { }
}

$startAt = Get-Date
$lastMove = Get-Date
$lastSize = -1L
try {
    while ($true) {
        Start-Sleep -Milliseconds $PollMillis
        if (-not (Get-Process -Id $ProcId -ErrorAction SilentlyContinue)) {
            Write-Output 'budget=finished'
            exit 0
        }
        $size = Get-RedirectBytes
        if ($size -ne $lastSize) { $lastSize = $size; $lastMove = Get-Date }
        $silentMin = ((Get-Date) - $lastMove).TotalMinutes
        $totalMin = ((Get-Date) - $startAt).TotalMinutes
        if ($silentMin -ge $SilenceMinutes) {
            Stop-RoundTree $ProcId
            Write-Output ("budget=silence-kill silent={0}min total={1}min" -f [int]$silentMin, [int]$totalMin)
            exit 3
        }
        if ($totalMin -ge $HardCapMinutes) {
            Stop-RoundTree $ProcId
            Write-Output ("budget=hard-cap-kill total={0}min" -f [int]$totalMin)
            exit 4
        }
    }
} catch {
    Write-Output "budget=guard-error $_"
    exit 1
}
