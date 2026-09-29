# -*- coding: utf-8 -*-
# R695 LC-006 ASR detached runner (writes .lc006-tmp/asr-check.srt + asr-exit.txt)
# R692 asr_r692.py pattern. R169 QC recipe: medium-int8 + beam5 + noctx, HF_HUB_OFFLINE=1 (R638 env law)
import os, sys, io
os.environ["HF_HUB_OFFLINE"] = "1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
rc = 0
try:
    sys.argv = ["whisper_to_srt.py",
                "--audio", r".lc006-tmp/audio.mp3",
                "--out", r".lc006-tmp/asr-check.srt",
                "--model", "medium", "--beam-size", "5", "--no-context"]
    import runpy
    runpy.run_path(r"src/render/whisper_to_srt.py", run_name="__main__")
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else 0
except Exception as ex:
    rc = 1
    io.open(r".lc006-tmp/asr-err.txt", "w", encoding="utf-8").write(repr(ex))
io.open(r".lc006-tmp/asr-exit.txt", "w", encoding="utf-8").write(str(rc))
