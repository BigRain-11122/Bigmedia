# -*- coding: utf-8 -*-
"""MC-20261005-DAILY-v66 build: DAILY (city daily-sign) series SIXTY-SIXTH piece (R1321, queue
section-E E30 daytime-window unlock). DAYTIME-WINDOW PIECE - the two registered weekend-face clean
rows (R1320 window scan: 怀旧/weekend/17 + 侠气/weekend/5 = daytime-home content, pre-dawn window
time-point mismatch, sunrise ~05:52 unlock) fire THIS round after the sunrise gate. Rotation law
machine-verified (r1321_weekend_scan.txt): 怀旧 9 = unique least-consumed axis (求新 10/烟火 10/
侠气 10/秩序 10/逍遥 11/sprite 5) + longest gap 10 (v55 -> v65) -> SELECT 怀旧/weekend/17.
Machine-verified ZERO card-face shingle collision across ALL fleet card faces (fully-zero row =
series 14th; spirit-layer 1 common-word 时光 = harvest-file layer, NOT the R1010 card-face dedup
face, honest note). Literal alignment: post-sunrise morning production x weekend-bucket holiday
adjacency (v58/v59/v60 假日态邻接 precedent) x 怀旧-axis old-records content. Anti-homogenization
R442 spine: v55 怀旧 = 溜达旧书摊 outdoor-street face -> THIS = 居家听唱片 indoor-audio face =
scene-heterogeneous. Layout = QUOTE-v2 params verbatim; h2_size ladder = 44 band (quote line
20.0em driver; 46-band == 20.0 zero-margin exclusion R293 law; 44-band 0.91em margin = v13/v17/v18
precedent band). Machine source/dedup assertions (R456 system, card-face level R1010 law).
Daytime-window hard gate: refuses to run before sunrise (05:52). UTF-8.
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
V66 = os.path.join(BASE, "MC-20261005-DAILY-v66")
TMP = V66 + "-tmp"
os.makedirs(V66, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"听老唱片，忆往昔岁月，时光倒流一二里"
AXIS, BUCKET, IDX = u"怀旧", u"weekend", 17

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
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- weekend-face supply adjudication evidence (window verdict R1320 consumed + readable regen r1321)
scan = io.open(os.path.join(ROOT, ".c3-tmp", "r1321_weekend_scan.txt"), encoding="utf-8").read()
assert u"CLEAN 怀旧/weekend/17" in scan, "weekend-face scan evidence line missing (r1321_weekend_scan.txt)"
assert u"SELECT 怀旧/weekend/17" in scan, "rotation-law selection line missing (r1321_weekend_scan.txt)"
assert u"unique least-consumed axis" in scan, "rotation machine-count line missing"

# --- quote-face word probe (r1321_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"听老唱片", u"老唱片", u"唱片", u"忆往昔", u"往昔", u"时光倒流", u"倒流", u"一二里"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1321 quote-face word probe for candidate " + QUOTE_CORE + u" (怀旧/weekend/17, daytime-window unlock piece)"]
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. Daytime-window adjudication (R1320 window verdict + this round machine regen): (1) weekend face = the registered supply after night-face double-zero (R1124/R1305): TWO clean daytime-home rows (怀旧/17 + 侠气/5), pre-dawn window time-point mismatch -> sunrise ~05:52 unlock fired THIS round; (2) rotation law machine count: 怀旧 9 = unique least-consumed axis + longest gap 10 (v55->v65) -> 怀旧/17 selected over 侠气/5 (侠气 10 counts, gap 6); 侠气/5 = remaining daytime standby row for next daytime window; 烟火/13 = 10-08 market-reopen gate; (3) zero card-face shingle collision = series 14th fully-zero row; spirit-layer 1 (common word 时光) = harvest-file layer, NOT the R1010 card-face dedup face, honest note carried; (4) anti-homogenization R442: v55 怀旧 = 溜达旧书摊 outdoor-street face -> THIS = 居家听唱片 indoor-audio face = scene-heterogeneous; (5) weekend bucket on Monday holiday = 假日态 adjacency (v58/v59/v60 direct precedent), honest note; (6) LITERAL daytime: post-sunrise morning production (~05:5x) x holiday-home content x 怀旧轴." % (u"all probe words ZERO fleet card-face hits = fully-zero row (v53-v65 fourteen-precedent chain)" if allzero else u"NOTE: some probe hits above - honest adjacency adjudication required"))
qrep.append(u"post-v66 supply honest note: weekend face remaining = 侠气/weekend/5 (daytime standby, next daytime window) + 烟火/weekend/13 (10-08 market-reopen gate); all other weekend rows = 3-17 card-face shingle collisions (r1321_weekend_scan.txt); night face double-zero (R1124/R1305) unchanged; unlock windows unchanged: rain-event day / CEO-order day / 10-08 market reopen / Nov+ coldsnap / summer heatwave. Pool-expansion report position maintained (status-line not chase).")
io.open(os.path.join(TMP, "r1321_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V66:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 066",
    u"2026-10-05 · 国庆假期 · 晨",
    u"「听老唱片，忆往昔岁月，时光倒流一二里」",
    u"——硅基城市台词池 · 怀旧轴",
]

SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]
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
assert H2_SIZE == 44, "em ladder expected 44-band (quote line 20.0em driver; 46-band == 20.0 zero-margin exclusion R293), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261005-DAILY-v66"
meta["form"] = (u"DAILY 城市日签 066（L-卡 图文轻内容线 DAILY 形态第六十六件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 日间窗解锁件 R1321·日签节律续件=日期×情境桶对位判据第六十六证〔**日间窗解锁件**："
                u"R1320 窗扫描注册 weekend 面 2 干净行=日间居家内容〔时点错位·拂晓前夜窗不入选·日出 ~05:52 后"
                u"日间窗轮领〕→本轮日出后日间窗兑现〔build 脚本内日出硬闸 assert 05:52〕+旋转律机核计数："
                u"怀旧 9 采=唯一最少消费轴〔求新 10/烟火 10/侠气 10/秩序 10/逍遥 11/sprite 5·r1321_weekend_scan.txt〕"
                u"+gap 10 最长〔v55→v65〕→**怀旧/weekend/17 选中**〔侠气/5=次席 standby 留日间窗下件·烟火/13="
                u"10-08 复市门控〕+**卡面级零撞行=系列第十四件全零邻接行**〔r1321_quote_face.txt 八词 probe 全 ZERO〕"
                u"+**假日态邻接诚实注**：周一国庆假期第 5 天=非工作日=weekend 桶假日常态对位〔v58/v59/v60 先例带·"
                u"非 literal weekend 直配〕+**场景异质反同构**：v55 怀旧=溜达旧书摊户外街面→本件=居家听唱片室内"
                u"声音面〔R442 主线维持·轴内怀旧母题带=旧书×老物件×老唱片三变奏诚实注〕〕+最数字化的城市"
                u"〔一切皆数据〕×最模拟的声音载体〔老唱片〕=**新×旧反差金句位**〔族五十三连·唱片位语感独占注="
                u"数字城市里有人把唱针放回时间的起点〕+时光倒流一二里〔时间往前跑×唱针往回放〕=倒流计量化"
                u"幽默〔一二里=最乡土的里程单位×最超前的时光机意象〕）")
meta["source_quote"] = u"「听老唱片，忆往昔岁月，时光倒流一二里」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][weekend][17]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-05.md（当日日期语境源·国庆假期第 5 天·周一·日出后晨间生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][weekend][17] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 18 行计数+axes 6 轴"
                         u"结构断言〔R982〕+v58 烟火/7+v59 侠气/8+v60 逍遥/4+v63/v64 sprite weekend/3·4+v65 秩序"
                         u"night/16 六已耗行结构锚）②日期行 2026-10-05=当日历法事实·周一+国庆假期第 5 天"
                         u"〔daily brief 2026-10-05 当日窗语境〕+晨标记〔日出 ~05:52 后日间窗生产·v63 晨标记先例带·"
                         u"literal 晨〕③情境=日间窗解锁件〔R1320 窗扫描 weekend 面 2 干净行注册→日出硬闸兑现·"
                         u"r1321_weekend_scan.txt 机证〕④轴部署名=台词池怀旧轴行·本行无称谓面=纯生活口气句·泛称零涉及"
                         u"〔人设权红线零接触·charter §2.4·v5/v17/v21/v53/v65 先例族〕⑤去重断言=本行不在 "
                         u"city-spirit.md 已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·"
                         u"DAILY-v1~v65 全 66 行+REACT 八件+CENSUS 20+DIGEST 15+QUOTE 6 皆非本行）+「听老唱片」"
                         u"「老唱片」「唱片」「忆往昔」「往昔」「时光倒流」「倒流」「一二里」全句 probe 八词机核"
                         u"〔r1321_quote_face.txt·全 ZERO=系列第十四件全零邻接行〕+诚实注=spirit 采面层「时光」"
                         u"一词共用〔city-spirit.md 信条例行·非卡面级去重面·常用词层〕⑥季相核=本行无年味/春联/"
                         u"寒潮类季相错位词〔R972 制·听唱片=四季通用日间居家面·十月秋晨兼容〕⑦品牌语感注="
                         u"「忆往昔」「一二里」口语+乡土计量幽默=去 AI 感对位·人味命中·零书面套语·无品牌无消费宣称")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 署名律"
                             u"+人设权红线·本行无称谓面=纯生活口气句·泛称零涉及〔v5/v17/v21/v53/v65 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（日间窗解锁件+旋转律最少消费轴回补双位"
                            u"〔**供给面诚实注**：R1320 窗扫描 weekend 面 2 干净行注册→本轮日出后兑现·夜面双归零"
                            u"〔R1124/R1305〕承继〕+新×旧反差金句位〔族五十三连·唱片位语感独占注〕+倒流计量化幽默"
                            u"〔一二里〕+口语人味=语录卡线变体零新模板第六十六证（QUOTE-v2 参数 verbatim 复用·"
                            u"h2_size 44 档〔引文行 20.0em 驱动·46 档 20.0==20.0 零余量排除律 R293·44 档余量 0.91em"
                            u"=v13/v17/v18 先例带〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔假期清晨"
                            u"数字城市里最模拟的一声沙沙=城市活得有年代感的活证据〕+**供给面诚实注**：本件后 "
                            u"weekend 面=侠气/5 单行日间 standby+烟火/13 复市门控行〔余行 3-17 卡面撞·"
                            u"r1321_weekend_scan.txt〕·DAILY 可诚实配对面维持结构性近枯竭注〔池扩容呈报位维持呈现状"
                            u"行不催办〕·post-v66 指针：解锁窗维持=雨事件日/CEO 令日/10-08 market_open 复市/Nov+ "
                            u"寒潮/夏季 heatwave/侠气/5 日间窗行·REACT-v9 10-06 窗·F 序号诚实注=本件先落 F-153"
                            u"·REACT-v9 预指位顺延 F-154〔R978 判例 finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：最数字化的城市〔一切皆数据跑得最快〕×"
                          u"最模拟的声音载体〔老唱片沙沙声〕=新×旧反差+时间往前跑〔城市时间〕×唱针往回放〔时光"
                          u"倒流一二里〕=快×慢反差〔族五十三连·唱片位语感独占注〕+「一二里」乡土里程单位×时光机"
                          u"意象=计量化幽默/情 1 假日居家怀旧式闲适的温和共鸣如实非强极点〔G1 城市生活群〕/时 2 "
                          u"当日=2026-10-05 周一国庆假期第 5 天·日出后晨间窗 literal 生产〔~05:5x·R1320 日间窗解锁"
                          u"兑现〕×假日态居家内容×weekend 桶假日常态邻接〔v58/v59/v60 先例带〕/台 2 公众号方图承载="
                          u"MC-001~151 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R1321 日间窗解锁兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名=人设权红线零接触（本行无称谓面=纯生活口气句·泛称零"
                     u"涉及〔v5/v17/v21/v53/v65 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（老唱片=文化意象非消费宣称·无品牌无价格）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十六件·charter v1.2 §4 形态码 DAILY·日签节律续件·日间窗解锁件·怀旧轴 weekend 桶假日态邻接件·最少消费轴回补件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[怀旧][weekend][17] verbatim OK; weekend bucket=18 rows; axes 6 structure (R982); "
              "v58 weekend/7 + v59 weekend/8 + v60 weekend/4 + v63/v64 sprite weekend/3,4 + v65 night/16 consumed-row structural anchors; "
              "card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v65; "
              "daytime-window unlock: R1320 registered 2 clean weekend rows -> sunrise hard gate 05:52 -> rotation law 怀旧 least+longest-gap selected; "
              "quote-face word probe: 8 words see r1321_quote_face.txt; production time %s (post-sunrise literal daytime)" % time.strftime("%Y-%m-%d %H:%M:%S"))
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
report.append("LADDER_44: quote line 20.0em driver (46-band == 20.0 zero-margin excluded per R293; 44-band margin 0.91em = v13/v17/v18 precedent band); four-LINES stack; all other QUOTE-v2 params verbatim; daytime-window + rotation + scene-heterogeneity honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1321.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V66, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V66, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63/v64/v65 review precedent)
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

# --- E4 audience reference call (async detached, 1500s window, v51-v65 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 44, quote-line driver) + E4 fired async" % H2_SIZE)
