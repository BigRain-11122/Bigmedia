# -*- coding: utf-8 -*-
"""MC-20261005-DAILY-v67 build: DAILY (city daily-sign) series SIXTY-SEVENTH piece (R1322, queue
section-E E30 daytime-window second-seat standby). Supply adjudication = R1321 post-v66 honest
note machine-registered: weekend face remaining = 侠气/weekend/5 (daytime standby, THIS round) +
烟火/weekend/13 (10-08 market-reopen gate); all other weekend rows = card-face shingle collisions
(r1321_weekend_scan.txt L75/L114/L115 machine evidence). Selection = supply-determined
second-seat (R1321 rotation count: 怀旧 was unique-least axis and fired as v66; 侠气/5 is the
only remaining weekend-face clean daytime row -> fires THIS round, same daytime window, same
holiday-Monday adjacency band). Scene heterogeneity R442 spine: v59 侠气 = 帆起云开 night-boat
outdoor sea/sky face -> THIS = 茶余饭后居家闲话 indoor social-chat face = scene-heterogeneous;
vs same-day v66 怀旧 (solitary listening) = axis + scene double-heterogeneous. Daytime-window
hard gate (sunrise 05:52) asserted in-build. em ladder = canonical band library
(em-budget-ladder.md: 50->46->44->40->36->32->28, max feasible): quote line 14.00em -> 50 band
(budget 18.40em, margins +4.80/+4.40/+5.75em, VERT gap +284px). Machine source/dedup assertions
(R456 system, card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

# --- daytime-window hard gate (R1320 registered unlock: sunrise ~05:52 on 2026-10-05)
_now = time.strftime("%H:%M")
assert _now >= "05:52", "daytime window not open yet (now %s, sunrise gate 05:52) - rerun after sunrise" % _now

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V67 = os.path.join(BASE, "MC-20261005-DAILY-v67")
TMP = V67 + "-tmp"
os.makedirs(V67, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"茶余饭后讲讲闲话，才不闷"
AXIS, BUCKET, IDX = u"侠气", u"weekend", 5

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
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- weekend-face supply adjudication evidence (R1321 post-v66 second-seat registration)
scan = io.open(os.path.join(ROOT, ".c3-tmp", "r1321_weekend_scan.txt"), encoding="utf-8").read()
assert u"CLEAN 侠气/weekend/5" in scan, "second-seat standby registration line missing (r1321_weekend_scan.txt L75)"
assert u"weekend-face clean daytime rows (R1320 verdict confirmed by machine shingle scan)" in scan, "clean-rows verdict line missing (L114)"
assert u"SELECT 怀旧/weekend/17" in scan, "rotation-law selection line missing (L115)"

# --- quote-face word probe (r1322_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"茶余饭后", u"讲讲闲话", u"闲话", u"才不闷", u"茶余", u"饭后"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1322 quote-face word probe for candidate " + QUOTE_CORE + u" (侠气/weekend/5, daytime-window second-seat piece)"]
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. Daytime-window second-seat adjudication (R1321 post-v66 registration + this round machine verify): (1) weekend face supply = 侠气/weekend/5 ONLY remaining clean daytime row (R1321 honest note: 怀旧/17 fired as v66 first-seat; 烟火/13 = 10-08 market-reopen gate; other weekend rows 3-17 = card-face shingle collisions r1321_weekend_scan.txt); (2) selection = supply-determined second-seat, not a fresh rotation-count claim (honest note: post-v66 counts 求新 10/烟火 10/侠气 10/秩序 10/怀旧 10/逍遥 11/sprite 5 - 侠气 NOT unique-least; the row fires because it is the only remaining registered daytime supply); (3) spirit-layer 2 hits (才不 / ，才) = harvest-file layer common words, NOT the R1010 card-face dedup face (v66 时光 single-hit precedent band), card-face shingles = 0 ZERO per r1321_weekend_scan L75; (4) scene heterogeneity R442: v59 侠气 = 夜航船户外海天面 -> THIS = 居家茶余饭后室内闲话面 = scene-heterogeneous; vs same-day v66 怀旧 (独处听唱片) = axis + scene double-heterogeneous; same-day 3-piece day precedent = 10-03 (v62 morning + v63 + v64); (5) weekend bucket on Monday holiday = 假日态 adjacency (v58/v59/v60/v66 direct precedent), two consecutive weekend-face pieces (v66+v67) = back-to-back same-face precedent v58/v59 (R1029), saturation honest note: after THIS, weekend face = 烟火/13 gated row ONLY -> face exhausted for daytime window; (6) LITERAL daytime: post-sunrise morning production (~06:2x) x holiday-home content x 侠气轴闲话声口." % (u"all probe words ZERO fleet card-face hits = fully-zero row (series 15th, v53-v66 fourteen-precedent chain)" if allzero else u"NOTE: some probe hits above - honest adjacency adjudication required"))
qrep.append(u"post-v67 supply honest note: weekend face remaining = 烟火/weekend/13 ONLY (10-08 market-reopen gate) -> weekend face EXHAUSTED for the daytime window; night face double-zero (R1124/R1305) unchanged; unlock windows unchanged: rain-event day / CEO-order day / 10-08 market reopen / Nov+ coldsnap / summer heatwave. DAILY honest-pairable face structurally near-exhausted note maintained (pool-expansion report position = status-line not chase).")
io.open(os.path.join(TMP, "r1322_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V67:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 067",
    u"2026-10-05 · 国庆假期 · 晨",
    u"「茶余饭后讲讲闲话，才不闷」",
    u"——硅基城市台词池 · 侠气轴",
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
meta["topic"] = "MC-20261005-DAILY-v67"
meta["form"] = (u"DAILY 城市日签 067（L-卡 图文轻内容线 DAILY 形态第六十七件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 日间窗次席 standby 兑现件 R1322·日签节律续件=日期×情境桶对位判据第六十七证〔**日间窗次席位**："
                u"R1321 post-v66 供给诚实注机注册=weekend 面余 侠气/weekend/5 单行日间 standby+烟火/13=10-08 复市门控"
                u"〔余行 3-17 卡面撞 r1321_weekend_scan.txt L114〕→本轮日出后日间窗续领兑现〔build 脚本内日出硬闸 assert 05:52·"
                u"生产 ~06:2x literal 日间晨〕+**选取=供给定谳次席位**（诚实注：post-v66 机数 求新 10/烟火 10/侠气 10/"
                u"秩序 10/怀旧 10/逍遥 11/sprite 5——侠气非唯一最少轴·本行入选=日间注册供给面仅剩单行〔非旋转律新计〕〕"
                u"+**卡面级零撞行**〔r1321_weekend_scan L75 shingles=0 ZERO+本轮六词 probe 机核〕+**假日态邻接诚实注**："
                u"周一国庆假期第 5 天=非工作日=weekend 桶假日常态对位〔v58/v59/v60/v66 先例带·非 literal weekend 直配〕"
                u"+v66+v67 背靠背同面双件=v58/v59 先例（R1029）·本件后 weekend 面=烟火/13 门控行单行=日间窗面枯竭诚实注"
                u"+**场景异质反同构**：v59 侠气=夜航船户外海天面→本件=居家茶余饭后室内闲话面〔R442 主线维持〕·"
                u"vs 同日 v66 怀旧（独处听唱片）=轴+场景双异质·同日三件先例=10-03 v62/v63/v64〕）+最数字化的城市"
                u"〔一切皆数据·跑得最快〕×最不着急的居家消遣〔茶余饭后一句闲话〕=**快×慢反差金句位**〔族五十四连·"
                u"闲话位语感独占注=数据城市里最慢的一声闲话〕+「才不闷」口语直判收尾=判词式人味命中")
meta["source_quote"] = u"「茶余饭后讲讲闲话，才不闷」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[侠气][weekend][5]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-05.md（当日日期语境源·国庆假期第 5 天·周一·日出后晨间生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[侠气][weekend][5] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 18 行计数+axes 6 轴"
                         u"结构断言〔R982〕+v58 烟火/7+v59 侠气/8+v60 逍遥/4+v63/v64 sprite weekend/3·4+v65 秩序"
                         u"night/16+v66 怀旧 weekend/17 七已耗行结构锚）②日期行 2026-10-05=当日历法事实·周一+国庆"
                         u"假期第 5 天〔daily brief 2026-10-05 当日窗语境〕+晨标记〔日出 ~05:52 后日间窗生产·v63/v66 "
                         u"晨标记先例带·literal 晨〕③情境=日间窗次席 standby 兑现件〔R1321 post-v66 注册→本轮续领兑现·"
                         u"r1321_weekend_scan.txt L75/L114/L115 机证承继〕④轴部署名=台词池侠气轴行·本行无称谓面=纯生活"
                         u"口气句·泛称零涉及〔人设权红线零接触·charter §2.4·v5/v17/v21/v53/v65/v66 先例族〕⑤去重断言="
                         u"本行不在 city-spirit.md 已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律）"
                         u"+「茶余饭后」「讲讲闲话」「闲话」「才不闷」「茶余」「饭后」全句 probe 六词机核"
                         u"〔r1322_quote_face.txt〕+诚实注=spirit 采面层「才不」「，才」二常用词共用〔city-spirit.md 信条例"
                         u"行·非卡面级去重面·v66「时光」单词同型带〕⑥季相核=本行无年味/春联/寒潮类季相错位词〔R972 制·"
                         u"茶余饭后闲话=四季通用日间居家面·十月秋晨兼容〕⑦品牌语感注=「茶余饭后」「才不闷」口语+判词"
                         u"收尾=去 AI 感对位·人味命中·零书面套语·无品牌无消费宣称")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·侠气轴）——池行无逐民署名·禁虚构居民名（charter v1.2 署名律"
                             u"+人设权红线·本行无称谓面=纯生活口气句·泛称零涉及〔v5/v17/v21/v53/v65/v66 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（日间窗次席 standby 兑现+同日三件节律"
                            u"〔**供给面诚实注**：R1321 post-v66 注册次席位→本轮兑现·weekend 面本件后=烟火/13 门控行"
                            u"单行=日间窗面枯竭〔r1321_weekend_scan L114〕·夜面双归零〔R1124/R1305〕承继〕+快×慢反差"
                            u"金句位〔族五十四连·闲话位语感独占注〕+「才不闷」判词式口语人味=语录卡线变体零新模板"
                            u"第六十七证（QUOTE-v2 参数 verbatim 复用·h2_size 50 档=canonical ladder 最大可行档"
                            u"〔em-budget-ladder.md 判例库正典 50→28·引文行 14.00em 驱动·预算 18.40em margin +4.40em·"
                            u"VERT 四行栈 R381 gap +284px〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款"
                            u"7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔假期"
                            u"清晨数据城市里最不着急的一声闲话=城市活得有人味的活证据〕+post-v67 指针：解锁窗维持="
                            u"雨事件日/CEO 令日/10-08 market_open 复市〔烟火/13〕/Nov+ 寒潮/夏季 heatwave·"
                            u"REACT-v9 10-06 窗·F 序号诚实注=本件先落 F-154·REACT-v9 预指位顺延 F-155〔R978 判例 "
                            u"finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：最数字化的城市〔一切皆数据·机队与系统跑得"
                          u"最快〕×最不着急的居家消遣〔茶余饭后讲闲话〕=快×慢反差〔族五十四连·闲话位语感独占注〕"
                          u"+台账里跑大事〔城市一切皆账〕×闲话里过日子〔街坊茶余饭后〕=公事×人情反差+「才不闷」"
                          u"口语直判收尾=判词式人味命中/情 1 假日居家街坊闲话的温和共鸣如实非强极点〔G1 城市生活群〕"
                          u"/时 2 当日=2026-10-05 周一国庆假期第 5 天·日出后晨间窗 literal 生产〔~06:2x·日间窗次席位"
                          u"续领〕×假日态居家内容×weekend 桶假日常态邻接〔v58/v59/v60/v66 先例带〕/台 2 公众号方图"
                          u"承载=MC-001~152 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R1322 日间窗次席兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名=人设权红线零接触（本行无称谓面=纯生活口气句·泛称零"
                     u"涉及〔v5/v17/v21/v53/v65/v66 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（茶余饭后=生活时段意象非消费宣称·无品牌无价格）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十七件·charter v1.2 §4 形态码 DAILY·日签节律续件·日间窗次席 standby 兑现件·侠气轴 weekend 桶假日态邻接件·v66+v67 背靠背同面双件注记）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[侠气][weekend][5] verbatim OK; weekend bucket=18 rows; axes 6 structure (R982); "
              "v58 weekend/7 + v59 weekend/8 + v60 weekend/4 + v63/v64 sprite weekend/3,4 + v65 night/16 + v66 weekend/17 consumed-row structural anchors; "
              "card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v66; "
              "daytime-window second-seat: R1321 post-v66 registration (侠气/5 = only remaining weekend-face clean daytime row) -> this round redemption; "
              "quote-face word probe: 6 words see r1322_quote_face.txt; production time %s (post-sunrise literal daytime)" % time.strftime("%Y-%m-%d %H:%M:%S"))
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
report.append("LADDER_50: quote line 14.00em driver (canonical band library em-budget-ladder.md 50->46->44->40->36->32->28 max-feasible pick; 50-band budget 18.40em margins +4.80/+4.40/+5.75em; four-LINES stack VERT +284px); all other QUOTE-v2 params verbatim; daytime-window second-seat + supply-determined + scene-heterogeneity honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1322.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V67, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V67, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63/v64/v65/v66 review precedent)
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

# --- E4 audience reference call (async detached, 1500s window, v51-v66 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (canonical ladder 50, quote-line driver) + E4 fired async" % H2_SIZE)
