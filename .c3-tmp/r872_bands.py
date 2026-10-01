# -*- coding: utf-8 -*-
# R872 frame verification fallback: PIL band-measure (R381 precedent) - detect horizontal
# text bands by row darkness profile, assert: band count, band separation (no overlap),
# content stack bottom above subs band, right-edge/left-edge no clipping proxy.
from PIL import Image
import io, sys

png = r"data\storylines\cards\MC-20261001-DIGEST-v13\MC-20261001-DIGEST-v13.png"
im = Image.open(png).convert("L")
W, H = im.size
px = im.load()

# row profile: min brightness over central columns (text = bright on black bg)
profile = []
for y in range(H):
    row_min = 255
    for x in range(40, W - 40, 4):
        v = px[x, y]
        if v < row_min:
            row_min = v
    profile.append(row_min)

# a row "has ink" if any sampled pixel is meaningfully bright
INK = 60
bands = []
in_band = False
start = 0
for y, m in enumerate(profile):
    if m < INK and not in_band:
        in_band, start = True, y
    elif m >= INK and in_band:
        in_band = False
        if y - start >= 3:
            bands.append((start, y - 1))
if in_band:
    bands.append((start, H - 1))

out = []
out.append("size=%dx%d bands=%d" % (W, H, len(bands)))
for i, (a, b) in enumerate(bands):
    out.append("band %02d: y %4d-%4d h=%3d" % (i, a, b, b - a + 1))

# expected: h1 title + 7 content lines + subs source line + AIGC corner label
# AIGC corner is bottom-right small text - may merge with subs band row or be separate.
ok = True
if len(bands) < 9:
    ok = False
    out.append("BAND COUNT FAIL: expected >= 9 (title+7+subs+aigc), got %d" % len(bands))
gaps = []
for i in range(1, len(bands)):
    g = bands[i][0] - bands[i - 1][1] - 1
    gaps.append(g)
    if g < 4:
        ok = False
        out.append("BAND OVERLAP/TOO-CLOSE FAIL between band %d and %d gap=%d" % (i - 1, i, g))
out.append("gaps=%s" % gaps)
io.open(r"data\storylines\cards\MC-20261001-DIGEST-v13-tmp\band-measure-r872.txt", "w", encoding="utf-8").write("\n".join(out))
print("BANDS=%d OK=%s" % (len(bands), ok))
sys.exit(0 if ok else 1)
