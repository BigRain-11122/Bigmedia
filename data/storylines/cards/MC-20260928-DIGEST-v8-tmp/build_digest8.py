# -*- coding: utf-8 -*-
"""MC-20260928-DIGEST-v8 build: DIGEST series 8th piece (R577, backlog #67 chronicle-event claim).
City supreme decision-council founding-day chronicle digest (committee section first established
2026-09-28 00:10 decision-round batch + C-20260927-02 organ/rule-slimming case supplementary
registration same batch = double anchor). Facts from group decisions.md council section header
(charter cph4/council.md v1.0, CEO order 2026-09-27 ~07:5x, decision round = standing
secretariat; seat opinions via each-company feedback face, independent first, risk seat
permanent devil's advocate; named voting full archive; ordinary pass >=4/7, major items >=5/7,
tie re-vote then CEO escalation; CEO attends/veto/final-review unchanged) + C-20260927-01
(commercialization pricing batch, first council item, 4 seats received incl. seat-6 BigStream
co-signed, topic-3 all lean A, window to 09-29 12:00) + C-20260927-02 (A1-A5 slimming + rule
budget phasing; rules ~65 vs entropy budget <=20 = 3x overline; seats 4/5 opinions filed, five
seats pending, window <=48h; pre-registration criteria merge-dedupe >=30% / four sensors alive
/ zero broken references / Monday patrol first check; before passage zero execution).
Own share: C-01 seat-6 opinion in-window (F-20260927-05), C-02 seat-6 opinion this round
F-20260928-01 approve-with-modifications. All cross-repo read-only, A-grade chronicle,
one-source-multi-use charter S3. Desensitization law: zero margin/cost/unpublished-finance
faces (council items = governance face, C-01 pricing figures already covered by v7, not
repeated - anti-duplication).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v7 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V7 = os.path.join(BASE, "MC-20260927-DIGEST-v7")
V8 = os.path.join(BASE, "MC-20260928-DIGEST-v8")
TMP = V8 + "-tmp"
os.makedirs(V8, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V7, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 008",
    u"决策委员会成立 2026-09-28 节首立",
    u"「平票重议再平升 CEO」",
    u"7 席记名投票 · 普通过 ≥4/7 · 重大件 ≥5/7",
    u"C-01 定价批：4 席已收 · 议题③同向 A",
    u"C-02 瘦身案补登：规则 65 vs 预算 20",
    u"双案意见窗 48 小时 · 风控席必议",
    u"CEO 列席 · 翻案权与终审权不变",
]

SUBS_LINE = u"基于硅基城市真实事件（决策委员会台账档案）"

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
meta["topic"] = "MC-20260928-DIGEST-v8"
meta["form"] = (u"DIGEST 盘点图文 008（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第七件·"
                u"#67 触发律=ledger/decisions 新 CEO 令级事件落账随轮领·史源=委员会节首立+C-20260927-02 补登双锚）")
meta["source_facts"] = (u"决策委员会成立日数字盘点八条：委员会节 2026-09-28 首立（decisions.md 委员会节=城市最高决策委员会·"
                        u"章程=cph4/council.md v1.0·CEO 令 2026-09-27 ~07:5x·决策轮=常设秘书处·2026-09-28 00:10 决策轮批落档）／"
                        u"席位机制=席位意见经各司反馈面出具（独立先行·风控席常任魔鬼代言人必议）·记名投票全档案落本节·"
                        u"普通过 ≥4/7·重大件（判据②③⑤）≥5/7·平票重议再平升 CEO·CEO 列席/翻案权/终审权不变（节头原文 verbatim）／"
                        u"C-20260927-01 商业化定价批（委员会节登记首件·2026-09-27）：四席意见已收〔席3 BigMoney/席4 BigCompute+BigDomain/"
                        u"席5 FluxVerse/席6 BigStream+BigLife·议题③四席同向 A·09-28 收取批登记 D-20260928-01③〕·余席 1/2/7 窗内至 09-29 12:00·"
                        u"票档随窗毕后首个决策轮归档·过会前各司零执行／"
                        u"C-20260927-02 机构与规则瘦身裁并案（首案补登·声明日 09-27 bm-c e72d94c·补登=D-20260928-06 拍板）："
                        u"A1 复盘 8→4 归层/A2 调研台账冻结/A3 哨兵双轨终态/A4 city-lab 三不维持/A5 委员会=决策轮秘书处+§四 规则瘦身分期"
                        u"（账目改法/分域预算〔城市正典 ≤10+治理 ≤10〕/合册批先行序/令令立件降温律）／"
                        u"量化实测=规则类 ≈65 vs 法熵预算 ≤20 超线 3 倍+混装/同题多层立规/令令立件/无总账四病灶（集团审视件 §一）／"
                        u"C-02 意见面=席4〔BigDomain R407 有条件赞成·八点〕/席5〔FluxVerse F-20260927-09 支持全案+分期〕两席已出·"
                        u"余五席（1/2/3/6/7）窗内出具·意见窗 ≤48h 至 09-29 ~10:0x·风控席必议·过会前各司零执行／"
                        u"C-02 预注册判据=合并去重率 ≥30%/四传感器在役零中断（patrol 点名面联动）/引用面零断链（grep 机械验）/周一 patrol 首验／"
                        u"本司份额=C-01 席6 意见已在窗内〔F-20260927-05·BigStream+BigLife 双司版〕+C-02 席6 意见当轮出具=F-20260928-01"
                        u"（赞成有修改：A1-A5+§四 分期赞成+三修改=退役件转指针件制引用面零断律/L0-L4 编号口径随集团定谳即改/"
                        u"治理 ≤10 预算按现行正典件计数·指针件不计）·记票随窗毕后 HQ 决策轮〔本司意见已出零动作〕")
meta["source_pointer"] = (u"FluxGroup/docs/decisions.md 委员会节（2026-09-28 00:10 决策轮批落档·节首立+C-20260927-01/C-02 两件全档案+节头机制原文·"
                           u"集团决策正典跨仓只读）+FluxGroup/docs/decisions.md D-20260928-01（C-01 四席意见收讫登记）/D-20260928-06"
                           u"（C-20260927-02 补登批拍板·集团决策正典跨仓只读）+cph4/council.md v1.0（委员会章程·CEO 令 2026-09-27 ~07:5x·跨仓只读）"
                           u"+集团审视件 organ-slimming-review-2026-09-27.md §一（规则 ≈65 vs 预算 ≤20 超线 3 倍量化实测·跨仓只读）"
                           u"+cph4/evolution-ledger.md P-20260927-06 行（瘦身审视令·集团进化台账跨仓只读）"
                           u"+HQ-FEEDBACK.md F-20260928-01 行（本司 C-02 席6 意见载体）+F-20260927-05 行（本司 C-01 席6 意见载体）"
                           u"+src/os/state.json R576 log（委员会节首立+C-02 补登收讫记账）——"
                           u"编年史 A 级史源（集团决策正典+集团章程+集团台账+本司台账·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=委员会节节头 verbatim 子串〔「平票重议再平升 CEO」=节头原句「平票重议再平升 CEO」零改字零重组·"
                             u"节头机制全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（决策委员会台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=决策委员会成立日数字盘点档案体（委员会成立=城市治理机制升级事件+双案在途记票=悬念收束位·"
                            u"过会前零执行如实口径；「平票重议再平升 CEO」=机制设计金句位·节头 verbatim；风控席必议=制衡设计面；"
                            u"公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：7 席委员会成立 vs 双案在途记票——C-01 4 席已收 vs 余 3 席在窗·"
                         u"C-02 规则 65 vs 预算 20 超线 3 倍——F-042 v2 对照数字结构同源第七证·七连母题〔v2 开闸/v3 三线/v4 技能/v5 节目重制/"
                         u"v6 对账夜/v7 商业化定价日/v8 委员会成立日〕+4/7 与 5/7 双门槛数字+双案意见窗 48 小时悬念位/"
                         u"情 1 城市治理新机制吃瓜温和如实非强极点〔G5 吃瓜未来党+G1 AI 效率实操党双群对位〕/"
                         u"时 2 事件 2026-09-28 当日〔CEO 令 09-27 ~07:5x 立章程→09-28 00:10 决策轮首立委员会节+C-02 补登·意见窗 48h 至 09-29〕/"
                         u"台 2 公众号方图承载=MC-001~051 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
                         u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                         u"#67 触发律=ledger/decisions 新 CEO 令级事件落账时随轮领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=零毛利/成本/电费/token 量/未公开财务面"
                     u"（委员会件=治理机制面零财务数字·C-01 定价数字不重复入卡〔v7 已盘点·反重复律〕·规则 65 vs 预算 20=治理量化实测非财务面）；"
                     u"P1 边界=委员会过会件纪实面零执行（过会前各司零执行·本件=纪实档案非投票非提案·本司席6 意见已出如实注记·零代签）；"
                     u"他司执行面细节不入卡面〔D-20260928-02/03 BigMoney 修法=批级知悉位〕；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第八件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r577.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V8, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V8, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
