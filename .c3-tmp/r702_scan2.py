# -*- coding: utf-8 -*-
# R702 #93 supplementary scan: .codely-cli breakdown, R2 footage registry, finished.md current pointers
import os, io, time, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
out = []
def w(s): out.append(s)
def sf(n):
    x = float(n)
    for u in ['B','KB','MB','GB']:
        if x < 1024: return "%.1f%s" % (x, u)
        x /= 1024.0
    return "%.2fTB" % x

def dirtree(base, label, depth=1):
    if not os.path.exists(base):
        w("%s ABSENT" % label); return
    agg = {}
    for dp, dn, fn in os.walk(base):
        rel = os.path.relpath(dp, base)
        lvl = 0 if rel == "." else rel.count(os.sep) + 1
        if lvl > depth:
            dn[:] = []
            continue
        s = 0
        for f in fn:
            try: s += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
        if rel != ".":
            agg[rel.replace("\\", "/")] = s
    tot = 0
    for dp, dn, fn in os.walk(base):
        for f in fn:
            try: tot += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
    w("[%s] total=%s" % (label, sf(tot)))
    for k, v in sorted(agg.items(), key=lambda kv: -kv[1])[:18]:
        w("  %-40s %s" % (k, sf(v)))

dirtree(os.path.join(ROOT, ".codely-cli"), "repo .codely-cli", depth=1)
dirtree(r"C:\Users\sjs20\.codely-cli", "user .codely-cli", depth=1)

# R2 footage sources registry face
ft = os.path.join(ROOT, "data", "sources", "footage")
w("-- data/sources/footage (R2 source assets):")
t = 0
rows = []
for f in sorted(os.listdir(ft)):
    fp = os.path.join(ft, f)
    if os.path.isfile(fp):
        s = os.path.getsize(fp); t += s
        rows.append((s, f, time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(fp)))))
for s, f, m in sorted(rows, reverse=True):
    w("  %-12s %s  mtime=%s" % (sf(s), f, m))
w("  footage total=%s files=%d" % (sf(t), len(rows)))

# storylines audio tmp (ignored amb beds)
dirtree(os.path.join(ROOT, "data", "storylines", "audio"), "data/storylines/audio", depth=1)

# finished.md current pointer classification
fin = os.path.join(ROOT, "output", "finished.md")
txt = io.open(fin, encoding="utf-8").read()
rd = os.path.join(ROOT, "output", "renders")
cur, hist, other = [], [], []
for f in sorted(os.listdir(rd)):
    fp = os.path.join(rd, f)
    if not os.path.isfile(fp): continue
    if f in txt:
        cur.append(f)
    else:
        other.append(f)
w("-- renders classification vs finished.md mention:")
w("  mentioned-in-finished(%d): %s" % (len(cur), ", ".join(cur)))
w("  NOT-mentioned(%d): %s" % (len(other), ", ".join(other)))

# piper models
pm = os.path.join(ROOT, "data", "assets", "piper-models")
if os.path.exists(pm):
    s = 0
    for dp, dn, fn in os.walk(pm):
        for f in fn:
            try: s += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
    w("piper-models total=%s" % sf(s))

io.open(os.path.join(TMP, "r702_scan2.txt"), "w", encoding="utf-8").write("\n".join(out))
print("SCAN2_DONE lines=%d" % len(out))
