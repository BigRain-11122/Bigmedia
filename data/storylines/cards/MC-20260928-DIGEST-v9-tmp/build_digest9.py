# -*- coding: utf-8 -*-
"""MC-20260928-DIGEST-v9 build: DIGEST series 9th piece (R631, backlog #67 chronicle-event claim,
two-step claim landed R630). Self-drive ecosystem order v2.1 numeric digest.
Facts from cph4/evolution-ledger.md L151 row P-20260928-02 (CEO direct order verbatim:
"ceo 命令，全面建立自驱力生态机制，全面激发创新和主动性，工作任务要拉满，要高效，
不能有任何闲置资源，还有空转浪费现象" - @8 lines, T1 fast-file, sister batch with same-day
zero-idle order self-drive.md v2.0) + own-share R630 two-step adaptation (ack <=10min detection
after 09:20:25 ledger landing, proposal-track step + idle-fast abolition, first proposal P-1).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v8 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V8 = os.path.join(BASE, "MC-20260928-DIGEST-v8")
V9 = os.path.join(BASE, "MC-20260928-DIGEST-v9")
TMP = V9 + "-tmp"
os.makedirs(V9, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V8, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 009",
    u"自驱力生态令 2026-09-28 落账 09:20:25",
    u"「不能有任何闲置资源，还有空转浪费现象」",
    u"3 缺口：创新无定轨 · 空转无定义 · 拉满张力",
    u"闭环 4 件：提案轨·空转禁令·诚实边界·计量回访",
    u"提案轨：三句式 · 无需 CEO 令 · 试点 ≤2 周",
    u"空转 4 形态定规 · idle-fast 跳轮路径全司废止",
    u"8 线点名 · 本司 ack ≤10 分钟 · 回访 10-05",
]

SUBS_LINE = u"基于硅基城市真实事件（集团台账与本司台账档案）"

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
meta["topic"] = "MC-20260928-DIGEST-v9"
meta["form"] = (u"DIGEST 盘点图文 009（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第八件·"
                u"#67 触发律=ledger 新 CEO 令级事件落账随轮领·R630 claim 两步制·"
                u"史源=P-20260928-02 自驱力生态机制 v2.1 增补令正行+本司 R630 两步适配实况双锚）")
meta["source_facts"] = (u"自驱力生态令数字盘点八条："
                        u"①「自驱力生态令 2026-09-28 落账 09:20:25」=cph4/evolution-ledger.md L151 P-20260928-02 正行"
                        u"（CEO 直令原话 verbatim「ceo 命令，全面建立自驱力生态机制，全面激发创新和主动性，工作任务要拉满，要高效，"
                        u"不能有任何闲置资源，还有空转浪费现象」·T1 快速件档·09:20:25 ledger 落账〔r630 基线 mtime 机证〕"
                        u"·与同日零空闲令 docs/self-drive.md v2.0 同族姊妹批〔v2.0 管「手上有活」·本批补「生态闭环」三缺口·"
                        u"按防重复律增补非重建·并行窗在途注记〕）／"
                        u"②引文行「不能有任何闲置资源，还有空转浪费现象」=CEO 原话 verbatim 子串（正行原句零改字零重组）／"
                        u"③「3 缺口」=正行缺口实证三件：创新主动性无定轨（P3 explore 产出无提案回流供给律）"
                        u"+空转无统一定义执法（idle-fast 各案停用未全司成法·卡面短标签「空转无定义」=全称「空转无统一定义」压缩）"
                        u"+拉满硬指标（GPU 常态>70%+队列空=事故+「没活=失败」）与诚实律张力无解／"
                        u"④「闭环 4 件」=正行生态闭环四件：①创新提案轨=每司每窗 ≥1 提案·三句式〔现象+建议+判据〕"
                        u"·无需 CEO 令〔P-20260926-03 法无禁止即可为承接〕·判据先立 ≤3 问·试点窗 ≤2 周·判负留痕合法"
                        u"〔负面结论也是产出〕·P3 产出必须回流提案面·连续两周零提案=值守轮点名催供；"
                        u"②空转统一定义与禁令=四形态〔轮零实质产出/产出无消费者/重复造轮/为指标造活〕"
                        u"+执法链=审计部哨兵每日双班+深审 3 日轮+空转事件计数入周报目标 0/周+idle-fast 空转路径全司废止"
                        u"〔队列空→启动规则补队列取活+转提案轨·不再跳轮·真无活可拉=一行声明合法〕；"
                        u"③拉满诚实边界=造活凑数本身=空转第四形态+保护态豁免面不算违规闲置"
                        u"〔主归属保主 fleet §二/YELLOW-HEAVY 让路 §10/RAM<4GB 禁新重活/门控型任务/声明待机/CEO 笔记本豁免位〕"
                        u"+结构性满载≠闲置·「想不出活」不合法·「声明后转创新轨」合法；"
                        u"④计量回访=周报新增自驱面一行〔三线 commit 占比/队列常备数/GPU 利用率均值/空转事件数/创新提案数 applied 计〕"
                        u"+首回访 10-05 周轮〔判据=九实体三线分布齐+提案 ≥1/司+空转事件趋零·不达标=修法或升 CEO·禁感觉良好式立法〕／"
                        u"⑤提案轨行=四件之①数字（三句式·无需 CEO 令·试点窗 ≤2 周·判据 ≤3 问入 source_facts 档案）／"
                        u"⑥「空转 4 形态定规 · idle-fast 跳轮路径全司废止」=四件之②verbatim 数字（四形态全录+idle-fast 全司废止）／"
                        u"⑦「8 线点名」=正行 @八线点名〔Biggame/BigMoney/BigStream/BigLife/BigDomain/BigCompute/FluxVerse/CPH4〕"
                        u"+集团口径八线哨兵即唤 ack ≤15min；「本司 ack ≤10 分钟」=本司 R630 ack 判读"
                        u"〔09:20:25 落账→09:23 轮首检出=检出距落账 ≤10 分钟·backlog #81 注记〕；"
                        u"「回访 10-05」=四件之④首回访 10-05 周轮／"
                        u"⑧底部行=虚实级+来源级标注／"
                        u"本司 R630 两步适配实况〔backlog #81 注记·commit 30750a3·HQ-FEEDBACK F-20260928-03·P-51 送达〕："
                        u"mandate 提案步=任务书空转规则创新提案轨步+docs/self-improvement-queue.md §D 提案面立制"
                        u"+首件提案 P-1〔REACT 台词池反套路化选句律 v2〕+idle-fast 改道=任务书空轮判定路径废止版"
                        u"〔五查静不再跳轮→取活→自进清单→提案轨→真无活=declared-idle 一行声明合法〕+os-protocol §6 v1.11")
meta["source_pointer"] = (u"cph4/evolution-ledger.md L151 P-20260928-02 正行（集团进化台账·CEO 直令原话 verbatim+三缺口+生态闭环四件全录·"
                           u"跨仓只读）+src/os/backlog.md #81 行（本司 R630 收令+ack 判读+两步适配注记·P-51 送达链）"
                           u"+#67 claim 行（两步制 claim 先落防撞）+HQ-FEEDBACK.md F-20260928-03 行（令面回执载体）"
                           u"+docs/os-protocol.md §6 v1.11（空轮判定路径+声明轮并窗=原 idle-fast 并窗改道）"
                           u"+docs/self-improvement-queue.md §D 提案面（首件提案 P-1 落件）+src/os/state.json R630 log"
                           u"（收令+ack+两步适配记账）+git commit 30750a3（ack 三载体 commit·P-51 送达判据）"
                           u"+.c3-tmp/r630_lednew5.txt（09:20:25 ledger 落账 mtime 机证基线）——"
                           u"编年史 A 级史源（集团进化台账+本司台账·charter §3 选题池双源①）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=CEO 原话 verbatim 子串〔「不能有任何闲置资源，还有空转浪费现象」=正行原句零改字零重组·"
                             u"CEO 令全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（集团台账与本司台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=自驱力生态令数字盘点档案体（1 句 CEO 直令 vs 当轮 8 线点名+4 件闭环立法=拉满高效母题·"
                            u"本司 ≤10 分钟 ack=「要高效」当轮兑现位·三缺口→四件闭环=「问题→立法」递进链·"
                            u"idle-fast 废止=旧路退役纪实·回访 10-05=悬念收束位·判负留痕合法=机制设计金句位；"
                            u"公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句 CEO 直令 vs 当轮 8 线点名+4 件闭环立法+本司 ≤10 分钟 ack"
                         u"——F-042 v2 对照数字结构同源第八证·八连母题〔v2 开闸/v3 三线/v4 技能/v5 节目重制/v6 对账夜/"
                         u"v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令〕+3 缺口/4 件/≤2 周窗/4 形态/≤10 分钟/10-05 六组数字/"
                         u"情 1 AI 自治机制升级吃瓜温和如实非强极点〔G5 吃瓜未来党+G1 AI 效率实操党双群对位·自驱力生态=AI 员工高效运转叙事面〕/"
                         u"时 2 事件 2026-09-28 当日〔CEO 直令→09:20:25 ledger 落账→09:23 本司轮首检出 ≤10 分钟→R630 当轮 ack+两步适配→R631 本件盘点〕/"
                         u"台 2 公众号方图承载=MC-001~052 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
                         u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                         u"#67 触发律=ledger 新 CEO 令级事件落账时随轮领（R630 claim 两步制·R517 收口注兑现）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=零毛利/成本/电费/token 量/未公开财务面"
                     u"（自驱力生态件=治理机制面·GPU>70% 与队列常备 25 条=治理拉满指标非财务面·仅档 source_facts 不入卡面）；"
                     u"P1 边界=本件=纪实档案非提案非表决（本司首件提案 P-1=司内提案面载体非本卡面·零自评宣传）；"
                     u"他司执行面细节不入卡面〔姊妹批 self-drive.md v2.0 各司适配=批级知悉位·八线各司 ack 细节不入〕；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第九件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

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
io.open(os.path.join(TMP, "em-check-r631.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V9, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V9, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
