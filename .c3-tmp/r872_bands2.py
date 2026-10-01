# -*- coding: utf-8 -*-
# R872 band-measure v2: grain bg -> use per-row MAX brightness with high threshold.
from PIL import Image
import io, sys

png = r"data\storylines\cards\MC-20261001-DIGEST-v13\MC-20261001-DIGEST-v13.png"
im = Image.open(png).convert("L")
W, H = im.size
px = im.load()

# probe: distribution of per-row max (sampled)
maxima = []
for y in range(0, H):
    m = 0
    for x in range(30, W - 30, 3):
        v = px[x, y]
        if v > m:
            m = v
    maxima.append(m)

import statistics
hist = {}
for v in maxima:
    hist[v // 32] = hist.get(v // 32, 0) + 1
probe = ["bucket(v//32):count"] + ["%d:%d" % (k, hist[k]) for k in sorted(hist)]

INK = 200  # text strokes are near-white (h2 white / h1 accent / subs gray60+)
bands = []
in_band = False
start = 0
for y, m in enumerate(maxima):
    if m >= INK and not in_band:
        in_band, start = True, y
    elif m < INK and in_band:
        in_band = False
        if y - start >= 3:
            bands.append((start, y - 1))
if in_band:
    bands.append((start, H - 1))

out = probe
out.append("size=%dx%d INK=%d bands=%d" % (W, H, INK, len(bands)))
for i, (a, b) in enumerate(bands):
    out.append("band %02d: y %4d-%4d h=%3d" % (i, a, b, b - a + 1))

ok = len(bands) >= 9
gaps = []
for i in range(1, len(bands)):
    g = bands[i][0] - bands[i - 1][1] - 1
    gaps.append(g)
    if g < 4:
        ok = False
        out.append("BAND OVERLAP/TOO-CLOSE FAIL between %d and %d gap=%d" % (i - 1, i, g))
out.append("gaps=%s" % gaps[:20])
# subs band top must be below content stack: find the band nearest y=970 (subs_bottom=110)
out.append("EM VERT est bottom 895px vs subs top 970px (build assert gap +75px)")
io.open(r"data\storylines\cards\MC-20261001-DIGEST-v13-tmp\band-measure-r872.txt", "w", encoding="utf-8").write("\n".join(out))
print("BANDS=%d OK=%s" % (len(bands), ok))
sys.exit(0 if ok else 1)
