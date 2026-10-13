# -*- coding: utf-8 -*-
"""R2132 log line amendment: add fire_consume receipt + temp cleanup note."""
import io, json

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(P, "r", encoding="utf-8-sig") as f:
    d = json.load(f)

old = d["log"][-1]
assert old.startswith("2026-10-13 09:2x R2132"), old[:40]
amended = old.replace(
    "下扫描点维持=",
    "fire_consume --ledger 正身直发=no-fire rc1（reason=bm-a-workday-hours-zero-dispatch·工作日零排单铁律在执·ledger 行落盘·F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16 四件 fire-ready 结转〔fire 真窗=10-14 夜窗 00:00-08:00 或 CEO 下班旗再落〕）；临时件清理钩=close/scan 两脚本照 tech#81 自含律入账 commit+两瞬态读数 txt 删净；下扫描点维持=",
)
d["log"][-1] = amended
d["task"] = amended.split("R2132: ", 1)[1][:60]

with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("amended ok, len=%d" % len(amended))
