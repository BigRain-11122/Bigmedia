# -*- coding: utf-8 -*-
"""MC-20260926-DIGEST-v2 build: DIGEST series 2nd piece (R380, backlog #67 chronicle-event claim).
Mass-production gate opening (D-BS-06, 2026-09-24) chronicle digest: CEO one-line order
verbatim quote + same-night seven decisions + N=6 stock unseal + 7-day veto window +
first-night five finished pieces + zero-question reporting protocol. All facts from
orders/decisions/finished ledgers (A-grade chronicle, one-source-multi-use charter S3).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310 precedent, margin>=0.2em).
Template = DIGEST v1 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V1 = os.path.join(BASE, "MC-20260925-DIGEST-v1")
V2 = os.path.join(BASE, "MC-20260926-DIGEST-v2")
TMP = V2 + "-tmp"
os.makedirs(V2, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V1, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 002",
    u"量产开闸日 2026-09-24 · 晚 21:26",
    u"「要决策的自己科学决策，不要再问我了。」",
    u"老板 1 句话 · AI 当晚 7 决全落",
    u"6 件弹药解封 · 否决窗 7 天",
    u"开闸首夜 · 5 件成品入库",
    u"此后 0 问询 · 报告只报实况与已决",
]

SUBS_LINE = u"基于硅基城市真实事件（量产开闸台账档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2  # zero-margin exclusion law (em-budget-ladder hard law; R293 pixel-overlap lesson)


def all_fit(size):
    budget = (frame_w - 160) / float(size)
    for ln in LINES[1:]:
        if _line_cost(ln) > budget - MARGIN_EM or len(wrap_for_width(ln, size, frame_w).split("\n")) != 1:
            return False
    return True


H2_SIZE = next(s for s in LADDER if all_fit(s))

meta = cfg["meta"]
meta["topic"] = "MC-20260926-DIGEST-v2"
meta["form"] = (u"DIGEST 盘点图文 002（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件首件·"
                u"R379 研究件 §5 选题池配置建议落地=DIGEST 续件=供给门等待期产能首选候选〔唯一 E4 9.0 峰形态+零供给门+史源在册〕）")
meta["source_facts"] = (u"量产开闸数字盘点六条：量产开闸日 2026-09-24 晚 21:26／CEO 原话一句「要决策的自己科学决策，不要再问我了。」verbatim／"
                        u"AI 当晚 7 决全落（D-BS-01 拣式/02 BGM/03 视觉/04 slug/05 节奏/06 量产开闸/07 人设）／N=6 存量弹药解封／"
                        u"否决窗一律 7 天至 2026-10-01／开闸首夜 5 件成品全链走门入库（F-001~F-005）／"
                        u"此后 0 问询（呈报口径=实况+已决事项知悉面·不再出现问询句）")
meta["source_pointer"] = (u"orders/O-20260924-2126-bm-a.md（CEO 委托决策令正件·原话与时间戳 21:26 verbatim+呈报口径变更节）"
                          u"+docs/decisions.md v1.0（七决台账 D-BS-01~07+变更记录「七决全落」+否决窗一律至 2026-10-01）"
                          u"+src/os/iteration_prompt.txt 生产段（N=6 存量弹药解封·O-2126 任务书热改正源）"
                          u"+output/finished.md（F-001 2026-09-24 R170／F-002 09-24 R174／F-003 09-25 R180／F-004 09-25 R187／"
                          u"F-005 09-25 05:3x R200·五件全链走门毕注记）——编年史 A 级史源（集团 git 史+令牌台账+城市事件流·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；CEO 原话=令牌台账正件 verbatim 引文）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（量产开闸台账档案）」；"
                        u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=量产开闸数字盘点档案体（数字对照结构+时间锚 2026-09-24 21:26+盘点体裁）——选材与排序即编辑动作"
                           u"（1 句话→7 决→6 弹药→首夜 5 件→0 问询=委托决策事件递进链·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句话 vs 当晚 7 决〔最短指令×最长决策清单=已验爆款母题·F-019 立国日 17 分钟对照数字结构同源〕"
                        u"+6 件弹药+7 天否决窗 vs 此后 0 问询〔授权三组数字反差前置〕/情 1 AI 自治吃瓜温和共鸣如实非强极点〔G5 吃瓜未来党+G1 AI 效率实操党双群对位〕"
                        u"/时 2 量产开闸 2 日时点+决策台账档案常青面如实/台 2 公众号方图承载=MC-001~041 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
                        u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=六条数字全为已过 M4 在册件口径（令件/决策台账/任务书/成品库）·"
                    u"零仓位/密钥/token 量/未公开财务面；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第二件·charter v1.2 §4 形态码·R379 研究件 §5 首选候选）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R313 precedent, renderer truth, assert-in-build, zero-margin exclusion) ---
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append(u"H1 size %d budget %.2fem | H2 size %d budget %.2fem (ladder pick, zero-margin exclusion margin>=%.1fem)" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM))
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
io.open(os.path.join(TMP, "em-check-r380.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V2, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V2, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
