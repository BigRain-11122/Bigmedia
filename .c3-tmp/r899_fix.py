# -*- coding: utf-8 -*-
"""R899 hygiene fix: repair R898 log line leading timestamp (%s placeholder leak from r898_close.py).
Uncommitted batch member; format-face fix only, zero content/score rewrite. Precedent: R804 dedup, R821 JSON repair."""
import io, json

SP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
BAD = "2026-10-01 %s R898:"
GOOD = "2026-10-01 22:04 R898:"  # R898 close ts = 2026-10-01 22:04:20 -> HH:MM log-line convention

s = json.load(io.open(SP, encoding="utf-8"))
hits = [i for i, l in enumerate(s["log"]) if BAD in l]
assert len(hits) == 1, ("expected exactly 1 malformed line, got", hits)
i = hits[0]
assert s["log"][i].startswith(BAD), s["log"][i][:40]
s["log"][i] = s["log"][i].replace(BAD, GOOD, 1)
io.open(SP, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=1))

# reload verify
v = json.load(io.open(SP, encoding="utf-8"))
assert v["log"][i].startswith(GOOD), v["log"][i][:40]
assert v["tick"] == 898 and v["ts"] == "2026-10-01 22:04:20", (v["tick"], v["ts"])
print("fixed log entry", i + 1, "->", v["log"][i][:30])
print("verify ok: json valid, tick", v["tick"], "ts", v["ts"])
