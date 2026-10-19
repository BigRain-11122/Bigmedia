# tools/run_suite.ps1 -- test-suite wrapper with TRUE exit-code capture.
# tech#33 (R1840). Root defect (R1839): piping `python -m unittest ... 2>&1`
# through PS 5.1 cmdlets wraps native stderr in ErrorRecords and can surface a
# pseudo-rc to the caller (a green suite once read as red). This wrapper never
# pipes python output: both streams are redirected to files via Start-Process
# and the real process exit code is reported and propagated.
#
# tech#35 (R1841): PS 5.1 Start-Process -Redirect* artifacts (and outer shell
# captures of this wrapper's own stdout) can carry NUL padding -- raw reads hit
# binary rejection or truncated-tail illusions (R1840 double evidence:
# bs-test-suite.log.err residue + NUL zone; wrapper stdout 566B with NULs).
# The canonical consumer surface is therefore NOT the .out/.err logs nor
# wrapper stdout, but the result file this wrapper writes itself via
# [IO.File]::WriteAllLines (exact-length UTF-8, no BOM, NUL-free -- PS cmdlet
# path, never a Start-Process redirect handle). Do not read the redirect
# artifacts raw; read the result file.
#
# tech#198 (R2336, pitfall ledger): NEVER build an evidence file by pointing
# PS `>` at this wrapper's or any native tool's output. PS 5.1 re-encodes the
# native byte stream through its own codepage and corrupts it (R2331 anchor:
# `python -m unittest > file 2>&1` produced a dead result-marker line, NUL
# padding, and mixed traceback frames -- the suite log read as a binary file).
# Evidence chains go through THIS wrapper's own result file, or through
# python subprocess capture_output written as raw bytes. PS `>` is reserved
# for PS object streams only.
#
# tech#240 (R2388): env preflight. Before the suite starts the wrapper
# checks ffmpeg AND ffprobe on two slots each (PATH slot via Get-Command
# application lookup + execution slot via `-version`). R2382 anchor: a
# winget upgrade race removed the old bin dir mid-session; 11 suite
# failures all landed on the ffprobe dependency face (source duration
# unprovable = fail-closed verdicts reading like code regressions) and
# burned ~10min, while ffmpeg's Tuanjie hub copy masked the half-broken
# env. Missing/unexecutable binary -> dedicated rc 126 + LOUD
# ENV-PREFLIGHT-FAIL banner on stdout AND in the canonical result file;
# the suite never starts on a broken env.
#
# Usage:
#   tools/run_suite.ps1                                   # full discovery (tests/)
#   tools/run_suite.ps1 -Module tests.test_board_check    # one module
#   tools/run_suite.ps1 -Module tests.test_x -Log C:\t\my.log [-ResultFile C:\t\r.txt]
# Output (machine-readable): SUITE_RC / SUITE_RAN / SUITE_SECONDS /
#   SUITE_RESULT lines on stdout AND (canonical, NUL-free) in the result
#   file next to the log.
# tech#168 (R2248): SUITE_SECONDS is parsed verbatim from unittest's own
#   "Ran N tests in X.Ys" line - the runner's own clock is the single
#   timing source, no wrapper-side stopwatch. Budget classification
#   (>=120s WARN / >=180s FORCED-EVAL) lives in src/os/suite_budget.py
#   (single truth; this wrapper never duplicates thresholds).
# Exit code = real python/unittest exit code.

