# R739 detached launcher (absolute-path law R728/R731: Start-Process with
# relative python entry fails silently under PS 5.1; .ps1 absolute path works).
$root = "C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
Start-Process -FilePath "python" -ArgumentList "$root\.lc018-tmp\s1_call.py" -WorkingDirectory $root -WindowStyle Hidden
Start-Sleep -Seconds 2
Start-Process -FilePath "python" -ArgumentList "$root\.c3-tmp\r739_tts_run.py v1" -WorkingDirectory $root -WindowStyle Hidden
Write-Output "LAUNCHED"
