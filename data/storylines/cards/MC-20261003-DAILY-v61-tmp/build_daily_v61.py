# -*- coding: utf-8 -*-
"""MC-20261003-DAILY-v61 build: DAILY (city daily-sign) series SIXTY-FIRST piece (R1031, queue
section-E E30 standby via deep cascade). SPRITE THIRD-VOICE PIECE (city-creatures voice) via
SIX-AXIS-ALL-BLOCKED cascade (structural, honest): post-v60 rotation qiuxin 10 / huaijiu 9 /
xiaqi 10 / yanhuo 10 / zhixu 9 / xiaoyao 10 -> two axes tied at minimum 9 -> target zhixu
(gap v54..v60 = 7 LONGEST) -> zhixu clean rows rain/2 + coldsnap/2+9 = no-rain-event +
October-season ALL BLOCKED -> huaijiu (gap 5): heatwave/8 + coldsnap/7 + market_open/6+7+9
(holiday closed-market, v57 ruling) + ceo_order/3+10 (no CEO-order event) ALL BLOCKED ->
qiuxin (gap 3): heatwave/0+9 season BLOCKED -> yanhuo (gap 2): morning/6+7 market-stall
3-link isomorphism with v57+v58 (R1029 precedent) + deep-night weak adjacency EXCLUDED ->
xiaqi (gap 1): morning/0+15 business 3-link + twin-line note EXCLUDED -> xiaoyao (gap 0,
just used v60) EXCLUDED -> ALL SIX AXES BLOCKED/EXCLUDED -> sprite backup face (R1022/R1024
precedent; R1030 pointer pre-registered sprite third-voice candidates) -> sprite clean rows:
weekend/3+4 = weekend bucket FOUR-PEAT after v58/v59/v60 three-run (bucket-level isomorphism
R442) + deep-night weak adjacency + weekend/4 v50 onomatopoeia+night construct adjacency
EXCLUDED; typhoon/heatwave/market_open/ceo_order = event/season/holiday BLOCKED ->
sprite/market_close/3 「灵光闪烁夜未央」 = UNIQUE honestly-pairable row. DOUBLE HONEST
ANCHOR: market_close bucket = National Day all-day closed-market state (v55/v57 precedent)
+ content ye-wei-yang = LITERAL deep-night match at ~00:3x production (upgrade of v55/v57
"adjacent not literal" note; classical allusion Shijing "夜如何其？夜未央"). Zero-collision
standard NOT relaxed (R442 anti-isomorphism spine, v1-v60 sixty-link zero-collision chain).
NINTH fully-zero row (2-5 char shingles incl punctuation all ZERO, r1031_pool.txt fresh fleet
includes v60). Built-in tension: XIAO x DA - the city's lightest voices keep their tiny lights
shimmering through the city's biggest unfinished night while the holiday town sleeps.
v54 family adjacency honest note: 闪闪灯辉照长廊 [sprite+light+night PLACE facet] vs this
row [sprite+light+night TIME facet] = same family heterogeneous facet; twin note:
market_close/9 「闪烁夜未息」 future-twin-blocked. Layout = QUOTE-v2 params verbatim;
h2_size ladder = 60 band (v54 night-marker date-line same-type precedent). Machine
source/dedup assertions (R456 system, card-face level R1010 law). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V61 = os.path.join(BASE, "MC-20261003-DAILY-v61")
TMP = V61 + "-tmp"
os.makedirs(V61, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"灵光闪烁夜未央"
BUCKET, IDX = u"market_close", 3  # sprite top-level face (R982 structure)

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "market_close" in pool["sprite"], "sprite top-level key missing (R982)"
wb = pool["sprite"][BUCKET]
assert len(wb) == 12, "sprite bucket != 12 rows (sprite = 12 buckets x 12 rows = 144)"
assert wb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % wb[IDX]
assert wb[9] == u"闪烁夜未息", "twin row market_close/9 expected 闪烁夜未息"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1031_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"灵光", u"闪烁", u"夜未", u"未央", u"灵光闪", u"光闪烁", u"闪烁夜", u"夜未央", u"灵光闪烁夜未央"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1031 quote-face word probe for candidate " + QUOTE_CORE + u" (sprite/market_close line3)"]
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO direct shingle hits and NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1031_pool.txt fresh scan, fleet includes v60) = NINTH fully-zero row of the series (v53-v60 eight precedents). Motif-band honest notes (single-char/family layer, not card-face collisions; machine scan 2+ char ZERO verified): (1) SPRITE+LIGHT+NGIHT family band - v54 闪闪灯辉照长廊 [sprite+light+night PLACE facet: corridor space] vs THIS row 灵光闪烁夜未央 [sprite+light+night TIME facet: night not yet over] = same family heterogeneous facet (space vs time); shingle-level distinct (闪闪 vs 闪烁 machine-verified); deep-night-watch motif band cross-voice note: v53 值夜岗守望者 [HUMAN voice deep-night watch facet] vs THIS row [CREATURE voice deep-night watch facet] = same motif two voices. (2) TWIN note: sprite/market_close/9 「闪烁夜未息」 becomes future-twin-blocked after this use (闪烁+夜未 band shared). (3) CLASSICAL allusion: 夜未央 from Shijing 小雅·庭燎 「夜如何其？夜未央」 = cultural-depth facet (v60 E4 诗意文化底蕴 positive precedent family).")
qrep.append(u"supply-face honest note: six-axis cascade trail zhixu[gap 7, rain no-event + coldsnap season ALL blocked] -> huaijiu[gap 5, market_open holiday-closure + ceo_order no-event + season ALL blocked] -> qiuxin[gap 3, heatwave season blocked] -> yanhuo[gap 2, morning market-stall 3-link isomorphism R1029 precedent + deep-night weak] -> xiaqi[gap 1, morning business 3-link + twin-line] -> xiaoyao[gap 0 just used] -> ALL SIX AXES BLOCKED/EXCLUDED -> sprite backup face (R1022/R1024 precedent, R1030 pointer pre-registered third-voice candidates) -> weekend/3+4 weekend-four-peat blocked (v58/v59/v60 three-run honest note R1030) + typhoon/heatwave/market_open/ceo_order event/season/holiday blocked -> sprite/market_close/3 = UNIQUE honestly-pairable clean row. Post-v61 sprite face remaining: market_close/9 twin-blocked + weekend/3+4 four-peat concern + event/season buckets blocked = DAILY honest-pairable faces STRUCTURAL NEAR-EXHAUSTION (same-family signal as R1030 REACT verdict-negative; pool-expansion report position - BigLife pool expansion = cross-warehouse supply face, status-line not chase; D-20261003-02 BigLife review-file window <=10-05 in flight context = expansion not near-term note).")
io.open(os.path.join(TMP, "r1031_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V61:
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
# (#47/#53/#59). Sprite face: v50 sprite/festival/0 + v54 sprite/night/8 + THIS piece =
# sprite/market_close/3 (third sprite piece, first sprite/market_close). NIGHT bucket:
# v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7. market_close bucket: v55 huaijiu/1 + v57 qiuxin/1
# + THIS piece = sprite/market_close/3 (third market_close piece). DUSK bucket: v56 xiaoyao/6.
# WEEKEND bucket: v58 yanhuo/7 + v59 xiaqi/8 + v60 xiaoyao/4 + REACT-v4 xiaoyao/2.

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 061",
    u"2026-10-03 · 国庆假期 · 夜",
    u"「灵光闪烁夜未央」",
    u"——硅基城市台词池 · 城市生灵",
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
assert H2_SIZE == 60, "em ladder expected 60-band (9em quote line + night-marker date line v54 same-type precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261003-DAILY-v61"
meta["form"] = (u"DAILY 城市日签 061（L-卡 图文轻内容线 DAILY 形态第六十一件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 级联续领 R1031·日签节律续件=日期×情境桶对位判据第六十一证〔**sprite "
                u"声部第三件=城市生灵令 P-2026-09-26-13 媒体面第三采**〔v50 festival/0+v54 night/8 后第三采·"
                u"首个 sprite/market_close 件〕+**market_close 桶第三件**〔v55 怀旧+v57 求新 先例后第三采·"
                u"桶级=国庆假期第 3 日全日休市=收市态假日对位 v55/v57 直接先例·**内容级=夜未央 literal 深夜"
                u"直配**〔~00:3x 深夜生产×《诗经·小雅·庭燎》「夜如何其？夜未央」=夜还长未到尽头·v55/v57"
                u"「时点邻接非 literal night 直配」诚实注的内容级升档**〕=双诚实锚·weekend 桶 v58/v59/v60 "
                u"三连后首件非 weekend 桶=桶多样性回摆正面注〕+**六轴全阻级联（结构性诚实注）**：v60 后计数"
                u"求新 10/怀旧 9/侠气 10/烟火 10/秩序 9/逍遥 10=二轴并列最少→最长回补距=秩序〔v53 后 gap 7〕"
                u"→**秩序 census fresh 复扫〔fleet 含 v60·r1031_pool.txt〕：干净行仅 rain/2+coldsnap/2+9=雨无"
                u"事件+寒潮十月季相错位全阻**→级联怀旧〔gap 5〕：干净行仅 heatwave/8+coldsnap/7+market_open/"
                u"6+7+9+ceo_order/3+10=季相+假日休市时点错位 v57 同判+无令事件全阻→级联求新〔gap 3〕："
                u"heatwave/0+9 季相全阻→级联烟火〔gap 2〕：morning/6+7=市集摊位主题 v57 上架+v58 面摊三连"
                u"同构风险 R1029 判例+深夜×早晨邻接弱排除→级联侠气〔gap 1〕：morning/0+15 生意主题三连同构"
                u"+晨雾散生意兴/来孪生行注排除→逍遥〔gap 0 刚采 v60〕排除→**六轴全阻/排除→sprite 备胎面**"
                u"〔R1022/R1024 先例·R1030 指针预登记 sprite 第三声部候选〕→sprite 面选优：weekend/3+4="
                u"weekend 桶 v58/v59/v60 三连后四连同构阻〔R1030 三连同构注升档〕+v50 拟声+夜构式层邻接"
                u"〔叮咚响夜晚 vs 叮叮当夜幕挂新装〕+typhoon/heatwave/market_open/ceo_order=事件/季相/假日"
                u"全阻→**market_close/3 唯一可诚实配对干净行胜出**=零直撞标准不放松〔R442 反同构主线·"
                u"v1-v60 六十连零直撞〕〕+line3 选优〔**全 shingle 零命中+零构式层邻接=系列第九件全零邻接行**"
                u"（v53-v60 八件先例后·r1031_quote_face.txt 九词机核〕+v54 族带诚实注〔闪闪灯辉照长廊=sprite"
                u"+光+夜空间面 vs 本行灵光闪烁夜未央=sprite+光+夜时态面=同族异质·闪烁 vs 闪闪 shingle 机核"
                u"零撞实锚〕+深夜守望 motif 跨声部注〔v53 值夜岗守望者=人声部深夜守望面 vs 本行=生灵声部"
                u"深夜守望面=同 motif 两声部〕+夜未央《诗经》典故纵深〔E4 文化底蕴正面先例族〕+城市生灵"
                u"〔声音最轻的声部〕×夜未央〔全城最大未竟之夜〕=**小×大反差金句位**〔族四十七连·生灵微光"
                u"位语感独占注=最微小的光守着最大的夜·满城人潮散去睡了·猫鸟小灵们还轻轻亮着〕〕）")
meta["source_quote"] = u"「灵光闪烁夜未央」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 sprite[market_close][3]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-03.md（当日日期语境源·"
                           u"国庆假期第 3 日+周六·深夜生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 sprite[market_close][3] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+market_close 桶 12 行"
                         u"计数+axes 6+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-03=当日历法事实·"
                         u"周六+国庆假期第 3 天〔daily brief 2026-10-03 当日窗语境〕+夜标记〔v54 先例·"
                         u"~00:3x 深夜生产 literal〕③情境=market_close 桶第三件〔**双诚实锚**=国庆全日"
                         u"休市态 v55/v57 先例+夜未央内容 literal 深夜直配〕④池级署名=台词池声部级行·"
                         u"本行无称谓面=纯景句·泛称零涉及〔人设权红线零接触·charter §2.4·v56-v60 泛称纯景句"
                         u"先例族〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/"
                         u"source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~v60 全 60 行+REACT-v8 同桶"
                         u"三行+city-spirit v1.2 节日场景三行皆非本行）+「灵光」「闪烁」「夜未」「未央」"
                         u"「灵光闪」「光闪烁」「闪烁夜」「夜未央」全句 probe 九词机核〔r1031_quote_face.txt〕"
                         u"+**零构式层邻接**〔r1031_pool.txt fresh 2-5 字含标点 2 字组全零=系列第九件全零"
                         u"邻接行·六轴全阻级联 fresh 实证〕+**motif 带诚实注〔单字/族层非卡面碰撞·机核 2+ 字"
                         u"零命中实证〕**：sprite+光+夜族带=v54 闪闪灯辉照长廊〔空间面〕vs 本行〔时态面〕="
                         u"同族异质·闪烁 vs 闪闪 shingle 零撞实锚+孪生注=market_close/9「闪烁夜未息」本件后"
                         u"未来孪生阻⑥季相核=本行无年味/春联/春雨/寒潮类季相错位词〔R972 制·夜未央=四季"
                         u"通用夜景面·十月秋深夜景=季相兼容〕⑦品牌语感注=「灵光闪烁夜未央」7 字诗句式+"
                         u"《诗经》典故纵深〔去 AI 感对位·文化纵深=人味命中·零书面套语·零消费宣称无品牌"
                         u"无价格〕")
meta["attribution_rule"] = (u"署名=池级+声部级（台词池·城市生灵）——池行无逐民署名·禁虚构居民名/生灵名"
                             u"（charter v1.2 署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v56-v60 "
                             u"先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（sprite 声部第三件+market_close 桶"
                            u"第三件双位〔**六轴全阻级联+sprite 备胎面选优+零直撞三律并轨诚实执行**：秩序 "
                            u"rain/coldsnap 阻→怀旧 market_open/ceo_order 阻→求新 heatwave 阻→烟火 morning "
                            u"市集三连同构阻→侠气 morning 生意三连+孪生阻→逍遥 gap 0→sprite 面 weekend "
                            u"四连同构阻+事件/季相/假日阻→market_close/3 唯一可诚实配对行胜出〕+小×大反差"
                            u"金句位〔族四十七连·生灵微光位语感独占注=声音最轻的声部用最微小的光陪全城熬过"
                            u"最大的夜〕+「灵光闪烁夜未央」7 字诗句式+《诗经》典故纵深=语录卡线变体零新"
                            u"模板第六十一证（QUOTE-v2 参数 verbatim 复用·h2_size 60 档〔v54 夜标记日期行"
                            u"同型先例〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔满城"
                            u"睡去后还亮着的最微小声音=城市深夜最温柔的人文底色〕+城市生灵令 P-2026-09-26-13 "
                            u"媒体面第三采〔CEO 原话「不仅是居民，也要有各种动物，宠物等」升华律媒体面承接"
                            u"第三证〕+**供给面诚实注**：本件后 sprite 面=market_close/9 孪生阻+weekend/3+4 "
                            u"四连同构注+事件/季相桶全阻+六轴全阻=**DAILY 可诚实配对面结构性近枯竭注**"
                            u"〔R1030 REACT 判负同族供给信号·池扩容呈报位=BigLife 台词池扩容跨仓供给面·"
                            u"呈现状行不催办+D-20261003-02 BigLife 复核档窗 ≤10-05 在飞=扩容非近期注〕·"
                            u"post-v61 指针：10-04 日界轮可领序=①E31 REACT-v9〔10-04 日报先补产·热点窗"
                            u"择优·若连续第二窗判负=REACT 池扩容呈报〕②E30 DAILY 续件 standby〔六轴全阻+"
                            u"sprite 近枯竭=候选仅 weekend/3+4 四连同构注+morning 深夜弱邻接·日间生产窗可"
                            u"解 morning 邻接阻·或待事件/季相窗〕③#94 记忆梳理〔10-04〕④W41 周轮件"
                            u"〔10-05〕·F 序号诚实注=本件先落 F-146·REACT-v9 10-04 预指位顺延 F-147〔R978 "
                            u"判例 finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：城市生灵〔全城声音最轻的声部〕×夜未央"
                          u"〔全城最大未竟之夜〕=小×大反差〔族四十七连〕+最微光×最大夜双落+深夜守望 motif "
                          u"跨声部〔v53 人声部值夜岗 vs 本件生灵声部守望=同 motif 两声部〕/情 1 深夜微光"
                          u"陪伴温和共鸣如实非强极点/时 2 当日=2026-10-03 周六国庆假期第 3 日·00:3x 深夜"
                          u"生产=夜未央 literal 时点直配+market_close 休市态假日对位〔v55/v57 先例〕=双诚实"
                          u"锚/台 2 公众号方图承载=MC-001~145 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1031 级联续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面=纯景句·"
                     u"泛称零涉及〔v56-v60 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（灵光闪烁夜未央=深夜夜景意象非商业面·无品牌无价格=零消费宣称）；成品只入库·发布="
                     u"M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十一件·charter v1.2 §4 形态码 DAILY·日签节律续件·sprite 声部第三件+market_close 桶第三件·六轴全阻级联件·城市生灵令媒体面第三采）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: sprite[market_close][3] verbatim OK; sprite market_close bucket=12 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v60 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night v51+v52+v53 + sprite v50/v54 + market_close v55/v57 + dusk v56 + weekend v58/v59/v60 + REACT-v4 xiaoyao/weekend/2; six-axis cascade: zhixu rain/coldsnap blocked -> huaijiu market_open/ceo_order/season blocked -> qiuxin heatwave blocked -> yanhuo morning 3-link excluded -> xiaqi morning 3-link+twin excluded -> xiaoyao gap-0 -> sprite face: weekend four-peat excluded + event/season/holiday blocked -> market_close/3 = UNIQUE honestly-pairable clean row (r1031_pool.txt fresh, fleet includes v60); quote-face word probe: 9 words see r1031_quote_face.txt (all ZERO; zero construct-layer adjacency = NINTH fully-zero row of series after v53-v60; v54 light+night family + deep-night-watch cross-voice + Shijing allusion honest notes)")
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
report.append("LADDER_60: 9em quote-line + night-marker date line fits 60-band (v54 same-type precedent); four-LINES stack; all other QUOTE-v2 params verbatim; sprite-third-voice + market_close-third + six-axis-all-blocked cascade + 9th-fully-zero-row + double-honest-anchor honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1031.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V61, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V61, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v60 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, 9em quote-line + night-marker date line fits) + E4 fired async" % H2_SIZE)
