# -*- coding: utf-8 -*-
"""fix2_state_r1779.py - remove illegal trailing comma on last log element."""
import io, json

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
S = io.open(P, encoding="utf-8").read()
bad = u'27b 试跑独占窗判断）",\n  ],'
good = u'27b 试跑独占窗判断）"\n  ],'
assert bad in S, "fix2 anchor missing"
S = S.replace(bad, good, 1)
io.open(P, "w", encoding="utf-8", newline="").write(S)
d = json.load(io.open(P, encoding="utf-8"))
print("JSON VALID; tick=%s; ts=%s; log_n=%d; last60=%s" % (
    d["tick"], d["ts"], len(d["log"]), d["log"][-1][-60:]))
