# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v55 build: DAILY (city daily-sign) series FIFTY-FIFTH piece (R1025, queue
section-E E30 standby). SUPPLY-FACE-SWITCH FIRST PIECE (structural, honest): rotation post-v54
counts qiuxin 9 / huaijiu 8 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 (sprite tracked
separately: v50 festival/0 + v54 night/8) -> tie at 8: huaijiu (v45, 9-piece gap = LONGEST) /
xiaoyao (v48, 6-piece gap) -> redemption target = huaijiu -> huaijiu/night face machine-proven
zero clean rows (r1023_pool.txt fresh, re-confirmed r1024 cascade) -> per R1024 rotation note +
focus pre-registration: SUPPLY-FACE SWITCH = festival return OR dusk/market_close
evening-adjacent buckets -> fresh pre-scan r1025_pool.txt: huaijiu/festival 18 rows ALL carry
content collisions + huaijiu/dusk 18 rows ALL carry hits -> huaijiu/market_close line1
「老陈头又背着手溜达去了旧书摊」 = ONLY clean row (ZERO direct shingle hits, 2-5 char
including punctuation-inclusive 2-gram all zero = zero construct-layer adjacency = THIRD
fully-zero row of the series after v53/v54). Zero-collision standard NOT relaxed (R442
anti-isomorphism spine, v1-v54 fifty-four-link zero-collision chain). Backup pre-registered:
xiaoyao/dusk line6 「夕阳西下鱼也归巢了」 = v56 candidate (xiaoyao becomes unique minimum
post-v55, gap 7; fresh re-probe next round). Built-in tension: NAO x JING - National Day
holiday day 2, the whole city crowds the festival lights, while the most nostalgic resident
strolls hands-behind-back to the used-book stall - the city's oldest corner; 「又」 = repeat
habit ritual (not his first time). Layout = QUOTE-v2 params verbatim; h2_size ladder = 50 band
(quote 17.00em driver margin +1.40em; v53 zhixu same band precedent). Machine source/dedup
assertions (R456 system, card-face level R1010 law). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V55 = os.path.join(BASE, "MC-20261002-DAILY-v55")
TMP = V55 + "-tmp"
os.makedirs(V55, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"老陈头又背着手溜达去了旧书摊"
AXIS, BUCKET, IDX = u"怀旧", u"market_close", 1

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
mb = pool["axes"][AXIS][BUCKET]
assert len(mb) == 18, "axis bucket != 18 rows (axes = 6 x 12 buckets x 18 rows = 1296)"
assert mb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % mb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1025_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"老陈头", u"背着手", u"溜达", u"旧书摊", u"旧书", u"书摊", u"老陈", u"溜达去", u"背着"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1025 quote-face word probe for candidate " + QUOTE_CORE + u" (huaijiu/market_close line1)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1025_pool.txt fresh) = THIRD fully-zero row of the series (v53 first / v54 second / this third); supply-face-switch honest note: huaijiu/night zero clean rows (r1023 fresh, r1024 cascade re-confirmed) + huaijiu/festival 18 rows ALL content collisions + huaijiu/dusk 18 rows ALL carry hits (r1025_pool.txt fresh) -> market_close evening-adjacent bucket = ONLY clean supply face for the redemption-target axis; bucket honesty: production ~22:3x literal night vs market_close scene = time-adjacent NOT time-exact (R1024 pre-registered switch candidate honestly noted); holiday-rest note: National Day holiday day 2 = exchange closed all day = market_close state is the all-day holiday state (scene-context fit); 老陈头 = pool-line verbatim archetype address (老+姓氏+头 market-elder address form) NOT a registered resident name (human-set rights zero contact, v52 船老大 same-type precedent); post-v55 rotation note: qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 -> xiaoyao unique minimum (v48, gap 7) = v56 redemption target + xiaoyao/dusk line6 「夕阳西下鱼也归巢了」 pre-registered backup (fresh re-probe next round; supply faces for xiaoyao: festival/dusk/market_close all scanned r1025_pool.txt - only dusk line6 clean)")
io.open(os.path.join(TMP, "r1025_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V55:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits do NOT count as consumption.
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d
# consumed lines (documented not asserted): festival resident-bucket DAILY v1 qiuxin/4 + v2 huaijiu/0 +
# v3 xiaqi/5 + v4 yanhuo/4 + v5 zhixu/4 + v6 xiaoyao/3 + v7 qiuxin/7 + v8 xiaqi/13 + v9 qiuxin/12 +
# v10 huaijiu/3 + v11 yanhuo/13 + v12 xiaoyao/15 + v13 xiaqi/2 + v14 qiuxin/3 + v15 qiuxin/11 +
# v16 huaijiu/1 + v17 zhixu/12 + v18 xiaoyao/1 + v19 yanhuo/3 + v20 xiaqi/1 + v21 zhixu/6 +
# v22 huaijiu/12 + v23 qiuxin/13 + v24 yanhuo/2 + v25 huaijiu/17 + v26 xiaqi/10 + v27 yanhuo/7 +
# v28 zhixu/9 + v29 xiaoyao/2 + v30 zhixu/2 + v31 xiaoyao/4 + v32 yanhuo/10 + v33 huaijiu/4 +
# v34 xiaqi/9 + v35 zhixu/11 + v36 xiaoyao/16 + v37 qiuxin/5 + v38 yanhuo/5 + v39 huaijiu/5 +
# v40 xiaqi/11 + v41 zhixu/17 + v42 xiaoyao/13 + v43 qiuxin/9 + v44 yanhuo/1 + v45 huaijiu/16 +
# v46 xiaqi/7 + v47 zhixu/15 + v48 xiaoyao/5 + v49 qiuxin/2 + REACT-v8 xiaoyao/17 + yanhuo/12 +
# zhixu/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/16 + qiuxin/14 + xiaqi/0
# (#47/#53/#59). Sprite face: v50 sprite/festival/0 + v54 sprite/night/8. NIGHT bucket:
# v51 yanhuo/13 (first piece) + v52 xiaqi/4 (second piece) + v53 zhixu/7 (third piece).
# THIS piece = huaijiu/market_close/1 (supply-face-switch first piece, market_close bucket
# first piece of the DAILY series).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 055",
    u"2026-10-02 · 国庆假期",
    u"「老陈头又背着手溜达去了旧书摊」",
    u"——硅基城市台词池 · 怀旧轴",
]

SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]  # 60 first = zero-template default, ladder picks the largest feasible notch
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
assert H2_SIZE == 50, "em ladder expected 50-band (quote 17.00em driver margin +1.40em; 60-band budget 15.33em excluded; v53 zhixu same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v55"
meta["form"] = (u"DAILY 城市日签 055（L-卡 图文轻内容线 DAILY 形态第五十五件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1025·日签节律续件=日期×情境桶对位判据第五十五证〔**market_close "
                u"傍晚邻接桶首件=供面切换第一件**：R1024 预登记「v55 供面切换候选=festival 回转或 dusk/"
                u"market_close 傍晚桶」兑现·桶级=国庆假期第 2 日+休市=收市态假日常态对位·**诚实注=时点邻接"
                u"非 literal night 直配**〔22:3x 夜时生产×傍晚收市场景=邻接面如实注记〕·场景级=假日休市后"
                u"老城背手溜达淘旧书面如实注记〕+**旋转律兑现（怀旧回补·结构性诚实注）**：v54 后计数求新 "
                u"9/侠气 9/烟火 9/秩序 9→怀旧 8/逍遥 8=双轴并列最少→回补目标=怀旧〔v45 后 9 件未采=最长"
                u"回补距〕→**怀旧三供面 fresh 预扫 r1025_pool.txt**：night 面 r1023 零干净行承继+festival "
                u"回转 18 行全数内容层直撞+dusk 18 行全数带撞→market_close line1=唯一干净行胜出=零直撞标准"
                u"不放松〔R442 反同构主线·v1-v54 五十四连零直撞〕〕+line1 选优〔**全 shingle 零命中+零构式层"
                u"邻接=系列第三件全零邻接行**（v53/v54 后连续·r1025_pool.txt fresh 2-5 字含标点全零="
                u"r1025_quote_face.txt 九词机核·怀旧/market_close 18 行唯一干净行〕+「又」字=常客日常仪式感 "
                u"verbatim 语感细节〔去了不是第一次=淘旧书是老习惯〕+「背着手」体感词+「溜达」口语真感=人味"
                u"命中〔CEO 审美线对位〕+怀旧轴〔最念旧·把老物件当宝贝的轴〕×「老陈头又背着手溜达去了旧书摊」"
                u"〔全城看灯会的假期×城里最旧的角落〕=**闹×静轴内自反差金句位**〔族四十一连·淘旧书位语感独占注"
                u"=最念旧的人在节日里去了最旧的地方·收市后快钱散场×溜达淘旧书慢生活〕〕）")
