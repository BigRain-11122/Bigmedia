# BigStream OS loop - OS-scheduled headless round launcher.
# Ported 2026-09-23 from the proven BigMoney pattern
# (quant/bigmoney/Tools/iteration_loop.ps1, live since 2026-09-23 14:33).
# CEO order O-20260923-1525-bm-a: infrastructure first, NO content production.
# The durable session cron only fires while a Codely CLI window is open - proven
# dead overnight (BigMoney evidence: 8.8h, zero beats). This OS task is the only
# 10-min channel that survives closed windows. Every beat: guards -> spawn ONE
# headless codely round (src/os/iteration_prompt.txt driven) -> heartbeat. Round
# budget v2 = liveness-gated: hard cap $RoundTimeoutMinutes (240) + SILENCE-KILL
# gate $RoundSilenceMinutes (25 min of ZERO output = hang); overlap prevented by
# round.lock + task-level IgnoreNew.
#
# v2 (2026-10-18 liveness-budget surgery, tech#217, BM 945c3f60 canonical
# port, group 10-18 root-cure ruling "solve it at the root"): the 2026-09-23
# port carried the MiniGame 25-min wall-clock kill. Every legitimate long
# round (batch re-renders, absorb chains, suite runs) that crossed 25 min
# was tree-killed mid-flight - the fleet-wide "dead window" epidemic
# ("died pre-closeout" family). v2 kills only on EVIDENCE: 25 min of zero
# output (true hang, round_budget_guard.ps1) or the 240-min hard cap.
# Productive long rounds survive. Lock faces scale with the budget
# (debounce floor + hard cap = 1.2 x 240 = 288 min), loop_health
# LOCK_AGE_MIN follows, task ExecutionTimeLimit raised past the cap.
#
# ENCODING RULE: this file must stay PURE ASCII. powershell.exe 5.1 decodes
# BOM-less .ps1 as ANSI/GBK and swallows quote bytes after multibyte sequences.
# All Chinese content lives in src/os/iteration_prompt.txt (UTF-8, read at
# runtime with explicit -Encoding UTF8).
#
# Self-heal recipe (run from an agent round when Get-ScheduledTask
# BigStream-OSLoop is missing - path-agnostic, works on any machine):
#   powershell -NoProfile -ExecutionPolicy Bypass -File src/os/register_loop_task.ps1
param(
    [string]$Project = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)),
    # v2 liveness budget (tech#217): 0 = auto = 1.2 x hard cap (288 min for
    # the 240 default). Lock faces must scale WITH the budget or the guard
    # would steal locks from legitimate long rounds at the old 40-min cap.
    [int]$LockMaxAgeMinutes = 0,
    [int]$RoundTimeoutMinutes = 240,
    [int]$RoundSilenceMinutes = 25
)
$ErrorActionPreference = 'Continue'
Set-Location $Project
$logDir = Join-Path $Project 'logs\iteration-loop'
New-Item -ItemType Directory -Force $logDir | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$runLog = Join-Path $logDir "run_$stamp.log"
$roundOut = Join-Path $logDir "round_$stamp.out"
$roundErr = Join-Path $logDir "round_$stamp.err"
$heart = Join-Path $Project 'logs\probe-heartbeat.txt'
$stormFlag = Join-Path $logDir 'api-storm.flag'

function Log([string]$m) {
    $line = "$(Get-Date -Format 'HH:mm:ss') $m"
    Write-Output $line
    Add-Content -Path $runLog -Value $line -Encoding UTF8
}
function Beat([string]$m) {
    Add-Content -Path $heart -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') osloop: $m" -Encoding UTF8
}

# ---- single-instance: D-20260925-03 guard (pid in lock + liveness probe
# + atomic CreateNew; debounce floor 1.2x budget, hard cap below). Manual-
# launch races now hit the same atomic grab; stale-lock restarts probe the
# recorded holder PID before taking over (old behavior was age-only).
# v2 scaling (tech#217): BOTH windows ride 1.2 x the 240-min hard cap, so a
# legitimately running long round is never lock-stolen mid-flight and a
# dead holder still yields inside the debounce floor (orphan child finish
# window). ----
$lock = Join-Path $logDir 'round.lock'
$guard = Join-Path $PSScriptRoot 'lock_guard.ps1'
$takeoverMin = [int][Math]::Round(1.2 * $RoundTimeoutMinutes)
if ($LockMaxAgeMinutes -le 0) { $LockMaxAgeMinutes = $takeoverMin }
$decision = & $guard -LockPath $lock -TakeoverMinMinutes $takeoverMin -HardCapMinutes $LockMaxAgeMinutes
if (-not $decision -or $decision -notmatch '^decision=own') {
    Log "skip: $decision"
    Beat 'skip (round in flight)'
    exit 0
}
Log "lock acquired: $decision"

