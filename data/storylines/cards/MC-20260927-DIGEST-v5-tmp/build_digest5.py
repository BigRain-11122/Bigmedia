# -*- coding: utf-8 -*-
"""MC-20260927-DIGEST-v5 build: DIGEST series 5th piece (R460, backlog #67 chronicle-event claim).
Program-remake day (P-20260926-11, 2026-09-26 ~20:1x) chronicle digest: CEO one-line verdict
verbatim quote (program quality "not good" -> unify+plain-language) + 4-dim self-review +
2 laws legislated (plain-language L18-L20 + series-template S5.5) + 4 episodes full-chain
remake (R445-R454, F-001~F-004 v15) + S1 gate 9/10+10/10x3 + E4 audience 8.0x4 band-top
+ 297 regression green. All facts from group ledger P-20260926-11 row / backlog #71 /
program-quality-audit / copy-craft v1.4 + visual-spec v1.2 / finished.md + review files
(A-grade chronicle, one-source-multi-use charter S3).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v4 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V4 = os.path.join(BASE, "MC-20260926-DIGEST-v4")
V5 = os.path.join(BASE, "MC-20260927-DIGEST-v5")
TMP = V5 + "-tmp"
os.makedirs(V5, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V4, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 005",
    u"节目重制日 2026-09-26 · 次日收官",
    u"「可视化表现要注意页面统一和措辞简单易懂，",
    u"现在媒体公司的节目做的很不好，统一优化」",
    u"直评 1 句 · 自审 4 维 · 立制 2 律",
    u"重制 4 件节目 · 全链走门收官",
    u"S1 门三连满分 · 参考线 8.0×4 持平顶",
    u"机检新引擎 · 297 项测试全绿",
]

SUBS_LINE = u"基于硅基城市真实事件（节目重制令台账档案）"

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
meta["topic"] = "MC-20260927-DIGEST-v5"
meta["form"] = (u"DIGEST 盘点图文 005（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第四件·"
                u"R459 指针=编年史事件候选领做·史源=P-20260926-11 节目质量整改令）")
meta["source_facts"] = (u"节目重制日数字盘点八条：质量整改令日 2026-09-26 晚 ~20:1X／"
                        u"CEO 原话一句「可视化表现要注意页面统一和措辞简单易懂，现在媒体公司的节目做的很不好，统一优化」verbatim／"
                        u"集团转办 P-20260926-11 P1 @BigStream 节目整改批（先自审→措辞简单易懂律→页面模板统一→重制最新节目呈 CEO 目检·"
                        u"三证判据=统一性+易懂性+节目质量）／"
                        u"自审 4 维=docs/audits/2026-09-26-program-quality-audit.md（R442 叙事/画面/节奏/措辞四维诚实记录·CEO 直评定为主判输入）／"
                        u"立制 2 律=copy-craft v1.4 §2.8 措辞简单易懂律 L18-L20+visual-spec v1.2 §5.5 系列模板统一律"
                        u"（含机检引擎 src/plain_language_check.py+词表 12 词交付 R443）／"
                        u"重制 4 件=F-001~F-004 v15 系（R445 渲染器工程位→R446-R454 逐件两律重制·S1 新旗面拍稿重走→TTS→对位→"
                        u"渲染〔系列角标+集数+§4.5 三开关〕→S2 三门→E8→M4→SUPERSEDED 更账·2026-09-27 收官）／"
                        u"门禁读数=S1 v1.5 门 F-001 9/10+F-002/003/004 10/10 三连满分+E4 参考仪四件全 8.0 重制带持平顶收官+297 全回归绿（R451 终值）／"
                        u"三证判据批次闭环·CEO 目检呈报毕（backlog #71 done 2026-09-27）")
meta["source_pointer"] = (u"cph4/evolution-ledger.md P-20260926-11 行（集团转办正行·CEO 原话 ~20:1X verbatim+三证判据·跨仓只读）"
                          u"+src/os/backlog.md #71（本司份额收讫 ack+R442 自审→R443 立法→R445 工程位→R446-R454 重制链全注记·"
                          u"P-51 送达判据 commit 含令号 10 件）"
                          u"+docs/audits/2026-09-26-program-quality-audit.md（R442 四维自审正件）"
                          u"+docs/copy-craft.md v1.4 §2.8+docs/visual-spec.md v1.2 §5.5（两律正典）"
                          u"+output/finished.md F-001~F-004 v15 行+docs/reviews/review-20260927-bs001~004v15-v1.md ×4（S1/E8/E4 读数）——"
                          u"编年史 A 级史源（集团令件正行+本司台账+审计件+正典+评审单·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；CEO 原话=令件台账正行 verbatim 引文）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（节目重制令台账档案）」；"
                        u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=节目重制日数字盘点档案体（数字对照结构+时间锚 2026-09-26 令→2026-09-27 收官+盘点体裁）——"
                           u"选材与排序即编辑动作（1 句直评→4 维自审→2 律立制→4 件重制→门禁读数收官=质量整改事件递进链·"
                           u"公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句直评「节目做的很不好」vs 两日内 4 件节目全链重制收官"
                        u"〔最短直评×当夜整改=F-042 v2「1 句话 vs 7 决」对照数字结构同源第四证·v2 开闸/v3 三线/v4 技能/v5 节目重制=四连母题〕"
                        u"+直评 1 句/自审 4 维/立制 2 律/重制 4 件四组数字+三连满分与 8.0×4 持平顶收官读数对照/情 1 AI 自治整改吃瓜温和共鸣如实非强极点"
                        u"〔G5 吃瓜未来党+G1 AI 效率实操党双群对位〕/时 2 令 2026-09-26 晚→收官 2026-09-27 凌晨两日时点+台账档案常青面如实/台 2 公众号方图承载="
                        u"MC-001~045 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·"
                        u"D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=八条数字全为已过 M4 在册件口径"
                    u"（集团令行/本司台账/审计件/正典/评审单）·零仓位/密钥/token 量/未公开财务面；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第五件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r460.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V5, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V5, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
