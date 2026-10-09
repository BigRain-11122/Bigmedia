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
# Usage:
#   tools/run_suite.ps1                                   # full discovery (tests/)
#   tools/run_suite.ps1 -Module tests.test_board_check    # one module
#   tools/run_suite.ps1 -Module tests.test_x -Log C:\t\my.log [-ResultFile C:\t\r.txt]
# Output (machine-readable): SUITE_RC / SUITE_RAN / SUITE_RESULT lines on
#   stdout AND (canonical, NUL-free) in the result file next to the log.
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
