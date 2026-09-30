# R735 detached launcher (R728 absolute-path law): S1 gate + TTS v1 for LC-017
Start-Process -FilePath 'python' -ArgumentList 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc017-tmp\s1_call.py' -WindowStyle Hidden
Start-Sleep -Seconds 2
Start-Process -FilePath 'python' -ArgumentList 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r735_tts_run.py','v1' -WindowStyle Hidden
