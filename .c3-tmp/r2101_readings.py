# -*- coding: utf-8 -*-
# R2092 deathline-window readings: release scan + cloudv2 + bmc-i2v + sample-v2 anchor.
import os, time, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r2101_readings.txt")
BASE = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\mv0001-handover\outbound\krea2"
lines = []
now = time.time()

def log(s):
    lines.append(str(s))

def newest(path, pat=None):
    best = None
    n = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if pat and pat not in f:
                continue
            p = os.path.join(dirpath, f)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            n += 1
            if best is None or m > best[1]:
                best = (p, m)
    return best, n

# 1. release/ scan (234s film watch)
rel = os.path.join(BASE, "30s-reel-v1", "release")
if os.path.isdir(rel):
    b, n = newest(rel)
    if b:
        log("release newest=%s mtime=%s age_min=%.1f files=%d" % (b[0].replace(BASE, "<BASE>"), time.strftime("%m-%d %H:%M", time.localtime(b[1])), (now - b[1]) / 60.0, n))
        log("release has 234s full film: %s" % ("234" in os.path.basename(b[0]) or "full" in os.path.basename(b[0]).lower()))
    else:
        log("release empty")
else:
    log("release dir ABSENT")

# 2. cloudv2 landing (CLOUDWAVE-2)
cv = os.path.join(BASE, "kf-demo-20261012", "cloudv2")
if os.path.isdir(cv):
    b, n = newest(cv, ".mp4")
    if b:
        log("cloudv2 mp4 count=%d newest=%s age_min=%.1f" % (n, os.path.basename(b[0]), (now - b[1]) / 60.0))
else:
    log("cloudv2 ABSENT")

# 3. bmc i2v (bm-c local lane, read-only watch)
bi = os.path.join(BASE, "kf-demo-20261012", "bmc", "i2v")
if os.path.isdir(bi):
    b, n = newest(bi, ".mp4")
    if b:
        log("bmc/i2v mp4 count=%d newest=%s age_min=%.1f" % (n, os.path.basename(b[0]), (now - b[1]) / 60.0))
    else:
        log("bmc/i2v dir empty")
else:
    log("bmc/i2v ABSENT")

# 4. krea2 root newest (session activity face, incl. 30s-reel-v1)
b, n = newest(os.path.join(BASE, "30s-reel-v1"))
if b:
    log("30s-reel-v1 newest=%s age_min=%.1f" % (os.path.basename(b[0]).replace(BASE, ""), (now - b[1]) / 60.0))

# 5. assembly outputs (any mp4 in handover outbound, last 12h fresh)
b, n = newest(BASE, ".mp4")
if b:
    log("krea2 outbound mp4 newest=%s age_min=%.1f" % (b[0].replace(BASE, "<BASE>"), (now - b[1]) / 60.0))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK %d lines" % len(lines))

