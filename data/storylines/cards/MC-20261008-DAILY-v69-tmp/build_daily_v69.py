# -*- coding: utf-8 -*-
"""MC-20261008-DAILY-v69 build: DAILY (city daily-sign) series SIXTY-NINTH piece (R1703, queue
section-E E30 market-reopen gate redemption). Supply adjudication = R1320/R1321 weekend-face
machine scan registered yanhuo/weekend/13 (market line) as the ONLY remaining weekend-face clean
row, gated for the 2026-10-08 market reopen (MARKET-GATE, r1321_weekend_scan.txt L14 machine
evidence, card-face shingles=0 ZERO); R1694-R1702 declared-idle window carried the standby
registration; THIS round = market-reopen day + post-sunrise daytime window -> redemption with a
DOUBLE hard gate asserted in-build (date == 2026-10-08 AND time >= 05:52; time-gate
mechanization 4th proof after R1321/R1322 sunrise gates + R1388 dusk gate, first date+clock
double-gate piece). Scene heterogeneity R442 spine: market-trading adjudication face (buyer-
seller bargaining fairness) vs business-family v57 tangyuan / v58 noodle-stall vendor-call faces
= same-family heterogeneous; weekend-bucket adjacency = market-reopen literal pairing (NOT the
holiday-state adjacency band v58/v59/v60/v66/v67 - 10-08 Thursday is the first post-holiday
trading day). em ladder = canonical band library (em-budget-ladder.md: 50->46->44->40->36->32->28,
max feasible): quote line 14.00em -> 50 band (budget 18.40em, margins +4.80/+4.40/+5.75em, VERT
gap +284px). Machine source/dedup assertions (R456 system, card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

# --- market-reopen double hard gate (R1320 MARKET-GATE registration: 10-08 reopen; sunrise 05:52)
_now_date = time.strftime("%Y-%m-%d")
_now = time.strftime("%H:%M")
assert _now_date == "2026-10-08", "market-reopen gate: this row is registered for 2026-10-08 reopen day (now %s)" % _now_date
assert _now >= "05:52", "daytime window not open yet (now %s, sunrise gate 05:52) - rerun after sunrise" % _now

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V69 = os.path.join(BASE, "MC-20261008-DAILY-v69")
TMP = V69 + "-tmp"
os.makedirs(V69, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"市场买卖讲价，公平公正正"
AXIS, BUCKET, IDX = u"烟火", u"weekend", 13

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "axes bucket != 18 rows (axes = 6 axes x 12 buckets x 18 rows = 1296)"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
assert pool["axes"][u"烟火"][u"weekend"][7] == u"面条汤滚着呢，爱喝热乎的来碗", "v58 consumed-row structural anchor expected"
assert pool["axes"][u"侠气"][u"weekend"][8] == u"帆起云开，海阔天空", "v59 consumed-row structural anchor expected"
assert pool["axes"][u"逍遥"][u"weekend"][4] == u"檐下观鱼跃，茶室笑谈多", "v60 consumed-row structural anchor expected"
assert pool["sprite"][u"weekend"][3] == u"嗡嗡嗡，晨风中的舞", "v63 consumed-row structural anchor expected"
assert pool["sprite"][u"weekend"][4] == u"叮咚响夜晚", "v64 consumed-row structural anchor expected"
assert pool["axes"][u"秩序"][u"night"][16] == u"别忘了关好自家门", "v65 consumed-row structural anchor expected"
assert pool["axes"][u"怀旧"][u"weekend"][17] == u"听老唱片，忆往昔岁月，时光倒流一二里", "v66 consumed-row structural anchor expected"
assert pool["axes"][u"侠气"][u"weekend"][5] == u"茶余饭后讲讲闲话，才不闷", "v67 consumed-row structural anchor expected"
assert pool["axes"][u"怀旧"][u"dusk"][13] == u"修了这么多伞，可算收工了", "v68 consumed-row structural anchor expected"
assert nb[10] == u"食堂炒菜香飘四方方" and nb[11] == u"邻里街坊亲亲热热热" and nb[12] == u"早点儿出来转转，心气儿顺顺", "reduplication family neighbors expected (pool-verbatim tail note)"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- market-gate registration evidence (R1320/R1321 machine scan, weekend face)
scan = io.open(os.path.join(ROOT, ".c3-tmp", "r1321_weekend_scan.txt"), encoding="utf-8").read()
assert u"[烟火/weekend/13] 市场买卖讲价，公平公正正" in scan, "market-gate registration line missing (r1321_weekend_scan.txt L14)"
assert u"MARKET-GATE 10-08 reopen (R1320); CLEAN 烟火/weekend/13" in scan, "market-gate verdict missing (L14)"

# --- quote-face word probe (r1703_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"市场买卖", u"讲价", u"公平公正", u"买卖", u"公平", u"正正"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1703 quote-face word probe for candidate " + QUOTE_CORE + u" (烟火/weekend/13, market-reopen gate redemption piece)"]
qrep.append(u"market-gate registration machine evidence (r1321_weekend_scan.txt L14, verbatim copy-in for self-contained chain): " +
            u"[烟火/weekend/13] 市场买卖讲价，公平公正正 | card-face-shingles=0 ZERO | spirit-layer=1 市场 | MARKET-GATE 10-08 reopen (R1320); CLEAN 烟火/weekend/13")
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. Market-reopen gate redemption adjudication (R1320/R1321 registration + this round machine verify): (1) weekend-face supply = 烟火/weekend/13 was the ONLY remaining registered clean row, gated for the 10-08 market reopen (R1320 MARKET-GATE, r1321_weekend_scan.txt L14); after v66/v67 fired the two daytime clean rows and v68 fired the dusk row, THIS is the last registered weekend-face row -> after this piece the weekend face is EXHAUSTED (zero clean rows left); (2) selection = registered market-gate redemption, supply-determined, not a fresh rotation-count claim (honest note: post-v68 counts unchanged in axes 烟火 10 -> this piece 11); (3) spirit-layer common word 市场 (scan L14 spirit-layer=1) = harvest-file layer, NOT the R1010 card-face dedup face (v66 时光 single-hit precedent band), card-face shingles = 0 ZERO per scan L14 + this round probe; (4) scene heterogeneity R442: market-trading adjudication face (buyer-seller bargaining fairness, both-party voice) vs business-family v57 tangyuan-stall / v58 noodle-stall vendor-call single-voice faces = same-family heterogeneous third position; (5) weekend-bucket adjacency honest note: 10-08 Thursday = first post-holiday TRADING day (not holiday state) - this row pairs by market-line literal content to the reopen day, NOT by the holiday-state adjacency band v58/v59/v60/v66/v67; (6) reduplication-tail note: 公平公正正 = pool-verbatim (neighbor rows 香飘四方方/亲亲热热热/心气儿顺顺 same-bucket reduplication family, machine-asserted), zero card-side edit; (7) LITERAL morning: post-sunrise production (build gate asserts 2026-10-08 + 05:52) x market-line content x reopen day = triple literal pairing." % (u"all probe words ZERO fleet card-face hits = fully-zero row (series 17th, v53-v68 sixteen-precedent chain)" if allzero else u"NOTE: some probe hits above - honest adjacency adjudication required"))
qrep.append(u"post-v69 supply honest note: weekend face = ZERO clean rows remaining -> weekend face EXHAUSTED; night face double-zero (R1124/R1305) unchanged; dusk face zero clean rows (post-v68 R1388) unchanged; festival face 1 clean row season-gated (R1337) unchanged; unlock windows after this piece = rain-event day / CEO-order day / Nov+ coldsnap / summer heatwave (market_open reopen window REDEEMED by this piece). DAILY honest-pairable face structurally near-exhausted note maintained (pool-expansion report position = status-line not chase).")
io.open(os.path.join(TMP, "r1703_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V69:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 069",
    u"2026-10-08 · 复市首日 · 晨",
    u"「市场买卖讲价，公平公正正」",
    u"——硅基城市台词池 · 烟火轴",
]

SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28]  # canonical band library (em-budget-ladder.md)
MARGIN_EM = 0.2  # zero-margin exclusion law (R293)

H1_GAP = int(cfg["font"]["h1_gap"])
OPT_C = float(cfg["font"]["optical_center"])
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])
PITCH_F = 1.35
GAP_MIN = 20


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
assert H2_SIZE == 50, "em ladder expected 50-band (canonical max band; quote 14.00em vs budget 18.40em margins +4.80/+4.40/+5.75, VERT +284px), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261008-DAILY-v69"
meta["form"] = (u"DAILY 城市日签 069（L-卡 图文轻内容线 DAILY 形态第六十九件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 复市日 market-reopen 门控兑现件 R1703·日签节律续件=日期×情境桶对位判据第六十九证〔**复市日门控位**："
                u"R1320/R1321 weekend 面 fresh 扫描机注册=烟火/weekend/13 市场行 MARKET-GATE 10-08 reopen〔r1321_weekend_scan.txt L14 机证·"
                u"card-face shingles=0 ZERO〕→R1694-R1702 declared-idle 窗全程挂账承继〔历轮车道注记承继〕→本轮复市日+日出窗开后兑现〔build 内"
                u"**双硬闸 assert 日期==2026-10-08+日出 05:52**·时间闸机制化第四证=R1321/R1322 日出闸+R1388 傍晚闸先例带后首个日期+时刻双闸件〕"
                u"+**卡面级零撞行**〔r1321 L14 shingles=0+本轮六词 probe 机核 r1703_quote_face.txt〕+**市场行 literal 对位诚实注**：本行入选="
                u"复市日×市场行内容 literal 直配〔MARKET-GATE 注册依据〕·weekend 桶=池结构位·非假日态邻接〔v58/v59/v60/v66/v67 假日态先例带"
                u"区分注·10-08 周四=假期后首个工作交易日〕+**市集生意族带异质诚实注**：v57 煮汤圆生意面+v58 面摊叫卖面=摊主单声口叫卖/"
                u"生意面→本件=买卖双方讲价交易判准面〔场景异质 R442·族内第三异质位〕+**叠词收尾=池行 verbatim 零改字**〔同桶 line10 香飘四方方/"
                u"line11 亲亲热热热/line12 心气儿顺顺 叠词族·「公正正」=池句原文非卡面笔误·build 内邻行结构锚断言〕〕）+最数字化的城市"
                u"〔一切皆数据·行情在屏幕上飞〕×最老派的市场人情〔讲价还价的你来我往〕=**快×慢/数据×人情双反差金句位**〔族五十六连·"
                u"讲价位语感独占注=数据城市里最市井的一声讲价〕+「公平公正正」叠词判词式收尾=人味命中")
meta["source_quote"] = u"「市场买卖讲价，公平公正正」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][weekend][13]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-08.md（当日日期语境源·国庆假期后首个交易日·周四·日出后晨间生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][weekend][13] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 18 行计数+axes 6 轴"
                         u"结构断言〔R982〕+v58 烟火 weekend/7+v59 侠气 weekend/8+v60 逍遥 weekend/4+v63/v64 sprite "
                         u"weekend/3·4+v65 秩序 night/16+v66 怀旧 weekend/17+v67 侠气 weekend/5+v68 怀旧 dusk/13"
                         u"**九已耗行结构锚**+叠词族邻行锚〔line10/11/12〕）②日期行 2026-10-08=当日历法事实·周四+国庆"
                         u"假期后首个交易日复市日〔daily brief 2026-10-08 当日窗语境〕+晨标记〔日出 ~05:52 后日间窗生产·"
                         u"v63/v66/v67 晨标记先例带·literal 晨〕③情境=复市日市场行 literal 对位件〔R1320 MARKET-GATE 注册→"
                         u"R1694-R1702 挂账承继→本轮复市日兑现·r1321_weekend_scan.txt L14 机证+build 内双硬闸断言〕"
                         u"④轴级署名=台词池烟火轴行·本行无称谓面=纯市场口气句·泛称零涉及〔人设权红线零接触·charter §2.4·"
                         u"v5/v17/v21/v53/v65/v66/v67 先例族〕⑤去重断言=本行不在 city-spirit.md 已采面+不在全成品卡面 lines/"
                         u"source_quote 任一（卡面级实扫=R1010 修正律）+「市场买卖」「讲价」「公平公正」「买卖」「公平」"
                         u"「正正」全句 probe 六词机核〔r1703_quote_face.txt·L14 gate 行 verbatim 抄录入证据件=链自足〕"
                         u"+诚实注=spirit 采面层「市场」共用词 1 处〔scan L14 spirit-layer=1·非卡面级去重面·v66「时光」同型带〕"
                         u"⑥季相核=本行无年味/春联/寒潮类季相错位词〔R972 制·市场买卖=四季通用市井面·十月秋晨兼容〕"
                         u"⑦叠词收尾=池行 verbatim 零改字〔「公正正」=池句原文·同桶叠词族三邻行结构锚断言在位〕"
                         u"⑧品牌语感注=「讲价」「公平公正正」市井口语+叠词判词收尾=去 AI 感对位·人味命中·零书面套语·无品牌无消费宣称")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 署名律"
                             u"+人设权红线·本行无称谓面=纯市场口气句·泛称零涉及〔v5/v17/v21/v53/v65/v66/v67 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（复市日门控兑现+快×慢/数据×人情双反差"
                            u"金句位〔族五十六连·讲价位语感独占注〕+叠词判词式市井人味=语录卡线变体零新模板"
                            u"第六十九证（QUOTE-v2 参数 verbatim 复用·h2_size 50 档=canonical ladder 最大可行档"
                            u"〔em-budget-ladder.md 判例库正典 50→28·引文行 14.00em 驱动·预算 18.40em margin +4.40em·"
                            u"VERT 四行栈 R381 gap +284px〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款"
                            u" 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔复市"
                            u"清晨数据城市里最市井的一声讲价=城市活得有人味的活证据〕+post-v69 供给注：**weekend 面=零"
                            u"干净行=weekend 桶面枯竭**〔夜面双归零 R1124/R1305+dusk 面零干净行 R1388 承继·festival 面 1 行"
                            u"季相门控 R1337〕·解锁窗=雨事件日/CEO 令日/Nov+ 寒潮/夏季 heatwave〔market_open 复市窗=本件"
                            u"兑毕〕·池扩容呈报位维持〔呈现状行不催办〕+F 序号诚实注=本件先落 F-165·REACT-v12 预指位"
                            u"顺延 F-166〔R978 判例·finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：最数字化的城市〔一切皆数据·行情在屏幕上飞〕"
                          u"×最老派的市场人情〔讲价还价的你来我往〕=快×慢/数据×人情反差+大交易所〔一切皆有行情〕×"
                          u"小摊位〔讲价讲的是公平〕=大×小反差〔族五十六连·讲价位语感独占注=数据城市里最市井的一声讲价〕"
                          u"+「公平公正正」叠词判词收尾=人味命中/情 1 复市清晨头一桩买卖成交的踏实温和共鸣如实非强极点"
                          u"〔G1 城市生活群〕/时 2 当日=2026-10-08 周四国庆假期后首个交易日·日出后晨间窗 literal 生产〔build 内"
                          u"双硬闸 assert 2026-10-08+05:52〕×市场行内容×复市日三重 literal 对位〔MARKET-GATE R1320 注册→"
                          u"R1694-R1702 挂账承继→复市日兑现〕/台 2 公众号方图承载=MC-001~155 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1703 复市日"
                          u"门控兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=市场口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名=人设权红线零接触（本行无称谓面=纯市场口气句·泛称零"
                     u"涉及）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（讲价=交易动作意象非消费宣称·无品牌无"
                     u"价格·「公平公正」=市井信条面非金融宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十九件·charter v1.2 §4 形态码 DAILY·日签节律续件·复市日 market-reopen 门控兑现件·烟火轴 weekend 桶市场行·weekend 面收官件注记）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[烟火][weekend][13] verbatim OK; weekend bucket=18 rows; axes 6 structure (R982); "
              "v58 weekend/7 + v59 weekend/8 + v60 weekend/4 + v63/v64 sprite weekend/3,4 + v65 night/16 + v66 weekend/17 + v67 weekend/5 + v68 dusk/13 consumed-row structural anchors; "
              "reduplication-family neighbor anchors line10/11/12; market-gate registration r1321_weekend_scan.txt L14 asserted; "
              "card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v68; "
              "market-reopen double gate: date==2026-10-08 asserted + sunrise 05:52 asserted; production time %s (post-sunrise literal morning, reopen day)" % time.strftime("%Y-%m-%d %H:%M:%S"))
report.append(u"H1 %d budget %.2fem | H2 %d budget %.2fem (ladder pick, margin>=%.1fem) | VERT stack bottom %.0fpx vs subs top %dpx gap %+.0fpx (need >=%d) R381" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM, stack_bottom(H2_SIZE, len(LINES) - 1), SUBS_TOP, SUBS_TOP - stack_bottom(H2_SIZE, len(LINES) - 1), GAP_MIN))
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
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
report.append("LADDER_50: quote line 14.00em driver (canonical band library em-budget-ladder.md 50->46->44->40->36->32->28 max-feasible pick; 50-band budget 18.40em margins +4.80/+4.40/+5.75em; four-LINES stack VERT +284px); all other QUOTE-v2 params verbatim; market-reopen double-gate + supply-determined + scene-heterogeneity + reduplication-verbatim honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1703.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V69, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V69, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63/v64/v65/v66/v67/v68 review precedent)
forms = {}
png_in_dirs = 0
for d in sorted(os.listdir(BASE)):
    if os.path.isdir(os.path.join(BASE, d)) and d.startswith("MC-"):
        for form in ("QUOTE", "DIGEST", "CENSUS", "REACT", "DAILY"):
            if ("-" + form + "-") in d:
                forms[form] = forms.get(form, 0) + 1
                break
        if os.path.isfile(os.path.join(BASE, d, d + ".png")):
            png_in_dirs += 1
flat_png = len([f for f in os.listdir(BASE) if f.endswith(".png") and os.path.isfile(os.path.join(BASE, f))])
print("FORMS: " + json.dumps(forms) + " | png-in-dirs=%d flat-png=%d" % (png_in_dirs, flat_png))

# --- E4 audience reference call (async detached, 1500s window, v51-v68 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (canonical ladder 50, quote-line driver) + E4 fired async" % H2_SIZE)
