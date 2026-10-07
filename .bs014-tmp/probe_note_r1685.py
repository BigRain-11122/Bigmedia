# -*- coding: utf-8 -*-
# R1685 probe-note patch: append three-probe readings to this round's own (uncommitted) records
import json, io

PROBE = "；⑨三探针=board 0 FAIL〔5 题 10 稿·5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次① 11 平台+M4 GATE 6/10+#17 needs-CEO〕+**1 在链预期红=render-unannot bs-014**〔R173/R192 同型先例·在链件五合法态（测试件/成品·批次/成品·落位/已被取代/弃件留档）皆不适用·F-162 登记即清·禁预标成品=假绿灯律①〕/loop_health 2F+151W 皆在案史实〔两 outage 09-26/09-28 不重复触发+account-drift done 1698 vs tick 1685 +13==adjudicated 14 基线带内〕"

sp = "src/os/state.json"
st = json.load(io.open(sp, encoding="utf-8"))
last = st["log"][-1]
assert "R1685" in last and "渲染腿毕" in last, last[:60]
marker = "。下轮=R1686"
assert marker in last
st["log"][-1] = last.replace(marker, PROBE + marker, 1)
io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(st, ensure_ascii=False, indent=2))

srp = "docs/reviews/station-reviews.md"
t = io.open(srp, encoding="utf-8").read()
old_tail = "——余腿（下轮）=E8 终审〔ASR 终轨 R169 QC+E4 参考仪〕→M4→F-162 登记 |"
new_tail = "——余腿（下轮）=E8 终审〔ASR 终轨 R169 QC+E4 参考仪〕→M4→F-162 登记·三探针=board 0F/readiness +1 在链预期红=render-unannot bs-014（R173/R192 先例·F-162 登记即清）/loop_health 2F+151W 皆在案史实（drift +13=adjudicated 14 带内） |"
assert t.count(old_tail) == 1, t.count(old_tail)
io.open(srp, "w", encoding="utf-8", newline="\n").write(t.replace(old_tail, new_tail, 1))
print("OK probe-note patched into R1685 state log + station-reviews row")
