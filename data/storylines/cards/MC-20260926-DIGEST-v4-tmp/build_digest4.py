# -*- coding: utf-8 -*-
"""MC-20260926-DIGEST-v4 build: DIGEST series 4th piece (R382, backlog #67 chronicle-event claim).
Skill mobilization day (P-20260926-01, 2026-09-26 ~00:35) chronicle digest: CEO one-line
order verbatim quote (find+build+use business-fit skills) + inventory 3 built-in session
skills + 2 self-built production skills (lcard pipeline + s2 probes) + 5-step build
(init/edit/package/install/register) + 48h fast-track window (count 09-27 00:35).
All facts from group ledger L116 / backlog #65 / README skills section / capabilities C-32
(A-grade chronicle, one-source-multi-use charter S3).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v3 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V3 = os.path.join(BASE, "MC-20260926-DIGEST-v3")
V4 = os.path.join(BASE, "MC-20260926-DIGEST-v4")
TMP = V4 + "-tmp"
os.makedirs(V4, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V3, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 004",
    u"技能动员日 2026-09-26 · 凌晨 00:35",
    u"「ceo 命令，全部去找适合业务的 skills",
    u"并使用，提升生产力」",
    u"盘点 3 件在役 · 自建 2 件入产线",
    u"建装 5 步 · 校验安装双 PASS",
    u"技能 1=四形态全链 · 技能 2=机检三门",
    u"快速件窗 48 小时 · 计数 09-27 00:35",
]

SUBS_LINE = u"基于硅基城市真实事件（技能动员令台账档案）"

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
meta["topic"] = "MC-20260926-DIGEST-v4"
meta["form"] = (u"DIGEST 盘点图文 004（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第三件·"
                u"R381 focus 候选=技能动员 2026-09-26 research §5 在册随轮领做）")
meta["source_facts"] = (u"技能动员日数字盘点七条：技能动员令日 2026-09-26 凌晨 00:35／"
                        u"CEO 原话一句「ceo 命令，全部去找适合业务的 skills 并使用，提升生产力」verbatim／"
                        u"集团技能动员令 P-20260926-01 T1 直派八线·快速件档 ≤48 小时（计数窗 09-27 00:35）／"
                        u"盘点=会话内置 3 件在役（codely-guide 平台 how-to/skill-creator 技能创建器/tuanjie-cli 团结引擎管理）+司内 tools/skills/ 此前零登记／"
                        u"自建 2 件入产线（bigstream-lcard-pipeline=L-卡四形态全链工艺+bigstream-s2-probes=S2 机检三门+验图采样面三律）／"
                        u"建装 5 步（skill-creator 官方范式 init→edit→package→install→登记·校验 PASS×2+安装成功×2）／"
                        u"capabilities C-32 新席（v1.33 live×27）+README 技能登记节首立（清单式回执）")
meta["source_pointer"] = (u"cph4/evolution-ledger.md L116（集团技能动员令正行·CEO 原话 00:35 verbatim+T1 直派八线+技能三问/技能律四条·跨仓只读）"
                          u"+src/os/backlog.md #65（本司份额收讫+R377 盘点+R378 建装交付注记·P-51 送达判据 commit 含令号）"
                          u"+README.md Skills 技能登记节（R378 首立·清单式回执=3 内置+2 自建）"
                          u"+docs/capabilities.md C-32（v1.33·live×27·skill-creator 五步建装双技能）——"
                          u"编年史 A 级史源（集团令件正行+本司台账+登记节+能力册·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；CEO 原话=令件台账正行 verbatim 引文）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（技能动员令台账档案）」；"
                        u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=技能动员日数字盘点档案体（数字对照结构+时间锚 2026-09-26 00:35+盘点体裁）——选材与排序即编辑动作"
                           u"（1 句话→3+2 件技能在册→5 步建装→48 小时窗=技能动员事件递进链·公众号低创作度条款 7.1-7.4 编辑价值面·"
                           u"charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：凌晨 00:35 一句令 vs 当轮 2 件自建技能入产线"
                        u"〔最短指令×当天产能到位=F-042 v2「1 句话 vs 7 决」对照数字结构同源第三证·v2 开闸/v3 三线/v4 技能=三连母题〕"
                        u"+3 件在役/2 件自建/5 步建装三组数字+48h 窗 vs 当轮交付提速对照/情 1 AI 自治技能进化吃瓜温和共鸣如实非强极点"
                        u"〔G5 吃瓜未来党+G3 科技硬核极客双群对位〕/时 2 技能动员 1 日时点+令件档案常青面如实/台 2 公众号方图承载="
                        u"MC-001~043 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·"
                        u"D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=七条数字全为已过 M4 在册件口径（集团令行/本司台账/登记节/能力册）·"
                    u"零仓位/密钥/token 量/未公开财务面；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第四件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r382.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V4, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V4, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
