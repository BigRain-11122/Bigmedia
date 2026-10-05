# -*- coding: ascii -*-
# R1422 close verification: JSON validity + heartbeat face + loop_health final
import json, io, subprocess, re

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

st = json.load(io.open(BS + r"\src\os\state.json", encoding="utf-8"))
print("STATE_JSON: OK")
print("TICK: %s" % st["tick"])
print("TS: %s" % st["ts"])
print("TASK_LEN: %d" % len(st["task"]))
print("TASK: %s" % st["task"])
log = st["log"]
print("LOG_ENTRIES: %d" % len(log))
last = log[-1]
print("LAST_LOG_PREFIX_OK: %s" % bool(re.match(r"^20\d\d-\d\d-\d\d \d{2}:\d{2}", last[:18])))
print("LAST_LOG_HEAD: %s" % last[:40])
# single-digit-hour scan must stay 1 (the historical one is now fixed -> 0)
raw = io.open(BS + r"\src\os\state.json", encoding="utf-8").read()
sib = re.findall(r'"20\d\d-\d\d-\d\d \d:[0-5]?\d', raw)
print("SINGLE_DIGIT_HOUR_HITS_NOW: %d" % len(sib))

ex = json.load(io.open(BS + r"\docs\status-export.json", encoding="utf-8"))
print("EXPORT_JSON: OK, export_ts=%s" % ex["export_ts"])
print("LIVE0: %s" % ex["live"][0][:60])

p = subprocess.run(["python", r"src\os\loop_health.py"], cwd=BS, capture_output=True, timeout=300)
o = (p.stdout or b"").decode("utf-8", "replace")
fails = [l.strip() for l in o.splitlines() if "[FAIL]" in l]
for f in fails:
    print("LH_FAIL: %s" % f[:120])
m = re.search(r"loop health: .*", o)
print("LH_SUMMARY: %s" % (m.group(0) if m else "?"))
print("LOG_TS_FAIL_PRESENT: %s" % ("log-ts" in o))
