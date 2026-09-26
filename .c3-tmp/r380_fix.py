# -*- coding: utf-8 -*-
# R380 close fix: duplicated date prefix in last log line (script bug, honest fix).
import io, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
last = st["log"][-1]
bad = u"2026-09-26 2026-09-26 "
assert last.startswith(bad), "unexpected last line: " + last[:40]
st["log"][-1] = last[len(u"2026-09-26 "):]  # strip one duplicated date prefix
# task field was derived from the (correct-length) double prefix; re-derive for safety
fixed = st["log"][-1]
prefix = u"2026-09-26 12:51 "
st["task"] = fixed[len(prefix):len(prefix) + 60]
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fixed:", st["log"][-1][:60])
print("task:", st["task"])
