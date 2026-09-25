@echo off
rem R316 C1 leg-3 pilot re-render: bs-001 douyin v15 with speed-ramp engine
rem (R315 legs 1-2). Same timeline inputs as F-006 v14b-douyin (cards/srt/
rem audio source reuse, anti-duplication law); only edit language gains
rem punch-beat speed ramps. Explicit PATH prepend (R199 lesson).
set "PATH=C:\Users\sjs20\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin;%PATH%"
cd /d C:\Users\sjs20\Desktop\FluxGroup\media\BigStream
python src\render\edit_craft.py --profile douyin --cards data\sources\bs001\cards-v12-matched.json --srt output\renders\.v11-trim\subs.srt --audio output\renders\.v11-trim\audio.mp3 --out output\renders\bs-001-v15-douyin-9x16.mp4 1>.bs001-dy-tmp\render-v15-stdout.txt 2>.bs001-dy-tmp\render-v15-stderr.txt
