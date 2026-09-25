# -*- coding: utf-8 -*-
# R255 repair 2: R255 entry is now the LAST log element; drop its trailing
# comma (JSON no-trailing-comma rule). ASCII-only.
import io
import json

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"

raw = io.open(P, encoding="utf-8", newline="").read()
lines = raw.split("\r\n")
i = 276
assert lines[i].rstrip().endswith(","), "R255 entry must currently end with comma"
assert lines[i + 1].strip() == "],", "next must be array close"
lines[i] = lines[i].rstrip()[:-1]
io.open(P, "w", encoding="utf-8", newline="").write("\r\n".join(lines))

d = json.load(io.open(P, encoding="utf-8"))
print("OK tick=%s log_len=%d ts=%s task_chars=%d" % (d["tick"], len(d["log"]), d["ts"], len(d["task"])))
tail = d["log"][-1]
print("last_log_prefix_ok=%s" % tail.startswith("2026-09-25 14:45 R255"))
print("prev_log_is_r254=%s" % d["log"][-2].startswith("2026-09-25 14:3x R254"))
