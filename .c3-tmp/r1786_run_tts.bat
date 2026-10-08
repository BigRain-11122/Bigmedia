@echo off
echo TTS-ROLES START %date% %time%
python "C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1786_tts_roles.py" > "C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1786_tts.log" 2>&1
echo TTS-ROLES RC=%errorlevel%
echo TTS-ROLES END %date% %time%
