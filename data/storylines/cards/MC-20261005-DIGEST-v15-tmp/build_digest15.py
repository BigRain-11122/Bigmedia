# -*- coding: utf-8 -*-
"""MC-20261005-DIGEST-v15 build: DIGEST series 15th piece (R1303, backlog #67 chronicle-event
trigger-law claim; E-pool DIGEST channel empty since E32/v14 out-take at R1095, the 2026-10-04
radar order batch never re-stocked = restock+consume same round, R1095/R970 precedent).
Event = 2026-10-04 late-night order batch (22:5x->23:1x, 4 CEO-direct rows): fleet second-level
dispatch chain order + Dudu full-project re-acceptance order + RADAR ROUTING LOOP design order
(ledger P-2026-10-04-01) + RADAR REVENUE-ORIENTATION calibration order (ledger P-2026-10-04-02).
Card focus = radar twin orders (one design, one calibration): seven-domain scanning + L1-L3
deep-research tiers + dual review channels + claim system + two-rate metrics; revenue lens =
3 priorities + 4-segment loop + benefit form 3 types. Machine assertions: orders.md 10-04 CEO
row count == 4, ledger P-2026-10-04 set == 01/02, CEO quote substring verbatim + fact fragments.
CEO verbatim quote split across two lines at comma-clause boundary (v5/v12/v14 precedent).
Em budget ladder with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack budget law (R381).
Template = DIGEST v14 build script. All output UTF-8.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V14 = os.path.join(BASE, "MC-20261003-DIGEST-v14")
V15 = os.path.join(BASE, "MC-20261005-DIGEST-v15")
TMP = V15 + "-tmp"
os.makedirs(V15, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

HQ = os.path.join(ROOT, "..", "..")
# --- machine count / verbatim assertions (content-addressed, build-time hard gates)
orders_txt = io.open(os.path.join(HQ, "docs", "orders.md"), encoding="utf-8", errors="replace").read()
ceo_rows = [ln for ln in orders_txt.splitlines()
            if "10-04 ~" in ln and ln.lstrip().startswith("|") and "\u300c" in ln and "\u300d" in ln]
assert len(ceo_rows) == 4, "orders.md 2026-10-04 CEO row count != 4: %d" % len(ceo_rows)

ledger_txt = io.open(os.path.join(HQ, "cph4", "evolution-ledger.md"), encoding="utf-8", errors="replace").read()
p_rows = sorted(set(re.findall(r"\bP-2026-10-04-\d{2}\b", ledger_txt)))
assert p_rows == ["P-2026-10-04-01", "P-2026-10-04-02"], \
    "ledger P-2026-10-04 rows != 01/02: %s" % p_rows

QUOTE = u"不仅仅是游戏的，那些其他方面的都要去抓取，然后去学习调研。深入调研。"
assert QUOTE in orders_txt, "CEO quote verbatim substring not found in orders.md radar order row"
for frag in [u"七司业务域", u"L1 判读", u"认领率+落地率", u"省 token/省工时/直接营收",
             u"商业化/自动化/创新绩效优先", u"研究→接线"]:
    assert frag in orders_txt, "radar fact fragment missing in orders.md: %s" % frag

cfg = json.load(io.open(os.path.join(V14, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 015",
    u"集团令批 2026-10-04（深夜 4 行 · 雷达双令）",
    u"「不仅仅是游戏的，那些其他方面的都要去抓取，",
    u"然后去学习调研。深入调研。」",
    u"雷达路由闭环 · 扫描七司业务域 · 深研 L1-L3",
    u"过目双通道 · 候选认领制 · 两率入周报",
    u"收益导向 · 可变现升权 · 四段闭环链",
    u"收益 3 型：省 token · 省工时 · 直接营收",
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
meta["topic"] = "MC-20261005-DIGEST-v15"
meta["form"] = (u"DIGEST 盘点图文 015（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第十四件·"
                u"#67 触发律=编年史事件随轮领〔R1303 claim·直领=E-pool DIGEST 通道 E32 R1095 出池后回空·"
                u"10-04 雷达令批未随批再入池→本件入池+出池同轮兑现〔R1095/R970 先例〕·"
                u"触发律照守非造活凑数〕·"
                u"史源=cph4/evolution-ledger.md P-2026-10-04-01/02+orders.md 2026-10-04 四行 CEO 直令"
                u"〔CEO 原话 verbatim+雷达双令一设计一校准〕）")
meta["source_facts"] = (u"集团令批数字盘点八条："
                        u"①「集团令批 2026-10-04（深夜 4 行 · 雷达双令）」=FluxGroup/docs/orders.md "
                        u"2026-10-04 四行 CEO 直令（22:5x 机队秒级分发链落地令 O-20261004-2255〔含追加令"
                        u"「我全面授权你操控电脑干任何事情，所以不要等我来，我现在已经放假了。你好好"
                        u"把这个机制给科学落实」〕+23:0x 吸嘟嘟全项目打回重验收令 O-20261004-2300〔@Biggame "
                        u"A 机窗口承接〕+23:0x 雷达路由闭环机制设计令〔ledger P-2026-10-04-01〕+23:1x 雷达"
                        u"收益导向校准令〔ledger P-2026-10-04-02〕——机核计数=python 实核 orders.md 日期列"
                        u"10-04 且 CEO 原话「」体行=4·build_digest15.py 内断言实锚）／"
                        u"②引文两行「不仅仅是游戏的，那些其他方面的都要去抓取，」「然后去学习调研。"
                        u"深入调研。」=P-2026-10-04-01 正行 CEO 原话 verbatim 连续子串零改字（逗号子句设计"
                        u"排版跨两行=v5/v12/v14 先例同型·CEO 令 1 全文 verbatim 入 source_facts 本条："
                        u"「不仅仅是游戏的，那些其他方面的都要去抓取，然后去学习调研。深入调研。"
                        u"然后让决策委员会去过目一下，或者是各个子公司去过目一下。设置领取对自己业务"
                        u"有赋能的。这其中怎么弄？你们好好想一想。」）／"
                        u"③「雷达路由闭环 · 扫描七司业务域 · 深研 L1-L3」=P-2026-10-04-01 雷达路由闭环"
                        u"机制设计令（①扫描面扩全领域=七司业务域+通用技术域分区清单逐窗实搜·禁偏科·"
                        u"核心七域每窗必扫+扩展域轮换②深研分级 L1 判读/L2 五门司域映射/L3 深研件"
                        u"〔R- 专项·机制拆解+落地判据预注册〕）／"
                        u"④「过目双通道 · 候选认领制 · 两率入周报」=同令③④⑤（③过目双通道=窗级候选清单"
                        u"走各司 OS 循环过目〔OH 切片面〕+周级简报走决策委员会过目〔进化轮五议程+决策轮"
                        u"上报包加输入路·秘书处分级转发〕④认领制=候选表逐件带认领位·各司在己方 OH 文件"
                        u"写固定格式认领行→转司内任务单·两窗未领=周轮三态处置⑤闭环计量=认领率+落地率"
                        u"入周报·正典=cph4/github-radar.md v1.1 增补路由闭环章〔全部寄宿既有轮·"
                        u"零新台账零新循环〕）／"
                        u"⑤「收益导向 · 可变现升权 · 四段闭环链」=P-2026-10-04-02 雷达收益导向校准令"
                        u"（①透镜=商业化/自动化/创新绩效优先——风向扫描升权可变现件·纯玩具类降权"
                        u"②落地链延长四段=研究→接线→执行→收益〔不停在派单·收益回访入闭环率〕）／"
                        u"⑥「收益 3 型：省 token · 省工时 · 直接营收」=同令③（每契合件必写预期收益形态"
                        u"·省 token/省工时/直接营收三型）+④简报 #2 起加收益面专节+⑤与商业化付费点批"
                        u"〔P-2026-09-27-02 四层定价〕/BigCompute 中枢/自驱力生态咬合引用不重建／"
                        u"⑦批族承接=P-2026-10-02-09 GitHub 收获机制立制令〔research-dept-charter v1.1 §五·"
                        u"CPH4 实验室主责=周轮雷达+五门评估+装包正典+司级自决分拨〕+P-2026-09-29-06 风向"
                        u"雷达职能〔雷达族源头〕——本司消费面=#70 OSS 借力 72h 窗〔窗 4=10-05 21:40 开·"
                        u"收益透镜+收益三型接线〕／⑧底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"cph4/evolution-ledger.md P-2026-10-04-01/02 正行集（雷达双令·跨仓只读·"
                          u"宿主机直读正典=本机即集团仓宿主机零 git 操作零写接触）+FluxGroup/docs/orders.md "
                          u"2026-10-04 四行 CEO 直令+cph4/github-radar.md v1.1（正典指针）+src/os/backlog.md "
                          u"#67 R1303 claim 行——编年史 A 级史源（集团令批台账·charter §3 选题池多源）·"
                          u"一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                            u"引文=CEO 原话 verbatim 连续子串零改字〔P-2026-10-04-01 正行原句零改字零重组·"
                            u"CEO 令全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（集团令批台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=集团令批数字盘点档案体（1 句「不仅仅是游戏的…都要去抓取」扩域令 vs "
                            u"路由闭环五件套〔扫描/分级/过目/认领/计量〕即刻接线=「一句话 vs 一套机制」母题·"
                            u"深夜 22:5x→23:1x 连发 4 行=夜令批密度叙事位·双令结构=一设计〔路由闭环〕×"
                            u"一校准〔收益导向〕配对叙事位·认领制+两率入周报=生态闭环问责位·四段闭环+收益三型="
                            u"不停在派单的落地链延长位·扩域→分级→过目→认领→计量→收益=「扫→研→领→收」"
                            u"递进链·v14 集团令批日同型=令批盘点先例承继第二件；公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：深夜 22:5x→23:1x 连发 4 行 vs "
                          u"雷达双令一设计一校准同批落地+1 句「你们好好想一想」机制设计问 vs 当窗 github-radar "
                          u"v1.1 正典落档执行+2 令雷达批 vs 路由闭环五件套〔扫描/分级/过目/认领/计量〕——"
                          u"F-042 v2 对照数字结构同源第十四证·十四连母题续〔v2 开闸/v3 三线/v4 技能/"
                          u"v5 节目重制/v6 对账夜/v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令/v10 云端 "
                          u"token 机制日/v11 产品优先令日/v12 集团外审日/v13 集团治理日/v14 集团令批日/"
                          u"v15 雷达令批夜〕+4/2/7/3/2/2/4/3 八组数字/情 1 AI 深夜自建生态+收益期待吃瓜"
                          u"温和如实非强极点〔G5 吃瓜未来党+G2 商业化党双群对位·CEO 深夜连令→机制当窗"
                          u"落档=AI 公司生态自进化叙事面·非强极点〕/时 2 事件 2026-10-04 深夜 23:1x 末令→"
                          u"本卡 2026-10-05 01:0x 连夜窗快反 ≈2h〔v14 一日滞后对照=本件更快·令批盘点连夜窗"
                          u"注记〕/台 2 公众号方图承载=MC-001~150 S3 实证复用·盘点=公众号主流图文格式"
                          u"〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                          u"#67 触发律=编年史事件随轮领〔R1303 claim·入池+出池同轮兑现·R1095/R970 先例〕")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为令批台账读数"
                     u"（令行数/司域数/分级数/闭环段数/收益型数=非 token 用量细节非财务非持仓面）入卡面；"
                     u"CEO 指令原文 verbatim 纪实照录；P1 边界=本件=纪实档案非提案非表决（雷达机制设计细节="
                     u"批级知悉位 source_facts 承载不入卡面·他司执行面细节〔吸嘟嘟审计细节/机队分发实弹"
                     u"细节〕不入卡面·v14 同型分界）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十五件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build)
report = []
report.append("orders.md 2026-10-04 CEO direct-order rows (machine count) = %d" % len(ceo_rows))
report.append("ledger P-2026-10-04 rows (set) = %s" % ",".join(p_rows))
report.append("CEO quote verbatim substring present in orders.md radar row: OK")
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
io.open(os.path.join(TMP, "em-check-r1303.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V15, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V15, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d ceo_rows=%d p_rows=%d" % (H2_SIZE, len(ceo_rows), len(p_rows)))
