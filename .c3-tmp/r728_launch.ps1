$root = "C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
$ver = $args[0]
if (-not $ver) { $ver = "v3" }
Start-Process -FilePath "python" -ArgumentList "`"$root\.c3-tmp\r728_tts_run.py`"","$ver" -WorkingDirectory $root -WindowStyle Hidden
Write-Output "LAUNCH_OK_$ver"
