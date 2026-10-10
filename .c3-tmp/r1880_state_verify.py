import io
import json

d = json.load(io.open("src/os/state.json", encoding="utf-8"))
last = d["log"][-1]
print("json-ok tick=%d log=%d ts=%s task=%r" % (d["tick"], len(d["log"]), d["ts"], d["task"]))
print("last-prefix: %s..." % last[:60])
assert d["tick"] == 1880, "tick mismatch"
assert "08:5x R1880" in last, "log prefix fix missing"
assert "group_scan.py" in last, "delivery note missing"
print("state-verify: PASS")
