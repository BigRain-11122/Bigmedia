# -*- coding: utf-8 -*-
# R1049 probe-3: B3 weekly (bilibili hot dissect) W40 status + full R1048 log entry + daily brief inventory
import json, glob, os, re
from pathlib import Path

ROOT = Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream")
L = []
def w(s=""): L.append(str(s))

w("== bilibili-hot-dissect file: W40 present? ==")
p = ROOT / "research/bilibili-hot-dissect-v1.md"
w("exists=%s size=%s" % (p.exists(), p.stat().st_size if p.exists() else "-"))
if p.exists():
    txt = p.read_text(encoding="utf-8")
    w("has W40=%s | has W39=%s | lines=%d" % ("W40" in txt, "W39" in txt, len(txt.splitlines())))
    w("version headers:")
    for ln in txt.splitlines():
        if re.match(r"^#{1,3} ", ln) or "v1." in ln[:14] or "W3" in ln[:10] or "W4" in ln[:10]:
            w("  " + ln[:150])
    w("--- tail 12 ---")
    w("\n".join(txt.splitlines()[-12:]))

w()
w("== daily brief inventory (this week) ==")
for f in sorted(glob.glob(str(ROOT / "data/intel/daily/*.md")))[-10:]:
    w(os.path.basename(f))

w()
w("== state log mentions of bilibili-hot-dissect / B3 (round numbers) ==")
state = json.loads((ROOT / "src/os/state.json").read_text(encoding="utf-8"))
log = state.get("log", [])
for e in log:
    s = str(e)
    if "hot-dissect" in s or "B站热门结构" in s:
        w(s[:150])
w("(total log=%d)" % len(log))

w()
w("== FULL R1048 log entry ==")
for e in log:
    if "R1048:" in str(e)[:40]:
        w(str(e))

out = "\n".join(L)
(ROOT / ".c3-tmp/r1049_probe3_out.txt").write_text(out, encoding="utf-8")
print("OK bytes=", len(out))
