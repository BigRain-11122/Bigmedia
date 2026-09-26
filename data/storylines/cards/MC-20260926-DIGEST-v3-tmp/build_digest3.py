# -*- coding: utf-8 -*-
"""MC-20260926-DIGEST-v3 build: DIGEST series 3rd piece (R381, backlog #67 chronicle-event claim).
Three-line expansion day (O-20260925-0850, 2026-09-25 ~08:50) chronicle digest: CEO one-line
order verbatim quote (audio-novel/web-novel/comic lines + Silicon City everything + research
first) + same-morning 09:1X receipt (research+charter+first chapter all closed in one batch)
+ 3 content lines + mass source library (10k census / 14 factions / 1200+ quote pool)
+ first chapter ~1100 chars + 4-panel comic PoC. All facts from orders/research/charter/novel
in-repo ledgers (A-grade chronicle, one-source-multi-use charter S3).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310 precedent, margin>=0.2em).
Template = DIGEST v2 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V2 = os.path.join(BASE, "MC-20260926-DIGEST-v2")
V3 = os.path.join(BASE, "MC-20260926-DIGEST-v3")
TMP = V3 + "-tmp"
os.makedirs(V3, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 003",
    u"三线扩展日 2026-09-25 · 晨 08:50",
    u"「创建有声小说，网文，漫画等一系列条线，",
    u"主打硅基城市里面发生的一切，",
    u"你们先调研，然后开始」",
    u"老板 1 句话 · 当天 3 条线立制开工",
    u"素材：万人库 · 14 派系 · 台词池 1200+",
    u"首章《立国日》约 1100 字 · 漫画首话四格",
]

SUBS_LINE = u"基于硅基城市真实事件（三线扩展令台账档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2  # zero-margin exclusion law (em-budget-ladder hard law; R293 pixel-overlap lesson)

# --- vertical stack budget (R381 new hard law: em check covers horizontal only;
# v3 7-line deck at h2=44 pushed stack bottom to y~991 vs subs top y=970 = 21px overlap,
# caught by verify-5-check. Model from measured v2/v3 bands: pitch = 1.318*size + ls,
# H2_h = size + (n-1)*pitch; h2 block bottom = h*optical_center + h1_gap + 1.5*H2_h.)
H1_GAP = int(cfg["font"]["h1_gap"])          # 36
OPT_C = float(cfg["font"]["optical_center"])  # 0.24
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])  # y=970
PITCH_F = 1.35   # conservative vs measured 1.318
GAP_MIN = 20     # px clearance to subs band (v2 empirical 86px, v3 overlap -21px)


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
meta["topic"] = "MC-20260926-DIGEST-v3"
meta["form"] = (u"DIGEST 盘点图文 003（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第二件·"
                u"R380 focus 候选序首位=三线扩展 O-20260925-0850·R379 研究件 §5 首选候选随轮领做）")
meta["source_facts"] = (u"三线扩展日数字盘点八条：三线扩展令日 2026-09-25 晨 08:50／"
                        u"CEO 原话一句「创建有声小说，网文，漫画等一系列条线，主打硅基城市里面发生的一切，你们先调研，然后开始」verbatim／"
                        u"同晨 09:1X 回执「调研+开工同批闭环」（调研件 v1.0+立制件 charter v1.0+首章开工三件全落）／"
                        u"3 条内容线（有声小说/网文/漫画）+「等一系列」架构可扩容位／"
                        u"题材主权=硅基城市（超体宇宙城 FluxVerse）里发生的一切／"
                        u"素材面=BigLife 万人库/思想六轴/14 派系/年轮/台词池 1200+/情绪日历/谣言链／"
                        u"网文首章《硅基城市·第一章·立国日》约 1100 字（纪实线·真实编年史改编）／"
                        u"漫画首话 PoC 单图整话四格（SC-002-01）")
meta["source_pointer"] = (u"orders/O-20260925-0850-bm-a.md（CEO 内容宇宙令正件·原话与时间戳 08:50 verbatim+执行回执 09:1X"
                          u"「调研+开工同批闭环」节）+research/city-storylines-research-v1.md v1.0（素材面 A 级盘点：万人库/思想六轴/"
                          u"14 派系/年轮/台词池 1200+/情绪日历/谣言链·全带只读指针）+docs/city-storylines-charter.md v1.0"
                          u"（立制件·三线编制+虚实边界律+人设权红线）+data/storylines/novel/SC-001-01-v1.md"
                          u"（首章《立国日》约 1100 字·纪实线·来源清单七条全可溯）+data/storylines/comic/SC-002-01-v1.png"
                          u"（漫画首话四格 PoC·1440×2893）——编年史 A 级史源（令件正典+调研件+立制件+正文文件·charter §3 选题池双源①）·"
                          u"一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；CEO 原话=令牌台账正件 verbatim 引文）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（三线扩展令台账档案）」；"
                        u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=三线扩展日数字盘点档案体（数字对照结构+时间锚 2026-09-25 08:50+盘点体裁）——选材与排序即编辑动作"
                           u"（1 句话→3 条线→万人素材库→首章 1100 字→漫画四格=内容宇宙扩展事件递进链·公众号低创作度条款 7.1-7.4 编辑价值面·"
                           u"charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句话 vs 当天 3 条线立制开工〔最短指令×整个内容宇宙="
                        u"已验爆款母题·F-042 v2 1 句话 vs 7 决对照数字结构同源第二证〕+万人库/14 派系/台词池 1200+ 素材纵深三组数字反差前置"
                        u"+首章 1100 字/漫画四格产出对照/情 1 IP 宇宙扩展期待吃瓜温和共鸣如实非强极点〔G5 吃瓜未来党+G2 超级个体野心家双群对位〕"
                        u"/时 2 三线扩展 1 日时点+令件档案常青面如实/台 2 公众号方图承载=MC-001~042 S3 实证复用·盘点=公众号主流图文格式"
                        u"〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                        u"R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=八条数字全为已过 M4 在册件口径（令件/调研件/立制件/正文文件）·"
                    u"零仓位/密钥/token 量/未公开财务面；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第三件·charter v1.2 §4 形态码·R379 研究件 §5 首选候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent, renderer truth, assert-in-build, zero-margin exclusion) ---
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
io.open(os.path.join(TMP, "em-check-r381.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V3, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V3, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
