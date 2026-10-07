# -*- coding: utf-8 -*-
import subprocess, os
os.makedirs(".bs013-tmp/frameverify-r1682", exist_ok=True)
HEAD = [0.35, 5.44, 8.80, 14.96, 19.30, 23.76, 28.88, 32.94, 38.76, 43.34, 48.08, 53.25]
CROSS = [("b0-pre", 4.30), ("b0-x", 4.42), ("b0-post", 4.54)]
FULL = [("t20-b4", 20.0), ("t53-b11", 53.30)]

def grab(t, name):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                    "-i", "output/renders/bs-013-v1-shipinhao-60s.mp4",
                    "-frames:v", "1", ".bs013-tmp/frameverify-r1682/%s.png" % name], check=True)

for i, t in enumerate(HEAD):
    grab(t, "head%02d" % i)
for n, t in CROSS:
    grab(t, n)
for n, t in FULL:
    grab(t, n)
print("OK frames extracted:", len(HEAD) + len(CROSS) + len(FULL))

from PIL import Image
def tile(paths, cols, out, w=360, h=640):
    ims = [Image.open(p).resize((w, h)) for p in paths]
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "black")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    sheet.save(out)
    print("OK sheet:", out)

D = ".bs013-tmp/frameverify-r1682/"
tile([D + "head%02d.png" % i for i in range(12)], 3, D + "sheet-heads.png")
tile([D + p for p in ["b0-pre.png", "b0-x.png", "b0-post.png", "t20-b4.png", "t53-b11.png"]], 3, D + "sheet-mix.png")