try {
    # ---- C-20261015-03 cloud concurrency cap v1.0 preflight (O-20261015-1800,
    # committee case: spawn-gate spec par.3, fleet-wide unified face).
    # Before igniting a new cloud LLM round, count live codely.exe on this
    # machine. C-20261016-05 correction (orders row 514, bigmoney 63943e50b
    # pattern): count HEADLESS -p faces only (autonomous lanes + bg agents);
    # CEO interactive windows are exempt per C-20261015-03 par.2 (bm-a
    # same-bug fix). live >= 2 -> defer this grid slot: ledger line + exit 0,
    # next slot auto-retries. Fail-open: a probe crash must never block.
    $capLedger = Join-Path $logDir 'cloud-cap-ledger.txt'
    try {
        $live = @(Get-CimInstance Win32_Process -Filter "Name='codely.exe'" -ErrorAction Stop | Where-Object { $_.CommandLine -match ' -p( |")' }).Count
        if ($live -ge 2) {
            Add-Content -Path $capLedger -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | CLOUD_CAP_DEFER live=$live" -Encoding UTF8
            Log "defer: cloud concurrency cap (live=$live >= 2, C-20261015-03)"
            Beat "cloud-cap defer (live=$live)"
            # PT-20261015-01 remediation option 1 (group orders row 456):
            # defer windows ran with zero round closes, so the fleet-audit
            # ts face read STALE 2.2h while the loop was alive retrying.
            # This spawner holds round.lock here (no round body can be
            # closing concurrently) - pulse ts + marker, ZERO accounting
            # touch (tick/log/task untouched; finalize_state stays the one
            # accounting writer). Fail-open: a failed pulse never blocks
            # the defer path.
            try {
                $pulseOut = @( & python (Join-Path $PSScriptRoot 'close_commit.py') --pulse "cloud-cap defer (live=$live)" 2>&1 )
                Log ("state pulse rc=${LASTEXITCODE}: " + ($pulseOut -join ' | '))
            } catch { Log "state pulse crashed (non-fatal): $_" }
            exit 0
        }
        Log "cloud-cap preflight ok (live=$live)"
    } catch { Log "cloud-cap preflight probe failed - fail-open ignition: $_" }

    Log "iteration round start $stamp"

    $codelyPath = (Get-Command codely -ErrorAction SilentlyContinue).Source
    if (-not $codelyPath) { Log 'FATAL: codely not on PATH for this context'; Beat 'error codely missing'; exit 2 }
    Log "codely=$codelyPath"

    # Round prompt (Chinese) lives outside this file - see ENCODING RULE above.
    $promptFile = Join-Path $Project 'src\os\iteration_prompt.txt'
    if (-not (Test-Path $promptFile)) { Log 'FATAL: iteration_prompt.txt missing'; Beat 'error prompt file missing'; exit 2 }
    $prompt = (Get-Content -Raw -Encoding UTF8 $promptFile).Trim()
    if ($prompt.Length -lt 50) { Log 'FATAL: iteration_prompt.txt too short'; Beat 'error prompt file empty'; exit 2 }

    # ---- tech#205 API 503-storm preflight (R2339 seed: the 00:52 storm burned
    # a full 25min round on backend 503 retries, launcher-killed, zero
    # accounting). Armed slots probe the backend with one tiny headless call
    # BEFORE ignition; probe fail -> defer pulse (budget conserved, next slot
    # retries), probe pass -> disarm + ignite. Fail-open on any machinery
    # crash; flag auto-expires (90min) so a stuck probe can never starve the
    # loop - a storm that outlives the cap costs one canary round per window.
    $gateDecision = ''
    try {
        $gateDecision = & (Join-Path $PSScriptRoot 'api_storm_gate.ps1') -Verb Gate -FlagPath $stormFlag -ProbeExe $codelyPath -WorkDir $Project -OutDir $logDir -LedgerFile $capLedger
    } catch { Log "storm-gate crashed - fail-open ignition: $_" }
    if ($gateDecision) { Log "storm-gate: $gateDecision" }
    if ($gateDecision -match '^decision=defer') {
        Beat 'api-storm defer (probe fail)'
        # same pulse contract as the cloud-cap defer path (PT-20261015-01):
        # this spawner holds round.lock -> pulse ts, ZERO accounting touch.
        try {
            $pulseOut = @( & python (Join-Path $PSScriptRoot 'close_commit.py') --pulse "api-storm defer (probe fail)" 2>&1 )
            Log ("state pulse rc=${LASTEXITCODE}: " + ($pulseOut -join ' | '))
        } catch { Log "state pulse crashed (non-fatal): $_" }
        exit 0
    }

    # Single-line prompt, no embedded double quotes (Start-Process argument passing).
    if ($prompt.Contains('"')) { $prompt = $prompt.Replace('"', "'") }
    $argLine = '-y -p "' + $prompt + '"'
    # ---- tech#217 v2 liveness budget (BM 945c3f60 canonical port): kill
    # ONLY on evidence. $RoundSilenceMinutes of zero output (true hang,
    # round_budget_guard.ps1 polls the redirect files) or the
    # $RoundTimeoutMinutes hard cap. A productive long round that streams
    # tool output is never killed by wall clock alone - the 25-min
    # guillotine behind the "died pre-closeout" dead-window epidemic is
    # retired. Guard faults never abandon the round to an unmonitored
    # eternity: a plain hard-cap wait backstops (fail-safe, not fail-open).
    Log "spawning headless round (hard-cap ${RoundTimeoutMinutes}min, silence-kill ${RoundSilenceMinutes}min, prompt_chars=$($prompt.Length), out=$roundOut)"
    # T0 CLOUD-OFF guard (CEO 2026-10-20): automation is local-only; never spawn the cloud CLI.
    # Resolution lives in cloud_off_gate.ps1: this task is registered through the
    # symlinked Desktop path, where a literal ancestor walk misses the canonical
    # marker (stale Desktop cph4 mirror) and cloud rounds kept igniting. A
    # resolver crash is fail-closed, never fail-open.
    $__gateRoot = $null
    $__gateCrash = $null
    try {
        . (Join-Path $PSScriptRoot 'cloud_off_gate.ps1')
        $__gateRoot = Get-CloudOffMarkerRoot -ScriptRoot $PSScriptRoot -Project $Project
    } catch { $__gateCrash = $_ }
    if ($__gateRoot -or $__gateCrash) {
        if ($__gateRoot) {
            $__cl = Join-Path $__gateRoot 'media\logs\cloud-off-suppressed.log'
        } else {
            $__cl = Join-Path (Split-Path -Parent (Split-Path -Parent $Project)) 'media\logs\cloud-off-suppressed.log'
            Log "cloud-off gate resolver crashed - fail-closed (T0): $__gateCrash"
        }
        $__cd = Split-Path -Parent $__cl
        if (-not (Test-Path $__cd)) { New-Item -ItemType Directory -Force -Path $__cd | Out-Null }
        $__why = if ($__gateCrash) { 'gate resolver crashed, fail-closed - suppressed cloud round (T0)' } else { 'suppressed cloud round (T0)' }
        Add-Content -Path $__cl -Value ((Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' | ' + [System.IO.Path]::GetFileName($PSCommandPath) + ' | ' + $__why) -Encoding UTF8
        exit 0
    }
    $p = Start-Process -FilePath $codelyPath -ArgumentList $argLine -WorkingDirectory $Project -PassThru -NoNewWindow -RedirectStandardOutput $roundOut -RedirectStandardError $roundErr
    $null = $p.Handle   # materialize handle so ExitCode is readable
    $budgetVerdict = ''
    try {
        $budgetVerdict = & (Join-Path $PSScriptRoot 'round_budget_guard.ps1') -ProcId $p.Id -OutFile $roundOut -ErrFile $roundErr -SilenceMinutes $RoundSilenceMinutes -HardCapMinutes $RoundTimeoutMinutes
    } catch { Log "budget guard crashed - hard-cap backstop engages: $_" }
    Log "budget-guard: $budgetVerdict"
    if ($budgetVerdict -match '^budget=finished') {
        $p.Refresh()
        Log "headless round finished exit=$($p.ExitCode)"
        Beat "round done exit=$($p.ExitCode)"
        exit $p.ExitCode
    }
    if ($budgetVerdict -match '^budget=(silence-kill|hard-cap-kill)') {
        # evidence kill: the guard already tree-killed the round; ledger the
        # verdict, then keep the tech#205 arm face on BOTH evidence paths
        # (a 503-retry storm can hang silent OR stream errors until the cap).
        Log "ROUND $($budgetVerdict -replace '^budget=', '') - headless process tree killed by liveness budget"
        $armDecision = ''
        try {
            $armDecision = & (Join-Path $PSScriptRoot 'api_storm_gate.ps1') -Verb Arm -ErrFile $roundErr -FlagPath $stormFlag
        } catch { Log "storm-arm crashed (non-fatal): $_" }
        if ($armDecision) { Log "storm-arm: $armDecision" }
        Beat "round killed ($budgetVerdict)"
        exit 3
    }
    # guard machinery fault (guard-error / crash / empty): plain hard-cap wait.
    Log "budget guard fault - engaging plain hard-cap wait (${RoundTimeoutMinutes}min)"
    if (-not $p.WaitForExit($RoundTimeoutMinutes * 60 * 1000)) {
        Log "ROUND HARD-CAP after ${RoundTimeoutMinutes}min (backstop) - killing headless process tree"
        try {
            Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)" -ErrorAction SilentlyContinue |
                ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        } catch { Log "kill failed: $_" }
        $armDecision = ''
        try {
            $armDecision = & (Join-Path $PSScriptRoot 'api_storm_gate.ps1') -Verb Arm -ErrFile $roundErr -FlagPath $stormFlag
        } catch { Log "storm-arm crashed (non-fatal): $_" }
        if ($armDecision) { Log "storm-arm: $armDecision" }
        Beat "round hard-cap killed (backstop, age over ${RoundTimeoutMinutes}min)"
        exit 3
    }
    $p.Refresh()
    Log "headless round finished exit=$($p.ExitCode) (backstop path)"
    Beat "round done exit=$($p.ExitCode)"
    exit $p.ExitCode
}
finally {
    Remove-Item $lock -Force -ErrorAction SilentlyContinue
}
