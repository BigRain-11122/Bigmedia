# -*- coding: utf-8 -*-
"""MC-20261008-DAILY-v70 build: DAILY (city daily-sign) series SEVENTIETH piece (R1738, queue
section-E E30 CEO-order-day gate redemption). Supply adjudication = R1703 post-v69 unlock-window
registration: "unlock windows after v69 = rain-event day / CEO-order day / Nov+ coldsnap /
summer heatwave (market_open reopen window REDEEMED by v69)". THIS round = 2026-10-08 CEO
order day in machine evidence (own orders/O-20261008-1105-bm-a.md CEO direct order 12:08:14 +
group docs/orders.md P-2026-10-08-05 MV-order-family rows through ~13:2x) -> CEO-order-day
gate fires; pool bucket = ceo_order (city-lord-issues-commands fictional situation), card-face
FIRST USE of the bucket across QUOTE/DIGEST/CENSUS/REACT/DAILY fleet (fresh bucket, R1548
four-fresh-bucket family: dusk/typhoon/coldsnap/ceo_order, coldsnap consumed by REACT-v11
R1676, this piece = ceo_order). Quote = axes[yanhuo][ceo_order][17] verbatim (city lord's
word x humblest breakfast stall = top-down command x grassroots steam-warmth contrast).
Line-level freshness (post-v6 criterion): yanhuo axis reused with a different line (v69 =
yanhuo/weekend/13 market line; this = yanhuo/ceo_order/17) - same-axis-different-line law.
em ladder = canonical band library: quote line 17.00em -> 50 band (budget 18.40em, margin
+1.40em). Machine source/dedup assertions (R456 system, card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

# --- CEO-order-day gate (R1703 unlock-window registration: CEO order day; machine anchors)
_now_date = time.strftime("%Y-%m-%d")
assert _now_date == "2026-10-08", "CEO-order-day gate: registered for 2026-10-08 (now %s)" % _now_date
_own_order = os.path.join(ROOT, "orders", "O-20261008-1105-bm-a.md")
assert os.path.isfile(_own_order), "CEO direct order O-20261008-1105 receipt file missing (CEO-order-day anchor)"
_group_orders = io.open(os.path.join(ROOT, "..", "..", "docs", "orders.md"), encoding="utf-8").read()
assert u"P-2026-10-08-05" in _group_orders, "group orders P-2026-10-08-05 CEO-order-family rows missing (CEO-order-day anchor)"

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V70 = os.path.join(BASE, "MC-20261008-DAILY-v70")
TMP = V70 + "-tmp"
os.makedirs(V70, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"城主发话了，早点铺子快忙活起来"
AXIS, BUCKET, IDX = u"烟火", u"ceo_order", 17

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "axes bucket != 18 rows (axes = 6 axes x 12 buckets x 18 rows = 1296)"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
assert nb[0] == u"白光一闪，早点摊主喊道：今儿的豆浆格外香！", "ceo_order bucket head structure anchor expected"
assert pool["axes"][u"烟火"][u"weekend"][13] == u"市场买卖讲价，公平公正正", "v69 consumed-row structural anchor expected"
assert pool["axes"][u"侠气"][u"coldsnap"][13] == u"街坊邻居得互相照应，这日子才过得多舒心", "REACT-v11 consumed-row structural anchor expected"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
assert QUOTE_CORE != u"市场买卖讲价，公平公正正", "line-level freshness vs v69 (same-axis-different-line law)"

# --- quote-face word probe (r1738_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"城主发话了", u"早点铺子", u"快忙活起来", u"城主", u"早点铺子快忙活"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1738 quote-face word probe for candidate " + QUOTE_CORE + u" (烟火/ceo_order/17, CEO-order-day gate redemption piece)"]
qrep.append(u"CEO-order-day gate machine evidence: own orders/O-20261008-1105-bm-a.md (CEO direct order 12:08:14) asserted present + group docs/orders.md P-2026-10-08-05 CEO-order-family rows asserted present; R1703 post-v69 unlock-window registration = rain-event day / CEO-order day / Nov+ coldsnap / summer heatwave -> CEO-order-day gate fires THIS round; ceo_order bucket = card-face first use across fleet (R1548 four-fresh-bucket family dusk/typhoon/coldsnap/ceo_order; coldsnap consumed by REACT-v11 R1676)")
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. CEO-order-day gate redemption adjudication (R1703 registration + this round machine verify): (1) unlock window CEO-order-day fires on 2026-10-08 with machine anchors (own CEO direct order receipt file + group orders P-2026-10-08-05 rows); (2) bucket selection = ceo_order fictional situation (city lord issues commands, brain-tower white light), card-face FIRST USE of the bucket in fleet; (3) line-level freshness = yanhuo axis different line from v69 (same-axis-different-line post-v6 law); (4) fictional-register honesty: card face speaks the fictional city lord register only - real CEO order facts stay in ledger meta (source_facts), zero token numbers / zero real names on card face (desensitization law); (5) hook = city lord's grandest word x humblest breakfast stall = top-down command x grassroots steam-warmth contrast." % (u"all probe words ZERO fleet card-face hits = fully-zero row + ceo_order bucket-family card-face freshness (word 城主 zero hits = bucket family never on any card face)" if allzero else u"NOTE: some probe hits above - honest adjacency adjudication required"))
qrep.append(u"post-v70 supply honest note: ceo_order face = 17 clean rows remaining after this piece (axes x6 each 18 rows, this = first card-face use); weekend face = ZERO clean rows (post-v69 exhausted) unchanged; night face double-zero unchanged; dusk face zero clean rows unchanged; festival face 1 clean row season-gated unchanged; unlock windows = rain-event day / next CEO-order day / Nov+ coldsnap / summer heatwave (each day one redemption; ceo_order bucket re-usable on future CEO-order days with different lines). DAILY honest-pairable face structurally near-exhausted note maintained (pool-expansion report position = status-line not chase).")
io.open(os.path.join(TMP, "r1738_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V70:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 070",
    u"2026-10-08 · 城主连令日 · 午",
    u"「城主发话了，早点铺子快忙活起来」",
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
assert H2_SIZE == 50, "em ladder expected 50-band (quote 17.00em vs budget 18.40em margin +1.40em, VERT +284px), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261008-DAILY-v70"
meta["form"] = (u"DAILY 城市日签 070（L-卡 图文轻内容线 DAILY 形态第七十件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 CEO 令日门控兑现件 R1738·日签节律续件=日期×情境桶对位判据第七十证〔**CEO 令日门控位**："
                u"R1703 post-v69 解锁窗注册=雨事件日/CEO 令日/Nov+ 寒潮/夏季 heatwave→本轮 2026-10-08 CEO 连令日"
                u"机证锚兑现〔build 内双锚 assert=own orders/O-20261008-1105-bm-a.md CEO 直令在位+集团 orders P-2026-10-08-05 "
                u"令族行在位〕→**ceo_order 桶=全 fleet 卡面首用**〔R1548 四新鲜桶族 dusk/typhoon/coldsnap/ceo_order 中 "
                u"coldsnap 已由 REACT-v11 R1676 消费·本件=ceo_order 首用〕+**卡面级零撞行**〔五词 probe 机核 "
                u"r1738_quote_face.txt·词「城主」全 fleet 卡面零命中=桶族卡面新鲜实锚〕+**线级新鲜度**〔v69 烟火/weekend/13 "
                u"市场行→本件 烟火/ceo_order/17=同轴异行律·post-v6 唯一面〕+**虚构声口诚实注**：卡面=虚构城市城主声口"
                u"（池内正典人物形象）·真实 CEO 令事实只入台账 meta 零上卡面〔脱敏律·零令号零真名〕〕）+城主之令"
                u"〔城市最高层号令·连令日全城动能〕×早点铺子〔最底层烟火蒸汽〕=**上令×下暖/号令×烟火双反差金句位**"
                u"〔族五十七连·大令落到小笼包上=层级×温度〕+「快忙活起来」市井动词收尾=人味命中")
meta["source_quote"] = u"「城主发话了，早点铺子快忙活起来」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][ceo_order][17]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+orders/O-20261008-1105-bm-a.md（CEO 直令当日窗语境·CEO 令日门控机证锚）"
                           u"+C:\\Users\\sjs20\\Desktop\\FluxGroup\\docs\\orders.md（集团令族行 P-2026-10-08-05·跨仓只读机证锚）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][ceo_order][17] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+ceo_order 桶 18 行计数+axes 6 轴"
                         u"结构断言〔R982〕+桶首行结构锚+v69 烟火/weekend/13+REACT-v11 侠气/coldsnap/0 已耗行结构锚"
                         u"〔双先例锚〕）②日期行 2026-10-08=当日历法事实·周四+城主连令日虚构情境标记〔午=日间窗生产·"
                         u"v63/v66/v67/v69 标记先例带〕③情境=CEO 令日解锁窗兑现件〔R1703 注册→本轮双机证锚兑现·"
                         u"r1738_quote_face.txt 链自足〕④轴级署名=台词池烟火轴行·本行无称谓面=纯市井口气句·泛称零涉及"
                         u"〔人设权红线零接触·charter §2.4·v5/v17/v21/v53/v65/v66/v67/v69 先例族〕⑤去重断言=本行不在 "
                         u"city-spirit.md 已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律）+"
                         u"「城主发话了」「早点铺子」「快忙活起来」「城主」「早点铺子快忙活」全句 probe 五词机核"
                         u"〔r1738_quote_face.txt〕⑥季相核=本行无年味/春联/寒潮类季相错位词〔R972 制·城主发令+早点"
                         u"开火=四季通用市井面·十月秋日午间兼容〕⑦品牌语感注=「发话了」「快忙活起来」市井口语动词"
                         u"=去 AI 感对位·人味命中·零书面套语·无品牌无消费宣称⑧虚构声口诚实注=城主=池内正典虚构"
                         u"人物〔台词池情境桶原生人物〕·真实 CEO 令事实=选材依据只入台账 meta〔source_facts 本行〕"
                         u"零上卡面〔脱敏律 O-1602：零令号/零真名/零未公开面〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 署名律"
                             u"+人设权红线·本行无称谓面=纯市井口气句·泛称零涉及〔v5/v17/v21/v53/v65/v66/v67/v69 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（CEO 令日门控兑现+上令×下暖/号令×烟火"
                            u"双反差金句位〔族五十七连·大令落到小笼包上=层级×温度〕+「快忙活起来」市井动词收尾=语录卡线"
                            u"变体零新模板第七十证（QUOTE-v2 参数 verbatim 复用·h2_size 50 档=canonical ladder 最大可行档"
                            u"〔em-budget-ladder.md 判例库正典 50→28·引文行 17.00em 驱动·预算 18.40em margin +1.40em·"
                            u"VERT 四行栈 R381 gap +284px〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款"
                            u" 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔连令"
                            u"日全城动能里最烟火的一声开火=城市活得有人味的活证据〕+post-v70 供给注：ceo_order 面=余 17 "
                            u"干净行〔桶族可复用于后续 CEO 令日·每令日一件异行兑换〕·weekend 面零干净行/dusk 面零干净行/"
                            u"夜面双归零/festival 面 1 行季相门控 承继注·解锁窗=雨事件日/下一 CEO 令日/Nov+ 寒潮/夏季 "
                            u"heatwave·池扩容呈报位维持〔呈现状行不催办〕+F 序号诚实注=本件先落 F-166·REACT-v12 预指位"
                            u"顺延 F-167〔R978 判例·finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：城主之令〔城市最高层号令·连令日全城动能〕×"
                          u"早点铺子〔最底层烟火蒸汽〕=上令×下暖/号令×烟火反差+最高指令落到热乎早点上=层级×温度"
                          u"〔族五十七连·大令落到小笼包上语感独占注〕+「快忙活起来」市井动词收尾=人味命中/情 1 连令"
                          u"落下全城开火做饭的踏实温和共鸣如实非强极点〔G1 城市生活群〕/时 2 当日=2026-10-08 CEO 连令日"
                          u"→城主连令日映射〔build 内双机证锚 assert 直令件+令族行〕×ceo_order 桶 literal 对位×日间窗"
                          u"生产/台 2 公众号方图承载=MC-001~158 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1738 CEO 令日门控兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=市井口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名=人设权红线零接触（本行无称谓面=纯市井口气句·泛称零"
                     u"涉及）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（发话开火=动作意象非消费宣称·无品牌无"
                     u"价格）+真实 CEO 令事实零上卡面只入台账 meta；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第七十件·charter v1.2 §4 形态码 DAILY·日签节律续件·CEO 令日门控兑现件·烟火轴 ceo_order 桶首用件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[烟火][ceo_order][17] verbatim OK; ceo_order bucket=18 rows; axes 6 structure (R982); "
              "bucket-head structure anchor + v69 weekend/13 + REACT-v11 coldsnap/0 consumed-row structural anchors; "
              "CEO-order-day gate: own CEO direct order receipt file + group orders P-2026-10-08-05 rows asserted; "
              "card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v69; "
              "CEO-order-day gate redemption production time %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
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
report.append("LADDER_50: quote line 17.00em driver (canonical band library em-budget-ladder.md 50->46->44->40->36->32->28 max-feasible pick; 50-band budget 18.40em margin +1.40em; four-LINES stack VERT +284px); all other QUOTE-v2 params verbatim; CEO-order-day double-anchor + ceo_order-bucket-first-use + same-axis-different-line + fictional-register honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1738.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V70, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V70, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63-v69 review precedent)
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

# --- E4 audience reference call (async detached, 1500s window, v51-v69 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
if os.path.isfile(os.path.join(TMP, "e4_call.py")):
    subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                     creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("BUILD OK h2_size=%d (canonical ladder 50, quote-line driver) + E4 fired async" % H2_SIZE)
else:
    print("BUILD OK h2_size=%d (canonical ladder 50, quote-line driver) + E4 call not yet written (fire after write)" % H2_SIZE)
