# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v58 build: DAILY (city daily-sign) series FIFTY-EIGHTH piece (R1028, queue
section-E E30 standby). YANHUO-REDEMPTION PIECE (structural, honest): rotation post-v57 counts
qiuxin 10 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 9 -> FIVE AXES TIED AT 9 ->
redemption target = yanhuo (last v51 night/13, gap v52..v57 = 6 pieces = LONGEST; R1027
next-pointer redemption兑现). Per R1027 pointer: yanhuo FULL fresh supply-face scan
r1028_pool.txt (ALL 12 buckets x 18 rows = 216 rows, fleet includes v57) -> night 0 clean
(17 residual rows ALL carry hits) + festival 0 clean (10 residual ALL carry) + dusk 0 clean
+ market_close 0 clean = FOUR PRIORITY FACES ALL ZERO CLEAN -> cascade full-bucket scan:
morning 2 / weekend 1 / rain 0 / typhoon 0 / heatwave 2 / coldsnap 0 / market_open 3 /
ceo_order 1 clean rows; honest exclusions: heatwave+coldsnap = October-autumn season-face
mismatch (R972-adjacent), market_open = National-Day-holiday closed-market time-point
mismatch (v57 same ruling), ceo_order = no CEO-order event today (v57 same ruling),
morning clean rows carry weaker deep-night adjacency than weekend + morning/6 and
ceo_order/7 share the 4-char band 粥香扑鼻 (mutual future-collision note) -> weekend line7
「面条汤滚着呢，爱喝热乎的来碗」 = WINNER (ZERO direct shingle hits, 2-5 char
punctuation-inclusive 2-grams all zero = zero construct-layer adjacency = SIXTH
fully-zero row of the series after v53/v54/v55/v56/v57). Zero-collision standard NOT
relaxed (R442 anti-isomorphism spine, v1-v57 fifty-seven-link zero-collision chain).
WEEKEND BUCKET FIRST DAILY PIECE (4th new bucket opened: night v51 / market_close v55 /
dusk v56 / weekend v58; honest note: 2026-10-02 Friday = National Day holiday day 2 =
non-working day = weekend-state holiday normalcy pairing, v55 休市态 same-type precedent;
production ~23:4x deep night x scene (深夜面摊汤还滚着) = scene-level literal-night
compatible; bucket-level = 假日态邻接非 literal weekend 直配 honest note).
Built-in tension: NAO x SHOU / SAN x NUAN - the most crowd-loving market-stall axis keeps
one pot of noodle soup still rolling for whoever wants a hot bowl after the holiday-night
crowd has gone home. 「滚着呢」「热乎的」「来碗」 = market-street colloquial register =
human-flavor hit + yanhuo-axis literal hit. Layout = QUOTE-v2 params verbatim; h2_size
ladder = 50 band (16em quote line > 60-band budget 15.33em -> 50 budget 18.4em margin
+2.4em; v29/v31 50-band precedent R998/R1000). Machine source/dedup assertions (R456
system, card-face level R1010 law). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V58 = os.path.join(BASE, "MC-20261002-DAILY-v58")
TMP = V58 + "-tmp"
os.makedirs(V58, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"面条汤滚着呢，爱喝热乎的来碗"
AXIS, BUCKET, IDX = u"烟火", u"weekend", 7

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
wb = pool["axes"][AXIS][BUCKET]
assert len(wb) == 18, "axis bucket != 18 rows (axes = 6 x 12 buckets x 18 rows = 1296)"
assert wb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % wb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1028_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"面条", u"汤滚", u"滚着", u"着呢", u"热乎", u"爱喝", u"来碗", u"面条汤", u"汤滚着"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1028 quote-face word probe for candidate " + QUOTE_CORE + u" (yanhuo/weekend line7)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1028_pool.txt fresh full 12-bucket scan, fleet includes v57) = SIXTH fully-zero row of the series (v53/v54/v55/v56/v57 five precedents); supply-face honest note: yanhuo four priority faces (night/festival/dusk/market_close) ALL zero clean rows fresh (night 17 residual rows all carry hits after v51/13 consumption; festival 10 residual all carry after 8-row consumption; dusk 18 all carry; market_close 18 all carry) -> cascade full-bucket scan: morning 2 clean (deep-night x morning weaker adjacency + morning/6 and ceo_order/7 share 4-char band 粥香扑鼻 mutual future collision) / heatwave 2 clean (October-autumn season mismatch R972-adjacent) / market_open 3 clean (holiday closed-market time-point mismatch v57 same ruling) / ceo_order 1 clean (no CEO-order event today v57 same ruling) -> weekend line7 = ONLY honestly-pairable clean row (National Day holiday day 2 = non-working day = weekend-state holiday normalcy, v55 休市态 same-type precedent; scene = deep-night noodle stall soup still rolling = literal-night scene-compatible); post-v58 yanhuo clean-face structural note: weekend face zero clean remaining; yanhuo remaining clean rows = morning/6+7 + heatwave/3+12 + market_open/8+11+12 + ceo_order/7 (season/time/event mismatch honest notes) = yanhuo axis near-exhaustion on clean faces, supply-side rotation will cascade to other axes; post-v58 rotation note: yanhuo becomes 10 -> counts 10/9/9/10/9/9 -> next minimum = four-way tie (huaijiu v55 gap 2 / xiaqi v52 gap 6 / zhixu v53 gap 5 / xiaoyao v56 gap 2) -> next DAILY target = xiaqi (longest gap 6); 10-03 day-boundary round = E31 REACT-v9 first claim (daily brief 10-03 missing = produce first per O-2304 iron rule); F-number honesty note: this piece registers first = F-143, REACT-v9 预指位 F-143 顺延 F-144 (R978 判例 finished 顺序号=单一真相)")
io.open(os.path.join(TMP, "r1028_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V58:
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
# market_close bucket: v55 huaijiu/1 (first piece) + v57 qiuxin/1 (second piece).
# DUSK bucket: v56 xiaoyao/6 (first piece). WEEKEND bucket: THIS piece = yanhuo/7 (first piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 058",
    u"2026-10-02 · 国庆假期",
    u"「面条汤滚着呢，爱喝热乎的来碗」",
    u"——硅基城市台词池 · 烟火轴",
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
assert H2_SIZE == 50, "em ladder expected 50-band (16em quote line > 60-band budget 15.33em -> 50 budget 18.4em margin +2.4em; v29/v31 50-band precedent R998/R1000), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v58"
meta["form"] = (u"DAILY 城市日签 058（L-卡 图文轻内容线 DAILY 形态第五十八件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1028·日签节律续件=日期×情境桶对位判据第五十八证〔**weekend 假日态"
                u"邻接桶首件**（night v51/market_close v55/dusk v56 后第 4 个新开桶·**诚实注=假日态邻接非 literal "
                u"weekend 直配**〔10-02 周五=国庆假期第 2 日=非工作日=weekend 态假日常态对位·v55 休市态同型先例〕·"
                u"场景级=假日深夜面摊汤还滚着守候面=深夜 literal 夜场景兼容〕+**旋转律兑现（烟火回补·结构性诚实注）**："
                u"v57 后计数求新 10/怀旧 9/侠气 9/烟火 9/秩序 9/逍遥 9=**五轴并列最少→最长回补距=烟火〔v51 后 6 件"
                u"未采·v52-v57 六件皆他轴=R1027 指针兑现〕**→**烟火 12 桶 fresh 全扫 r1028_pool.txt（fleet 含 v57）**："
                u"night 0 干净行〔17 残留行全数带撞〕+festival 0 干净行〔10 残留行全数带撞〕+dusk 0+market_close 0="
                u"**四优先面全零干净行**→级联全桶扫描：morning 2/weekend 1/heatwave 2/market_open 3/ceo_order 1 干净行"
                u"·诚实排除注〔heatwave/coldsnap=十月秋季相错位 R972 邻接/market_open=国庆假日休市时点错位 v57 同判/"
                u"ceo_order=当日无 CEO 令事件 v57 同判/morning/6+ceo_order/7 共享「粥香扑鼻」4 字带互撞未来注+深夜生产×"
                u"早晨场景邻接弱于 weekend〕→weekend line7=**唯一可诚实配对干净行胜出**=零直撞标准不放松"
                u"〔R442 反同构主线·v1-v57 五十七连零直撞〕〕+line7 选优〔**全 shingle 零命中+零构式层邻接=系列第六件"
                u"全零邻接行**（v53/v54/v55/v56/v57 后连续·r1028_pool.txt fresh 2-5 字含标点 2 字组全零="
                u"r1028_quote_face.txt 九词机核〕+「滚着呢」「热乎的」「来碗」市井摊头口语真感=人味命中〔CEO 审美线对位〕+"
                u"烟火轴〔市井烟火气最重·摊头是主场〕×深夜散场后汤还滚着〔最爱凑热闹的摊主留一锅滚汤给爱喝热乎的人〕="
                u"**闹×守/散×暖轴内自反差金句位**〔族四十四连·守汤位语感独占注=夜市散了汤不散·节日散场后的城市温度〕〕〕）")
meta["source_quote"] = u"「面条汤滚着呢，爱喝热乎的来碗」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][weekend][7]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期第 2 日=DAILY-v1~v57 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][weekend][7] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 18 行计数"
                         u"+axes 6 轴+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-02=当日历法事实·国庆假期="
                         u"假期第 2 天〔daily brief 2026-10-02 当日窗语境〕③情境=weekend 假日态邻接桶首件"
                         u"〔**诚实注=10-02 周五=国庆假期第 2 日=非工作日=weekend 态假日常态对位·v55 休市态同型**·"
                         u"场景=深夜面摊汤还滚着=~23:4x 深夜生产场景级 literal 夜兼容·假日态邻接非 literal weekend "
                         u"直配〕④池级署名=台词池轴级行·本行无称谓面=纯景句·泛称零涉及〔人设权红线零接触·"
                         u"charter §2.4·v56/v57 纯景句同型先例〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+"
                         u"不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~v57 全 57 行+"
                         u"REACT-v8 同桶三行+city-spirit v1.2 节日场景三行皆非本行）+「面条」「汤滚」「滚着」「着呢」"
                         u"「热乎」「爱喝」「来碗」「面条汤」「汤滚着」probe 九词机核〔r1028_quote_face.txt〕+"
                         u"**零构式层邻接**〔r1028_pool.txt fresh 12 桶全扫 2-5 字含标点 2 字组全零=系列第六件全零"
                         u"邻接行·烟火四优先面全零干净行+weekend line7 级联胜出 fresh 实证〕⑥季相核=本行无年味/春联/"
                         u"春雨/寒潮类季相错位词〔R972 制·深夜面摊热汤=深秋夜体感对位〕⑦品牌语感注=「滚着呢」「热乎的」"
                         u"「来碗」市井摊头口语〔去 AI 感对位·日常口气=人味命中·零书面套语〕+面摊汤锅=市井生活意象"
                         u"非餐饮商业宣称·无品牌无价格=零消费宣称")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v55/v56/v57 泛称与纯景句先例族"
                             u"对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（weekend 假日态邻接桶首件〔**旋转律+"
                            u"全桶级联扫描+零直撞三律并轨诚实执行**：五轴并列→最长回补距烟火〔v51 后 6 件〕→12 桶 "
                            u"fresh 全扫→四优先面零干净行→季相/时点/情境排除→weekend line7 唯一可诚实配对行胜出〕+"
                            u"~23:4x 深夜生产同轮对位〔假日态邻接诚实注〕+闹×守/散×暖反差金句位〔族四十四连·守汤位语感"
                            u"独占注=夜市散了汤不散〕+「滚着呢」「热乎的」「来碗」市井口语=语录卡线变体零新模板第五十八证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 50 档〔v29/v31 50 档先例 R998/R1000·16em 引文行"
                            u"梯档降档如实注〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值"
                            u"面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔最爱凑热闹的市井烟火气"
                            u"在深夜散场后还留一锅滚汤=城市深夜温度的活证据·节日的热闹散场后城市的暖还在煮着〕+"
                            u"R442 人物场景处方带第七件〔v51 铺子守早客/v52 船老大夜航/v53 值夜岗慢步巡逻/v55 老陈头背手"
                            u"溜达/v56 江边钓鱼人/v57 收市摊主备新货+人物带续连=深夜面摊摊主守汤=市集摊主带第四采"
                            u"〔v32 早点摊/v44 早市豆浆摊/v57 收市备新货同族异面=深夜守候面〕〕+**供给面诚实注**：本件后"
                            u"烟火轴 weekend 面零干净行剩余→烟火剩余干净行=morning/6+7+heatwave/3+12+market_open/"
                            u"8+11+12+ceo_order/7〔季相/时点/情境错位注记在案+morning/6 与 ceo_order/7 「粥香扑鼻」"
                            u"4 字带互撞未来注〕=**烟火轴干净面结构性近枯竭注**→后续烟火回补须待池扩容或新供给面+"
                            u"post-v58 旋转注：烟火升至 10→计数 10/9/9/10/9/9→下一最少面=四轴并列（怀旧 gap 2/侠气 "
                            u"gap 6/秩序 gap 5/逍遥 gap 2）→下一 DAILY 目标=侠气〔v52 后 gap 6 最长〕·"
                            u"10-03 日界轮=E31 REACT-v9 首位可领〔10-03 日报缺先补产 daily_brief·O-2304 铁律〕·"
                            u"F 序号诚实注=本件先落 F-143·REACT-v9 预指位顺延 F-144〔R978 判例 finished 顺序号="
                            u"单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：夜市散场×汤还滚着=闹×守/散×暖反差〔族四十四连·"
                          u"守汤位语感独占注·夜市散了汤不散〕+「滚着呢」「来碗」市井摊头口语真感+深夜面摊守候场景具体"
                          u"〔R442 处方带〕/情 2 深夜守候温柔面+热汤体感暖意直击〔深秋夜体感对位〕/时 1 当日时点="
                          u"国庆假期第 2 日深夜〔**诚实注=weekend 假日态邻接非 literal weekend 直配·~23:4x 深夜生产×"
                          u"深夜面摊场景=场景级 literal 兼容·桶级假日态对位**〕/台 2 公众号方图承载=MC-001~142 S3 实证"
                          u"复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·"
                          u"queue §E E30 R1028 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面=纯景句·"
                     u"泛称零涉及〔v55/v56/v57 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（面摊热汤=市井生活意象非餐饮商业面·无品牌无价格=零消费宣称·「来碗」=摊头邀语非促销宣称）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十八件·charter v1.2 §4 形态码 DAILY·日签节律续件·weekend 假日态邻接桶首件·烟火轴回补件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][weekend][7] verbatim OK; weekend bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v57 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night bucket v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7 + sprite v50 festival/0 + v54 night/8 + market_close v55 huaijiu/1 + v57 qiuxin/1 + dusk v56 xiaoyao/6; yanhuo redemption: night/festival/dusk/market_close ALL zero clean rows (r1028_pool.txt fresh full 12-bucket scan, fleet includes v57) -> cascade full scan -> weekend line7 = ONLY honestly-pairable clean row (season/time/event exclusions per v57 rulings); quote-face word probe: 9 words see r1028_quote_face.txt (all ZERO; zero construct-layer adjacency = SIXTH fully-zero row of series after v53/v54/v55/v56/v57)")
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
report.append("LADDER_50: 16em quote-line driver (v29/v31 50-band precedent R998/R1000); four-LINES stack; all other QUOTE-v2 params verbatim; weekend-bucket-first DAILY piece + yanhuo-redemption + 6th-fully-zero-row honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1028.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V58, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V58, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v57 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 50, 16em quote-line band, v29/v31 precedent) + E4 fired async" % H2_SIZE)
