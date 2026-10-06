# -*- coding: utf-8 -*-
"""MC-20261006-DIGEST-v16 build: DIGEST series 16th piece (R1536, backlog #67 chronicle-event
trigger-law direct claim; broken-round absorb = prior body 21:22 died on backend moderation
guardrail mid-production, this body inherits + completes accounting under same round number,
R155/R1506 precedent). Event = 2026-10-06 group first-report day batch (orders.md 5 rows):
00:37 CEO GPU-recovery decision row + ~12:0x group brief-report order O-20261006-1200 +
~12:0x theme-deepening order O-20261006-1207 (BigMoney lane, off-card) + ~12:1x self-built
mail direct-send order O-20261006-1215 (250 QUEUED) + ~12:1x synthesis order O-20261006-1218
(BigMoney lane, off-card). Card focus = brief-report + direct-send twin: nine-company brief
compiled -> SMTP legacy code leak-banned -> "any method you want" -> protocol needs no auth
code verdict -> self-built direct-send tool -> mx3.qq.com 250 QUEUED same window.
Supply-blot fix = 10-06 order batch never re-stocked into E-pool DIGEST channel after E32
(v14 R1095) -> restock+consume same round (R1095/R970 precedent; R870 derive-gap family).
Machine assertions: orders.md 10-06 row count == 5, CEO-quote row count == 4, CEO quote
substring verbatim + fact fragments. Em budget ladder with ZERO-MARGIN EXCLUSION
(R293/R310) + vertical stack budget law (R381). Template = DIGEST v15 build script.
All output UTF-8.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V15 = os.path.join(BASE, "MC-20261005-DIGEST-v15")
V16 = os.path.join(BASE, "MC-20261006-DIGEST-v16")
TMP = V16 + "-tmp"
os.makedirs(V16, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

HQ = os.path.join(ROOT, "..", "..")
# --- machine count / verbatim assertions (content-addressed, build-time hard gates)
orders_txt = io.open(os.path.join(HQ, "docs", "orders.md"), encoding="utf-8", errors="replace").read()
all_rows = [ln for ln in orders_txt.splitlines() if ln.lstrip().startswith("|") and ln.lstrip().startswith("| 10-06")]
assert len(all_rows) == 5, "orders.md 2026-10-06 total row count != 5: %d" % len(all_rows)
ceo_quote_rows = [ln for ln in all_rows if "\u300c" in ln and "\u300d" in ln]
assert len(ceo_quote_rows) == 4, "orders.md 2026-10-06 CEO-quote row count != 4: %d" % len(ceo_quote_rows)

QUOTE = u"自己写一个发送邮件的小程序，然后通过这小程序去发送吗？不管你用什么方法。"
assert QUOTE in orders_txt, "CEO quote verbatim substring not found in orders.md direct-send row"
for frag in [u"发简要报告", u"九司+委员会全量整理", u"邮件协议本无需授权码",
             u"mx3.qq.com 250 QUEUED", u"Tools/mail-direct-send.py",
             u"旧 SMTP 授权码入 git 史", u"新码轮换=CEO 物理件", u"10-06 12:2x"]:
    assert frag in orders_txt, "fact fragment missing in orders.md: %s" % frag

assert os.path.exists(os.path.join(ROOT, "orders", "O-20261006-1410-HQ-C.md")), \
    "own dispatch order O-20261006-1410-HQ-C.md missing"

cfg = json.load(io.open(os.path.join(V15, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 016",
    u"集团首报日 2026-10-06（5 行令批 · 首报+直投）",
    u"「自己写一个发送邮件的小程序，",
    u"然后通过这小程序去发送吗？不管你用什么方法。」",
    u"首报令 12:0x · 九司+委员会全量整理 · 简报成文",
    u"发送受阻如实呈报 · 旧码判泄露禁用 · 新码挂物理件",
    u"方法定谳 · 邮件协议本无需授权码 · 自建直投程序",
    u"实弹 250 QUEUED · 直连收件方 MX · 10-06 12:2x 受理",
]

SUBS_LINE = u"基于硅基城市真实事件（集团首报直投台账档案）"

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
meta["topic"] = "MC-20261006-DIGEST-v16"
meta["form"] = (u"DIGEST 盘点图文 016（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第十五件·"
                u"#67 触发律=编年史事件随轮领〔R1536 直领·断轮承接=R1536 先行体 21:22 backend moderation "
                u"guardrail 断·本 body 同轮号承接续产〔R155/R1506 先例〕·E-pool DIGEST 通道 E32 R1095 出池后"
                u"回空·10-06 首报日批未随批入池=供给盲区 R870 同型→本件入池+出池同轮兑现〔R1095/R970 先例〕·"
                u"触发律照守非造活凑数〕·史源=FluxGroup/docs/orders.md 2026-10-06 五行令批〔首报令 "
                u"O-20261006-1200+邮件直投令 O-20261006-1215「250 QUEUED」主承重双令·CEO 原话 verbatim〕+"
                u"本司响应链 orders/O-20261006-1410-HQ-C〔R1496(b)-R1500〕）")
meta["source_facts"] = (u"集团首报日数字盘点八条："
                        u"①「集团首报日 2026-10-06（5 行令批 · 首报+直投）」=FluxGroup/docs/orders.md "
                        u"2026-10-06 五行台账（00:37 CEO 回收令兑现〔FluxVerse GPU HOLD 份额回收转配 "
                        u"BigCompute·他司执行面〕+~12:0x 集团近期成果与进度简要报告令 O-20261006-1200"
                        u"〔CEO 原话 verbatim「集团，子公司，决策委员会等全部整理近期成果和进度，发简要"
                        u"报告，邮箱 sjs208@qq.com」·九司+委员会全量整理·报告已成文 docs/audits/CEO-简报-"
                        u"2026-10-06.md 集团仓只读引用〕+~12:0x 题材深化批令 O-20261006-1207〔@BigMoney "
                        u"研究部承接·他司执行面不入卡面〕+~12:1x 自建邮件直投程序令 O-20261006-1215"
                        u"〔CEO 原话 verbatim·本卡引文主承重令〕+~12:1x 经验与外源综合研判令 O-20261006-1218"
                        u"〔@BigMoney 研究部·他司执行面不入卡面〕——机核计数=python 实核 orders.md「| 10-06」"
                        u"行=5·「」体 CEO 直令行=4·build_digest16.py 内断言实锚）／"
                        u"②引文两行「自己写一个发送邮件的小程序，」「然后通过这小程序去发送吗？不管你用"
                        u"什么方法。」=O-20261006-1215 直投令行 CEO 原话 verbatim 连续子串零改字（逗号子句"
                        u"设计排版跨两行=v5/v12/v14/v15 先例同型·CEO 令全文 verbatim 入 source_facts 本条："
                        u"「自己写一个发送邮件的小程序，然后通过这小程序去发送吗？不管你用什么方法。吧，"
                        u"因为这玩意，现在 STMP 码已经被各种地方都封了，配不好。」）／"
                        u"③「首报令 12:0x · 九司+委员会全量整理 · 简报成文」=O-20261006-1200 报告令"
                        u"（①整理面=集团运行态+决策委员会 10-05/06 批+八司一句话进度·证据锚制②报告已成文="
                        u"docs/audits/CEO-简报-2026-10-06.md〔集团仓只读引用〕——发送面挂物理件窗注记见④）／"
                        u"④「发送受阻如实呈报 · 旧码判泄露禁用 · 新码挂物理件」=同令③（发送阻塞如实呈报="
                        u"旧 SMTP 授权码入 git 史〔P-01 判泄露禁用〕·新码轮换=CEO 物理件——收到新码即轮换"
                        u"补发 sjs208@qq.com）／"
                        u"⑤「方法定谳 · 邮件协议本无需授权码 · 自建直投程序」=O-20261006-1215 直投令①"
                        u"（方法定谳=邮件协议本无需授权码〔授权码仅「经服务商转发」时需要〕→自建 "
                        u"Tools/mail-direct-send.py：DNS MX 解析→EHLO/STARTTLS→MAIL FROM→RCPT→DATA·"
                        u"UTF-8 正文+可复用参数面·值班链简报基建位）／"
                        u"⑥「实弹 250 QUEUED · 直连收件方 MX · 10-06 12:2x 受理」=同令③（实弹结果="
                        u"mx3.qq.com 250 QUEUED〔协议层受理成功·10-06 12:2x〕·发件身份=flux-brief@"
                        u"fluxverse.cn→收件 sjs208@qq.com〔CEO 令原文亲署收件邮箱=令件 verbatim 面·卡面零"
                        u"邮箱呈现〕·简报发送面转常设）／"
                        u"⑦批族承接+本司响应链=orders/O-20261006-1410-HQ-C 巡检整改派单〔PT-20261006-02 "
                        u"P2·14:14:41 落〕→本司当日全链响应四件套（R1496(b) 破静续拍领池+R1497 漫画试点"
                        u"双话四件+R1498 artgen 发射包+R1500 origin_gap_check 根修·本司执行面·入 "
                        u"source_facts 承载不入卡面）／⑧底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"FluxGroup/docs/orders.md 2026-10-06 五行台账（首报令 O-20261006-1200+直投令 "
                          u"O-20261006-1215 主承重·跨仓只读·宿主机直读正典=本机即集团仓宿主机零 git 操作"
                          u"零写接触）+docs/audits/CEO-简报-2026-10-06.md（集团仓只读引用）+Tools/"
                          u"mail-direct-send.py（集团仓只读·程序件名引证）+orders/O-20261006-1410-HQ-C.md"
                          u"（本司派单正件）+src/os/backlog.md #67 R1536 注——编年史 A 级史源（集团首报日"
                          u"台账·charter §3 选题池多源）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                            u"引文=CEO 原话 verbatim 连续子串零改字〔O-20261006-1215 直投令原句零改字零重组·"
                            u"CEO 令全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（集团首报直投台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=集团首报日数字盘点档案体（1 句「不管你用什么方法」任意方法令 vs 当窗自建"
                            u"直投程序+250 QUEUED 实弹受理=「一句话 vs 一套自愈」母题·STMP 授权码全被封"
                            u"〔受阻面〕vs 邮件协议本无需授权码〔方法定谳自愈面〕=基建受阻×方法自愈反差"
                            u"对仗叙事位·首报→整理→受阻→定谳→自建→实弹受理=「令→报→堵→法→受」递进链·"
                            u"发送阻塞如实呈报=诚实律叙事位〔不谎报发送成功·挂物理件窗〕·v14 集团令批日/"
                            u"v15 雷达令批夜同型=令批盘点先例承继第三件；公众号低创作度条款 7.1-7.4 编辑"
                            u"价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句「不管你用什么方法」任意方法令 vs "
                          u"当窗实弹 250 QUEUED 协议层受理+「STMP 码已经被各种地方都封了」全被封受阻面 vs "
                          u"「邮件协议本无需授权码」方法定谳自愈面+5 行令批 vs 首报+直投双落——F-042 v2 对照"
                          u"数字结构同源第十五证·十五连母题续〔v2 开闸/v3 三线/v4 技能/v5 节目重制/v6 对账夜/"
                          u"v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令/v10 云端 token 机制日/v11 产品优先"
                          u"令日/v12 集团外审日/v13 集团治理日/v14 集团令批日/v15 雷达令批夜/v16 集团首报直投日〕"
                          u"+5/9/1/1/250/12:2x 六组数字/情 1 AI 自治基建自愈吃瓜温和如实非强极点〔G5 吃瓜未来党+"
                          u"G1 信任党双群对位·CEO 一句任意方法令→当窗自建程序直投受理=AI 公司方法自愈叙事面·"
                          u"非强极点〕/时 2 事件 2026-10-06 12:0x 报告令→12:2x 250 QUEUED→本卡 2026-10-06 当日"
                          u"零滞后〔v15 连夜窗 ≈2h 对照=本件同日件更快〕/台 2 公众号方图承载=MC-001~156 S3 实证"
                          u"复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级"
                          u"事件+数字密度）·#67 触发律=编年史事件随轮领〔R1536 直领·入池+出池同轮兑现·"
                          u"R1095/R970 先例〕")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为令批台账读数"
                     u"（行数/整理面数/受理码读数/时点读数=非 token 用量细节非财务非持仓面）+CEO 令原文亲署"
                     u"收件邮箱=令件 verbatim 面非第三方私隐面〔卡面零邮箱呈现·只入 source_facts〕；CEO 指令"
                     u"原文 verbatim 纪实照录；P1 边界=本件=纪实档案非提案非表决（他司执行面细节〔BigMoney "
                     u"题材/经验两令内容/FluxVerse 回收细节〕不入卡面·批级行计数位合法=v14 同型分界）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十六件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build)
report = []
report.append("orders.md 2026-10-06 total rows (machine count) = %d" % len(all_rows))
report.append("orders.md 2026-10-06 CEO-quote rows (machine count) = %d" % len(ceo_quote_rows))
report.append("CEO quote verbatim substring present in orders.md direct-send row: OK")
report.append("fact fragments (8) present in orders.md: OK")
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
io.open(os.path.join(TMP, "em-check-r1536.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V16, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V16, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d all_rows=%d ceo_quote_rows=%d" % (H2_SIZE, len(all_rows), len(ceo_quote_rows)))
