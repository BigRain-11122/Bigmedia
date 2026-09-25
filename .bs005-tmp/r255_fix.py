# -*- coding: utf-8 -*-
# R255 repair: R254 log line was last array element (no trailing comma);
# after inserting R255 entry it needs the comma back. ASCII-only.
import io
import json

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
Q = chr(34)

raw = io.open(P, encoding="utf-8", newline="").read()
lines = raw.split("\r\n")
i = 275
assert lines[i].rstrip().endswith(Q), "R254 line must end with quote"
assert lines[i + 1].lstrip().startswith(Q + "2026-09-25"), "next must be R255 entry"
lines[i] = lines[i] + ","
io.open(P, "w", encoding="utf-8", newline="").write("\r\n".join(lines))

d = json.load(io.open(P, encoding="utf-8"))
print("OK tick=%s log_len=%d ts=%s task_chars=%d last_ts=%s"
      % (d["tick"], len(d["log"]), d["ts"], len(d["task"]),
         d["log"][-1][:16]))
