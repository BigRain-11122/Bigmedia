# -*- coding: utf-8 -*-
"""R1794 fast-path remainder: decisions dnum diff + ledger anchor + 3 probes."""
import json
import re
import subprocess
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path("..").resolve().parent  # not used; run from repo root

# 1) decisions dnum content-addressing diff (D-20260930-18/19 law)
dec = Path(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md")
if dec.exists():
    txt = dec.read_text(encoding="utf-8", errors="replace")
    cur = set(re.findall(r"\b([DC]-\d{8}-\d{1,3})\b", txt))
    st = json.loads(Path("src/os/state.json").read_text(encoding="utf-8"))
    wm = set(st["decisions_watermark"]["dnums"])
    print("decisions NEW:", sorted(cur - wm) if (cur - wm) else "[]",
          "| mtime:", dec.stat().st_mtime)
else:
    print("decisions: MISSING")

led = Path(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md")
if led.exists():
    ltxt = led.read_text(encoding="utf-8", errors="replace")
    hits = [l[:160] for l in ltxt.splitlines() if "@BigStream" in l]
    print("ledger @BigStream rows:", len(hits), "| mtime:", led.stat().st_mtime)
    for h in hits[-3:]:
        print("  TAIL:", h)
else:
    print("ledger: MISSING")

for name in ("src/board_check.py", "src/readiness.py", "src/os/loop_health.py"):
    r = subprocess.run([sys.executable, name], capture_output=True)
    tail = r.stdout.decode("utf-8", errors="replace").strip().splitlines()
    print("== %s rc=%d ==" % (name, r.returncode))
    for line in tail[-6:]:
        print("  ", line)