param(
    [string]$Module = "",
    [string]$Log = "",
    [string]$ResultFile = ""
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
if (-not $Log) { $Log = Join-Path ([System.IO.Path]::GetTempPath()) "bs-test-suite.log" }
if (-not $ResultFile) { $ResultFile = "$Log.result" }
$outLog = "$Log.out"
$errLog = "$Log.err"

# tech#240 (R2388): ffmpeg/ffprobe env preflight - the suite must never
# start on a half-broken media env (R2382 anchor: winget upgrade race
# removed the old bin dir; 11 ffprobe-dependent failures burned ~10min and
# read like code regressions while ffmpeg's Tuanjie hub copy masked the
# break). Two slots per binary: PATH slot (Get-Command application
# lookup) + execution slot (-version must actually run). Refusal =
# dedicated rc 126 + LOUD banner on stdout AND in the canonical result
# file.
$preflightRc = 0
$preflightLines = @()
foreach ($bin in @("ffmpeg", "ffprobe")) {
    $slot = $null
    try {
        $slot = (Get-Command -Name $bin -CommandType Application -ErrorAction SilentlyContinue |
                 Select-Object -First 1).Source
    } catch { $slot = $null }
    if (-not $slot) {
        $preflightRc = 126
        $preflightLines += ("ENV-PREFLIGHT-FAIL: " + $bin + " NOT FOUND ON PATH (tech#240) - suite refused, fix the media env before burning a suite run")
        continue
    }
    $pfOut = Join-Path ([System.IO.Path]::GetTempPath()) ("bs-preflight-" + $bin + ".out")
    $pfErr = Join-Path ([System.IO.Path]::GetTempPath()) ("bs-preflight-" + $bin + ".err")
    try {
        Remove-Item -Path $pfOut, $pfErr -ErrorAction SilentlyContinue
        $pfp = Start-Process -FilePath $slot -ArgumentList "-version" -NoNewWindow -Wait -PassThru -RedirectStandardOutput $pfOut -RedirectStandardError $pfErr
        Remove-Item -Path $pfOut, $pfErr -ErrorAction SilentlyContinue
        if ($pfp.ExitCode -ne 0) {
            $preflightRc = 126
            $preflightLines += ("ENV-PREFLIGHT-FAIL: " + $bin + " FOUND AT " + $slot + " BUT -version EXIT " + $pfp.ExitCode + " (tech#240) - suite refused")
        }
    } catch {
        $preflightRc = 126
        $preflightLines += ("ENV-PREFLIGHT-FAIL: " + $bin + " FOUND AT " + $slot + " BUT -version THREW: " + $_.Exception.Message + " (tech#240) - suite refused")
    }
}
if ($preflightRc -ne 0) {
    $summary = @("SUITE_RC=126")
    $summary += $preflightLines
    $summary += ("SUITE_RESULT=ENV-PREFLIGHT-REFUSED (tech#240)")
    $summary += ("SUITE_RESULT_FILE=" + $ResultFile)
    [System.IO.File]::WriteAllLines($ResultFile, [string[]]$summary)
    foreach ($l in $preflightLines) { Write-Output $l }
    Write-Output "SUITE_RC=126"
    Write-Output ("SUITE_RESULT=ENV-PREFLIGHT-REFUSED (tech#240)")
    Write-Output ("SUITE_RESULT_FILE=" + $ResultFile)
    exit 126
}
Write-Output ("run_suite: env-preflight ffmpeg+ffprobe OK (tech#240)")

$argList = @("-X", "utf8", "-m", "unittest")
$target = $Module
if ($Module) {
    $argList += $Module
} else {
    $argList += @("discover", "-s", "tests", "-p", "test_*.py")
    $target = "discover tests/"
}

# Start-Process redirect does NOT truncate an existing log: a stale run's
# summary (or a crashed short run tailing into it) could be misread as this
# run's result. Delete all three artifacts so each run starts from byte zero.
# Concurrent runs must pass distinct -Log paths.
Remove-Item -Path $outLog -ErrorAction SilentlyContinue
Remove-Item -Path $errLog -ErrorAction SilentlyContinue
Remove-Item -Path $ResultFile -ErrorAction SilentlyContinue

Write-Output ("run_suite: repo=" + $repo)
Write-Output ("run_suite: target=" + $target)
Write-Output ("run_suite: python " + ($argList -join " "))

$summary = @()
try {
    $proc = Start-Process -FilePath "python" `
        -ArgumentList $argList `
        -WorkingDirectory $repo `
        -RedirectStandardOutput $outLog `
        -RedirectStandardError $errLog `
        -Wait -PassThru -NoNewWindow
} catch {
    $summary = @("SUITE_RC=127")
    $summary += ("SUITE_RESULT_FILE=" + $ResultFile)
    [System.IO.File]::WriteAllLines($ResultFile, [string[]]$summary)
    Write-Output ("run_suite: FAILED to start python: " + $_.Exception.Message)
    Write-Output ($summary | ForEach-Object { $_ })
    exit 127
}

$rc = $proc.ExitCode

# unittest writes progress and the result summary to stderr. Strip any NUL
# chars from the lines (redirect artifacts may embed U+0000 -- defense in
# depth for the tail we mirror into the result file).
$ranLine = ""
$resultLine = ""
$tail = @()
if (Test-Path $errLog) {
    $tail = @(Get-Content -Path $errLog -Tail 12 -Encoding UTF8 |
        ForEach-Object { $_ -replace "\x00", "" })
    foreach ($l in $tail) {
        if ($l -match '^Ran \d+ tests?') { $ranLine = $l.Trim() }
        if ($l -match '^(OK|FAILED)') { $resultLine = $l.Trim() }
    }
}

$summary = @("SUITE_RC=" + $rc)
if ($ranLine)    { $summary += ("SUITE_RAN=" + $ranLine) }
# tech#168: surface the runner-reported duration as its own machine-readable
# line (verbatim digits from the RAN line - no wrapper-side timing).
$secLine = ""
if ($ranLine -match 'in (\d+(?:\.\d+)?)s') { $secLine = $Matches[1] }
if ($secLine) { $summary += ("SUITE_SECONDS=" + $secLine) }
if ($resultLine) { $summary += ("SUITE_RESULT=" + $resultLine) }
$summary += ("SUITE_LOG_OUT=" + $outLog)
$summary += ("SUITE_LOG_ERR=" + $errLog)
$summary += ("SUITE_RESULT_FILE=" + $ResultFile)
if ($tail.Count -gt 0) {
    $summary += "run_suite: last stderr lines:"
    $summary += @($tail | Select-Object -Last 5 | ForEach-Object { "  " + $_ })
}

# Canonical NUL-free artifact: exact-length UTF-8 (no BOM) written by the
# wrapper itself through the PS cmdlet path, never a Start-Process handle.
# [IO.File]::WriteAllLines truncates to exact content (R1802 precedent).
[System.IO.File]::WriteAllLines($ResultFile, [string[]]$summary)

$summary | ForEach-Object { Write-Output $_ }
exit $rc
