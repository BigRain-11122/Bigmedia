# R734 detached launcher (R728 absolute-path law): ASR final track + E4 reference for LC-016 closeout
Start-Process -FilePath 'python' -ArgumentList 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r734_asr.py' -WorkingDirectory 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream' -WindowStyle Hidden
Start-Sleep -Seconds 2
Start-Process -FilePath 'python' -ArgumentList 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc016-tmp\e4_call.py' -WorkingDirectory 'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream' -WindowStyle Hidden
