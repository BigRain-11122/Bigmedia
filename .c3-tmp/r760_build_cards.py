# -*- coding: utf-8 -*-
# R760: BS-007 cards-v1-matched.json build (base=.bs007-tmp/cards.json TTS baseline
# clock x visual declarations; probe-first honest req per footage-matching-spec)
import json, io

base = json.load(io.open(r".bs007-tmp\cards.json", encoding="utf-8"))
LL = "data/sources/footage/looplog-vertical.mp4"
BG = "data/sources/footage/biggame-cockpit-vertical.mp4"
RD = "data/sources/footage/reviewsdoc-vertical.mp4"

VIS = {
    0: (LL, "系统日志本体在帧（BS-OSLoop.log 终端=hook 口播「系统日志」字面直证·三颗心脏的公司实况=循环日志本体·拍头帧即日志文件名可读）"),
    1: (None, "量化拍=BigMoney 持仓画面判敏感禁用先例（R757 素材预评估·R179/R186 同型）——量化心由字卡承载（「每 10 分钟干活」卡锚行即证据面）"),
    2: (BG, "游戏快照直证（像素小镇驾驶舱=每 10 分钟重写的游戏世界本体·HUD 行股/得仓/库存计数器实时可见=快照机制运行实况·R757 预评估双直证之一）"),
    3: (LL, "进化引擎=循环日志本体（轮次推进/心跳/评审 PASS 行在帧=周日 09:17 一跳的运行痕迹·同源多用注记）"),
    4: (LL, "频率分层=日志时间戳节奏直证（tick/beat/done 轮号节律在帧·同源多用注记）"),
    5: (LL, "10 分钟节律运行证据（轮次窗口时间戳=「太密空转·太疏过夜」论证对象的运行实况·同源多用注记）"),
    6: (LL, "一轮窗口=轮号+心跳窗口直证（Loop health 对账读数在帧·故障暴露不超过一轮=日志轮次窗口语义·BS-006 b7 同位先例）"),
    7: (LL, "任务板=进程表直证（日志内 backlog/plan.json 处理行=任务板运行实况·同源多用注记）"),
    8: (RD, "看门狗=站审台账节律直证（Station Reviews Ledger 评审行/verdict 列在帧=定时自检的台账本体·BS-006 b7 Loop health 对账同位先例）"),
    9: (RD, "「公司 OS」=结构直证（台账表格结构=文件系统/结构语义的画面证据·评审单指针列逐行可读·同源多用注记）"),
    10: (LL, "无人值守运行实况（循环日志自动轮转在帧=电脑空闲才干活的运行本体·同源多用注记）"),
    11: (None, "CTA 常规拍（完整拆解指引·F-001 v15 b11/BS-006 b11 同位惯例·字卡收尾）"),
}

cards = []
for i, c in enumerate(base["cards"]):
    card = {"start": c["start"], "end": c["end"], "lines": c["lines"]}
    src, req = VIS[i]
    if src:
        card["visual"] = {"source": src, "req": req}
    else:
        card["visual"] = {"cards-only": True, "reason": req}
    cards.append(card)

base["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
base["meta"]["storyboard"] = (
    "BS-007 稿集件视觉动态=频率分层+结构对照（源=BS-002 公众号母稿哲学切面·R757 选稿定谲）——"
    "looplog（BS-OSLoop.log 系统日志终端）×7+biggame-cockpit（像素小镇驾驶舱）×1+reviewsdoc（站审台账）×2"
    "+cards-only×2（量化拍=BigMoney 持仓画面判敏感禁用·CTA 常规拍）·对位 10/12=0.83（F-002 v15 同源带·R757 预评估口径）·"
    "素材探针先行定谳（probe-r760/probe-src-tile.png 三源三时点多模态=零录穿·looplog/reviewsdoc 静态终端·biggame 活游戏）"
)
base["cards"] = cards

out = r"data\sources\bs007\cards-v1-matched.json"
json.dump(base, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n_vis = sum(1 for c in cards if "source" in c["visual"])
print("BUILT", out, "cards=%d visual=%d ratio=%.3f" % (len(cards), n_vis, n_vis / 12.0))
