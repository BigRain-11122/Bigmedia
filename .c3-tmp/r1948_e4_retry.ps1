# E4 patient retry loop for SC-004-01 (R1948)
# Polls GPU window via call_expert's built-in guard; exits on verdict or after max attempts.
$material = "data\storylines\audio\sc004-01-v1-tmp\e4-material.md"
$out = "data\storylines\audio\sc004-01-v1-tmp\e4-run-r1948-retry.out"
$err = "data\storylines\audio\sc004-01-v1-tmp\e4-run-r1948-retry.err"
$max = 24
for ($i = 1; $i -le $max; $i++) {
    $ts = Get-Date -Format "HH:mm:ss"
    Add-Content $out "attempt $i at $ts"
    $p = Start-Process -FilePath "python" -ArgumentList "src\call_expert.py --expert E4-audience --material $material --timeout 1500 --gpu-guard" -RedirectStandardOutput "$env:TEMP\e4r_out.txt" -RedirectStandardError "$env:TEMP\e4r_err.txt" -WindowStyle Hidden -PassThru -Wait
    $txt = Get-Content "$env:TEMP\e4r_out.txt" -Raw -ErrorAction SilentlyContinue
    if ($txt -match "DEFER") {
        Add-Content $out "attempt $i DEFER (window closed), waiting 45s"
        Start-Sleep -Seconds 45
    } else {
        Add-Content $out "attempt $i non-DEFER result:"
        Add-Content $out $txt
        break
    }
}
Add-Content $out "loop end at $(Get-Date -Format 'HH:mm:ss')"
