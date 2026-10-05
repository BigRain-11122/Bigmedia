# -*- coding: utf-8 -*-
# R1409 amend: time-gate operational-red honest accounting (slice blades ran 21:3x, window opened 21:40)
# pre-commit self-record fix on THIS round's own uncommitted artifacts (R1018 in-round fix precedent)
# scope: state last-log line (2 surgical spots) + backlog R1409 annotation head + OH slice header + export outs[0] + ts refresh
import json, io, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
now_s = now.strftime("%Y-%m-%d %H:%M:%S")

# ---- [1] state.json last log line ----
sp = repo + r"\src\os\state.json"
st = json.load(io.open(sp, encoding="utf-8"))
assert st["log"][-1].startswith("2026-10-05") and "R1409" in st["log"][-1], "last log is not R1409"

old_head = "R1409: 生产轮·#70 OSS 窗 4 切片 1 开窗即领（实活轮·窗位 2/6 即收=os-protocol §6 实活触发·commit 覆盖 R1407-R1409 区间）"
new_head = "R1409: 生产轮·#70 OSS 窗 4 切片 1 交付（实活轮·窗位 2/6 即收=os-protocol §6 实活触发·commit 覆盖 R1407-R1409 区间·**时点闸前拉操作红如实入账见③**）"
old_gate = "③窗 4 时闸 21:40 开·当窗即领（OH-20261005-bigstream.md 新建=窗 4 首档"
new_gate = "③**时点闸操作红如实入账**=三刀起跑 21:33-21:39 早于开窗时点 21:40 约 7 分钟（探针基线 21:32 判定后预算内顺跑未守时点闸=R1408「不前拉」纪律违例·交付 commit 落窗内 21:40+·窗 4 每窗 ≥1 切片义务达成不受影响·执法注记=切片起跑时刻须 ≥ 开窗时点·R1021 开窗即领 21:5x 口径·下窗照守）——OH-20261005-bigstream.md 新建=窗 4 首档"
assert old_head in st["log"][-1] and old_gate in st["log"][-1], "state anchors missing"
st["log"][-1] = st["log"][-1].replace(old_head, new_head, 1).replace(old_gate, new_gate, 1)
st["ts"] = now_s
st["task"] = st["log"][-1][len("2026-10-05 2x:xx "):][:60] if False else st["task"]  # task head unchanged
io.open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))
print("state amended ts=%s" % now_s)

# ---- [2] backlog R1409 annotation head ----
bp = repo + r"\src\os\backlog.md"
bt = io.open(bp, encoding="utf-8").read()
old_bk = "[R1409 交付毕 2026-10-05：#70 窗 4 切片 1 走门毕=开窗即领（窗 4=10-05 21:40 开→当窗即领·"
new_bk = "[R1409 交付毕 2026-10-05：#70 窗 4 切片 1 走门毕=窗内交付（**时点闸前拉操作红如实入账**=三刀起跑 21:33-21:39 早于 21:40 开窗 ~7 分钟·交付 commit 落窗内·义务达成不受影响·下窗起跑须 ≥ 开窗时点；窗 4=10-05 21:40 开·"
if old_bk in bt:
    bt = bt.replace(old_bk, new_bk, 1)
    io.open(bp, "w", encoding="utf-8").write(bt)
    print("backlog amended")
else:
    print("backlog anchor miss (check manually)")

# ---- [3] OH slice header (group repo single-file exception) ----
op = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20261005-bigstream.md"
ot = io.open(op, encoding="utf-8").read()
old_oh = "## 切片 1（R1409·2026-10-05 21:4x）—"
new_oh = "## 切片 1（R1409·2026-10-05 21:3x 起跑 → 21:4x 窗内交付）—"
old_oh2 = "> 实体：BigStream（bm-a OSLoop R1409 切片 1）"
new_oh2 = "> 实体：BigStream（bm-a OSLoop R1409 切片 1）\n> **时点闸操作红注记**：三刀起跑 21:33-21:39 早于本窗开窗时点 21:40 约 7 分钟（探针基线 21:32 判定后预算内顺跑未守时点闸）；交付 commit 落窗内 21:40+，每窗 ≥1 切片义务达成不受影响；执法注记=切片起跑时刻须 ≥ 开窗时点（R1021 开窗即领 21:5x 口径·下窗照守）。"
if old_oh in ot:
    ot = ot.replace(old_oh, new_oh, 1)
    if old_oh2 in ot:
        ot = ot.replace(old_oh2, new_oh2, 1)
    io.open(op, "w", encoding="utf-8").write(ot)
    print("OH amended")
else:
    print("OH anchor miss (check manually)")

# ---- [4] export outs[0] ----
ep = repo + r"\docs\status-export.json"
ex = json.load(io.open(ep, encoding="utf-8"))
old_ex = "R1409 生产轮=#70 OSS 窗 4 切片 1 开窗即领（实活轮闭 R1407-R1408 声明窗·os-protocol §6）"
new_ex = "R1409 生产轮=#70 OSS 窗 4 切片 1 窗内交付（实活轮闭 R1407-R1408 声明窗·os-protocol §6·时点闸前拉操作红如实入账=起跑 21:3x 早于 21:40 开窗 ~7min·commit 落窗内）"
if old_ex in ex["outs"][0][1]:
    ex["outs"][0][1] = ex["outs"][0][1].replace(old_ex, new_ex, 1)
    ex["export_ts"] = now_s
    io.open(ep, "w", encoding="utf-8").write(json.dumps(ex, ensure_ascii=False, indent=2))
    print("export amended")
else:
    print("export anchor miss (check manually)")
print("amend done")
