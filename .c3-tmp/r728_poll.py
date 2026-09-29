# -*- coding: utf-8 -*-
import io, os, glob, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = os.path.join(ROOT, ".c3-tmp", "r728_tts_v2.txt")
now = time.time()
for pat in ("seg00.mp3", "seg11.mp3", "audio.mp3", "subs.srt"):
    hits = glob.glob(os.path.join(ROOT, ".lc015-tmp", pat))
    if hits:
        print(pat, "age_min=", round((now - os.path.getmtime(hits[0])) / 60, 1))
print("result_exists=", os.path.exists(f))
if os.path.exists(f):
    print(io.open(f, encoding="utf-8").read()[:400])
