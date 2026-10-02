# -*- coding: utf-8 -*-
# R1049 probe-2: GB gate date verify + queue pools + backlog tail items + R1032 judgment entry
import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream")
L = []
def w(s=""): L.append(str(s))

w("== global-benchmarks structure ==")
gb = (ROOT / "docs/global-benchmarks.md").read_text(encoding="utf-8")
lines = gb.splitlines()
w("total lines=%d" % len(lines))
for i, ln in enumerate(lines, 1):
    if ("更新记录" in ln) or ("§④" in ln) or ("§①" in ln) or ("动态面" in ln):
        w("L%d: %s" % (i, ln.strip()[:120]))
mi = None
for i, ln in enumerate(lines, 1):
    if "更新记录" in ln:
        mi = i
        break
if mi:
    w("--- block around 更新记录 (first=oldest? check dates) ---")
    for ln in lines[mi:mi + 12]:
        w(ln[:160])

w()
w("== queue full scan (sections + non-gated candidates) ==")
qt = (ROOT / "docs/self-improvement-queue.md").read_text(encoding="utf-8")
for i, ln in enumerate(qt.splitlines(), 1):
    if re.match(r"^#{1,3} ", ln) or "§" in ln[:12]:
        w("L%d: %s" % (i, ln.strip()[:130]))
w("--- queue §D proposal face ---")
di = qt.find("§D")
if di >= 0:
    w(qt[di:di + 1400])

w()
w("== backlog tail items (headers only, first 260 chars) ==")
bl = (ROOT / "src/os/backlog.md").read_text(encoding="utf-8").splitlines()
for ln in bl:
    if re.match(r"^\d+\.", ln):
        w(ln[:260])
        w()

w("== state log R1032 entry (full) ==")
state = json.loads((ROOT / "src/os/state.json").read_text(encoding="utf-8"))
for e in state.get("log", []):
    if re.search(r"R1032:", str(e)[:40]):
        w(str(e)[:2200])

out = "\n".join(L)
(ROOT / ".c3-tmp/r1049_probe2_out.txt").write_text(out, encoding="utf-8")
print("OK bytes=", len(out))
