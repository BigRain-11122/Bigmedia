# -*- coding: utf-8 -*-
"""MC-20261001-DIGEST-v13 build: DIGEST series 13th piece (R872, backlog #67 chronicle-event
claim, E29 stock candidate consumed per R871 closing order: REACT 10-02 / OSS w3 both
time-gated -> E29 first claimable). Event = 2026-10-01 group governance batch: three CEO
direct orders to council (info-sync / rule-inflation / idle-root-cure), same-window close,
3 cases voted 7/7, governance 6+5+4 clauses effective same day, batch = 11 rows
(machine regex-set count: D-20261001-01..08 + C-20261001-01..03 = 11; C-20260101-01 typo
row is a same-case anchor per D-08 note 5, wrong-year digits never match 20261001).
CEO verbatim quote = C-20261001-02 row (rule inflation order), split across two lines at
comma clause boundary (v5/v12 cross-line quote precedent). Numbers: 70% vs 6% rule-share
contrast (C-02 evidence), 321 rule files (C-02), 47 unlogged dispatches backfilled (C-01
same-window implementation), review window 2026-10-08 (three cases same window), veto
window one-sentence-CEO (T1 to 10-08). Em budget ladder with ZERO-MARGIN EXCLUSION
(R293/R310) + vertical stack budget law (R381). Template = DIGEST v12 build script.
All output UTF-8.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V12 = os.path.join(BASE, "MC-20261001-DIGEST-v12")
V13 = os.path.join(BASE, "MC-20261001-DIGEST-v13")
TMP = V13 + "-tmp"
os.makedirs(V13, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# --- machine count of the 2026-10-01 batch rows (content-addressed, set semantics)
dec = io.open(os.path.join(ROOT, "..", "..", "docs", "decisions.md"), encoding="utf-8").read()
batch_set = sorted(set(re.findall(r"\b([DC]-20261001-\d{2})\b", dec)))
assert len(batch_set) == 11, "governance batch count != 11: %s" % batch_set

cfg = json.load(io.open(os.path.join(V12, "cards.json"), encoding="utf-8"))

# CEO verbatim substring from C-20261001-02 row (zero char change; comma-clause
# boundary design split across two lines, v5/v12 cross-line quote precedent)
LINES = [
    u"城市盘点 013",
    u"集团治理日 2026-10-01（CEO 一日三令 · 同窗收口）",
    u"「立了一大堆规则和机制，产出却很少，",
    u"委员会好好治理」",
    u"三案：信息同步 · 规则通胀 · 闲置根治（表决 7/7）",
    u"单日批 11 行 · 治理 6+5+4 条同日生效",
    u"规则面 70% vs 标杆 6% · 规则存量 321 件 md",
    u"47 单补录清偿 · 回访 10-08 · 否决窗一句话可翻",
]

SUBS_LINE = u"基于硅基城市真实事件（集团治理批台账档案）"

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
meta["topic"] = "MC-20261001-DIGEST-v13"
meta["form"] = (u"DIGEST 盘点图文 013（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第十二件·"
                u"#67 触发律=编年史事件随轮领〔R872 claim·E29 备货位领做=R871 收口可领序第三位兑现"
                u"（前两位 REACT 10-02/OSS w3=时间闸未开）〕·史源=FluxGroup/docs/decisions.md 集团治理批 "
                u"D-20261001-01→08+C-20261001-01→03〔CEO 一日三令 verbatim+三案 7/7+单日 11 行机核计数〕）")
meta["source_facts"] = (u"集团治理日数字盘点八条："
                        u"①「集团治理日 2026-10-01（CEO 一日三令 · 同窗收口）」=FluxGroup/docs/decisions.md "
                        u"10-01 批三治理案正行（C-20261001-01 机队信息同步时效审查与治理案·CEO 令 10-01 ~10:4x"
                        u"「我发现机队之间的信息同步很不及时，委员会去审查，然后治理」+C-20261001-02 规则通胀与"
                        u"产出不足治理案+C-20261001-03 机队生产力闲置根治案=三 CEO 直令点名委员会通道同窗收口"
                        u"〔council §五 排期律〕·跨仓只读·D-20261001-03 宿主机直读正典=本机即集团仓宿主机"
                        u"零 git 操作零写接触）／"
                        u"②引文两行「立了一大堆规则和机制，产出却很少，委员会好好治理」=C-20261001-02 正行 "
                        u"CEO 原话 verbatim 连续子串零改字（逗号子句边界设计排版跨两行=v5/v12 跨两行先例·"
                        u"CEO 令全文 verbatim 入 source_facts 本条·批评面照录禁软化禁重组）／"
                        u"③「三案：信息同步 · 规则通胀 · 闲置根治（表决 7/7）」=C-01/C-02/C-03 三案表决全 "
                        u"7/7 赞成（Tools/council_vote.py 实跑 VERDICT: PASS·C-01 普通门槛 ≥4/7·"
                        u"C-02 --major 门槛 5/7·C-03 --major 门槛 5/7·记名票档七席全录）／"
                        u"④「单日批 11 行」=docs/decisions.md 10-01 批机核计数（python regex set 实核 "
                        u"2026-10-01：[DC]-20261001-\\d{2} 集合=11 行·D-20261001-01~08+C-20261001-01~03·"
                        u"C-20260101-01 伪号=同案锚〔D-20261001-08 ⑤注记 typo·年位数字 20260101≠20261001 "
                        u"不匹配正则不入计数〕·决策批盘点=v6 深夜决策批/v12 集团外审日同型先例承继）／"
                        u"⑤「治理 6+5+4 条同日生效」=C-01 治理六条（发射台账硬律/态翻面 SLA 工作窗 ≤2h/"
                        u"回执收件加密并入 EngineTick 10min 步/影子缺口清偿律常态窗 ≤5/会话任务持久化律/"
                        u"判据预注册五条）+C-02 治理五条（立法预算帽新规则 ≤2 件/周/仓·条款瘦身 ≤120 字/条·"
                        u"产出计分制能跑能玩能看 2 分实改 1 分纯 md 记账 0 分记账 ≤5 行·执法优先律·"
                        u"回访判据产出化）+C-03 根治四条（机队利用率小时台账/常设备货池 ≥10 件已建 11 单/"
                        u"心跳停跳外部兜底探测/0 分派工自动化）／"
                        u"⑥「规则面 70% vs 标杆 6% · 规则存量 321 件 md」=C-02 实证列（近 7 日 commit 构成"
                        u"扫读：HQ 仓规则/治理面占 70%·BigLife 标杆 6%·FluxVerse 43%/BigDomain 40%/"
                        u"MiniGame 37%+规则存量 321 件 md 6.54MB+近 3 日 HQ 实物产出抽样 8/8 为台账/审计类）／"
                        u"⑦「47 单补录清偿 · 回访 10-08」=C-01 同窗实施列（C 会话直射 47 单未登台账="
                        u"U259 执行违例自首→存量补录清偿毕 cloudF-queue-c.jsonl）+三案判据回访窗 2026-10-08 "
                        u"治理日同窗（C-01 判据预注册五条/C-02 加规则面占比 ≤30%+周产出分 ≥3/C-03 判据五条）／"
                        u"⑧「否决窗一句话可翻」=三案 T1 分级否决窗 7 天至 10-08·CEO 翻案权保留（一句话可翻）／"
                        u"⑨底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"FluxGroup/docs/decisions.md 集团治理批 D-20261001-01→08+C-20261001-01→03 正行集"
                          u"（10-01 单日 11 行·C-01 信息同步治理六条/C-02 规则通胀治理五条/C-03 闲置根治四条·"
                          u"三案 7/7+判据回访 10-08·跨仓只读·宿主机直读正典）+docs/self-improvement-queue.md "
                          u"§E E29 备货位行（R870 入池·E-pool 第五路=DIGEST 通道未消费存量候选·R871 收口"
                          u"「E29 standby 维持」）+src/os/backlog.md #67 R872 claim 行——编年史 A 级史源"
                          u"（集团决策正典台账·charter §3 选题池多源）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=CEO 原话 verbatim 连续子串零改字〔C-20261001-02 正行原句零改字零重组·"
                             u"CEO 令全文 verbatim 入 source_facts·批评面照录禁软化〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（集团治理批台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=集团治理日数字盘点档案体（1 日 3 道 CEO 直令 vs 同窗 3 案 7/7 收口="
                            u"「一句话 vs 一批决」母题·「立了一大堆规则」的委员会给规则立规矩=自指反差叙事位·"
                            u"规则面 70% vs 标杆 6%=标杆反差位·47 单自首补录清偿=诚实机制位·回访 10-08="
                            u"治理闭环悬念位·批评→审查→表决→立规→自首清偿→回访=「问题→表决→立法→自检」"
                            u"递进链·v6 深夜决策批/v12 集团外审日同型=决策批盘点先例承继；公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 日 3 道 CEO 直令 vs 同窗 3 案 7/7 "
                          u"收口+「立了一大堆规则」vs 治理后立法预算帽 ≤2 件/周=给规则立规矩自指反差+"
                          u"规则面 70% vs 标杆 6%——F-042 v2 对照数字结构同源第十二证·十二连母题续"
                          u"〔v2 开闸/v3 三线/v4 技能/v5 节目重制/v6 对账夜/v7 商业化定价日/v8 委员会成立日/"
                          u"v9 自驱力生态令/v10 云端 token 机制日/v11 产品优先令日/v12 集团外审日/"
                          u"v13 集团治理日〕+3/11/7/6/5/4/70%/6%/321/47/10-08 十一组数字/情 1 AI 自治问责→"
                          u"自纠吃瓜温和如实非强极点〔G5 吃瓜未来党+G1 产品优先党双群对位·CEO 批评→委员会"
                          u"同窗自纠+47 单自首补录=AI 公司自我治理叙事面·v11 产品优先令日同弧〕/时 2 事件 "
                          u"2026-10-01→本卡 2026-10-01 当日+台账档案常青〔决策批盘点=v6 当日时点先例〕/"
                          u"时序链=CEO 三令 10-01→三案审查→表决 7/7→15 条立规→自首清偿→回访 10-08→本卡 "
                          u"R872）/台 2 公众号方图承载=MC-001~083 S3 实证复用·盘点=公众号主流图文格式"
                          u"〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                          u"#67 触发律=编年史事件随轮领〔R872 claim·E29=R871 收口可领序备货位领做非造活凑数〕")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为治理台账读数"
                     u"（占比/规则计数/清偿单数/回访日期=非 token 用量非财务非持仓面·v10 206/98%、"
                     u"v11 10,524 commit、v12 40 决同型分界）入卡面；CEO 指令原文 verbatim 纪实照录"
                     u"（批评面照录禁软化禁重组）；P1 边界=本件=纪实档案非提案非表决（治理案执行细节="
                     u"他司份额不入卡面·白名单文件/备货池单目=批级知悉位）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十三件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build)
report = []
report.append("governance batch machine count (regex set) = %d rows: %s" % (len(batch_set), ",".join(batch_set)))
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
io.open(os.path.join(TMP, "em-check-r872.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V13, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V13, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d batch_rows=%d" % (H2_SIZE, len(batch_set)))
