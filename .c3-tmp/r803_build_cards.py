# -*- coding: utf-8 -*-
# R803: BS-009 cards-v1-matched.json build (base=.bs009-tmp/cards.json TTS v1
# baseline clock x visual declarations; R800 build_cards chain-inheritance,
# probe-first honest req; F-004 v15 same-family precedent)
import json, io

base = json.load(io.open(r".bs009-tmp\cards.json", encoding="utf-8"))
LL = "data/sources/footage/looplog-vertical.mp4"
RD = "data/sources/footage/reviewsdoc-vertical.mp4"
EG = "data/sources/footage/editgrid-vertical.mp4"

VIS = {
    0: (LL, "系统日志本体在帧（hook 口播「系统日志：调出公司第一条红线」字面直证·红线原文=日志记录本体·拍头帧即日志文件名可读·F-004 v15 b0 同拍位先例·同源多用注记）"),
    1: (EG, "并列网格形态可见（「满屏/条条」=多条漂亮曲线并列的网格意象·自产字卡网格非实盘素材·意象对位声明·F-004 v15 b11 五句清单同型）"),
    2: (LL, "时间戳/逐行推进行可见（参数反复调试=日志逐年逐行推进的运行记录形态·F-004 v15 b7 五道门流水线工序同型·意象对位声明·同源多用注记）"),
    3: (RD, "台账在册/定义条目行可见（「这有名字」=登记命名形态·F-004 v15 b8 注册证书同拍位先例·意象对位声明·同源多用注记）"),
    4: (LL, "红线原文/规则行可见（「红线原文」字面=规则文本在日志的记录形态·b0 同源直证·F-004 v15 b1 全灭现场同拍位先例·同源多用注记）"),
    5: (RD, "PASS/verdict 判定行可见（「不等于有本事」=判定语义的证据形态·意象对位声明·同源多用注记）"),
    6: (LL, "FAIL/判定行可见（口播「日志判定：这叫骗自己」字面直证·F-004 v15 b1 全灭现场同拍位先例·同源多用注记）"),
    7: (RD, "台账在册条目行可见（「先管住我们自己」=红线在册自治理台账形态·意象对位声明·同源多用注记）"),
    8: (RD, "verdict+证据链列可见（「先证明」=判定+证据链的证明形态·F-004 v15 b9 诚实律同拍位先例·同源多用注记）"),
    9: (LL, "系统日志本体在帧（「系统在说真话」字面直证·b0 同源·F-004 v15 b0 同拍位先例·同源多用注记）"),
    10: (LL, "红线原文/收束规则行可见（「红线只有一句」=红线文本的日志记录形态·b0/b4 同源直证·同源多用注记）"),
    11: (None, "CTA 导流拍常规纯字卡+量化合规拍纯字卡强化「不构成投资建议」声明（footage-matching-spec §1·F-004 v15 b11 同拍位先例）"),
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
    "BS-009 稿集件视觉动态=红线日志本体+判定证据（源=BS-004 公众号母稿曲线拟合红线切面·R802 选优定谳）——"
    "looplog（BS-OSLoop.log 系统日志终端=红线原文/判定行本体）×6+reviewsdoc（站审台账=在册/verdict/证明证据）×4"
    "+editgrid（自产字卡网格=「满屏/条条」并列形态）×1+cards-only×1（CTA 合规拍）"
    "·对位 11/12=0.92（层 1.8 visual-ratio ≥0.80 面·F-002/F-004 0.83 带上探）"
    "·素材探针先行定谳（probe-r803/probe-src-tile.png 三源三时点多模态=零录穿·looplog/reviewsdoc 静态终端·editgrid 静态网格）"
)
base["cards"] = cards

out = r"data\sources\bs009\cards-v1-matched.json"
json.dump(base, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n_vis = sum(1 for c in cards if "source" in c["visual"])
print("BUILT", out, "cards=%d visual=%d ratio=%.3f" % (len(cards), n_vis, n_vis / 12.0))
