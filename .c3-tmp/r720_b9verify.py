# -*- coding: utf-8 -*-
# R720: b9 frame re-verification after fix (extract + PIL geometry)
# b9 window 41.71-49.35; head/mid/tail samples; verify cards-block top y is
# BELOW the source-line band (band y 745-767, R719 evidence), i.e. no overlap.
import subprocess, os
from PIL import Image

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
MP4 = os.path.join(ROOT, "output", "renders", "lc-013-v1-shipinhao-60s.mp4")
TMP = os.path.join(ROOT, ".lc013-tmp")

samples = [("b9head", 42.6), ("b9mid", 45.5), ("b9tail", 48.4)]
for tag, t in samples:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", MP4,
                    "-frames:v", "1", os.path.join(TMP, "r720_%s.png" % tag)],
                   check=True)

def bright_cols(img, y, x0, x1, thr=200):
    row = 0
    px = img.load()
    for x in range(x0, x1):
        r, g, b = px[x, y][:3]
        if r > thr and g > thr and b > thr:
            row += 1
    return row

out = open(os.path.join(TMP, "r720_b9verify.txt"), "w", encoding="utf-8")
for tag, t in samples:
    fp = os.path.join(TMP, "r720_%s.png" % tag)
    img = Image.open(fp).convert("RGB")
    W, H = img.size
    # scan rows 680-900: find topmost row with a wide bright text run (block L1)
    top = None
    for y in range(680, 900):
        n = bright_cols(img, y, 150, 930)
        if n >= 300:  # wide white text row (block line is ~912px wide)
            top = y
            break
    # band rows 745-767: count bright pixels in band center (source line zone)
    band_bright = [bright_cols(img, y, 150, 930) for y in range(743, 770)]
    out.write("%s: block_top_y=%s band745-767 max_bright_cols=%d\n"
              % (tag, top if top else ">900", max(band_bright)))
    # evidence crops: band strip + block region
    band = img.crop((0, 730, W, 790))
    band.save(os.path.join(TMP, "r720_band_%s.png" % tag))
out.close()

# side-by-side with R719 broken evidence (r719_b9mid_full.png same t=45.5 window)
broken = Image.open(os.path.join(TMP, "r719_b9mid_full.png")).convert("RGB")
fixed = Image.open(os.path.join(TMP, "r720_b9mid.png")).convert("RGB")
W = 1080
stack = Image.new("RGB", (W, 400), "black")
stack.paste(broken.crop((0, 700, W, 900)).resize((W, 200)), (0, 0))
stack.paste(fixed.crop((0, 700, W, 900)).resize((W, 200)), (0, 200))
stack.save(os.path.join(TMP, "r720_ab_b9_band.png"))
print("B9VERIFY_DONE")
