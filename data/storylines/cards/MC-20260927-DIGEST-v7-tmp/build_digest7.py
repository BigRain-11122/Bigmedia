# -*- coding: utf-8 -*-
"""MC-20260927-DIGEST-v7 build: DIGEST series 7th piece (R517, backlog #67 chronicle-event claim).
Commercialization paypoint-design day chronicle digest (P-2026-09-27-02, 2026-09-27 ~08:0x):
one CEO line -> same-day 19-paypoint matrix + four-layer price architecture + committee batch
C-20260927-01 registered same day (N1-N7 adoption + N2 resident-growth-archive subscription
design value 9.9/month + 29.9-vs-49.9 entry-tier choice pending CEO) + external anchor wave
31 sources (AI-companion normative band 20-39/month) + own share leg-3 narrative mapping
delivered same morning (R487). All facts from group ledger L141 / master doc
R-20260927-commercial-paypoints / decisions.md C-20260927-01 / own mapping doc /
HQ-FEEDBACK F-20260927-04 (A-grade chronicle, one-source-multi-use charter S3).
Desensitization law: zero margin/cost/electricity/token/unpublished-finance faces; all price
figures cited as in-canon DESIGN VALUES pending adjudication, never live prices.
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v6 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V6 = os.path.join(BASE, "MC-20260927-DIGEST-v6")
V7 = os.path.join(BASE, "MC-20260927-DIGEST-v7")
TMP = V7 + "-tmp"
os.makedirs(V7, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V6, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 007",
    u"商业化定价日 2026-09-27 落账",
    u"「合理的付费点，还有包装价格」",
    u"一句令 · 当日 19 付费点全对表",
    u"定价四层 · 29.9 与 49.9 二选一待裁",
    u"居民档案订阅 9.9 元/月设计值",
    u"外部锚 31 源 · 陪伴常态带 20-39 元",
    u"过会件当日落档 · 7 席 48 小时记票",
]

SUBS_LINE = u"基于硅基城市真实事件（商业化定价令台账档案）"

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
meta["topic"] = "MC-20260927-DIGEST-v7"
meta["form"] = (u"DIGEST 盘点图文 007（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第六件·"
                u"#67 触发律=ledger 新 CEO 令级事件落账随轮领·史源=P-2026-09-27-02 商业化付费点与定价包装体系设计令）")
meta["source_facts"] = (u"商业化定价日数字盘点八条：CEO 令 2026-09-27 ~08:0x 落账（原话 verbatim 全句「商业化公司，全面了解现在的业务架构，"
                        u"挖掘与现实之间。合理的付费点，还有包装价格什么之类的。在合法的框架范围内。」·ledger P-2026-09-27-02·orders O-2026-0927-10）／"
                        u"付费点矩阵 19 项=在册 12+新挖 7（主件 §三·N1-N7 逐点标合规闸·纯 LBS 城市玩法充值判负留痕=一起来捉妖停运先例）／"
                        u"四层价格架构=钩子抽取 2-9.9 元·主力 19.9 元·订阅 29.9（建议新增入门档·待 CEO 裁）/49.9/99 元·身份与 B 端 199-19,800 元"
                        u"（主件 §四·一律设计值口径非上架价）／委员会过会件 C-20260927-01 当日落档（decisions.md 委员会节登记首件：N1-N7 采纳面与采纳序"
                        u"〔BigDomain 提案建议 N2 P1 先行〕+N2 居民成长档案订阅定价档设计值 9.9 元/月+29.9 入门订阅档二选一〔A 降价拉客 vs B 维持 49.9 起"
                        u"溢价叙事〕·七席意见窗 48 小时至 2026-09-29 12:00·普通过 ≥4/7·票档下轮决策轮归档·过会前各司零执行）／"
                        u"外部锚点波 31 源（姊妹件 web：AI 陪伴订阅常态带 20-39 元/月·现设 49.9-99 高出常态带 1.3-2.5×·星野 20 元/月+2 元/抽新华网原文坐实·"
                        u"妙鸭 9.9/套 4000 人排队锚）／本司轮办③包装叙事线当晨交付=付费点×内容选题映射 v1.0（19 点全对表·价值锚逐行引主件原文零改写·"
                        u"《你的 19.9 去哪了》首件付费点叙事选题候选入池·R487）／轮办四司分工=BigCompute 定价执行与出口统辖·BigDomain 价目正典增补·"
                        u"BigStream 包装叙事线·决策委员会商业席位过会输入件（ledger P-02 轮办节原文）／合规闸映射=包装规范全商品通用（AIGC 显著标识="
                        u"标识办法第四条(五)虚拟场景起始画面标识正中条款 A 级+虚拟商品三声明+非投顾提示+未成年人保护+盲盒指引叠加+陪伴类服务连续性条款前置·"
                        u"主件 §四/§五）")
meta["source_pointer"] = (u"cph4/evolution-ledger.md P-2026-09-27-02 行（CEO 原话 verbatim+轮办四司·集团进化台账 A 级跨仓只读）"
                           u"+cph4/research/R-20260927-commercial-paypoints.md（集团主件 §一-§六：架构全景+付费点矩阵+四层定价+合规闸·跨仓只读）"
                           u"+FluxGroup/docs/decisions.md C-20260927-01 行（委员会过会件·集团决策正典跨仓只读）"
                           u"+docs/research/R-20260927-bigstream-02-paypoint-narrative-mapping.md（本司轮办③件·R487）"
                           u"+HQ-FEEDBACK.md F-20260927-04 行（本司回执载体行）+src/os/backlog.md #75 done 行——"
                           u"编年史 A 级史源（集团台账+集团主件+集团决策正典+本司台账·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=CEO 令原话 ledger P-2026-09-27-02 verbatim 子串〔「合理的付费点，还有包装价格」=原句零改字零重组〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（商业化定价令台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=商业化定价日数字盘点档案体（1 句令→当日全链=对照数字结构+当日时间锚+盘点体裁——"
                            u"选材与排序即编辑动作（合法框架句=CEO 合规意识金句位·全文 verbatim 入 source_facts 引文块；"
                            u"29.9 与 49.9 二选一待裁=留悬念收束位·过会前零执行如实口径；公众号低创作度条款 7.1-7.4 编辑价值面·"
                            u"charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句商业化令 vs 当日 19 付费点矩阵+四层定价+过会件当日落档——"
                         u"F-042 v2 对照数字结构同源第六证·六连母题〔v2 开闸/v3 三线/v4 技能/v5 节目重制/v6 对账夜/v7 商业化定价日〕"
                         u"+29.9 与 49.9 二选一待裁悬念位/"
                         u"情 1 商业化解锁期待温和吃瓜如实非强极点〔G2 超级个体野心家+G5 吃瓜未来党双群对位〕/"
                         u"时 2 事件 2026-09-27 当日〔令 ~08:0x→当日过会登记·意见窗 48 小时至 09-29 12:00〕/"
                         u"台 2 公众号方图承载=MC-001~047 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
                         u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                         u"#67 触发律=ledger 新 CEO 令级事件落账时随轮领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=零毛利/成本/电费/token 量/未公开财务面"
                     u"（卡面定价数字=集团正典在册设计值口径〔C-20260927-01+主件 §四〕·一律标设计值/待裁非上架价）；"
                     u"P1 边界=商业化执行面零触碰（定价出口=BigCompute·价目正典=BigDomain·过会=决策委员会商业席位·"
                     u"过会前各司零执行·本件=纪实档案非提案执行·本司提案面零代签）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第七件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r517.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V7, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V7, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
