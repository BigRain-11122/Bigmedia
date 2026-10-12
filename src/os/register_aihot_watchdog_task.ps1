# Registers BigStream-AIHotWatchdog: PT5M AIHOT stack autoheal watchdog
# (tech#127, gap anchor R2046 node-kill case family / R2048 case-5 PG port).
# Zero-window law (U060): task action = pythonw.exe (GUI subsystem, no
# console). The watchdog itself spawns every console-subsystem child with
# CREATE_NO_WINDOW, so nothing can flash. Idempotent via -Force.
# Pure ASCII. Path-agnostic (paths derived from this script's location).
$Project = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$script = Join-Path $Project 'src\os\aihot_watchdog.py'
if (-not (Test-Path $script)) { Write-Output "FATAL: $script missing"; exit 1 }
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { Write-Output "FATAL: python not on PATH"; exit 1 }
$pythonw = Join-Path (Split-Path -Parent $py) 'pythonw.exe'
if (-not (Test-Path $pythonw)) { Write-Output "FATAL: $pythonw missing"; exit 1 }
$a = New-ScheduledTaskAction -Execute $pythonw `
    -Argument ('"' + $script + '"') `
    -WorkingDirectory $Project
$start = Get-Date -Minute 0 -Second 0
while ($start -le (Get-Date)) { $start = $start.AddMinutes(4) }
$t = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
$s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName 'BigStream-AIHotWatchdog' -Action $a -Trigger $t -Settings $s -Force | Out-Null
Write-Output "registered BigStream-AIHotWatchdog (pythonw=$pythonw), first fire $start"
