# -*- coding: utf-8 -*-
"""MC-20261001-DIGEST-v11 build: DIGEST series 11th piece (R870, backlog #67 chronicle-event
claim, supply blind-spot correction round: R810 five-face supply inventory omitted the DIGEST
channel - last consumed R682 v10 09-29 11:21; the product-first CEO order P-2026-09-29-07
(~13:0x, after v10) was never evaluated as DIGEST candidate while the pool ran LC E1-E21 +
draft E22-E26). Product-first order numeric digest.
Facts: cph4/evolution-ledger.md P-2026-09-29-07 row (CEO verbatim full sentence + audit
readout 8 repos 7 days 10,524 commits, BigStream doc/bookkeeping share 46%) + own chain
(iteration_prompt.txt product-first block: scoring 2/1/0, bookkeeping cap <=5/round, export
3-line <=48h window, 24h all-zero = idle-verdict) + output/finished.md F-057 (R685 09-29
14:05) -> F-081 (R809 10-01 06:08) = 25 pieces in 40 hours + this card = 26th since the order.
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v10 build script. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V10 = os.path.join(BASE, "MC-20260929-DIGEST-v10")
V11 = os.path.join(BASE, "MC-20261001-DIGEST-v11")
TMP = V11 + "-tmp"
os.makedirs(V11, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V10, "cards.json"), encoding="utf-8"))

# CEO verbatim substring from ledger row P-2026-09-29-07 (zero char change, comma-boundary
# design split across two lines, v5 cross-line quote precedent; full sentence in source_facts)
LINES = [
    u"城市盘点 011",
    u"产品优先令 2026-09-29 午后落账（CEO 直令）",
    u"「产出落地很少，品质也很差，请从源头梳理和解决这个问题，",
    u"提高效率，过程能看到，结果早点出」",
    u"审计：8 仓 7 天 10,524 commit · 本司文档簿记 46%",
    u"立制：实物 2 分 · 改动 1 分 · 纯记账 0 分",
    u"回应：成品 25 件 40 小时入库 · F-057→F-081",
    u"24 小时全 0 分=空转判负 · 本卡=令后第 26 件",
]

SUBS_LINE = u"基于硅基城市真实事件（产品优先令台账档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2  # zero-margin exclusion law (em-budget-ladder hard law; R293 pixel-overlap lesson)

# --- vertical stack budget (R381 hard law; model from measured v2/v3 bands)
H1_GAP = int(cfg["font"]["h1_gap"])          # 36
OPT_C = float(cfg["font"]["optical_center"])  # 0.24
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])  # y=970
PITCH_F = 1.35   # conservative vs measured 1.318
GAP_MIN = 20     # px clearance to subs band


def stack_bottom(size, n):
    pitch = PITCH_F * size + 12
    h2_h = size + (n - 1) * pitch
    return cfg["video"]["height"] * OPT_C + H1_GAP + 1.5 * h2_h


def all_fit(size):
    budget = (frame_w - 160) / float(size)
    for ln in LINES[1:]:
        if _line_cost(ln) > budget - MARGIN_EM or len(wrap_for_width(ln, size, frame_w).split("\n")) != 1:
            return False
    return stack_bottom(size, len(LINES) - 1) <= SUBS_TOP - GAP_MIN


H2_SIZE = next(s for s in LADDER if all_fit(s))

meta = cfg["meta"]
meta["topic"] = "MC-20261001-DIGEST-v11"
meta["form"] = (u"DIGEST 盘点图文 011（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第十件·"
                u"#67 触发律=编年史事件随轮领〔R870 claim·供给盲区修正轮〕·"
                u"史源=P-2026-09-29-07 产品优先令正行〔CEO 直令 verbatim 全句+诊断读数〕+本司台账链双锚）")
meta["source_facts"] = (u"产品优先令数字盘点八条："
                        u"①「产品优先令 2026-09-29 午后落账（CEO 直令）」=cph4/evolution-ledger.md "
                        u"P-2026-09-29-07 正行（CEO 令 09-29 ~13:0x·P1·决策委员会工作轮·跨仓只读）"
                        u"+src/os/iteration_prompt.txt 生产段【产品优先律】块（任务书热改正源·"
                        u"「本块优先级高于本文件其余条款」·v2 DIGEST 同型任务书正源引证先例）／"
                        u"②引文两行「产出落地很少，品质也很差，请从源头梳理和解决这个问题，提高效率，"
                        u"过程能看到，结果早点出」=ledger 正行 CEO 原话 verbatim 连续子串零改字"
                        u"（逗号子句边界设计排版跨两行=v5 跨两行先例·全句另含前段「我感觉城市和子公司 集团 "
                        u"一致在写规则，写流程，文档什么的」与后续完整原文 verbatim 入 source_facts 本条·"
                        u"引文行 28.00em=h2_size 32 档驱动行）／"
                        u"③「审计：8 仓 7 天 10,524 commit · 本司文档簿记 46%」=ledger 正行诊断读数"
                        u"（8 仓 7 天 10,524 commit·文档/簿记类占比 BigStream 46%·集团正典已落档口径入卡面"
                        u"=v10 206/98% 治理审计读数同型分界；病灶实证=纯记账轮形态·集团横切诊断面）／"
                        u"④「立制：实物 2 分 · 改动 1 分 · 纯记账 0 分」=iteration_prompt.txt 产品优先律 1. 条"
                        u"计分制 Executive Protocol v1.1 三档原文（能跑/能看/能用实物=2 分；实际文件改动=1 分；"
                        u"纯 md 文档与纯记账=0 分·措辞简单易懂律白话表述=卡面三短语对表原文）"
                        u"+2. 条记账帽（纯记账类动作每轮 ≤5 处·数据/产品管线产出不算记账）"
                        u"+5. 条 export 三行（当前活/最近实物/下个里程碑窗 ≤48h·「过程能看到」原文直应位）"
                        u"+6. 条空转判负（连续 24h 全部 commit 均 0 分=空转判负）／"
                        u"⑤「回应：成品 25 件 40 小时入库 · F-057→F-081」=output/finished.md 台账链"
                        u"（F-057 R685 2026-09-29 14:05 首件→F-081 R809 2026-10-01 06:08=25 件连续登记·"
                        u"40 小时窗〔14:05→06:08 次次日=40h03m 机算〕·src/os/state.json R685-R809 log "
                        u"时间戳链逐件可核·构成=拆条 LC-003~021+稿集 BS-007~011+REACT v6/v7 全视频线成品）／"
                        u"⑥「24 小时全 0 分=空转判负」=产品优先律 6. 条原文压缩（空转判负·值守轮点名·"
                        u"回访 10-06 三锚）／⑦「本卡=令后第 26 件」=F-082 登记（本件）·F-057 起算第 26 件"
                        u"（25 前件+本卡=自指收束位·v9 计量回访行同型自指先例）／⑧底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"cph4/evolution-ledger.md P-2026-09-29-07 正行（集团进化台账·CEO 直令原话 verbatim "
                           u"全句+诊断读数 8 仓 7 天 10,524 commit/本司文档簿记 46%+病灶实证全录·跨仓只读）"
                           u"+src/os/iteration_prompt.txt 生产段【产品优先律】块（任务书热改正源·计分三档/"
                           u"记账帽 ≤5/export 三行窗 ≤48h/24h 零实物判负原文·v2 DIGEST 任务书正源引证先例）"
                           u"+output/finished.md F-057~F-081 台账行（令后 25 件成品链·逐件可机核）"
                           u"+src/os/state.json R685/R809 log（首件 14:05/末件 06:08 时间戳锚·40h 窗机算）"
                           u"+src/os/backlog.md #67 R870 claim 行（供给盲区修正注记=P-51 送达链）"
                           u"+docs/self-improvement-queue.md §E 批活池 E27 行（lane 供给修正面）——"
                           u"编年史 A 级史源（集团进化台账+任务书正源+成品库台账·charter §3 选题池多源）·"
                           u"一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=CEO 原话 verbatim 连续子串零改字〔ledger 正行原句零改字零重组·CEO 令全文 verbatim "
                             u"入 source_facts·批评面照录禁软化禁重组=问责纪实位〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（产品优先令台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=产品优先令数字盘点档案体（1 句 CEO 直评 vs 立制三档+40 小时 25 件回应链="
                            u"「要实物」母题·诊断读数〔8 仓 7 天 10,524 commit/本司 46%〕=令的必要性证据位·"
                            u"直评→诊断→立制→回应→判负执法=「问题→立法→交货」递进链·本卡第 26 件=自指收束位"
                            u"（机制自证面）·「过程能看到，结果早点出」原文与 export 三行窗直应位=金句回环；"
                            u"公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句 CEO 直评「产出落地很少」 vs "
                          u"8 仓 7 天 10,524 commit 诊断读数+立制三档 2/1/0 vs 40 小时 25 件成品回应+本卡第 26 件自指"
                          u"——F-042 v2 对照数字结构同源第十证·十连母题〔v2 开闸/v3 三线/v4 技能/v5 节目重制/"
                          u"v6 对账夜/v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令/v10 云端 token 机制日/"
                          u"v11 产品优先令日〕+三档/≤5/≤48h/25 件/40h/46%/第 26 件七组数字/"
                          u"情 1 AI 自治问责吃瓜温和如实非强极点〔G5 吃瓜未来党+G1 AI 效率实操党双群对位·"
                          u"CEO 批评照录+本司 46% 短板自曝+当夜立制+照单交货=AI 公司自我治理叙事面〕/"
                          u"时 2 令 2026-09-29 午后→本卡 2026-10-01 两日跨度+台账档案常青〔v5 两日时点先例〕/"
                          u"时序链=令 09-29 ~13:0x→首件 F-057 14:05→末件 F-081 10-01 06:08→本卡 R870）/"
                          u"台 2 公众号方图承载=MC-001~081 S3 实证复用·盘点=公众号主流图文格式"
                          u"〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                          u"#67 触发律=编年史事件随轮领〔R870 claim·供给盲区修正轮=R810 五面盘点遗漏 DIGEST 通道"
                          u"·最后消费 R682 v10 后产品优先令落账未评估·本件=通道重开首件非造活凑数〕")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=诊断读数为治理审计读数"
                     u"（集团正典已落档口径·commit 计数与占比=非 token 用量非财务面·v10 206/98% 同型分界）"
                     u"入卡面；CEO 批评原文 verbatim 纪实照录=批评面不软化不重组（问责档案位）；"
                     u"P1 边界=本件=纪实档案非提案非表决（计分制执行面=任务书正源纪实非本司自评宣传）；"
                     u"他司执行面细节不入卡面（8 仓分布他司占比=批级知悉位）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十一件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append(u"H1 size %d budget %.2fem | H2 size %d budget %.2fem (ladder pick, zero-margin exclusion margin>=%.1fem)" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM))
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
report.append(u"VERT stack bottom est %.0fpx vs subs top %dpx gap %+.0fpx (need >=%dpx) (R381 vertical law)" % (vb, SUBS_TOP, SUBS_TOP - vb, GAP_MIN))
assert SUBS_TOP - vb >= GAP_MIN, "vertical stack budget FAIL"
for ln in LINES:
    cost = _line_cost(ln)
    size = h1_size if ln is LINES[0] else H2_SIZE
    budget = budget_h1 if ln is LINES[0] else budget_h2
    single = len(wrap_for_width(ln, size, frame_w).split("\n")) == 1
    margin = budget - cost
    fits = margin >= (0.0 if ln is LINES[0] else MARGIN_EM)
    ok = ok and single and fits
    report.append(u"%-6.2fem  budget %-6.2fem  margin %+-5.2fem  single=%s  %s" % (cost, budget, margin, single, ln))
subs_cost = _line_cost(SUBS_LINE)
subs_budget = (frame_w - 160) / float(subs_size)
report.append(u"subs   %-6.2fem  budget %-6.2fem  margin %+-5.2fem  %s" % (subs_cost, subs_budget, subs_budget - subs_cost, SUBS_LINE))
ok = ok and subs_cost <= subs_budget
report.append("EM_CHECK: " + ("ALL OK" if ok else "FAIL"))
io.open(os.path.join(TMP, "em-check-r870.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V11, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V11, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
