# -*- coding: utf-8 -*-
# r456 close fix: results[4] = library-count entry (index misread in r456_close; no damage done).
import io, json

P = "docs/status-export.json"
d = json.load(io.open(P, encoding="utf-8"))
r = d["results"]
assert r[4][0] == "43", "unexpected results[4][0]: %s" % r[4][0]
r[4][0] = "44"
assert u"F-008~F-044" in r[4][1], "F-range not found in results[4][1]"
r[4][1] = r[4][1].replace(u"F-008~F-044", u"F-008~F-045")
json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.load(io.open(P, encoding="utf-8"))
print("FIX OK results[4] 43->44 + F-008~F-045")
