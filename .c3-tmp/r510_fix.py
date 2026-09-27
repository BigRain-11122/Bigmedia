# -*- coding: utf-8 -*-
# R510 honesty fix: remove false over-budget note (round closed 12:14, inside 25-min window)
# + orders receipt minute placeholder correction.
import io, json

SP = r"src\os\state.json"
OD = r"orders\O-20260927-1050-HQ-C.md"

with io.open(SP, encoding="utf-8") as f:
    st = json.load(f)
old_note = ("\u2014\u2014\u957f\u8f6e\u6ce8=\u8d77\u94fe+\u56db\u9053\u7a7a\u6c14\u9884\u7b97\u8fed\u4ee3+\u53f0\u8d26\u8017\u00b7"
            "\u8d85 25 \u5206\u949f\u9884\u7b97 WARN \u7ea7\u5982\u5b9e\u5165\u8d26\uff08loop_health heartbeat-gap \u9762\uff09")
new_note = "\uff08\u8f6e\u9884\u7b97 25 \u5206\u949f\u5185\u6536\u8d26\u00b712:14\uff09"
fixed = 0
for i, ln in enumerate(st["log"]):
    if old_note in ln:
        st["log"][i] = ln.replace(old_note, new_note)
        fixed += 1
assert fixed == 1, "log note hits=%d" % fixed
with io.open(SP, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write("\n")

with io.open(OD, encoding="utf-8") as f:
    txt = f.read()
old_m = "[R510 \u6536\u884c 2026-09-27 ~12:2X\uff1a"
new_m = "[R510 \u6536\u884c 2026-09-27 ~12:1X\uff1a"
assert old_m in txt, "orders anchor missing"
txt = txt.replace(old_m, new_m)
with io.open(OD, "w", encoding="utf-8") as f:
    f.write(txt)

json.load(io.open(SP, encoding="utf-8"))
print("honesty fix OK")
