# -*- coding: utf-8 -*-
"""MC-20261005-DAILY-v68 build: DAILY (city daily-sign) series SIXTY-EIGHTH piece (R1388, queue
section-E E30 dusk-window standby redemption). Supply adjudication = R1337 fresh dusk-face scan
(r1337_dusk_scan.txt: 123 rows machine-scanned -> exactly 1 CLEAN row 怀旧/dusk/13) registered as
dusk-window standby with a ~18:00 time gate; gate held through the declared-idle window
R1338-R1387 (five-checks fresh, lane notes carried every round); THIS round redeems after the
gate opens. Selection = supply-determined seat (R1322 v67 precedent): the row fires because it
is the only dusk-face clean row, not a fresh rotation-count claim (post-v67 counts: 求新 10/
烟火 10/侠气 10/秩序 10/逍遥 11/怀旧 10->11 after this/sprite 5). Honest adjacency: 伞 craft
motif family = v22 修伞铺节日凑热闹面 -> THIS 傍晚收工面 = same-craft-family heterogeneous
(scene+bucket+time-of-day all different); same-day same-axis double = v66 怀旧晨 + THIS 怀旧傍晚
= one-day-two-signs time-of-day pair (scene heterogeneous: 听唱片室内独处 -> 修伞摊劳作收工).
Dusk-window hard gate (18:00, sunset anchor ~17:37 R1123) asserted in-build. em ladder =
canonical band library (em-budget-ladder.md: 50->46->44->40->36->32->28, max feasible): quote
line 14.00em -> 50 band (budget 18.40em). Machine source/dedup assertions (R456 system,
card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

# --- dusk-window hard gate (R1337 standby registration: dusk window opens ~18:00; sunset ~17:37 R1123)
_now = time.strftime("%H:%M")
assert _now >= "18:00", "dusk window not open yet (now %s, gate 18:00) - rerun at/after 18:00" % _now

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V68 = os.path.join(BASE, "MC-20261005-DAILY-v68")
TMP = V68 + "-tmp"
os.makedirs(V68, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"修了这么多伞，可算收工了"
AXIS, BUCKET, IDX = u"怀旧", u"dusk", 13

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "axes bucket != 18 rows (axes = 6 axes x 12 buckets x 18 rows = 1296)"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
assert pool["axes"][u"逍遥"][u"dusk"][6] == u"夕阳西下鱼也归巢了", "v56 consumed-row structural anchor expected (dusk face)"
assert pool["axes"][u"怀旧"][u"festival"][12] == u"修伞铺也要来凑个热闹", "v22 consumed-row structural anchor expected (伞 motif family anchor)"
assert pool["axes"][u"烟火"][u"weekend"][7] == u"面条汤滚着呢，爱喝热乎的来碗", "v58 consumed-row structural anchor expected"
assert pool["axes"][u"侠气"][u"weekend"][8] == u"帆起云开，海阔天空", "v59 consumed-row structural anchor expected"
assert pool["axes"][u"逍遥"][u"weekend"][4] == u"檐下观鱼跃，茶室笑谈多", "v60 consumed-row structural anchor expected"
assert pool["sprite"][u"weekend"][3] == u"嗡嗡嗡，晨风中的舞", "v63 consumed-row structural anchor expected"
assert pool["sprite"][u"weekend"][4] == u"叮咚响夜晚", "v64 consumed-row structural anchor expected"
assert pool["axes"][u"秩序"][u"night"][16] == u"别忘了关好自家门", "v65 consumed-row structural anchor expected"
assert pool["axes"][u"怀旧"][u"weekend"][17] == u"听老唱片，忆往昔岁月，时光倒流一二里", "v66 consumed-row structural anchor expected"
assert pool["axes"][u"侠气"][u"weekend"][5] == u"茶余饭后讲讲闲话，才不闷", "v67 consumed-row structural anchor expected"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- dusk-face supply adjudication evidence (R1337 fresh scan registration, held to this round)
scan = io.open(os.path.join(ROOT, ".c3-tmp", "r1337_dusk_scan.txt"), encoding="utf-8").read()
assert u"[怀旧/dusk/13] 修了这么多伞，可算收工了 | card-face-shingles=0 ZERO" in scan, "clean-row line missing (r1337_dusk_scan.txt)"
assert u"dusk-face CLEAN rows: 怀旧/dusk/13 修了这么多伞，可算收工了" in scan, "CLEAN verdict line missing"

# --- quote-face word probe (r1388_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"修了这么多伞", u"可算收工了", u"修了", u"收工", u"可算", u"多伞"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1388 quote-face word probe for candidate " + QUOTE_CORE + u" (怀旧/dusk/13, dusk-window standby redemption piece)"]
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. Dusk-window standby redemption adjudication (R1337 registration + this round machine verify): (1) supply = R1337 fresh dusk-face scan 123 rows -> exactly 1 CLEAN row 怀旧/dusk/13 (r1337_dusk_scan.txt machine evidence), registered as dusk-window standby with ~18:00 gate, held through declared-idle window R1338-R1387 (lane note carried every round), redeemed THIS round after gate open (build hard-assert 18:00; production ~18:0x literal dusk); (2) selection = supply-determined seat (R1322 v67 precedent): the row fires because it is the only dusk-face clean row, NOT a rotation-count claim (honest: post-v67 counts 求新 10/烟火 10/侠气 10/秩序 10/逍遥 11/sprite 5, 怀旧 10->11 after this - 怀旧 not unique-least); (3) spirit-layer 3 hits (了这/伞，/，可) = harvest-file layer common 2-gram words, NOT the R1010 card-face dedup face (v66 时光/v67 才不 precedent band), card-face shingles = 0 ZERO per r1337_dusk_scan; (4) 伞 craft-motif family honest adjacency: v22 怀旧/festival/12 修伞铺节日凑热闹面 -> THIS 傍晚收工静面 = same-craft-family heterogeneous (bucket festival->dusk, scene 热闹凑节->收工收摊, time-of-day 节日白昼->傍晚; v22 build-anchor asserted); (5) same-day same-axis double honest note: v66 怀旧晨间听唱片 + THIS 怀旧傍晚修伞收工 = one-day-two-signs time-of-day pair (10-03 v62/v63/v64 three-piece-day precedent), scene heterogeneous (室内独处声音面 -> 摊头劳作收工面, R442 spine); (6) LITERAL dusk: ~18:0x production (post-sunset anchor ~17:37 R1123) x 傍晚收工内容 x dusk 桶三重 literal 对位; (7) post-v68 supply honest note: dusk face = 0 clean rows remaining (face exhausted), unlock windows unchanged: rain-event day / CEO-order day / 10-08 market reopen (烟火/13 weekend gated row) / Nov+ coldsnap / summer heatwave; festival face = 1 clean row 季相门控 (R1337 registration, window not yet); night face double-zero (R1124/R1305) - DAILY honest-pairable face structurally near-exhausted note maintained (pool-expansion report position = status-line not chase)." % (u"all probe words ZERO fleet card-face hits = fully-zero row (series 16th, v53-v67 fifteen-precedent chain)" if allzero else u"NOTE: some probe hits above - honest adjacency adjudication required"))
io.open(os.path.join(TMP, "r1388_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V68:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 068",
    u"2026-10-05 · 国庆假期 · 傍晚",
    u"「修了这么多伞，可算收工了」",
    u"——硅基城市台词池 · 怀旧轴",
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
assert H2_SIZE == 50, "em ladder expected 50-band (canonical max band; quote 14.00em vs budget 18.40em margins +3.80/+4.40/+5.75, VERT +284px), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261005-DAILY-v68"
meta["form"] = (u"DAILY 城市日签 068（L-卡 图文轻内容线 DAILY 形态第六十八件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 傍晚窗 standby 兑现件 R1388·日签节律续件=日期×情境桶对位判据第六十八证〔**傍晚窗 standby 位**："
                u"R1337 dusk 面 fresh 扫 123 行→唯一 CLEAN 行 怀旧/dusk/13〔r1337_dusk_scan.txt 机证·card-face shingles=0 ZERO〕"
                u"=傍晚窗 standby 注册〔~18:00 时间闸·R1337 注册→R1338-R1387 declared-idle 窗全程挂账承继〕→本轮闸开后兑现"
                u"〔build 内硬闸 assert 18:00·生产 ~18:0x literal 傍晚·日落锚 ~17:37 R1123〕+**选取=供给定谳席位**"
                u"（诚实注：post-v67 机数 求新 10/烟火 10/侠气 10/秩序 10/逍遥 11/sprite 5·怀旧 10→本件后 11——怀旧非唯一最少轴·"
                u"本行入选=傍晚窗注册供给面唯一干净行〔供给定谳非旋转律新计·R1322 v67 先例〕〕+**卡面级零撞行**"
                u"〔r1337_dusk_scan shingles=0 ZERO+本轮六词 probe 机核〕+**伞匠艺母题族诚实注**：v22 怀旧/festival/12 修伞铺节日"
                u"凑热闹面→本件=傍晚收工静面〔同匠艺族异质：桶 festival→dusk·场景凑节→收摊·时点节日白昼→傍晚·v22 结构锚 build 内断言〕"
                u"+**同日同轴双件诚实注**：v66 怀旧晨间听唱片+本件怀旧傍晚修伞收工=一日两签时点对位〔10-03 v62/v63/v64 同日三件先例〕"
                u"·场景异质=室内独处声音面→摊头劳作收工面〔R442 主线维持〕〕）+最数字化的城市〔一切皆数据·机队与系统跑得最快〕"
                u"×最老派的匠艺收工〔修了这么多伞的一日劳作〕=**快×慢反差金句位**〔族五十五连·收工位语感独占注=数据城市里"
                u"最手艺人的一声收工〕+「可算」口语直判收尾=松快人味命中")
meta["source_quote"] = u"「修了这么多伞，可算收工了」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][dusk][13]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-05.md（当日日期语境源·国庆假期第 5 天·周一·日落后傍晚窗生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][dusk][13] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+dusk 桶 18 行计数+axes 6 轴"
                         u"结构断言〔R982〕+v56 逍遥 dusk/6+v22 怀旧 festival/12〔伞匠艺族锚〕+v58 烟火 weekend/7+v59 侠气"
                         u"weekend/8+v60 逍遥 weekend/4+v63/v64 sprite weekend/3·4+v65 秩序 night/16+v66 怀旧 weekend/17"
                         u"+v67 侠气 weekend/5 十一已耗行结构锚）②日期行 2026-10-05=当日历法事实·周一+国庆假期第 5 天"
                         u"〔daily brief 2026-10-05 当日窗语境〕+傍晚标记〔~18:0x 日落后傍晚窗生产·v51 「· 夜」标记先例带·"
                         u"literal 傍晚〕③情境=傍晚窗 standby 兑现件〔R1337 注册→R1338-R1387 挂账承继→本轮闸开后兑现·"
                         u"r1337_dusk_scan.txt 机证〕④轴部署名=台词池怀旧轴行·本行无称谓面=纯手艺人口气句·泛称零涉及"
                         u"〔人设权红线零接触·charter §2.4·v5/v17/v21/v53/v65/v66/v67 先例族〕⑤去重断言=本行不在 city-spirit.md"
                         u" 已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律）+「修了这么多伞」「可算收工了」"
                         u"「修了」「收工」「可算」「多伞」全句 probe 六词机核〔r1388_quote_face.txt〕+诚实注=spirit 采面层"
                         u"「了这」「伞，」「，可」三常用二字组共用〔city-spirit.md 信条例行·非卡面级去重面·v66「时光」单词同型带〕"
                         u"⑥季相核=本行无年味/春联/寒潮类季相错位词〔R972 制·修伞收工=四季通用匠艺日常面·十月秋傍晚兼容〕"
                         u"⑦品牌语感注=「修了这么多伞」「可算」口语+松快直判收尾=去 AI 感对位·人味命中·零书面套语·"
                         u"无品牌无消费宣称")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 署名律"
                             u"+人设权红线·本行无称谓面=纯手艺人口气句·泛称零涉及〔v5/v17/v21/v53/v65/v66/v67 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（傍晚窗 standby 兑现+同日两签节律"
                            u"〔**供给面诚实注**：R1337 注册→本轮兑现·dusk 面本件后=零干净行=傍晚面枯竭〔r1337_dusk_scan〕"
                            u"·夜面双归零〔R1124/R1305〕·festival 面 1 干净行季相门控〔R1337 注册〕·weekend 面 烟火/13=10-08"
                            u" 复市门控行承继〕+快×慢反差金句位〔族五十五连·收工位语感独占注〕+「可算」松快判词式口语人味"
                            u"=语录卡线变体零新模板第六十八证（QUOTE-v2 参数 verbatim 复用·h2_size 50 档=canonical ladder"
                            u"最大可行档〔em-budget-ladder.md 判例库正典 50→28·引文行 14.00em 驱动·预算 18.40em"
                            u" margin +4.40em·VERT 四行栈 R381 gap +284px〕·charter §1「日签变体随时可续」兑现）·"
                            u"公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令"
                            u" O-20260928-1910 对位〔假期傍晚数据城市里最老派的一声收工=城市活得有人味的活证据〕"
                            u"+post-v68 指针：解锁窗维持=雨事件日/CEO 令日/10-08 market_open 复市〔烟火/13〕/Nov+ 寒潮/"
                            u"夏季 heatwave·REACT-v9 10-06 窗·F 序号诚实注=本件先落 F-155·REACT-v9 预指位顺延 F-156"
                            u"〔R978 判例 finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：最数字化的城市〔一切皆数据·机队与系统跑得最快〕"
                          u"×最老派的匠艺收工〔修了这么多伞的一日劳作〕=快×慢反差〔族五十五连·收工位语感独占注=数据城市里"
                          u"最手艺人的一声收工〕+节日满城看灯的闲〔假期游人如织〕×老匠人一天劳作后收工的踏实〔可算收工了〕"
                          u"=闲×劳反差+「可算」口语直判收尾=松快人味命中/情 1 傍晚收工的踏实温和共鸣如实非强极点〔G1 城市生活群〕"
                          u"/时 2 当日=2026-10-05 周一国庆假期第 5 天·日落后傍晚窗 literal 生产〔~18:0x·傍晚窗 standby 位兑现〕"
                          u"×dusk 桶傍晚收工内容×三重 literal 对位/台 2 公众号方图承载=MC-001~154 S3 实证复用）"
                          u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·"
                          u"queue §E E30 R1388 傍晚窗兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名=人设权红线零接触（本行无称谓面=纯手艺人口气句·泛称零"
                     u"涉及〔v5/v17/v21/v53/v65/v66/v67 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（修伞=匠艺劳作意象非消费宣称·无品牌无价格）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十八件·charter v1.2 §4 形态码 DAILY·日签节律续件·傍晚窗 standby 兑现件·怀旧轴 dusk 桶首件·同日两签 v66+v68 时点对位注记）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[怀旧][dusk][13] verbatim OK; dusk bucket=18 rows; axes 6 structure (R982); "
              "v56 dusk/6 + v22 festival/12 (伞 motif anchor) + v58 weekend/7 + v59 weekend/8 + v60 weekend/4 + v63/v64 sprite weekend/3,4 "
              "+ v65 night/16 + v66 weekend/17 + v67 weekend/5 consumed-row structural anchors; "
              "card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v67); "
              "dusk-window standby redemption: R1337 registration (r1337_dusk_scan.txt 1 CLEAN row) -> held through R1338-R1387 -> redeemed this round; "
              "quote-face word probe: 6 words see r1388_quote_face.txt; production time %s (post-sunset literal dusk)" % time.strftime("%Y-%m-%d %H:%M:%S"))
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
report.append("LADDER_50: quote line 14.00em driver (canonical band library em-budget-ladder.md 50->46->44->40->36->32->28 max-feasible pick; 50-band budget 18.40em margins +3.80/+4.40/+5.75em; four-LINES stack VERT +284px); all other QUOTE-v2 params verbatim; dusk-window standby + supply-determined + 伞-motif-family + same-day-two-signs honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1388.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V68, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V68, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63-v67 review precedent)
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

# --- E4 audience reference call (async detached, 1500s window, v51-v67 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (canonical ladder 50, quote-line driver) + E4 fired async" % H2_SIZE)
