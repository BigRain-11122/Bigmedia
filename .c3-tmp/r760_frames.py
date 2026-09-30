# -*- coding: utf-8 -*-
# R760: frame-verify three laws for bs-007 (head 12 + mid/tail of 3 longest beats)
import subprocess, json, io, os
from PIL import Image

VID = r"output\renders\bs-007-v1-shipinhao-60s.mp4"
D = r".bs007-tmp\frameverify-r760"
os.makedirs(D, exist_ok=True)
cfg = json.load(io.open(r"data\sources\bs007\cards-v1-matched.json", encoding="utf-8"))
cards = cfg["cards"]

def grab(t, out):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-ss", "%.3f" % t, "-i", VID, "-frames:v", "1", out], check=True)

# law1: beat head frames (start+0.5 fully visible)
heads = []
for i, c in enumerate(cards):
    t = c["start"] + 0.5
    f = "%s/h%02d.png" % (D, i)
    grab(t, f)
    heads.append(f)

# law2: mid+tail of three longest beats
durs = [(c["end"] - c["start"], i) for i, c in enumerate(cards)]
top3 = sorted(durs, reverse=True)[:3]
mids = []
for d, i in sorted(top3, key=lambda x: x[1]):
    c = cards[i]
    grab((c["start"] + c["end"]) / 2.0, "%s/m%02d.png" % (D, i))
    grab(c["end"] - 0.3, "%s/t%02d.png" % (D, i))
    mids += [i]
print("top3 longest beats:", mids, ["%.2f" % d for d, _ in top3])

# tiles: heads 4x3, midtail 3x2
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

# law3: crossings honest computation (matched src starts at off 0, wraps if beat>src)
SRC_DUR = {"looplog": 12.0, "biggame": 45.0, "reviews": 10.0}
cross = []
for i, c in enumerate(cards):
    v = c["visual"]
    if "source" in v:
        dur = SRC_DUR["looplog" if "looplog" in v["source"] else ("biggame" if "biggame" in v["source"] else "reviews")]
        if (c["end"] - c["start"]) > dur:
            cross.append(i)
print("crossings:", cross if cross else "{}")
print("TILES DONE")
