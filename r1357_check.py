# -*- coding: utf-8 -*-
# R1357 round check: probe script inventory, backlog undone items, benchmarks freshness, watermark closure
import os, re, glob, json, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GROUP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
def w(s): out.append(str(s))

# 1. probe script inventory
w("== src/os/*.py ==")
for p in sorted(glob.glob(os.path.join(ROOT, "src", "os", "*.py"))):
    w("  " + os.path.basename(p))
w("== root probe-named scripts (r*.py) tracked? ==")
g = subprocess.run(["git", "ls-files", "r*.py", "r*.txt"], cwd=ROOT, capture_output=True, text=True)
w(g.stdout.strip() or "(none tracked)")

# 2. backlog undone items (top 8)
bl = open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
undone = [(i + 1, l) for i, l in enumerate(bl) if re.match(r"^\d+\.\s", l) and "[done" not in l]
w("== backlog undone items: %d total, top 8 ==" % len(undone))
for n, l in undone[:8]:
    w("  L%d: %s" % (n, l[:260]))

# 3. benchmarks section tail + all dates
gb = open(os.path.join(ROOT, "docs", "global-benchmarks.md"), encoding="utf-8").read()
w("== global-benchmarks.md: size %d chars ==" % len(gb))
idx = gb.rfind("更新记录")
seg = gb[idx:idx + 1500] if idx >= 0 else "(marker not found)"
for l in seg.splitlines()[:20]:
    w("  | " + l[:240])
dates = re.findall(r"2026-\d{2}-\d{2}", gb)
w("all dates: first=%s last=%s count=%d" % (dates[0] if dates else None, dates[-1] if dates else None, len(dates)))

# 4. watermark closure for 10-05 batch
st = json.load(open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
w("== watermark closure check ==")
w("watermark size: %d" % len(wm))
for n in range(1, 12):
    tok = "D-20261005-%02d" % n
    if tok in wm:
        w("  %s: IN watermark" % tok)
w("D-20260930-1 (unpadded artifact) in watermark: %s" % ("D-20260930-1" in wm))

# 5. exact context of D-20260930-1 in group decisions.md L158
dec = open(os.path.join(GROUP, "docs", "decisions.md"), encoding="utf-8").read()
for m in re.finditer(r"D-20260930-1(?![0-9])", dec):
    a, b = max(0, m.start() - 90), m.end() + 90
    w("== artifact context: ...%s..." % dec[a:b].replace("\n", " "))

open(os.path.join(ROOT, "r1357_check.txt"), "w", encoding="utf-8").write("\n".join(out))
print("OK")
