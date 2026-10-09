# tools/run_suite.ps1 -- test-suite wrapper with TRUE exit-code capture.
# tech#33 (R1840). Root defect (R1839): piping `python -m unittest ... 2>&1`
# through PS 5.1 cmdlets wraps native stderr in ErrorRecords and can surface a
# pseudo-rc to the caller (a green suite once read as red). This wrapper never
# pipes python output: both streams are redirected to files via Start-Process
# and the real process exit code is reported and propagated.
#
# Usage:
#   tools/run_suite.ps1                                   # full discovery (tests/)
#   tools/run_suite.ps1 -Module tests.test_board_check    # one module
#   tools/run_suite.ps1 -Module tests.test_x -Log C:\t\my.log
# Output (machine-readable): SUITE_RC / SUITE_RAN / SUITE_RESULT / log paths.
# Exit code = real python/unittest exit code.

param(
    [string]$Module = "",
    [string]$Log = ""
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
if (-not $Log) { $Log = Join-Path ([System.IO.Path]::GetTempPath()) "bs-test-suite.log" }
$outLog = "$Log.out"
$errLog = "$Log.err"

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
# run's result. Delete both logs so each run starts from byte zero.
# Concurrent runs must pass distinct -Log paths.
Remove-Item -Path $outLog -ErrorAction SilentlyContinue
Remove-Item -Path $errLog -ErrorAction SilentlyContinue

Write-Output ("run_suite: repo=" + $repo)
Write-Output ("run_suite: target=" + $target)
Write-Output ("run_suite: python " + ($argList -join " "))

try {
    $proc = Start-Process -FilePath "python" `
        -ArgumentList $argList `
        -WorkingDirectory $repo `
        -RedirectStandardOutput $outLog `
        -RedirectStandardError $errLog `
        -Wait -PassThru -NoNewWindow
} catch {
    Write-Output ("run_suite: FAILED to start python: " + $_.Exception.Message)
    exit 127
}

$rc = $proc.ExitCode

# unittest writes progress and the result summary to stderr
$ranLine = ""
$resultLine = ""
$tail = @()
if (Test-Path $errLog) {
    $tail = @(Get-Content -Path $errLog -Tail 12 -Encoding UTF8)
    foreach ($l in $tail) {
        if ($l -match '^Ran \d+ tests?') { $ranLine = $l.Trim() }
        if ($l -match '^(OK|FAILED)') { $resultLine = $l.Trim() }
    }
}

Write-Output ("SUITE_RC=" + $rc)
if ($ranLine)   { Write-Output ("SUITE_RAN=" + $ranLine) }
if ($resultLine) { Write-Output ("SUITE_RESULT=" + $resultLine) }
Write-Output ("SUITE_LOG_OUT=" + $outLog)
Write-Output ("SUITE_LOG_ERR=" + $errLog)
if ($tail.Count -gt 0) {
    Write-Output "run_suite: last stderr lines:"
    $tail | Select-Object -Last 5 | ForEach-Object { Write-Output ("  " + $_) }
}
exit $rc
