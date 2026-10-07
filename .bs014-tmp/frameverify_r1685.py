# -*- coding: utf-8 -*-
import subprocess, os, io, re
os.makedirs(".bs014-tmp/frameverify-r1685", exist_ok=True)
# card start times from matched cards timeline
import json
c = json.load(io.open("data/sources/bs014/cards-v1-matched.json", encoding="utf-8"))
starts = [cd["start"] for cd in c["cards"]]
HEAD = [round(s + 0.35, 2) for s in starts]
CROSS = [("b0-pre", 4.30), ("b0-x", 4.42), ("b0-post", 4.54)]
FULL = [("t30-b8", starts[8] + 0.5), ("t57-b11", starts[11] + 0.4)]

def grab(t, name):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                    "-i", "output/renders/bs-014-v1-shipinhao-60s.mp4",
                    "-frames:v", "1", ".bs014-tmp/frameverify-r1685/%s.png" % name], check=True)

for i, t in enumerate(HEAD):
    grab(t, "head%02d" % i)
for n, t in CROSS:
    grab(t, n)
for n, t in FULL:
    grab(t, n)
print("OK frames extracted:", len(HEAD) + len(CROSS) + len(FULL), "HEAD=", HEAD)

from PIL import Image
def tile(paths, cols, out, w=360, h=640):
    ims = [Image.open(p).resize((w, h)) for p in paths]
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "black")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    sheet.save(out)
    print("OK sheet:", out)

D = ".bs014-tmp/frameverify-r1685/"
tile([D + "head%02d.png" % i for i in range(12)], 3, D + "sheet-heads.png")
tile([D + p for p in ["b0-pre.png", "b0-x.png", "b0-post.png", "t30-b8.png", "t57-b11.png"]], 3, D + "sheet-mix.png")
