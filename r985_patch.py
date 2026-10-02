# -*- coding: utf-8 -*-
"""R985 log patch: record render-unannot finding fix (v15 leftover + v16 byproduct moved to
piece-tmp per v14 precedent; readiness re-probe 0 findings) - honest ledger, no fake green."""
import io, json

st = json.load(io.open("src/os/state.json", encoding="utf-8"))
assert st["tick"] == 985
entry = st["log"][-1]
old = u"副产 mp4 76KB 入 renders）"
new = u"副产 mp4 76KB——**轮内真发现即修=render-unannot 双件**：readiness 探针揭 output/renders/ 存 mc-daily-v15/v16-card.mp4 两件未注账（R984 v15 副产未入 tmp=R984 log「副产 mp4 入 tmp」未执行于盘上的如实勘正+本件 v16 副产同批）→双件移入各自 piece-tmp 目录〔MC-20261002-DAILY-v15.mp4/v16.mp4=14 前例惯例·mp4 gitignored 盘上留档〕→readiness 复跑 **0 findings**〔3 blockers 皆外部 CEO 面维持·假绿灯律② 承接：R984「72 renders 全注账」读数时点=mp4 尚未落 renders 或探针先于渲染·本轮盘上实证勘正不掩盖〕）"
assert old in entry, "anchor not found"
st["log"][-1] = entry.replace(old, new)
json.dump(st, io.open("src/os/state.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("log patched: render-unannot finding-fix recorded")
