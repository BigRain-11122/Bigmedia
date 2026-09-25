# R291 log-row timestamp prefix fix: 21:3x -> 21:2x (ts=21:28:18 actual; log-order hygiene).
import json, io

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
s = json.load(io.open(P, encoding="utf-8"))
last = s["log"][-1]
if last.startswith("2026-09-25 21:3x R291:"):
    s["log"][-1] = last.replace("2026-09-25 21:3x R291:", "2026-09-25 21:2x R291:", 1)
    json.dump(s, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    chk = json.load(io.open(P, encoding="utf-8"))
    print("FIXED_OK" if chk["log"][-1].startswith("2026-09-25 21:2x R291:") else "FIX_FAIL")
else:
    print("NO_MATCH prefix=%s" % last[:30])
