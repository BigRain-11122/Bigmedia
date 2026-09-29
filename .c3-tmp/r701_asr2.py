# -*- coding: utf-8 -*-
# R701 LC-008 ASR final track, attempt 2 (re-download path: HF cache wiped post-09-24 anchor;
# network probed reachable 0.56-0.92s; HF_HUB_OFFLINE unset per R638 pitfall resolution)
import os, sys
sys.argv = ["whisper_to_srt.py",
            "--audio", r".lc008-tmp/audio.mp3",
            "--out", r".lc008-tmp/asr-check.srt",
            "--model", "medium", "--beam-size", "5", "--no-context"]
import runpy
try:
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    print("exit=", e.code)
