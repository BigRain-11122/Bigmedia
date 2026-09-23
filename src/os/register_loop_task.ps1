# Registers the BigStream-OSLoop: 10-minute self-iteration round launcher.
# Ported 2026-09-23 from the proven BigMoney pattern (Tools/register_loop_task.ps1).
# CEO order O-20260923-1525-bm-a: infrastructure first, rules, self-iteration,
# NO content production (see src/os/iteration_prompt.txt).
# PATH-AGNOSTIC (any machine, any folder): every path is derived from this
# script's own location - zero edits needed on a new machine.
# Pure ASCII (see iteration_loop.ps1 ENCODING RULE). Idempotent via -Force.
# Re-registering refreshes the task definition - safe to re-run for self-heal.
$Project = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$launcher = Join-Path $Project 'src\os\iteration_loop.ps1'
$vbs = Join-Path $Project 'src\os\InvisibleRunner.vbs'
if (-not (Test-Path $launcher)) { Write-Output "FATAL: $launcher missing"; exit 1 }
if (-not (Test-Path $vbs)) { Write-Output "FATAL: $vbs missing"; exit 1 }
$a = New-ScheduledTaskAction -Execute 'wscript.exe' `
    -Argument ('//B //nologo "' + $vbs + '" powershell.exe -NoProfile -ExecutionPolicy Bypass -File "' + $launcher + '"') `
    -WorkingDirectory $Project
$start = Get-Date -Minute 0 -Second 0
while ($start -le (Get-Date)) { $start = $start.AddMinutes(8) }
$t = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 3650)
$s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 35)
Register-ScheduledTask -TaskName 'BigStream-OSLoop' -Action $a -Trigger $t -Settings $s -Force | Out-Null
Write-Output "registered BigStream-OSLoop (project=$Project), first fire $start"
