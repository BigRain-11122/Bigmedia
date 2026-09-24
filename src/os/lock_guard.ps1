# BigStream OSLoop single-instance lock guard.
# Group standard D-20260925-03 adaptation (backlog #25, 48h receipt window):
#   lock content = "<launcherPid> <stamp>"  (lock carries PID)
#   takeover requires PID liveness probe first (heartbeat-touch NOT adopted)
#   atomic grab via [IO.FileMode]::CreateNew (no Test-Path+Set-Content race)
#   debounce floor = 1.2 x round budget (30 min for 25-min rounds): a dead
#     holder is not taken over before the floor, so an orphaned round child
#     (launcher died, codely still writing) can finish first
#   hard cap (default 40 min): age past cap takes over even if the probe says
#     alive - protects against PID-reuse false positives on long-lived boxes
# Output: exactly one decision line, "decision=own|skip reason=... pid=... age=..."
# Pure ASCII (see iteration_loop.ps1 ENCODING RULE). No exit - caller parses.
param(
    [Parameter(Mandatory = $true)][string]$LockPath,
    [int]$TakeoverMinMinutes = 30,
    [int]$HardCapMinutes = 40
)
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'

function New-Lock {
    # CreateNew fails atomically if another instance owns the lock.
    $fs = [System.IO.File]::Open($LockPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
    try {
        $w = New-Object System.IO.StreamWriter($fs)
        try { $w.Write("$PID $stamp") } finally { $w.Dispose() }
    } finally { $fs.Dispose() }
}

function Own([string]$reason) { Write-Output "decision=own reason=$reason pid=$PID" }
function Skip([string]$reason, $ageMin) { Write-Output "decision=skip reason=$reason pid=$PID age=$([int]$ageMin)" }

try {
    New-Lock
    Own 'create-new'
    return
} catch [System.IO.IOException] {
    # lock exists -> analyze holder before any takeover
}

$lockPid = 0
$raw = ''
try { $raw = (Get-Content -Raw -ErrorAction Stop $LockPath) } catch { }
$t0 = ($raw -split '\s+')[0]
if ($t0 -match '^\d+$') { $lockPid = [int]$t0 }
$ageMin = 0.0
try { $ageMin = ((Get-Date) - (Get-Item -ErrorAction Stop $LockPath).LastWriteTime).TotalMinutes } catch { }

$holderAlive = $false
if ($lockPid -gt 0) { $holderAlive = [bool](Get-Process -Id $lockPid -ErrorAction SilentlyContinue) }

if ($holderAlive -and $ageMin -lt $HardCapMinutes) {
    Skip "pid-alive (holder $lockPid running)" $ageMin
    return
}
if ($ageMin -lt $TakeoverMinMinutes) {
    # dead/legacy holder but debounce floor not reached: orphan child may still be writing
    if ($lockPid -gt 0) { Skip "dead-pid-debounce (holder $lockPid gone)" $ageMin }
    else { Skip "legacy-lock-debounce (no pid on record)" $ageMin }
    return
}

$reason = if ($holderAlive) { "hard-cap (holder $lockPid alive past ${HardCapMinutes}min, suspect pid reuse)" }
          elseif ($lockPid -gt 0) { "pid-dead-takeover (holder $lockPid gone)" }
          else { "legacy-stale-takeover (no pid on record)" }
try {
    Remove-Item -Force -ErrorAction Stop $LockPath
    New-Lock
    Own $reason
} catch [System.IO.IOException] {
    Skip 'lost-race (another launcher took over first)' $ageMin
}
