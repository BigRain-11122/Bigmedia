# -*- coding: utf-8 -*-
# R803: frame-verify three laws for bs-009 (head 12 + mid/tail of 3 longest beats)
# (R800 frames chain-inheritance)
import subprocess, json, io, os
from PIL import Image

VID = r"output\renders\bs-009-v1-shipinhao-60s.mp4"
D = r".bs009-tmp\frameverify-r803"
os.makedirs(D, exist_ok=True)
cfg = json.load(io.open(r"data\sources\bs009\cards-v1-matched.json", encoding="utf-8"))
cards = cfg["cards"]

def grab(t, out):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-ss", "%.3f" % t, "-i", VID, "-frames:v", "1", out], check=True)

heads = []
for i, c in enumerate(cards):
    t = c["start"] + 0.5
    f = "%s/h%02d.png" % (D, i)
    grab(t, f)
    heads.append(f)

durs = [(c["end"] - c["start"], i) for i, c in enumerate(cards)]
top3 = sorted(durs, reverse=True)[:3]
mids = []
for d, i in sorted(top3, key=lambda x: x[1]):
    c = cards[i]
    grab((c["start"] + c["end"]) / 2.0, "%s/m%02d.png" % (D, i))
    grab(c["end"] - 0.3, "%s/t%02d.png" % (D, i))
    mids += [i]
print("top3 longest beats:", mids, ["%.2f" % d for d, _ in top3])

def tile(files, cols, path, w=270, h=480):
    rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (w * cols, h * rows), "black")
    for i, f in enumerate(files):
        im.paste(Image.open(f).convert("RGB").resize((w, h)), (w * (i % cols), h * (i // cols)))
    im.save(path)
    return path

tile(heads, 4, D + "/heads-tile.png")
mt = []
for i in mids:
    mt += ["%s/m%02d.png" % (D, i), "%s/t%02d.png" % (D, i)]
tile(mt, 3, D + "/midtail-tile.png")

SRC_DUR = {"looplog": 12.0, "reviews": 10.0, "editgrid": 10.0}
cross = []
for i, c in enumerate(cards):
    v = c["visual"]
    if "source" in v:
        dur = SRC_DUR["looplog" if "looplog" in v["source"] else ("reviews" if "reviews" in v["source"] else "editgrid")]
        if (c["end"] - c["start"]) > dur:
            cross.append(i)
print("crossings:", cross if cross else "{}")
print("TILES DONE")
