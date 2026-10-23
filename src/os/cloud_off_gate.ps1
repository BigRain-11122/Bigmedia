# T0 CLOUD-OFF gate resolver (CEO order 2026-10-20, CLOUD-OFF-LOCAL-ONLY-v1).
# The gate marker lives at <FluxGroupRoot>\cph4\fleet\CLOUD-OFF-LOCAL-ONLY-v1.md.
#
# Literal ancestor walking alone is not enough: on this machine the scheduled
# task registers media/BigStream through a symlinked Desktop path
# (C:\Users\<user>\Desktop\FluxGroup\media -> D:\FluxGroup\media), and the
# Desktop tree carries its own stale cph4 mirror without the marker. The walk
# therefore found nothing, the guard stayed silent, and cloud rounds kept
# igniting every 5 minutes - a T0 violation. git reports the physical toplevel,
# so its ancestors are searched too.
#
# Pure ASCII (powershell.exe 5.1 decodes BOM-less .ps1 as ANSI/GBK).

function Get-CloudOffMarkerRoot {
    param(
        [string]$ScriptRoot = $PSScriptRoot,
        [string]$Project = ''
    )

    $seeds = New-Object System.Collections.Generic.List[string]
    $seeds.Add($ScriptRoot)
    if ($Project) {
        try {
            $top = & git -C $Project rev-parse --show-toplevel 2>$null
            if ($LASTEXITCODE -eq 0 -and $top) {
                $seeds.Add(($top.Trim() -replace '/', '\'))
            }
        } catch { }
    }

    # Climb from every seed: the script root may sit under a symlink, while git
    # reports the physical toplevel whose ancestors hold the marker.
    foreach ($seed in $seeds) {
        $cur = $seed
        while ($cur) {
            $marker = Join-Path $cur 'cph4\fleet\CLOUD-OFF-LOCAL-ONLY-v1.md'
            if (Test-Path $marker) { return $cur }
            $parent = Split-Path -Parent $cur
            if (-not $parent -or $parent -eq $cur) { break }
            $cur = $parent
        }
    }
    return $null
}