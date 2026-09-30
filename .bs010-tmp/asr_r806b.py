# -*- coding: utf-8 -*-
# R806 BS-010 ASR final track - retry with online re-download (HF cache cleared again,
# 4th occurrence per R701/R761/R801 judgment; self-heal = HF_HUB_OFFLINE=0 re-download)
import os, sys
os.environ["HF_HUB_OFFLINE"] = "0"
sys.argv = ["whisper_to_srt.py",
            "--audio", r".bs010-tmp/audio.mp3",
            "--out", r".bs010-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
