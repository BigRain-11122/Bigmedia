# -*- coding: utf-8 -*-
# R1683 BS-013 ASR final track (R169 QC recipe: medium int8 + beam5 + noctx, HF_HUB_OFFLINE=1)
# pattern: .bs012-tmp/asr_r1680.py (offline-first, online self-heal if LocalEntryNotFound)
import os, sys
os.environ["HF_HUB_OFFLINE"] = "1"
sys.argv = ["whisper_to_srt.py",
            "--audio", r".bs013-tmp/audio.mp3",
            "--out", r".bs013-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
