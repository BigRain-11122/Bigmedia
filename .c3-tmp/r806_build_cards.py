# -*- coding: utf-8 -*-
# R806: BS-010 cards-v1-matched.json build (base=.bs010-tmp/cards.json TTS v1
# baseline clock x visual declarations; R803 build_cards chain-inheritance,
# probe-first honest req; full-res looplog recheck = BS-OSLoop-Log window)
import json, io

base = json.load(io.open(r".bs010-tmp\cards.json", encoding="utf-8"))
LL = "data/sources/footage/looplog-vertical.mp4"
RD = "data/sources/footage/reviewsdoc-vertical.mp4"
EG = "data/sources/footage/editgrid-vertical.mp4"

VIS = {
    0: (LL, "系统日志本体在帧（BS-OSLoop-Log 窗口标题+轮次日志行可读=hook 口播「系统日志」字面直证·拍头帧即日志名可读·F-004 v15 b0 同拍位先例·同源多用注记）"),
    1: (LL, "AI 循环日志本体在帧（AI 工作循环实况=口播主语「AI」的主体实据·病象判定的主语位·同源多用注记·意象对位声明）"),
    2: (EG, "并列网格形态可见（2×2 字卡网格=「一个接一个」并列意象·自产字卡网格非实盘素材·意象对位声明·F-004 v15 b11 同型）"),
    3: (LL, "纪律执行行可见（轮首核验/收账判语逐轮出现=「治法早写好了」的执行在案形态·b0 同源直证·同源多用注记）"),
    4: (RD, "规则判定行可见（Rollout Review Ledger 评审台账=规则执行判定记录形态·「铁律原文」的落账证据形态·F-004 v15 b9 诚实律同拍位先例·意象对位声明）"),
    5: (LL, "同仓退避行可见（日志行「在途缓避让」字样实帧可读=「同仓，只留一个写手」的避让实况直证·全分辨率复核 probe-r806/looplog-full.png·同源多用注记）"),
    6: (LL, "逐轮对账行可见（tick/beats/done 对账字样=每轮产出落账的账目形态·「白干一轮」判定的账面意象·同源多用注记·意象对位声明）"),
    7: (LL, "循环日志实时实况可见（在跑循环的日志本体=「这条纪律正在跑」字面直证·b0 同源·同源多用注记）"),
    8: (RD, "台账清单在帧（评审台账文档=「账本」字面直证·「每一步落账」的台账形态·F-004 v15 b9 同拍位先例·同源多用注记）"),
    9: (RD, "在册条目行可见（台账条目=新产出登记形态·「没造过的东西」在册意象·意象对位声明·同源多用注记）"),
    10: (LL, "下轮指针行可见（日志行「下轮=」字样实帧可读=「去造下一个」字面直证·全分辨率复核在案·b0 同源·同源多用注记）"),
    11: (None, "CTA 导流拍常规纯字卡（footage-matching-spec §1·F-004 v15 b11 同拍位先例）"),
}

cards = []
SPLIT = {}
for i, c in enumerate(base["cards"]):
    card = {"start": c["start"], "end": c["end"], "lines": SPLIT.get(i, c["lines"])}
    src, req = VIS[i]
    if src:
        card["visual"] = {"source": src, "req": req}
    else:
        card["visual"] = {"cards-only": True, "reason": req}
    cards.append(card)

base["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
base["meta"]["storyboard"] = (
    "BS-010 稿集件视觉动态=循环日志本体+台账证据（源=BS-002 公众号母稿设计细节之人味第三细节反重复铁律切面·R805 选优定谳）——"
    "looplog（BS-OSLoop-Log 系统日志终端=系统日志/AI 本体/同仓退避/逐轮对账/在跑证明/下轮指针）×7"
    "+reviewsdoc（Rollout Review Ledger 评审台账=铁律判定/账本/在册）×3"
    "+editgrid（自产字卡网格=「一个接一个」并列形态）×1+cards-only×1（CTA 拍）"
    "·对位 11/12=0.92（层 1.8 visual-ratio ≥0.80 面·BS-009 同位带）"
    "·素材探针先行定谳（probe-r806 三源三时点多模态=零录穿·三源静态稳定·全分辨率复核 looplog=BS-OSLoop-Log 窗口+「在途缓避让」「下轮=」字样实帧可读）"
)
base["cards"] = cards

out = r"data\sources\bs010\cards-v1-matched.json"
json.dump(base, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n_vis = sum(1 for c in cards if "source" in c["visual"])
print("BUILT", out, "cards=%d visual=%d ratio=%.3f" % (len(cards), n_vis, n_vis / 12.0))
