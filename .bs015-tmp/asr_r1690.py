# -*- coding: utf-8 -*-
# R1690 BS-015 ASR final track (R169 QC recipe: medium int8 + beam5 + noctx, HF_HUB_OFFLINE=1)
# pattern: .bs014-tmp/asr_r1686.py (offline-first)
import os, sys
os.environ["HF_HUB_OFFLINE"] = "1"
sys.argv = ["whisper_to_srt.py",
            "--audio", r".bs015-tmp/audio.mp3",
            "--out", r".bs015-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
