# -*- coding: utf-8 -*-
"""S2 static-frame spec probe for MC-20261015-REACT-v20 (R2281).
Checks mp4 against cards.json: width/height/fps/duration + zero audio."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MP4 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(HERE)))), "output", "renders", "mc-20261015-react-v20-card.mp4")
CARDS = os.path.join(os.path.dirname(HERE), "MC-20261015-REACT-v20", "cards.json")

d = json.load(open(CARDS, encoding="utf-8"))
exp_w, exp_h, exp_fps = d["video"]["width"], d["video"]["height"], d["video"]["fps"]
exp_dur = d["cards"][0]["end"] + d.get("tail", 0.8)

r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=width,height,avg_frame_rate",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1", MP4],
                   capture_output=True, text=True)
ra = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                     "-show_entries", "stream=index",
                     "-of", "default=noprint_wrappers=1", MP4],
                    capture_output=True, text=True)
got = {}
for ln in r.stdout.splitlines():
    if "=" in ln:
        k, v = ln.split("=", 1)
        got[k] = v
audio_streams = [l for l in ra.stdout.splitlines() if l.strip()]

fails = []
w, h = int(got["width"]), int(got["height"])
dur = float(got["duration"])
num, den = got["avg_frame_rate"].split("/")
fps = float(num) / float(den)
ok_wh = (w, h) == (exp_w, exp_h)
ok_fps = abs(fps - exp_fps) < 0.5
ok_dur = abs(dur - exp_dur) < 0.25
ok_audio = len(audio_streams) == 0
print("spec probe r2281 (static-frame path, cards.json as spec source)")
print("dims %dx%d vs %dx%d expected: %s" % (w, h, exp_w, exp_h, "PASS" if ok_wh else "FAIL"))
print("fps %.3f vs %d expected: %s" % (fps, exp_fps, "PASS" if ok_fps else "FAIL"))
print("duration %.3fs vs %.2fs (card %.1f + tail %.1f) expected: %s"
      % (dur, exp_dur, d["cards"][0]["end"], d.get("tail", 0.8), "PASS" if ok_dur else "FAIL"))
print("audio streams: %d (%s)" % (len(audio_streams), "PASS zero-audio" if ok_audio else "FAIL has audio"))
if not (ok_wh and ok_fps and ok_dur and ok_audio):
    sys.exit(1)
print("SPEC PROBE: ALL PASS")
