# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v1 build: DAILY (city daily-sign) series FIRST piece (R970, backlog #97
new-line claim). Form chartered in city-storylines-charter v1.2 S1/S4 (form code DAILY=
city daily sign; source law=lines pool cognition/pools.json + pool-level attribution; R289
in-case proposal anchor). Lane blind-spot correction of R810 five-face supply inventory
(same class as R870 DIGEST channel reopen: unconsumed stock missed by closure verdict).
Day context 2026-10-02 = National Day holiday day 2 -> festival bucket direct match
(REACT-v8 same-day precedent). Quote = qiuxin/festival/4 pool line verbatim + card framing
(R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim (zero-new-template law). Em budget
ladder + zero-margin exclusion (R293) + vertical stack law (R381) + machine source/dedup
assertions (R456 system). All output UTF-8.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V1 = os.path.join(BASE, "MC-20261002-DAILY-v1")
TMP = V1 + "-tmp"
os.makedirs(V1, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"直播间的观众都说，我家的灯笼最独特"
AXIS, BUCKET, IDX = u"求新", u"festival", 4

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        assert QUOTE_CORE not in io.open(cj, encoding="utf-8").read(), "line already consumed by %s" % d
# consumed-by-REACT-v8 festival lines (same bucket, different indices - documented not asserted):
# xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (MC-20261002-REACT-v8 source_facts)

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 001",
    u"2026-10-02 · 国庆假期",
    u"「直播间的观众都说，",
    u"我家的灯笼最独特。」",
    u"——硅基城市台词池 · 求新轴",
]

SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]  # QUOTE-v2 own size 60 first = zero-template change
MARGIN_EM = 0.2  # zero-margin exclusion law (R293)

H1_GAP = int(cfg["font"]["h1_gap"])
OPT_C = float(cfg["font"]["optical_center"])
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])
PITCH_F = 1.35
GAP_MIN = 20


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
meta["topic"] = "MC-20261002-DAILY-v1"
meta["form"] = (u"DAILY 城市日签 001（L-卡 图文轻内容线 DAILY 形态立线首件·charter v1.2 §4 形态码 DAILY·"
                u"#97 新线 claim R970·供给盲区修正轮=R810 五面盘点遗漏 DAILY 通道重开首件〔R870 DIGEST 通道"
                u"重开同型：R289 提案在案「日签变体=语录卡线随时可续」+charter §1 素材法=台词池+池级署名在册·"
                u"零件产出=未消费存量面·非造活凑数〕）")
meta["source_quote"] = u"「直播间的观众都说，我家的灯笼最独特。」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[求新][festival][4]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite=1440 行·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期=REACT-v8 F-085 当日件同窗国庆语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[求新][festival][4] verbatim 零改字（「」与句号="
                         u"卡面排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02="
                         u"当日历法事实·国庆假期=国庆节次日假期第 2 天（daily brief 2026-10-02 当日窗语境="
                         u"REACT-v8 F-085 国庆网红猫同窗印证）③情境=festival 情境桶当日直配（12 桶中节日情境"
                         u"与当日唯一对位·R909 REACT-v8 festival 首用同窗第二消费）④池级署名=台词池行无居民名"
                         u"〔人设权红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 38 条已采面+"
                         u"不在全成品 cards.json 任一 source_facts（build 脚本 fleet 级扫描实锚·REACT-v8 同桶三行"
                         u"〔逍遥/17+烟火/12+秩序/14〕皆非本行）")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·求新轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配=日期×情境对位"
                            u"判据·求新轴候选质量选优=「直播间×灯笼」金句位·R909 REACT-v8 桶对位判据同型）+"
                            u"最老手艺×最新媒介=城市古今融汇叙事位（R-2026-09-28-09 融汇设计令「合理不突兀」"
                            u"对位=直播间晒灯笼=合理不突兀的融汇示范·M1 入城因果律）+语录卡线变体=零新模板"
                            u"（QUOTE v2 参数 verbatim 复用·charter §1「日签变体随时可续」兑现）·公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：最老手艺（灯笼）×最新媒介（直播间）="
                          u"古今融汇反差金句位+「我家的灯笼最独特」=第一人称匠人自豪=具体稀缺性/情 1 求新乐观"
                          u"与匠人自豪温和共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日+festival 情境桶直配"
                          u"+池句常青/台 2 公众号方图承载=MC-001~085 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·charter §4 形态码 DAILY·#97 新线 R970 claim")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触；脱敏律=池句无令牌号/无个体可识别面；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态首件·charter v1.2 §4 形态码 DAILY·台词池日签节律首件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[festival][4] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit + all cards.json)" )
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
report.append(u"H1 %d budget %.2fem | H2 %d budget %.2fem (ladder pick, margin>=%.1fem) | VERT stack bottom %.0fpx vs subs top %dpx gap %+.0fpx (need >=%d) R381" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM, vb, SUBS_TOP, SUBS_TOP - vb, GAP_MIN))
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
io.open(os.path.join(TMP, "em-check-r970.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V1, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V1, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d (QUOTE-v2 param match=%s)" % (H2_SIZE, H2_SIZE == 60))
