# -*- coding: utf-8 -*-
# R711 LC-011 ASR final track (R169 QC recipe: medium int8 + beam5 + noctx, HF_HUB_OFFLINE=1)
# pattern: r708_asr.py (R685/R688/R692/R695/R698/R701/R705/R708 precedent)
import os, sys
os.environ["HF_HUB_OFFLINE"] = "1"
sys.argv = ["whisper_to_srt.py",
            "--audio", r".lc011-tmp/audio.mp3",
            "--out", r".lc011-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
