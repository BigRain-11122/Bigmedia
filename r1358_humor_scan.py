# -*- coding: utf-8 -*-
# B5 slice2 A-level sampling leg (pre-registered R1357):
#  Q1 humor presence on hot lists (bilibili-popular / zhihu-hot title face, zero new collection)
#  Q1-b fleet production baseline: designed laugh points in shipped voiceover beats
# Output: r1358_humor_scan.txt (UTF-8 evidence file)
import os, re, glob

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
DAILY = os.path.join(ROOT, "data", "intel", "daily")
out = []
def w(s):
    try:
        out.append(str(s))
    except Exception:
        out.append(repr(s))

# humor markers for title-face flagging (verbatim hits kept for human review)
HUMOR = re.compile(u"(\u7b11|\u641e\u7b11|\u6bb5\u5b50|\u6c99\u96d5|\u6574\u6d3b|\u79bb\u8c31|\u4e50\u5b50|\u7ef7\u4e0d|\u53d1\u75af|\u62bd\u8c61|\u5410\u69fd|\u795e\u4eba|\u7206\u7b11|\u6897|\u6253\u5de5|\u7834\u9632|\u5410\u69fd|\u8c10\u661f|\u641c\u7b11\u56fe)")
# designed-gag vocabulary for the beats baseline pass (self-deprecation / blame-shift / dare / comment hooks)
GAG = re.compile(u"(\u7529\u9505|\u50ac\u66f4|\u9a82\u6211|\u4f5c\u6b7b|\u81ea\u5632|\u6562\u60f3\u6562\u505a)")
BEATS_PAT = re.compile(HUMOR.pattern + "|" + GAG.pattern)

# ---- 1. daily briefs: bilibili-popular + zhihu-hot title face ----
files = sorted(glob.glob(os.path.join(DAILY, "*.md")))
w("== A-level scan: daily briefs (existing collection, zero new fetch) ==")
w("brief files: %d" % len(files))
bt = bh = zt = zh_ = 0
for f in files:
    day = os.path.basename(f)[:-3]
    try:
        txt = open(f, encoding="utf-8").read()
    except Exception as e:
        w("  [READ_FAIL %s] %r" % (day, e))
        continue
    m_b = re.search(r"##\s*bilibili-popular[^\n]*\n(.*?)##\s*zhihu-hot", txt, re.S)
    m_z = re.search(r"##\s*zhihu-hot[^\n]*\n(.*)", txt, re.S)
    bili = re.findall(r"^\s*\d+\.\s*(.+)$", m_b.group(1), re.M) if m_b else []
    zhq = re.findall(r"^\s*\d+\.\s*(.+)$", m_z.group(1), re.M) if m_z else []
    bhit = [t for t in bili if HUMOR.search(t)]
    zhit = [t for t in zhq if HUMOR.search(t)]
    bt += len(bili); bh += len(bhit); zt += len(zhq); zh_ += len(zhit)
    w("  day %s: bili %d scanned / %d humor-hit | zhihu %d scanned / %d humor-hit" % (day, len(bili), len(bhit), len(zhq), len(zhit)))
    for t in bhit:
        w("    [bili %s] %s" % (day, t.strip()[:90]))
    for t in zhit:
        w("    [zhihu %s] %s" % (day, t.strip()[:90]))
w("")
w("AGG bilibili-popular title face: %d/%d humor-hit = %.1f%%" % (bh, bt, (100.0 * bh / bt) if bt else 0.0))
w("AGG zhihu-hot title face:        %d/%d humor-hit = %.1f%%" % (zh_, zt, (100.0 * zh_ / zt) if zt else 0.0))

# ---- 2. fleet baseline: shipped production beats ----
w("")
w("== fleet baseline: production voiceover beats (designed laugh-point face) ==")
beats = sorted(glob.glob(os.path.join(ROOT, "data", "sources", "*", "*beats*.txt")))
w("beats files: %d" % len(beats))
tot_lines = 0
tot_hit = 0
pieces_hit = set()
for f in beats:
    try:
        txt = open(f, encoding="utf-8").read()
    except Exception as e:
        w("  [READ_FAIL %s] %r" % (f, e))
        continue
    lines = [l for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")]
    hits = [l for l in lines if BEATS_PAT.search(l)]
    tot_lines += len(lines)
    tot_hit += len(hits)
    if hits:
        piece = os.path.basename(os.path.dirname(f))
        pieces_hit.add(piece)
        w("  [HIT %s / %s]" % (piece, os.path.basename(f)))
        for l in hits:
            w("     | " + l.strip()[:150])
w("fleet beat lines scanned: %d | humor-marker beat lines: %d | pieces with >=1 hit: %d" % (tot_lines, tot_hit, len(pieces_hit)))

open(os.path.join(ROOT, "r1358_humor_scan.txt"), "w", encoding="utf-8").write("\n".join(out))
print("SCAN_OK")
