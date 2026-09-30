# -*- coding: utf-8 -*-
# R733: LC-016 3-law frame sampling (R725 framecheck.py adapted; 3 longest beats chosen dynamically)
import json, io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".lc016-tmp")
MP4 = os.path.join("output", "renders", "lc-016-v1-shipinhao-60s.mp4")

with io.open(os.path.join(ROOT, "data", "sources", "lc016", "cards-v1-matched.json"), encoding="utf-8") as fh:
    j = json.load(fh)
cards = j["cards"]
beats = [(i, c["start"], c["end"]) for i, c in enumerate(cards)]

# wrap-crossing honest calculation: beat dur vs source dur (13.0s)
SRC_DUR = 13.0
crossings = []
for i, s, e in beats:
    if (e - s) > SRC_DUR:
        crossings.append((i, round(e - s, 2)))
print("crossings:", crossings)

# heads
for i, s, e in beats:
    t = s + 0.15
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", MP4,
                    "-frames:v", "1", os.path.join(TMP, "fs-h%02d.png" % i)], check=True)

# mid/tail for 3 longest beats (dynamic)
durs = sorted(range(len(beats)), key=lambda i: -(beats[i][2] - beats[i][1]))[:3]
top3 = sorted(durs)
print("top3_longest:", [(i, round(beats[i][2] - beats[i][1], 2)) for i in top3])
for i in top3:
    s, e = beats[i][1], beats[i][2]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(s + (e - s) / 2), "-i", MP4,
                    "-frames:v", "1", os.path.join(TMP, "fs-m%02d.png" % i)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(e - 0.15), "-i", MP4,
                    "-frames:v", "1", os.path.join(TMP, "fs-t%02d.png" % i)], check=True)

# tiles: heads 4x3 (each scaled 270x480), midtail 2x3
def tile(names, out, cols, scale=270):
    inputs = []
    for n in names:
        inputs += ["-i", os.path.join(TMP, n)]
    n = len(names)
    rows = (n + cols - 1) // cols
    fc = ""
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= n:
                break
            fc += "[%d:v]scale=%d:%d[v%d];" % (idx, scale, scale * 2, idx)
            idx += 1
    row_elems = []
    idx = 0
    for r in range(rows):
        row_vs = []
        for c in range(cols):
            if idx >= n:
                break
            row_vs.append("[v%d]" % idx)
            idx += 1
        if len(row_vs) > 1:
            fc += "".join(row_vs) + "hstack=inputs=%d[row%d];" % (len(row_vs), r)
        else:
            fc += "%snull[row%d];" % (row_vs[0], r)
        row_elems.append("[row%d]" % r)
    fc += "".join(row_elems) + "vstack=inputs=%d[out]" % len(row_elems)
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs +
                   ["-filter_complex", fc, "-map", "[out]", "-frames:v", "1",
                    os.path.join(TMP, out)], check=True)

heads = ["fs-h%02d.png" % i for i in range(12)]
tile(heads, "fs-tile-heads.png", 4)
tile(["fs-m%02d.png" % i for i in top3] + ["fs-t%02d.png" % i for i in top3],
     "fs-tile-midtail.png", 3)

# AIGC dual-label pair: two full-res head frames side by side (no downscale)
pair = ["fs-h04.png", "fs-h11.png"]
inputs = []
for n in pair:
    inputs += ["-i", os.path.join(TMP, n)]
fc = "[0:v][1:v]hstack=inputs=2[out]"
subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs +
               ["-filter_complex", fc, "-map", "[out]", "-frames:v", "1",
                os.path.join(TMP, "fs-pair-h04-h11.png")], check=True)
print("frame sampling done")