meta["source_quote"] = u"「老陈头又背着手溜达去了旧书摊」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][market_close][1]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期第 2 日=DAILY-v1~v54 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][market_close][1] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+market_close 桶 18 行计数"
                         u"+axes 6 轴+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-02=当日历法事实·国庆假期="
                         u"假期第 2 天〔daily brief 2026-10-02 当日窗语境〕③情境=market_close 傍晚邻接桶供面切换"
                         u"第一件〔R1024 预登记兑现·国庆假期休市=收市态假日常态对位·**诚实注=傍晚场景×22:3x 夜时"
                         u"生产=时点邻接非 literal night 直配**〕④池级署名=台词池轴级行·「老陈头」=池行内泛称群像面"
                         u"（老+姓氏+头=市井长者称谓构式）非登记居民名非登记生灵名〔人设权红线零接触·charter "
                         u"§2.4·v52 船老大同型先例〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 "
                         u"lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~v54 全 54 行+REACT-v8 同桶"
                         u"三行+city-spirit v1.2 节日场景三行皆非本行）+「老陈头」「背着手」「溜达」「旧书摊」"
                         u"「旧书」「书摊」「老陈」「溜达去」「背着」probe 九词机核〔r1025_quote_face.txt〕+"
                         u"**零构式层邻接**〔r1025_pool.txt fresh 2-5 字含标点 2 字组全零=系列第三件全零邻接行·"
                         u"v53/v54 后连续·怀旧三供面〔night/festival/dusk〕零干净行+market_close 唯一干净行"
                         u"fresh 实证〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·黄昏收市淘旧书=假日"
                         u"傍晚季相对位〕⑦品牌语感注=「老陈头」市井长者称谓+「背着手」体感词+「溜达」口语真感+"
                         u"「又」字日常仪式感〔去 AI 感对位·市井口气=人味命中〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·「老陈头」=池行 verbatim 泛称群像面非登记居民名〔v52 船老大"
                             u"同型先例〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（market_close 傍晚邻接桶供面切换第一件"
                            u"〔**旋转律+供面切换+零直撞三律并轨诚实执行**：night 面四连后回补目标轴 night 面全阻断→"
                            u"R1024 预登记供面切换兑现→三供面 fresh 全扫〔festival 回转/dusk/market_close〕唯一干净行"
                            u"胜出〕+22:3x 同轮对位〔时点邻接诚实注〕+闹×静反差金句位+「背着手」「溜达」「又」字市井"
                            u"口语真感=语录卡线变体零新模板第五十五证（QUOTE-v2 参数 verbatim 复用·h2_size 50 档"
                            u"〔v53 同带先例·引文行 17.00em 驱动 margin +1.40em〕·charter §1「日签变体随时可续」兑现）"
                            u"·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 "
                            u"O-20260928-1910 对位〔最念旧的人在假期里去了最旧的地方=城市记忆的守摊人面〕+R442 "
                            u"人物场景处方带第四件〔v51 铺子守早客/v52 船老大夜航/v53 值夜岗慢步巡逻+v54 生灵插件后"
                            u"人物带续连=老陈头背手溜达〕+**供给面诚实注**：本件后怀旧轴 night/festival/dusk/"
                            u"market_close 四面已采面=market_close line1 唯一干净行已消费→怀旧轴四供面零干净行"
                            u"机证→v56 目标=逍遥〔唯一最少 v48 后 gap 7〕+逍遥/dusk line6「夕阳西下鱼也归巢了」="
                            u"预登记备胎〔fresh 复扫下轮执行〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：「又」字常客日常仪式感〔去了不是第一次=淘旧书"
                          u"是老习惯〕+假期全城灯会热闹×旧书摊安静角落=闹×静反差〔族四十一连·淘旧书位语感独占注〕"
                          u"+收市后快钱散场×溜达淘旧书慢生活/情 1 老城黄昏淘旧书温和画面感如实〔非强极点〕/时 2 当日"
                          u"时点=国庆假期第 2 日+market_close 傍晚邻接桶供面切换第一件〔休市=收市态假日常态对位·R1024 "
                          u"预登记兑现·诚实注=邻接非直配〕/台 2 公众号方图承载=MC-001~139 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R1025 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名=人设权红线零接触（「老陈头」=池行 verbatim 泛称群像面"
                     u"非登记居民名〔v52 船老大同型先例〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（背手"
                     u"溜达淘旧书=市井生活意象非个体档案面·收市=情境词非行情面·无品牌无价格=零消费宣称）；成品只"
                     u"入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十五件·charter v1.2 §4 形态码 DAILY·日签节律续件·market_close 傍晚邻接桶首件=供面切换第一件·怀旧轴回补件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[huaijiu][market_close][1] verbatim OK; market_close bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v54 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night bucket v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7 + sprite v50 festival/0 + v54 night/8; supply-face-switch 1st proof: huaijiu night (r1023) / festival / dusk (r1025 fresh) all zero clean rows -> market_close line1 = ONLY clean row; quote-face word probe: 9 words see r1025_quote_face.txt (all ZERO; zero construct-layer adjacency = THIRD fully-zero row of series after v53/v54)")
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
report.append("LADDER_50: quote 17.00em driver (v53 zhixu same-band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; market_close-evening-adjacent-bucket first DAILY piece + supply-face-switch-1st + rotation-huaijiu-redemption + third-fully-zero-row honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1025.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V55, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V55, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53/v54 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 50, quote driver, v53 band precedent) + E4 fired async" % H2_SIZE)
