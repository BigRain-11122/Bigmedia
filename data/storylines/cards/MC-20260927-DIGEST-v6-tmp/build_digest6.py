# -*- coding: utf-8 -*-
"""MC-20260927-DIGEST-v6 build: DIGEST series 6th piece (R461, backlog #67 chronicle-event claim).
Midnight decision-batch chronicle digest (D-20260927-01~05, 2026-09-27 00:05): five decisions
in one batch + 10-point adjudication + zero rejections; headline story = skill-mobilization
count corrected 5/8 (batch D-01-7) -> 6/8 (own-ledger correction row F-20260927-01, 9 evidence
items via P-51 dual-carrier union); own share 2/5 (D-01 correction receipt + D-05-2 orders
full-file scan script r444_check.py); decisions ledger 45 non-empty rows; D-03 OSS ledger-slot
ruling cites 3-company write practice (FluxVerse/BigLife/BigStream OH files). All facts from
group decisions.md D-20260927-01~05 rows / HQ-FEEDBACK F-20260927-01 / state.json R444 log /
r444_check.py / OH-20260926-bigstream.md (A-grade chronicle, one-source-multi-use charter S3).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v5 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V5 = os.path.join(BASE, "MC-20260927-DIGEST-v5")
V6 = os.path.join(BASE, "MC-20260927-DIGEST-v6")
TMP = V6 + "-tmp"
os.makedirs(V6, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V5, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 006",
    u"深夜决策批 2026-09-27 00:05 落档",
    u"「技能动员令计数修正 5/8」",
    u"「技能动员令计数应 6/8」",
    u"决策 5 连落 · 拍板 10 点 · 驳回 0 条",
    u"本司份额 2/5 · 扫面脚本 1 件落账",
    u"夜轮点名后翻台账 · 自证证据 9 件",
    u"开源借力台账位裁定 · 三司实践在案",
]

SUBS_LINE = u"基于硅基城市真实事件（决策批台账档案）"

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
GAP_MIN = 20     # px clearance to subs band (v3 measured 32px at h2=40 / 7 rows)


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
meta["topic"] = "MC-20260927-DIGEST-v6"
meta["form"] = (u"DIGEST 盘点图文 006（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第五件·"
                u"R460 指针=编年史事件候选领做·史源=D-20260927-01~05 深夜决策批）")
meta["source_facts"] = (u"深夜决策批数字盘点八条：决策批落档 2026-09-27 00:05（decisions.md D-20260927-01~05 五行新落·"
                        u"R444 收讫窗内回执）／五决连落=D-01 回执核销批 5+台账勘正·D-02 BigCompute 午班加轮+OrderSentinel·"
                        u"D-03 BigDomain OSS 台账位三选一·D-04 复审锚热票面禁令·D-05 台账可见性与写入卫生包（他司执行面=批级知悉位·细节不入卡面）／"
                        u"D-01 拍板十点①~⑩（⑦ 技能动员令计数修正 5/8 verbatim·余 BigStream 窗 00:35 到点→夜轮点名）／"
                        u"本司自证计数应 6/8=HQ-FEEDBACK F-20260927-01 更正行（P-51 双载体并集核验·commit 57dfce5/bfca664 消息含 "
                        u"P-20260926-01+state.json×5 处+finished.md×1 处+backlog #65 done 行=证据 9 件）／"
                        u"五决科学判断闸全过审零驳回（R444 回执·D-01 引证列「昨日 overruled=0·台账全扫零驳回行」）／"
                        u"本司份额 2/5=D-01⑦ 计数勘正回执+D-05② orders 全文件扫面自评采纳（编辑检测线落件 r444_check.py）／"
                        u"决策台账 45 行在册（decisions.md 非空行·r461_check.py 本轮实测）／"
                        u"D-03 OSS 台账位裁定采③豁免精确口径（FluxVerse/BigLife/BigStream 三司 OH-20260926-*.md 实体写盘实践在案·"
                        u"本司 OH 件=首窗三切片 R432/R458/R459）")
meta["source_pointer"] = (u"FluxGroup/docs/decisions.md D-20260927-01~05 五行（集团决策正典·A 级跨仓只读）"
                           u"+HQ-FEEDBACK.md F-20260927-01 行（本司计数更正载体·证据 9 件链）"
                           u"+src/os/state.json R444 log 行（五决回执·科学判断闸零驳回）"
                           u"+.c3-tmp/r444_check.py（D-05② orders 全文件扫面自评落件）"
                           u"+cph4/oss-harvest/OH-20260926-bigstream.md（D-03 证据件·三司实践在案）——"
                           u"编年史 A 级史源（集团决策正典+本司台账+工具件·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                            u"引文=集团决策正典行 D-20260927-01⑦+本司台账行 F-20260927-01 verbatim 双源对读）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（决策批台账档案）」；"
                        u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=深夜决策批数字盘点档案体（数字对照结构+时间锚 00:05 落批+盘点体裁）——"
                           u"选材与排序即编辑动作（5/8→6/8 计数对账故事=批内点名×台账自证的诚实对账链·"
                           u"公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：总部批内计数 5/8 vs 本仓台账核验 6/8——"
                        u"同一夜「点名」×「翻台账自证证据 9 件」=F-042 v2 对照数字结构同源第五证·五连母题"
                        u"〔v2 开闸/v3 三线/v4 技能/v5 节目重制/v6 对账夜〕+00:05 深夜落批幕后纪实/"
                        u"情 1 机器诚实对账温和共鸣如实非强极点〔G1 AI 效率实操党+G5 吃瓜未来党双群对位〕/"
                        u"时 2 事件 2026-09-27 00:05 当日+台账档案常青面如实/"
                        u"台 2 公众号方图承载=MC-001~046 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
                        u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=八条数字全为已过 M4 在册件口径"
                    u"（集团决策正典行/本司台账/工具件）·零仓位/密钥/token 量/未公开财务面·"
                    u"他司执行面细节不入卡面（D-02/D-04 仅批级知悉位）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第六件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r461.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V6, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V6, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
