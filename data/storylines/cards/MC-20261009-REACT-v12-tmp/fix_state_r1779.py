# -*- coding: utf-8 -*-
"""fix_state_r1779.py - repair comma + watermark ts + accounting ts, validate JSON."""
import io, json, re

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
S = io.open(P, encoding="utf-8").read()

# fix 1: comma after R1778 last log line
bad = u'或全静续声明）"\n    "2026-10-09'
good = u'或全静续声明）",\n    "2026-10-09'
assert bad in S, "fix1 anchor missing"
S = S.replace(bad, good, 1)

# fix 2: restore watermark ts if hijacked
bad2 = '"ts": "2026-10-09 00:17:54",\n    "law":'
good2 = '"ts": "2026-10-08 20:51:06",\n    "law":'
if bad2 in S:
    S = S.replace(bad2, good2, 1)
    print("watermark ts restored")
else:
    print("watermark ts not hijacked (no restore needed)")

# fix 3: set the real accounting ts at file end (anchored to task line)
pat = re.compile(r'(\n  "ts": )"[^"]*"(,\n  "task": )', re.S)
S2, n = pat.subn(lambda m: m.group(1) + '"2026-10-09 00:19:30"' + m.group(2), S, count=1)
print("accounting ts replacements:", n)

io.open(P, "w", encoding="utf-8", newline="").write(S2)
d = json.load(io.open(P, encoding="utf-8"))
print("JSON VALID; tick=%s; watermark_ts=%s; ts=%s; log_last=%s..." % (
    d["tick"], d["decisions_watermark"]["ts"], d["ts"], d["log"][-1][:60]))
