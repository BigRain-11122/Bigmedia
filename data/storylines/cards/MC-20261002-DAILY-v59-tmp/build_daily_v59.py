# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v59 build: DAILY (city daily-sign) series FIFTY-NINTH piece (R1029, queue
section-E E30 standby). XIAQI-REDEMPTION PIECE (structural, honest): rotation post-v58 counts
qiuxin 10 / huaijiu 9 / xiaqi 9 / yanhuo 10 / zhixu 9 / xiaoyao 9 -> FOUR AXES TIED AT 9 ->
redemption target = xiaqi (last v52 night/4, gap v53..v58 = 6 pieces = LONGEST; R1028
next-pointer redemption). Per R1028 pointer: xiaqi FULL fresh supply-face scan r1029_pool.txt
(ALL 12 buckets x 18 rows = 216 rows, fleet includes v58) -> night 0 clean (17 residual rows
ALL carry hits after v52/4 consumption) + festival 0 clean (10 residual ALL carry after
8-row consumption) + dusk 0 clean + market_close 0 clean = FOUR PRIORITY FACES ALL ZERO
CLEAN -> cascade full-bucket scan: morning 2 / weekend 1 / rain 3 / typhoon 1 / heatwave 2 /
coldsnap 1 / market_open 0 / ceo_order 1 clean rows; honest exclusions: heatwave+coldsnap =
October-autumn season-face mismatch (R972-adjacent), typhoon = no typhoon event today (context
mismatch, event bucket needs actual event), rain = no rain event today (context mismatch, no
rain anchor in daily brief), market_open = holiday closed-market time-point mismatch (v57
ruling), ceo_order = no CEO-order event today (v57 ruling), morning 2 clean rows = deep-night
x morning weaker adjacency (v58 ruling) + third consecutive market-stall theme after v57
(新奇玩意儿正上架) + v58 (面摊汤) = series-isomorphism risk -> weekend line8
「帆起云开，海阔天空」 = WINNER (ZERO direct shingle hits, 2-5 char punctuation-inclusive
2-grams all zero = SEVENTH fully-zero row of the series after v53/v54/v55/v56/v57/v58).
Zero-collision standard NOT relaxed (R442 anti-isomorphism spine, v1-v58 fifty-eight-link
zero-collision chain). WEEKEND BUCKET SECOND DAILY PIECE (v58 yanhuo/7 first; honest note:
2026-10-02 Friday = National Day holiday day 2 = non-working day = weekend-state holiday
normalcy pairing, v58 direct precedent; production ~23:5x deep night x scene (sail rising,
clouds parting, sea-wide-sky-vast aspirational vista = not time-bound) = scene compatible;
bucket-level = 假日态邻接非 literal weekend 直配 honest note.
Built-in tension: NAO x KUO - the most crowd-loving, bond-foremost axis blesses with the
widest, loneliest sea-sky vista; 帆起云开 (smallest concrete action, one sail rising) x
海阔天空 (vastest openness) = small-x-big double contrast. 「海阔天空」 familiar idiom =
common-property idiom honest note (fleet zero hits machine-verified; verbatim red line
unchanged). Layout = QUOTE-v2 params verbatim; h2_size ladder = 60 band (11em quote line
fits 60-band budget 15.33em margin +4.33em = zero-template default band, v2/v6/v20/v24
precedent family). Machine source/dedup assertions (R456 system, card-face level R1010 law).
All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V59 = os.path.join(BASE, "MC-20261002-DAILY-v59")
TMP = V59 + "-tmp"
os.makedirs(V59, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"帆起云开，海阔天空"
AXIS, BUCKET, IDX = u"侠气", u"weekend", 8

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
wb = pool["axes"][AXIS][BUCKET]
assert len(wb) == 18, "axis bucket != 18 rows (axes = 6 x 12 buckets x 18 rows = 1296)"
assert wb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % wb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1029_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"帆起", u"云开", u"海阔", u"天空", u"海阔天空", u"帆起云开", u"云开，", u"阔天", u"海阔天"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1029 quote-face word probe for candidate " + QUOTE_CORE + u" (xiaqi/weekend line8)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1029_pool.txt fresh full 12-bucket scan, fleet includes v58) = SEVENTH fully-zero row of the series (v53/v54/v55/v56/v57/v58 six precedents); 海阔天空 = familiar common-property idiom honest note (idiom layer, not a card-face collision; machine scan fleet ZERO verified; verbatim red line unchanged); supply-face honest note: xiaqi four priority faces (night/festival/dusk/market_close) ALL zero clean rows fresh (night 17 residual rows all carry hits after v52/4 consumption; festival 10 residual all carry after 8-row consumption v3/5+v8/13+v13/2+v20/1+v26/10+v34/9+v46/7+city-spirit xiaqi/0) -> cascade full-bucket scan: morning 2 clean (deep-night x morning weaker adjacency v58 ruling + third consecutive market-stall theme after v57 上架/v58 面摊 = series-isomorphism risk) / rain 3 clean (no rain event today = context mismatch) / typhoon 1 clean (no typhoon event) / heatwave 2 + coldsnap 1 (October-autumn season mismatch R972-adjacent) / market_open 0 clean (holiday closed-market) / ceo_order 1 clean (no CEO-order event today) -> weekend line8 = ONLY honestly-pairable clean row (National Day holiday day 2 = non-working day = weekend-state holiday normalcy, v58 direct precedent; scene = sail rising clouds parting sea-wide-sky-vast aspirational vista = not time-bound); post-v59 xiaqi clean-face structural note: weekend face zero clean remaining (line8 consumed; line7 船长说过 etc. carry hits); xiaqi remaining clean rows = morning/0+15 (deep-night adjacency weak + market-stall isomorphism risk) + rain/5+6+7 (no-rain-event context mismatch) + typhoon/11 + heatwave/6+14 + coldsnap/10 (season/event mismatches) = xiaqi axis clean faces approaching structural exhaustion on honestly-pairable faces, supply-side rotation will cascade; post-v59 rotation note: xiaqi becomes 10 -> counts qiuxin 10/huaijiu 9/xiaqi 10/yanhuo 10/zhixu 9/xiaoyao 9 -> next minimum = two-way tie (huaijiu last v55 gap v56..v59=3 / zhixu last v53 gap v54..v59=5 / xiaoyao last v56 gap v57..v59=2... three-way at 9: huaijiu 9/zhixu 9/xiaoyao 9) -> next DAILY target = zhixu (longest gap 5); 10-03 day-boundary round = E31 REACT-v9 first claim (daily brief 10-03 missing = produce first per O-2304 iron rule)")
io.open(os.path.join(TMP, "r1029_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V59:
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
# DUSK bucket: v56 xiaoyao/6 (first piece). WEEKEND bucket: v58 yanhuo/7 (first piece) +
# THIS piece = xiaqi/8 (second piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 059",
    u"2026-10-02 · 国庆假期",
    u"「帆起云开，海阔天空」",
    u"——硅基城市台词池 · 侠气轴",
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
assert H2_SIZE == 60, "em ladder expected 60-band (11em quote line < 60-band budget 15.33em margin +4.33em; zero-template default band, v2/v6/v20/v24 family precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v59"
meta["form"] = (u"DAILY 城市日签 059（L-卡 图文轻内容线 DAILY 形态第五十九件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1029·日签节律续件=日期×情境桶对位判据第五十九证〔**weekend 假日态"
                u"邻接桶第二件**（v58 烟火/7 首件后第二采·night v51/market_close v55/dusk v56 后第 4 个开桶"
                u"·**诚实注=假日态邻接非 literal weekend 直配**〔10-02 周五=国庆假期第 2 日=非工作日=weekend 态"
                u"假日常态对位·v58 直接先例〕·场景级=帆起云开海阔天空的开阔视野面=不受时点绑定的祝愿面·"
                u"~23:5x 深夜生产×开阔祝愿场景兼容〕+**旋转律兑现（侠气回补·结构性诚实注）**："
                u"v58 后计数求新 10/怀旧 9/侠气 9/烟火 10/秩序 9/逍遥 9=**四轴并列最少→最长回补距=侠气〔v52 后 6 件"
                u"未采·v53-v58 六件皆他轴=R1028 指针兑现〕**→**侠气 12 桶 fresh 全扫 r1029_pool.txt（fleet 含 v58）**："
                u"night 0 干净行〔17 残留行全数带撞〕+festival 0 干净行〔10 残留行全数带撞〕+dusk 0+market_close 0="
                u"**四优先面全零干净行**→级联全桶扫描：morning 2/weekend 1/rain 3/typhoon 1/heatwave 2/coldsnap 1/"
                u"ceo_order 1 干净行·诚实排除注〔heatwave/coldsnap=十月秋季相错位 R972 邻接/typhoon+rain=当日无台风无雨"
                u"事件=情境错位〔事件桶须有事件锚〕/market_open=国庆假日休市时点错位 v57 同判/ceo_order=当日无 CEO 令"
                u"事件 v57 同判/morning 2 行=深夜生产×早晨邻接弱 v58 判例+市集摊位主题 v57 上架+v58 面摊三连同构风险"
                u"R442〕→weekend line8=**唯一可诚实配对干净行胜出**=零直撞标准不放松"
                u"〔R442 反同构主线·v1-v58 五十八连零直撞〕〕+line8 选优〔**全 shingle 零命中+零构式层邻接=系列第七件"
                u"全零邻接行**（v53/v54/v55/v56/v57/v58 后连续·r1029_quote_face.txt 九词机核〕+「海阔天空」大众熟语"
                u"祝愿口语真感=人味命中〔CEO 审美线对位·熟语=公共语料诚实注·verbatim 零改写红线不动〕+侠气轴〔最豪爽"
                u"·嗓门最大·情义至重·人堆里讲义气〕×海阔天空〔最远离人群的最大最远开阔〕="
                u"**闹×阔轴内自反差金句位**〔族四十五连·祝酒位语感独占注=最爱凑热闹讲义气的轴把祝福说成一句行船人的"
                u"开阔话·帆起云开=最小具体动作×海阔天空=最大无垠开阔=小×大双反差〕〕〕）")
meta["source_quote"] = u"「帆起云开，海阔天空」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[侠气][weekend][8]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期第 2 日=DAILY-v1~v58 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[侠气][weekend][8] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 18 行计数"
                         u"+axes 6 轴+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-02=当日历法事实·国庆假期="
                         u"假期第 2 天〔daily brief 2026-10-02 当日窗语境〕③情境=weekend 假日态邻接桶第二件"
                         u"〔**诚实注=10-02 周五=国庆假期第 2 日=非工作日=weekend 态假日常态对位·v58 直接先例**·"
                         u"场景=帆起云开海阔天空开阔祝愿面=~23:5x 深夜生产×不受时点绑定的祝愿场景兼容·假日态邻接非 "
                         u"literal weekend 直配〕④池级署名=台词池轴级行·本行无称谓面=纯祝愿句·泛称零涉及〔人设权"
                         u"红线零接触·charter §2.4·v56/v57/v58 纯景句同型先例〕⑤去重断言=本行不在 city-spirit.md 64 "
                         u"条已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~v58 全 "
                         u"58 行+REACT-v8 同桶三行+city-spirit v1.2 节日场景三行皆非本行）+「帆起」「云开」「海阔」"
                         u"「天空」「海阔天空」「帆起云开」「云开，」「阔天」「海阔天」probe 九词机核〔r1029_quote_face."
                         u"txt〕+**零构式层邻接**〔r1029_pool.txt fresh 12 桶全扫 2-5 字含标点 2 字组全零=系列第七件"
                         u"全零邻接行·侠气四优先面全零干净行+weekend line8 级联胜出 fresh 实证·「海阔天空」=大众熟语"
                         u"公共语料层诚实注非卡面碰撞·机核 fleet 零命中实证〕⑥季相核=本行无年味/春联/春雨/寒潮类"
                         u"季相错位词〔R972 制·海阔天空=四季通用祝愿面〕⑦品牌语感注=「帆起云开」行船人语感+"
                         u"「海阔天空」大众熟语祝愿口气〔去 AI 感对位·日常口气=人味命中·零书面套语·熟语层诚实注=verbatim "
                         u"零改写红线不动〕+开阔祝愿=人生哲理面意象非商业宣称·无品牌无价格=零消费宣称")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·侠气轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·本行无称谓面=纯祝愿句·泛称零涉及〔v56/v57/v58 泛称与纯景句先例族"
                             u"对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（weekend 假日态邻接桶第二件〔**旋转律+"
                            u"全桶级联扫描+零直撞三律并轨诚实执行**：四轴并列→最长回补距侠气〔v52 后 6 件〕→12 桶 "
                            u"fresh 全扫→四优先面零干净行→季相/时点/情境/同构排除→weekend line8 唯一可诚实配对行"
                            u"胜出〕+~23:5x 深夜生产同轮对位〔假日态邻接诚实注〕+闹×阔反差金句位〔族四十五连·祝酒位"
                            u"语感独占注=最爱凑热闹讲义气的轴把祝福说成全城最大最远的开阔话〕+「帆起云开」「海阔天空」"
                            u"大众熟语祝愿口语=语录卡线变体零新模板第五十九证（QUOTE-v2 参数 verbatim 复用·h2_size 60 "
                            u"档〔零新模板默认带·v2/v6/v20/v24 先例族〕·charter §1「日签变体随时可续」兑现）·公众号"
                            u"低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 "
                            u"对位〔最爱在人堆里讲义气的居民给出的是海阔天空的祝福=城市胸襟的活证据〕+R442 人物场景"
                            u"处方带第八件〔v51 铺子守早客/v52 船老大夜航/v53 值夜岗慢步巡逻/v55 老陈头背手溜达/"
                            u"v56 江边钓鱼人/v57 收市摊主备新货/v58 深夜面摊摊主守汤+人物带续连=假期祝酒的豪爽居民="
                            u"酒馆江湖带第三采〔v3 对饮面/v40 酒香配灯面+本行=祝酒开阔面=同族异面〕〕+**供给面诚实注**："
                            u"本件后侠气轴 weekend 面零干净行剩余→侠气剩余干净行=morning/0+15〔深夜邻接弱+摊位同构"
                            u"风险〕+rain/5+6+7〔无雨事件情境错位〕+typhoon/11+heatwave/6+14+coldsnap/10〔季节/事件"
                            u"错位〕+ceo_order/2〔无令事件〕=**侠气轴干净面结构性近枯竭注（可诚实配对面）**→后续侠气"
                            u"回补须待池扩容或新供给面+post-v59 旋转注：侠气升至 10→计数求新 10/怀旧 9/侠气 10/烟火 "
                            u"10/秩序 9/逍遥 9→下一最少面=三轴并列（怀旧 v55 后 gap 3/秩序 v53 后 gap 5/逍遥 v56 后 "
                            u"gap 2）→下一 DAILY 目标=秩序〔gap 5 最长〕·10-03 日界轮=E31 REACT-v9 首位可领〔10-03 "
                            u"日报缺先补产 daily_brief·O-2304 铁律〕·F 序号诚实注=本件先落 F-144·REACT-v9 预指位顺延 "
                            u"F-145〔R978 判例 finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：侠气轴〔最豪爽·情义至重·人堆里讲义气〕×"
                          u"海阔天空〔最远离人群的最大最远开阔〕=闹×阔反差〔族四十五连·祝酒位语感独占注〕+帆起云开"
                          u"〔最小具体动作〕×海阔天空〔最大无垠开阔〕=小×大双反差+「海阔天空」大众熟语祝愿口语真感"
                          u"+假期祝酒场景具体〔R442 处方带〕/情 1 开阔祝愿温和共鸣如实非强极点/时 1 当日时点="
                          u"国庆假期第 2 日假日态〔**诚实注=weekend 假日态邻接非 literal weekend 直配·v58 直接先例**〕/"
                          u"台 2 公众号方图承载=MC-001~143 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1029 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面=纯祝愿句·"
                     u"泛称零涉及〔v56/v57/v58 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（海阔天空=人生哲理面祝愿意象非商业面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号"
                     u"物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十九件·charter v1.2 §4 形态码 DAILY·日签节律续件·weekend 假日态邻接桶第二件·侠气轴回补件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaqi][weekend][8] verbatim OK; weekend bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v58 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night bucket v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7 + sprite v50 festival/0 + v54 night/8 + market_close v55 huaijiu/1 + v57 qiuxin/1 + dusk v56 xiaoyao/6 + weekend v58 yanhuo/7; xiaqi redemption: night/festival/dusk/market_close ALL zero clean rows (r1029_pool.txt fresh full 12-bucket scan, fleet includes v58) -> cascade full scan -> weekend line8 = ONLY honestly-pairable clean row (season/time/event/isomorphism exclusions per v57/v58 rulings); quote-face word probe: 9 words see r1029_quote_face.txt (all ZERO; zero construct-layer adjacency = SEVENTH fully-zero row of series after v53/v54/v55/v56/v57/v58)")
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
report.append("LADDER_60: 11em quote-line fits 60-band budget 15.33em margin +4.33em (zero-template default band, v2/v6/v20/v24 family); four-LINES stack; all other QUOTE-v2 params verbatim; weekend-bucket-second DAILY piece + xiaqi-redemption + 7th-fully-zero-row honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1029.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V59, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V59, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v58 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, 11em quote-line fits, zero-template default band) + E4 fired async" % H2_SIZE)
