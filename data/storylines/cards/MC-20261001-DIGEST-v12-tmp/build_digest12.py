# -*- coding: utf-8 -*-
"""MC-20261001-DIGEST-v12 build: DIGEST series 12th piece (R871, backlog #67 chronicle-event
claim, E28 stock candidate consumed per R870 closing order "E28/E29 sui-lun-ling"). Event =
2026-09-30 group external-audit decision batch: CEO order D-20260930-06 verbatim
(external-expert full-group audit) -> 12 audit rounds -> 40 decisions in one day
(D-20260930-01..41, D-10 gap; queue stock note "41" = tail-number off-by-one, machine
regex-set count = 40, honest correction recorded). Numbers: XL-1..21 improvement list (D-06),
RW-1..7 credibility repair order (D-05), M1~M7 methodology (D-37), Q1~Q9 audit probes
(D-27 + D-31, first run 4 hits incl. 1 P0), 5 self-corrections (D-25 section 7), six laws into
charter (D-26), veto window 7 days to 10-07.
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381). Template = DIGEST v11 build script. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V11 = os.path.join(BASE, "MC-20261001-DIGEST-v11")
V12 = os.path.join(BASE, "MC-20261001-DIGEST-v12")
TMP = V12 + "-tmp"
os.makedirs(V12, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V11, "cards.json"), encoding="utf-8"))

# CEO verbatim substring from group decisions row D-20260930-06 (zero char change,
# slash-clause boundary design split across two lines, v5 cross-line quote precedent)
LINES = [
    u"城市盘点 012",
    u"集团外审日 2026-09-30（CEO 直令 · 12 轮外审）",
    u"「作为外部专家逐个看业务/子公司/集团，",
    u"输入改进清单，让他们科学决策落实」",
    u"单日批 40 决（编号至 D-20260930-41）",
    u"改进清单 XL-1→21 · 修复单 RW-1→7",
    u"方法论 M1→M7 · 审计探针 Q1→Q9（P0 命中）",
    u"外审 5 次自我勘正 · 六律入章程 · 窗至 10-07",
]

SUBS_LINE = u"基于硅基城市真实事件（集团外审决策批台账档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2  # zero-margin exclusion law (em-budget-ladder hard law; R293 pixel-overlap lesson)

# --- vertical stack budget (R381 hard law; model from measured v2/v3 bands)
H1_GAP = int(cfg["font"]["h1_gap"])
OPT_C = float(cfg["font"]["optical_center"])
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])
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
meta["topic"] = "MC-20261001-DIGEST-v12"
meta["form"] = (u"DIGEST 盘点图文 012（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第十一件·"
                u"#67 触发律=编年史事件随轮领〔R871 claim·E28 备货位领做=R870 收口可领序首位兑现〕·"
                u"史源=FluxGroup/docs/decisions.md 集团外审批 D-20260930-01→41〔CEO 直令 verbatim+12 轮外审"
                u"+单日 40 决机核计数〕）")
meta["source_facts"] = (u"集团外审日数字盘点八条："
                        u"①「集团外审日 2026-09-30（CEO 直令 · 12 轮外审）」=FluxGroup/docs/decisions.md "
                        u"D-20260930-06 正行（CEO 令 09-30「作为外部专家逐个看业务/子公司/集团，输入改进清单，"
                        u"让他们科学决策落实」·跨仓只读·D-20261001-03 宿主机直读正典=本机即集团仓宿主机零 git "
                        u"操作零写接触）+D-20260930-25 正行（外审第十二轮〔末轮〕收口=12 轮外审读数·"
                        u"诊断/清单/决策/派工/收执五段前四段完成）／"
                        u"②引文两行「作为外部专家逐个看业务/子公司/集团，输入改进清单，让他们科学决策落实」"
                        u"=D-20260930-06 正行 CEO 原话 verbatim 连续子串零改字（斜杠子句边界设计排版跨两行="
                        u"v5 跨两行先例·CEO 令全文 verbatim 入 source_facts 本条）／"
                        u"③「单日批 40 决（编号至 D-20260930-41）」=docs/decisions.md 09-30 批机核计数"
                        u"（python regex set 实核 2026-10-01：D-20260930-01~09+11~41=40 行·D-10 空号·"
                        u"queue §E E28 备货位「41 决」=尾号读数差如实勘正·决策批盘点=v6 深夜决策批同型先例承继）／"
                        u"④「改进清单 XL-1→21」=D-20260930-06（集团全域改进清单 XL-1~XL-21·七路外审"
                        u"〔六业务线+CPH4+集团治理层〕·T0 五项呈 CEO/自决六项/各司自领六项·"
                        u"BigStream 份额 XL-14=dirty 908→<50+≥1 条真发布回写链接+产出报表三列）／"
                        u"⑤「修复单 RW-1→7」=D-20260930-05（BigMoney 可信度修复单 RW-1~RW-7·"
                        u"CEO 令 09-30「指出问题，指明方向」+五路专家独立审计+HQ 复算·P0 级缺陷即时修）／"
                        u"⑥「方法论 M1→M7」=D-20260930-37（量化方法论增强七件 M1~M7+独立净值复核层 M7·"
                        u"CEO 令 09-30「算了，你专注去搞我的量化金融这一块，打磨方法论等」）"
                        u"+「审计探针 Q1→Q9（P0 命中）」=D-20260930-27（量化独立审计探针首跑 Q1~Q5·"
                        u"4 项命中含 1 项 P0 定价缺陷）+D-20260930-31（探针二批 Q6~Q9·含外审自我撤回一次）／"
                        u"⑦「外审 5 次自我勘正 · 六律入章程」=D-20260930-25 §七（五次自我勘正台账·"
                        u"外审也会误判·由集团自有机制当场纠正=双向诚实律）+D-20260930-26（外审前置与验收六律"
                        u"入章程 docs/audit-charter.md 附录 A·六条方法律由六次自纠反推）／"
                        u"⑧「否决窗 7 天至 10-07」=09-30 批 T1/T2 通行判据（科学自决+否决窗 7 天至 2026-10-07·"
                        u"CEO 一句话可翻）／⑨底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"FluxGroup/docs/decisions.md 集团外审批 D-20260930-01→41 正行集（09-30 单日 40 决·"
                           u"D-06 令源/D-05 修复单/D-25 收口·五勘正/D-26 六律/D-27+D-31 探针/D-37 方法论·"
                           u"跨仓只读·宿主机直读正典）+docs/self-improvement-queue.md §E E28 备货位行"
                           u"（R870 入池·E-pool 第五路=DIGEST 通道未消费存量候选）+src/os/backlog.md #67 R871 "
                           u"claim 行（P-51 送达链·断轮承接注记）——编年史 A 级史源（集团决策正典台账·"
                           u"charter §3 选题池多源）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=CEO 原话 verbatim 连续子串零改字〔D-20260930-06 正行原句零改字零重组·"
                             u"CEO 令全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（集团外审决策批台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=集团外审日数字盘点档案体（1 句 CEO 直令 vs 单日 40 决回应链="
                            u"「一句话 vs 一批决」母题·12 轮外审 vs 5 次自我勘正=「外部专家也会错、错了当场改」"
                            u"诚实机制叙事位·六律入章程=方法论沉淀位·否决窗 10-07=治理闭环悬念位·"
                            u"直评→风暴→清单→修复→立规→自省=「问题→清单→立法」递进链·"
                            u"v6 深夜决策批同型=决策批盘点先例承继；公众号低创作度条款 7.1-7.4 编辑价值面·"
                            u"charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句 CEO 直令「作为外部专家」 vs "
                          u"单日 40 决风暴批+12 轮外审 vs 5 次自我勘正+XL-21/RW-7/M-7/Q-9 四组清单数字"
                          u"——F-042 v2 对照数字结构同源第十一证·十一连母题〔v2 开闸/v3 三线/v4 技能/"
                          u"v5 节目重制/v6 对账夜/v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令/"
                          u"v10 云端 token 机制日/v11 产品优先令日/v12 集团外审日〕+40/12/21/7/9/5/10-07 七组数字/"
                          u"情 1 AI 自治问责吃瓜温和如实非强极点〔G5 吃瓜未来党+G3 技能学习党双群对位·"
                          u"外部专家全团体检+外审自纠 5 次+六律反推=AI 公司自我治理叙事面〕/"
                          u"时 2 事件 2026-09-30→本卡 2026-10-01 一日跨度+台账档案常青〔决策批盘点=v6 当日时点先例〕/"
                          u"时序链=CEO 令 09-30→12 轮外审→单日 40 决→六律入册→本卡 R871）/"
                          u"台 2 公众号方图承载=MC-001~082 S3 实证复用·盘点=公众号主流图文格式"
                          u"〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                          u"#67 触发律=编年史事件随轮领〔R871 claim·E28=R870 queue §E 备货位领做非造活凑数〕")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为治理台账读数"
                     u"（决策计数/清单编号/轮次/否决窗日期=非 token 用量非财务非持仓面·v10 206/98%、"
                     u"v11 10,524 commit 同型分界）入卡面；CEO 指令原文 verbatim 纪实照录"
                     u"（批评面照录禁软化禁重组）；P1 边界=本件=纪实档案非提案非表决"
                     u"（外审执行面细节=他司份额不入卡面·BigMoney RW/量化细目=批级知悉位）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十二件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r871.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V12, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V12, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
