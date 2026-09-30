# -*- coding: utf-8 -*-
# R691 honesty fix: ledger count 6->5 (backlog #79 note skipped, anchor not found)
import json, io

p1 = r"src/os/state.json"
st = json.load(io.open(p1, encoding="utf-8"))
old = (u"⑤台账六件=renders README〔声明行渲染腿收口+在链表行〕+station-reviews R691 S2 行+lc005 README 生产记录+"
       u"queue §E burn 行+backlog #79 R691 注+status-export 刷（live 三行=R691 实况）")
new = (u"⑤台账五件=renders README〔声明行渲染腿收口+在链表行〕+station-reviews R691 S2 行+lc005 README 生产记录+"
       u"queue §E burn 行+status-export 刷（live 三行=R691 实况·backlog #79 注=锚行未觅如实跳过）")
assert old in st["log"][-1], "log 5 anchor missing"
st["log"][-1] = st["log"][-1].replace(old, new)
io.open(p1, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))

p2 = r"docs/status-export.json"
ex = json.load(io.open(p2, encoding="utf-8"))
old2 = (u"台账六件（renders 声明行收口+在链行/station-reviews S2 行/lc005 README/queue burn/backlog #79 注/status-export live）")
new2 = (u"台账五件（renders 声明行收口+在链行/station-reviews S2 行/lc005 README/queue burn/status-export live·"
        u"backlog #79 注=锚行未觅如实跳过）")
assert old2 in ex["results"][-1][1], "export results anchor missing"
ex["results"][-1][1] = ex["results"][-1][1].replace(old2, new2)
io.open(p2, "w", encoding="utf-8").write(json.dumps(ex, ensure_ascii=False, indent=1))

st2 = json.load(io.open(p1, encoding="utf-8"))
ex2 = json.load(io.open(p2, encoding="utf-8"))
print("FIX_OK tick", st2["tick"], "log", len(st2["log"]),
      "state5", u"台账五件" in st2["log"][-1],
      "export5", u"台账五件" in ex2["results"][-1][1],
      "json_valid", True)
