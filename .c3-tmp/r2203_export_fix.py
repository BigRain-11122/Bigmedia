# -*- coding: utf-8 -*-
"""R2203 export fixup: first-pass patch had a 155-char do-line (writer
refusal, product-priority section 5 cap 120); re-run the canonical writer
with a compliant do-line + the same live three-liner."""
import sys, os, io, json

sys.path.insert(0, os.path.join("src", "os"))
import export_refresh as er

patch = {
    "do": "R2203 收令轮毕：CEO 云端放开令知悉；决策 C-20261013-01 ack；tech#126 冒烟抽读 16 笔·校准版在役；fire 四件候 MV 让位。",
    "live": [
        "当前活：夜窗已提前开（CEO 下班令 21:0x）：AI 日报 Worker 复役+重排池在磨+校准冒烟抽读毕；L 卡四件 fire 候 MV sprint 让位。",
        "最近实物：城市盘点 019（10-12）；本轮=ORDERS 380-381+决策 C-20261013-01 消费收口+tech#126 冒烟证据（10-13 23:0x）。",
        "下个里程碑：10-14 08:00 tech#92/#126 权威窗读数（城市源 ≥60 判据）；MV 让位后 F-180~183 fire 接力（窗 ≤10-15）。",
    ],
}
rc, lines, violations = er.refresh_export(os.path.join("docs", "status-export.json"), patch=patch)
for l in lines:
    print(l.encode("ascii", "replace").decode("ascii"))
print("rc:", rc, "violations:", violations)
sys.exit(rc)
