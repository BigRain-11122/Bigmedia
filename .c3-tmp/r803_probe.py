# -*- coding: utf-8 -*-
# R803: BS-009 render-leg source probe (three sources x three time points,
# R800 probe chain-inheritance; tile for multimodal zero-leak adjudication)
import subprocess, os
from PIL import Image

SRCS = {
    "looplog": ("data/sources/footage/looplog-vertical.mp4", [1.0, 6.0, 10.5]),
    "reviewsdoc": ("data/sources/footage/reviewsdoc-vertical.mp4", [1.0, 5.0, 9.0]),
    "editgrid": ("data/sources/footage/editgrid-vertical.mp4", [1.0, 5.0, 9.0]),
}
D = r".bs009-tmp\probe-r803"
os.makedirs(D, exist_ok=True)
files = []
for name, (src, times) in SRCS.items():
    for k, t in enumerate(times):
        f = "%s/%s-t%d.png" % (D, name, k)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                       "-ss", "%.2f" % t, "-i", src, "-frames:v", "1", f], check=True)
        files.append((name, k, f))

w, h = 270, 480
im = Image.new("RGB", (w * 3, h * 3), "black")
for idx, (name, k, f) in enumerate(files):
    row = idx // 3
    col = idx % 3
    im.paste(Image.open(f).convert("RGB").resize((w, h)), (w * col, h * row))
tile = D + "/probe-src-tile.png"
im.save(tile)
print("PROBE DONE", len(files), "frames ->", tile)
