# -*- coding: utf-8 -*-
# R800: BS-008 cards-v2-matched.json build (base=.bs008-tmp/cards.json TTS v2
# baseline clock x visual declarations; probe-first honest req; F-004 v15
# same-family precedent, R757/R759 pre-eval adjudicated)
import json, io

base = json.load(io.open(r".bs008-tmp\cards.json", encoding="utf-8"))
LL = "data/sources/footage/looplog-vertical.mp4"
RD = "data/sources/footage/reviewsdoc-vertical.mp4"
EG = "data/sources/footage/editgrid-vertical.mp4"

VIS = {
    0: (LL, "系统日志本体在帧（hook 口播「系统日志：432 全灭」字面直证·档案=日志文件本体·拍头帧即日志文件名可读·F-004 v15 b0 同拍位先例·同源多用注记）"),
    1: (LL, "拦截/FAIL 判定行可见（门禁链=拦截不放行的判定形态·三场全灭的日志现场·F-004 v15 b2 门禁职责同拍位先例·同源多用注记）"),
    2: (RD, "PASS/verdict 判定行可见（唯一通关=台账 PASS 判定的证据形态·「1 员 PASS」判定语义直证·意象对位声明）"),
    3: (RD, "台账在册条目+日期行可见（注册件=台账登记的证据形态·F-004 v15 b8 注册证书同拍位先例·同源多用注记）"),
    4: (None, "核心读数=量化实况（样本外 Sharpe 2.057·BigMoney 总控唯一源判敏感禁用·F-004 v15 b5 随机基线同拍位先例·footage-matching-spec §2 在案），纯字卡声明不造假素材"),
    5: (EG, "逐条并列网格形态可见（522 笔一笔不漏=逐笔并列的清单形态·F-004 v15 b11 五句清单同型意象对位声明·同源多用注记）"),
    6: (LL, "时间戳逐年推进行可见（最差一年/无崩年=档案逐年记录的运行形态·意象对位声明·F-004 v15 b7 五道门流水线工序同型·同源多用注记）"),
    7: (LL, "FAIL/超时判定行可见（死法标注=失败判定的日志记录形态·「连死法都标」的档案语义直证·F-004 v15 b1 全灭现场同拍位先例·同源多用注记）"),
    8: (RD, "verdict+证据链接列可见（诚实律=判定+证据链的台账形态·F-004 v15 b9 诚实标注「强到哪·死在哪」同锚行同拍位先例·同源多用注记）"),
    9: (RD, "台账在册条目行可见（在册 3 名=台账登记证据形态·「同一道链无例外」的台账语义·同源多用注记）"),
    10: (LL, "轮次/检查挂账行可见（首月检查=轮次节律的检查语义·10-31 检查挂账行在帧·意象对位声明·同源多用注记）"),
    11: (None, "CTA 导流拍常规纯字卡+量化合规拍纯字卡强化「不构成投资建议」声明（footage-matching-spec §1·F-004 v15 b11 同拍位先例）"),
}

cards = []
# R800 frame-verify fix: explicit clean splits at the CJK dot separator for the
# two long subtitle anchors, so wrapping never breaks inside a number/word
# (b4 split "2.057" mid-number on first render - tile-verified; verbatim text
# unchanged, only line boundaries)
SPLIT = {
    4: ["核心读数", "样本外 Sharpe 2.057", "成本 ×2 存活"],
    7: ["死法标注", "成本 ×3 不存活", "厚度上限 2 倍"],
}
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
    "BS-008 稿集件视觉动态=档案本体+判定证据（源=BS-004 公众号母稿幸存者档案切面·R798/R799 选优定谳）——"
    "looplog（BS-OSLoop.log 系统日志终端=档案/判定行本体）×5+reviewsdoc（站审台账=PASS/在册/verdict 证据）×4"
    "+editgrid（自产字卡网格=逐笔清单形态）×1+cards-only×2（核心读数=BigMoney 判敏感禁用·CTA 合规拍）"
    "·对位 10/12=0.83（F-002/F-004 同源带·R799 预评估口径兑现·biggame-cockpit 弱对位弃用）"
    "·素材探针先行定谳（probe-r800/probe-src-tile.png 三源三时点多模态=零录穿·looplog/reviewsdoc 静态终端·editgrid 静态网格）"
)
base["cards"] = cards

out = r"data\sources\bs008\cards-v2-matched.json"
json.dump(base, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n_vis = sum(1 for c in cards if "source" in c["visual"])
print("BUILT", out, "cards=%d visual=%d ratio=%.3f" % (len(cards), n_vis, n_vis / 12.0))
