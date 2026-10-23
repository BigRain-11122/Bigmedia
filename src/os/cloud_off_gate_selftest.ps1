# Self-test for the T0 CLOUD-OFF gate resolver (order 2026-10-20 section 8.5).
# Runs the resolution only - never spawns a round. Pure ASCII.
# Exit 0 = all assertions pass, 2 = failure.

. (Join-Path $PSScriptRoot 'cloud_off_gate.ps1')

$script:fail = 0
function Assert-That {
    param([bool]$Cond, [string]$Name)
    if ($Cond) { "PASS $Name" } else { "FAIL $Name"; $script:fail++ }
}

# 1. Physical repo path resolves to the FluxGroup root that holds the marker.
$realRepo = 'D:\FluxGroup\media\BigStream'
if (Test-Path $realRepo) {
    $got = Get-CloudOffMarkerRoot -ScriptRoot (Join-Path $realRepo 'src\os') -Project $realRepo
    Assert-That ($got -eq 'D:\FluxGroup') "real tree -> FluxGroup root (got: $got)"
} else {
    "SKIP real tree (not present on this machine)"
}

# 2. The symlinked Desktop path (the one the scheduled task uses) resolves to the
#    same physical root. This is the regression case: the marker is absent from
#    the Desktop tree's own cph4 mirror.
$linkRepo = 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
if (Test-Path $linkRepo) {
    $got = Get-CloudOffMarkerRoot -ScriptRoot (Join-Path $linkRepo 'src\os') -Project $linkRepo
    Assert-That ($got -eq 'D:\FluxGroup') "symlinked tree -> physical FluxGroup root (got: $got)"
} else {
    "SKIP symlinked tree (not present on this machine)"
}

# 3. A tree with no marker anywhere resolves to $null (gate stays open).
$tmp = Join-Path $env:TEMP ('co-gate-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force $tmp | Out-Null
$got = Get-CloudOffMarkerRoot -ScriptRoot (Join-Path $tmp 'src\os') -Project ''
Assert-That ($null -eq $got) "no marker -> null (got: $got)"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue

if ($script:fail -gt 0) { "SELFTEST FAIL ($script:fail)"; exit 2 }
"SELFTEST OK"
exit 0