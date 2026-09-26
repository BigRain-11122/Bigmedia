# -*- coding: utf-8 -*-
# R357 idle-fast five-check probe (ASCII output only)
import os, io, re, datetime

BASE = r"C:\Users\sjs20\Desktop\FluxGroup"
MS = os.path.join(BASE, "media", "BigStream")
out = []

# 1. supply gate: anchors canonical position only (R316 discipline)
anchor_dir = os.path.join(BASE, "life", "BigLife", "census", "anchors")
if os.path.isdir(anchor_dir):
    names = sorted(os.listdir(anchor_dir))
    out.append("anchors_dir=OK n=%d tail=%s" % (len(names), names[-2:]))
    out.append("C-00030=%s C-00031=%s" % (
        os.path.exists(os.path.join(anchor_dir, "C-00030.md")),
        os.path.exists(os.path.join(anchor_dir, "C-00031.md"))))
else:
    out.append("anchors_dir=MISSING")

# 2. group ledger four-mode count (anchor 21)
tokens = [u"@BigStream", u"@七线全司", u"@全司", u"@六司"]
cnt = 0
led = os.path.join(BASE, "cph4", "evolution-ledger.md")
with io.open(led, encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(t in line for t in tokens):
            cnt += 1
out.append("ledger_fourmode_lines=%d anchor=21" % cnt)

# 3. group decisions non-empty lines (anchor 33, tail D-20260926-04)
dec = os.path.join(BASE, "docs", "decisions.md")
with io.open(dec, encoding="utf-8", errors="replace") as f:
    lines = [l for l in f.read().splitlines() if l.strip()]
tail = ""
for l in reversed(lines):
    m = re.search(r"D-\d{8}-\d+", l)
    if m:
        tail = m.group(0)
        break
mt = datetime.datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%m-%d %H:%M:%S")
out.append("decisions_nonempty=%d anchor=33 tail=%s mtime=%s" % (len(lines), tail, mt))

# 4. storylines novel/audio/comic writes on 09-26 (ch.5 v3 signal)
TH = 1790352000  # 2026-09-26 00:00 local
neww = []
for sub in ("novel", "audio", "comic"):
    d = os.path.join(MS, "data", "storylines", sub)
    for root, dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                if os.path.getmtime(p) >= TH:
                    neww.append(os.path.relpath(p, MS))
            except OSError:
                pass
out.append("storylines_new_0926_novel_audio_comic=%d" % len(neww))
if neww:
    out.append("new_files=%s" % neww[:6])

# ch.5 v3 landing check: novel SC-001-05 versions
nd = os.path.join(MS, "data", "storylines", "novel")
v5 = sorted(f for f in os.listdir(nd) if f.startswith("SC-001-05")) if os.path.isdir(nd) else []
ch6 = sorted(f for f in os.listdir(nd) if f.startswith("SC-001-06")) if os.path.isdir(nd) else []
out.append("novel_SC-001-05=%s ch6=%s" % (v5, ch6))

# 5. daily report in place
dd = os.path.join(MS, "data", "intel", "daily", "2026-09-26.md")
out.append("daily_0926=%s" % os.path.exists(dd))

# 6. index.lock
out.append("index_lock=%s" % os.path.exists(os.path.join(MS, ".git", "index.lock")))

print("\n".join(out))
