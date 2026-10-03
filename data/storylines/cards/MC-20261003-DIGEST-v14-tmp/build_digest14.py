# -*- coding: utf-8 -*-
"""MC-20261003-DIGEST-v14 build: DIGEST series 14th piece (R1095, backlog #67 chronicle-event
direct trigger-law claim; E-pool DIGEST channel empty since R872 double-stock consumed, the
2026-10-02 group order batch never re-stocked = R677-type derive blind-spot correction round).
Event = 2026-10-02 group order batch: (a) committee case C-20261002-01 token three-face audit
continuation, CEO verbatim quote, same-window close 7/7 PASS, six clauses D1-D6, review 10-08;
(b) silicon-city problem audit order (CEO 10-01 ~23:5x), verdict thick-thin 3 + issue classes
P0x3/P1x4/P2x3 + Steam seven-title benchmark + ten first-tier laws + milestones 10-09/12-31;
(c) patrol dispatch+urge double rows (34h silent main-line receipt window <=10-05 + stale-read
FETCH-FAIL fix); (d) five CEO decision/urge rows dated 2026-10-02 in group orders.md
(00:37/13:39/16:49/21:38/23:38). Machine assertions: orders CEO-row count == 5, ledger
P-2026-10-02 rows == 4, CEO quote substring present verbatim. CEO verbatim quote split across
two lines at question-mark sentence boundary (v5/v12 comma-clause precedent, same genre).
Em budget ladder with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack budget law (R381).
Template = DIGEST v13 build script. All output UTF-8.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V13 = os.path.join(BASE, "MC-20261001-DIGEST-v13")
V14 = os.path.join(BASE, "MC-20261003-DIGEST-v14")
TMP = V14 + "-tmp"
os.makedirs(V14, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

HQ = os.path.join(ROOT, "..", "..")
# --- machine count / verbatim assertions (content-addressed, build-time hard gates)
orders_txt = io.open(os.path.join(HQ, "docs", "orders.md"), encoding="utf-8", errors="replace").read()
ceo_rows = [ln for ln in orders_txt.splitlines()
            if "2026-10-02" in ln and "[CEO" in ln]
assert len(ceo_rows) == 5, "orders.md 2026-10-02 CEO row count != 5: %d" % len(ceo_rows)

ledger_txt = io.open(os.path.join(HQ, "cph4", "evolution-ledger.md"), encoding="utf-8", errors="replace").read()
p_rows = sorted(set(re.findall(r"\bP-2026-10-02-\d{2}\b", ledger_txt)))
assert p_rows == ["P-2026-10-02-01", "P-2026-10-02-02", "P-2026-10-02-03", "P-2026-10-02-04"], \
    "ledger P-2026-10-02 rows != 01..04: %s" % p_rows

QUOTE = u"检查到底是什么在大量耗费token？委员会继续开展节省云端token，加强本地算力工作"
assert QUOTE in ledger_txt, "CEO quote verbatim substring not found in ledger P-2026-10-02-01 row"
for frag in [u"三厚三薄", u"一线十定律", u"P0×3", u"Steam 七作"]:
    assert frag in ledger_txt or frag in orders_txt, "audit fact fragment missing: %s" % frag
assert u"主产线静默 ~34h" in ledger_txt, "patrol 34h fact missing in ledger P-03 row"

cfg = json.load(io.open(os.path.join(V13, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 014",
    u"集团令批 2026-10-02（两审计令 · 5 行决策催办）",
    u"「检查到底是什么在大量耗费token？",
    u"委员会继续开展节省云端token，加强本地算力工作」",
    u"token 三面审计 7/7 通过 · 六款续执 · 回访 10-08",
    u"硅基城审计三厚三薄 · 问题分级 3+4+3 · 对标七作",
    u"一线十定律 · 里程碑 10-09 可逛切片 · 12-31 预研",
    u"巡检双单 34h 静默回执窗 10-05 · 假读治本标记",
]

SUBS_LINE = u"基于硅基城市真实事件（集团令批台账档案）"

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
meta["topic"] = "MC-20261003-DIGEST-v14"
meta["form"] = (u"DIGEST 盘点图文 014（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第十三件·"
                u"#67 触发律=编年史事件随轮领〔R1095 claim·直领=E-pool DIGEST 通道 R872 双出池后回空·"
                u"10-02 集团令批未随批再入池=R677 型 derive 盲区修正轮·触发律照守非造活凑数〕·"
                u"史源=cph4/evolution-ledger.md P-2026-10-02-01→04+orders.md 10-02 五行 CEO 决策/催办"
                u"〔CEO 原话 verbatim+委员会案 7/7+巡检双单〕）")
meta["source_facts"] = (u"集团令批数字盘点八条："
                        u"①「集团令批 2026-10-02（两审计令 · 5 行决策催办）」=cph4/evolution-ledger.md "
                        u"P-2026-10-02-01→04 正行集（跨仓只读·宿主机直读正典=本机即集团仓宿主机零 git 操作"
                        u"零写接触）+FluxGroup/docs/orders.md 2026-10-02 五行 CEO 决策/催办（00:37 FluxVerse "
                        u"CPU 解冻令+13:39 BigLife 有条件复启令+16:49 FluxVerse CitySim 催办+21:38 BigLife "
                        u"复启催办+23:38 CPH4 GitHub 收获机制观察令——机核计数=python 实核 orders.md 日期列"
                        u"2026-10-02 且含 [CEO 标记行=5·build_digest14.py 内断言实锚）／"
                        u"②引文两行「检查到底是什么在大量耗费token？委员会继续开展节省云端token，"
                        u"加强本地算力工作」=P-2026-10-02-01 正行 CEO 原话 verbatim 连续子串零改字"
                        u"（？句边界设计排版跨两行=v5/v12 逗号子句先例同型·CEO 令全文 verbatim 入 "
                        u"source_facts 本条）／"
                        u"③「token 三面审计 7/7 通过 · 六款续执 · 回访 10-08」=P-2026-10-02-01 委员会案 "
                        u"C-20261002-01（CEO 直令·同窗收口 7/7 PASS·六款=D1 云重制 ≤1 轮/D2 G17 fork 维持 "
                        u"X027/D3 本地批 24h 收割闭环/D4 BGM 路由本地 ACE-Step/D5 基线表首报+夜报流量行/"
                        u"D6 滞留 >4h 入影子探针·泄洪池清零 13 单+G10 收割 11/14·判据六条回访 2026-10-08）／"
                        u"④「硅基城审计三厚三薄 · 问题分级 3+4+3」=P-2026-10-02-02 硅基城问题审计批"
                        u"（CEO 令 10-01 ~23:5x 原话「重点审计硅基城市的问题！务必对标steam一线城市类游戏」·"
                        u"审计件=docs/audits/silicon-city-problem-audit-2026-10-02.md·三厚三薄定谳+P0×3"
                        u"+P1×4+P2×3·调研/正典/机制厚·交付/可玩/产品闸薄）／"
                        u"⑤⑥「对标七作」「一线十定律」=同审计令行 Steam 七作实测表（C:S1 92%·100,705 评为"
                        u"基线）+一线十定律+里程碑 M1≤10-09 可逛切片→M4≤12-31 Steam 发行预研／"
                        u"⑦「巡检双单 34h 静默回执窗 10-05」=P-2026-10-02-03 集团巡检班派单 @BigLife"
                        u"（PT-20261002-03 主产线静默 ~34h 车道自检回执·回执窗 ≤2026-10-05）+"
                        u"P-2026-10-02-04 巡检班催办 @HQ（probe fetch 静默回退陈旧本地面·治本=FETCH-FAIL "
                        u"行内标+origin refs freshest-wins＝「假读治本标记」卡面短语对位）／"
                        u"⑧底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"cph4/evolution-ledger.md P-2026-10-02-01→04 正行集（委员会案 C-20261002-01 "
                          u"token 三面审计+硅基城问题审计批+巡检班派单催办双单·跨仓只读·宿主机直读正典）"
                          u"+FluxGroup/docs/orders.md 2026-10-02 五行 CEO 决策/催办+docs/audits/"
                          u"silicon-city-problem-audit-2026-10-02.md（审计件指针）+src/os/backlog.md "
                          u"#67 R1095 claim 行——编年史 A 级史源（集团令批台账·charter §3 选题池多源）·"
                          u"一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                            u"引文=CEO 原话 verbatim 连续子串零改字〔P-2026-10-02-01 正行原句零改字零重组·"
                            u"CEO 令全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（集团令批台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=集团令批数字盘点档案体（1 句「到底是什么在耗费token」追问 vs 当窗三面审计 "
                            u"7/7 全过收口=「一句话 vs 一批决」母题·深夜审计令（10-01 23:5x）次日全批定谳="
                            u"夜令日清叙事位·三厚三薄=厚薄自诊断诚实位·Steam 七作对标=外部标尺位·里程碑 "
                            u"10-09/12-31=排期闭环悬念位·34h 静默点名+回执窗 10-05=问责时效位·追问→审计→"
                            u"定谳→对标→排期→巡检验收=「令→查→判→排」递进链·v6 深夜决策批/v12 集团外审日/"
                            u"v13 集团治理日同型=决策批盘点先例承继；公众号低创作度条款 7.1-7.4 编辑价值面·"
                            u"charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句 token 追问 vs 当窗三面审计 "
                          u"7/7 收口+深夜令 10-01 23:5x vs 次日三厚三薄全批定谳+34h 静默点名 vs 10-05 回执窗"
                          u"——F-042 v2 对照数字结构同源第十三证·十三连母题续〔v2 开闸/v3 三线/v4 技能/"
                          u"v5 节目重制/v6 对账夜/v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令/v10 云端 "
                          u"token 机制日/v11 产品优先令日/v12 集团外审日/v13 集团治理日/v14 集团令批日〕+"
                          u"2/5/7-7/六款/3+4+3/七作/十定律/10-09/12-31/34h/10-05/10-08 十四组数字/"
                          u"情 1 AI 自治问责→同窗自纠吃瓜温和如实非强极点〔G5 吃瓜未来党+G1 产品优先党双群"
                          u"对位·CEO 追问→委员会同窗审计 7/7 收口=AI 公司自我治理叙事面·v13 治理日同弧〕/"
                          u"时 2 事件 2026-10-01 深夜→10-02 全日批→本卡 2026-10-03 当窗〔决策批盘点=v6 当日"
                          u"时点先例带内·一日滞后+E-pool 漏登盲区修正如实注记〕/时序链=硅基城令 10-01 23:5x→"
                          u"10-02 令批全日→委员会案同窗 7/7→巡检双单→回访 10-08→本卡 R1095）/台 2 公众号方图"
                          u"承载=MC-001~148 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 "
                          u"A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 "
                          u"§5 判据锚定（编年史 A 级事件+数字密度）·#67 触发律=编年史事件随轮领〔R1095 claim·"
                          u"直领=通道回空后新批随轮再入池义务由本件入池+出池同轮兑现·R677 型盲区修正轮〕")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为令批台账读数"
                     u"（审计款数/问题分级/对标作数/里程碑日期/静默时长/回执窗=非 token 用量细节非财务"
                     u"非持仓面·CEO 引文含「耗费token」措辞=令件原文 verbatim 照录非用量数值·v10 206/98%、"
                     u"v11 10,524 commit、v12 40 决、v13 321 件同型分界）入卡面；CEO 指令原文 verbatim "
                     u"纪实照录；P1 边界=本件=纪实档案非提案非表决（委员会案 D1-D6 款目细节与审计行动面="
                     u"批级知悉位 source_facts 承载不入卡面·他司执行面细节不入卡面）；成品只入库·发布="
                     u"M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十四件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build)
report = []
report.append("orders.md 2026-10-02 CEO decision/urge rows (machine count) = %d" % len(ceo_rows))
report.append("ledger P-2026-10-02 rows (set) = %s" % ",".join(p_rows))
report.append("CEO quote verbatim substring present in ledger P-01 row: OK")
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
io.open(os.path.join(TMP, "em-check-r1095.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V14, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V14, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d ceo_rows=%d p_rows=%d" % (H2_SIZE, len(ceo_rows), len(p_rows)))
