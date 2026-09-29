# -*- coding: utf-8 -*-
# R711 diagnostic: transcribe isolated middle window (27-54s) to adjudicate VAD chunk-state issue
import os, sys
os.environ["HF_HUB_OFFLINE"] = "1"
sys.argv = ["whisper_to_srt.py",
            "--audio", r".lc011-tmp/mid-27-54.mp3",
            "--out", r".lc011-tmp/mid-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
