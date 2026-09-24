# Loop-log display window for footage capture (footage-matching-spec S2).
# Opens a titled console that keeps tailing the OS loop state + heartbeat
# so the "10-minute self-wake" beat records a LIVE log face. ASCII only.
$host.UI.RawUI.WindowTitle = "BS-OSLoop-Log"
Set-Location "C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
for () {
    Clear-Host
    Write-Output "=== BigStream OS Loop :: state tail ==="
    Get-Content "src\os\state.json" -Tail 28 -Encoding UTF8
    Write-Output ""
    Write-Output "=== probe heartbeat tail ==="
    Get-Content "logs\probe-heartbeat.txt" -Tail 6 -Encoding UTF8
    Start-Sleep -Seconds 3
}
