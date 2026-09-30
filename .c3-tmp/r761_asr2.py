# -*- coding: utf-8 -*-
# R761 BS-007 ASR final track, attempt 2 (re-download path per R701 precedent: HF cache wiped again
# by group disk-sweep after R756 15:24 run; in-service ASR production line self-heal, 1.46GB medium model).
# HF_HUB_OFFLINE unset per R638/R701 pitfall resolution.
import os, sys
if "HF_HUB_OFFLINE" in os.environ:
    del os.environ["HF_HUB_OFFLINE"]
sys.argv = ["whisper_to_srt.py",
            "--audio", r".bs007-tmp/audio.mp3",
            "--out", r".bs007-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
