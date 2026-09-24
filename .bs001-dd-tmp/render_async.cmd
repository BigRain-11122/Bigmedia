@echo off
rem R199 relaunch of the R198 DD bilibili render: the async child lacked
rem ffmpeg on PATH (winget user-PATH not inherited). Explicit PATH prepend
rem immunizes the launch. Fleet grain standard = 0 (verified empirically
rem R199: flat patches std 0.00 on F-003/F-004 current pieces).
set "PATH=C:\Users\sjs20\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin;%PATH%"
cd /d C:\Users\sjs20\Desktop\FluxGroup\media\BigStream
python src\render\edit_craft.py --profile bilibili --cards data\sources\bs001-dd\cards-dd-v1-matched-16x9.json --srt .bs001-dd-tmp\subs.srt --audio .bs001-dd-tmp\audio.mp3 --out output\renders\bs-001-dd-v1-bilibili-16x9.mp4 1>.bs001-dd-tmp\render-stdout.txt 2>.bs001-dd-tmp\render-stderr.txt
