# -*- coding: utf-8 -*-
"""R1444 fix: task field prefix strip (05:2x single-digit-minute + x)."""
import io, json, re

PATH = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
st = json.loads(io.open(PATH, encoding="utf-8").read())
log_last = st["log"][-1]
m = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{1,2}[xX]? ", log_last)
assert m, "prefix still not matched: %r" % log_last[:30]
st["task"] = log_last[m.end():][:60]
out = json.dumps(st, ensure_ascii=False, indent=2) + "\n"
io.open(PATH, "w", encoding="utf-8", newline="\n").write(out)
print("task_len=%d" % len(st["task"]))
print("OK")
