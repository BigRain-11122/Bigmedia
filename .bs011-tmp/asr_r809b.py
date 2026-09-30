# -*- coding: utf-8 -*-
# R809 BS-011 ASR final track - flight B (online self-heal after offline LocalEntryNotFound,
# HF cache 5th-clear precedent: R701/R761/R801/R806 -> R809 fifth occurrence)
import os, sys
os.environ["HF_HUB_OFFLINE"] = "0"
sys.argv = ["whisper_to_srt.py",
            "--audio", r".bs011-tmp/audio.mp3",
            "--out", r".bs011-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
