# -*- coding: utf-8 -*-
# R697: LC-007 3-law frame sampling (R694 LC-006 pattern): heads x12 + mid/tail of 3 longest beats + tiles
import json, io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".lc007-tmp")
MP4 = os.path.join("output", "renders", "lc-007-v1-shipinhao-60s.mp4")

with io.open(os.path.join(ROOT, "data", "sources", "lc007", "cards-v1-matched.json"), encoding="utf-8") as fh:
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

# mid/tail for 3 longest beats (b3 7.08 / b5 6.38 / b6 5.75)
for i in (3, 5, 6):
    s, e = beats[i][1], beats[i][2]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(s + (e - s) / 2), "-i", MP4,
                    "-frames:v", "1", os.path.join(TMP, "fs-m%02d.png" % i)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(e - 0.15), "-i", MP4,
                    "-frames:v", "1", os.path.join(TMP, "fs-t%02d.png" % i)], check=True)

# tiles: heads 4x3 (each scaled 270x480), midtail 2x3
def tile(names, out, cols):
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
            fc += "[%d:v]scale=270:480[v%d];" % (idx, idx)
            idx += 1
    # hstack rows then vstack
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
tile(["fs-m03.png", "fs-m05.png", "fs-m06.png", "fs-t03.png", "fs-t05.png", "fs-t06.png"],
     "fs-tile-midtail.png", 3)
print("frame sampling done")
