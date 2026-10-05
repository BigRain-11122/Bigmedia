# -*- coding: utf-8 -*-
import json, io

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sp = repo + r"\src\os\state.json"
st = json.load(io.open(sp, encoding="utf-8"))
log = st.get("log", [])
old = log[-1]
if "14:5x R1369:" in old:
    log[-1] = old.replace("2026-10-05 14:5x R1369:", "2026-10-05 14:4x R1369:", 1)
    io.open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))
    print("fixed: 14:5x -> 14:4x in R1369 log line")
else:
    print("no fix needed; tail head=" + old[:40])
