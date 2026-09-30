# -*- coding: utf-8 -*-
# R735 S1 second-flight poll (ASCII-only console output per PS5.1 GBK law)
import io
import json
import os
import re
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RES = REPO / ".lc017-tmp" / "s1-result.json"
OUT = REPO / ".c3-tmp" / "r735_s1poll.txt"

deadline = time.time() + 100
landed = False
while time.time() < deadline:
    if RES.exists():
        try:
            r = json.load(io.open(RES, encoding="utf-8"))
        except Exception:
            r = None
        if r and r.get("exit") == 0 and str(r.get("verdict_file", "")).endswith(
                time.strftime("%H%M%S", time.localtime(os.path.getmtime(RES))) + "-S1-script.md"):
            pass
        if r and r.get("exit") == 0 and os.path.getmtime(RES) > time.time() - 110:
            landed = True
            break
    time.sleep(5)

if not (RES.exists()):
    print("S1_POLL=not-landed")
    raise SystemExit(0)

r = json.load(io.open(RES, encoding="utf-8"))
v = r.get("verdict", "") or ""
lines = [l.strip() for l in v.splitlines() if l.strip()]
has_total = any(re.search(r"总分", l) and re.search(r"0-10|10|9", l) for l in lines)
m = re.search(r"总分[^\d]*(\d+(?:\.\d+)?)", v)
score = m.group(1) if m else "?"
has_vlist = any("违律" in l for l in lines)
has_verdict = any(re.search(r"总裁决|^\**PASS|^\**FAIL", l) for l in lines)
no_violation = ("无" in v and "违律" in v)
first = lines[0][:80] if lines else ""
rep = ["S1_POLL=exit%s" % r.get("exit"),
       "SCORE=%s" % score,
       "HAS_TOTAL=%s HAS_VLIST=%s HAS_VERDICT=%s NO_VIOLATION=%s" % (
           has_total, has_vlist, has_verdict, no_violation),
       "VFILE=%s" % r.get("verdict_file", "-"),
       "HEAD=" + first]
(io.open(OUT, "w", encoding="utf-8")).write(
    "\n".join(rep) + "\n\n[verdict full]\n" + v)
print("SCORE=%s HAS_TOTAL=%s HAS_VLIST=%s HAS_VERDICT=%s" % (
    score, has_total, has_vlist, has_verdict))
print("VFILE=" + str(r.get("verdict_file", "-")))
print("HEADASCII_OK")
