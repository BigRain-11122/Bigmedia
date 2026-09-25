# r345 fast-path check (ASCII output only)
import os, re, datetime

R = r"C:\Users\sjs20\Desktop\FluxGroup"
B = os.path.join(R, "media", "BigStream")

# 1) supply gate: CENSUS anchor canonical spot (life/BigLife/census/anchors/)
ad = os.path.join(R, "life", "BigLife", "census", "anchors")
try:
    names = sorted(os.listdir(ad))
    anchors_tail = names[-3:] if len(names) >= 3 else names
    print("anchors_count", len(names))
    print("anchors_tail", ",".join(anchors_tail))
except Exception as e:
    print("anchors_ERR", e)
print("C00030_exists", os.path.exists(os.path.join(ad, "C-00030.md")))
print("C00031_exists", os.path.exists(os.path.join(ad, "C-00031.md")))

# 2) group ledger scan: strict @ four-mode line count (anchor 21)
led = os.path.join(R, "cph4", "evolution-ledger.md")
pat = re.compile(r"@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8)")
n = 0
with open(led, encoding="utf-8", errors="replace") as f:
    for line in f:
        if pat.search(line):
            n += 1
print("ledger_lines", n, "anchor_21", n == 21)

# 3) group decisions.md non-empty line count (anchor 33, tail D-20260926-04)
dec = os.path.join(R, "docs", "decisions.md")
nonempty = []
with open(dec, encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.strip():
            nonempty.append(line.strip())
print("decisions_nonempty", len(nonempty), "anchor_33", len(nonempty) == 33)
tail = nonempty[-1][:80] if nonempty else ""
print("decisions_tail", tail.encode("unicode_escape").decode("ascii")[:100])

# 4) daily brief 2026-09-26 in place
print("daily_2026_09_26", os.path.exists(os.path.join(B, "data", "intel", "daily", "2026-09-26.md")))

# 5) ch.5 v3 manuscript check (bm-a face): any new writes 09-26 in storylines novel/audio/comic
base = os.path.join(B, "data", "storylines")
cut = datetime.datetime(2026, 9, 26, 0, 0).timestamp()
neww = []
for sub in ("novel", "audio", "comic"):
    d = os.path.join(base, sub)
    if not os.path.isdir(d):
        continue
    for root, _dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                if os.path.getmtime(p) >= cut:
                    neww.append(sub + "/" + fn)
            except OSError:
                pass
print("storylines_new_today", len(neww))
for x in neww[:8]:
    print("  new:", x.encode("unicode_escape").decode("ascii")[:90])

# 6) orders dir latest by name
od = os.path.join(B, "orders")
ons = sorted(x for x in os.listdir(od) if x.startswith("O-"))
print("orders_top", ons[-1] if ons else "none")

# 7) W39 audit + global-benchmarks first-line date
print("w39_audit", os.path.exists(os.path.join(B, "docs", "audits", "2026-W39-self-audit.md")))
gb = os.path.join(B, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    with open(gb, encoding="utf-8", errors="replace") as f:
        gtxt = f.read()
    m = re.search(r"2026-09-\d\d", gtxt)
    print("gb_first_date", m.group(0) if m else "none")
