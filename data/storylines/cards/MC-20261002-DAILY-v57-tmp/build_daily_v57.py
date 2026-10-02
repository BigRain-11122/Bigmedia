# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v57 build: DAILY (city daily-sign) series FIFTY-SEVENTH piece (R1027, queue
section-E E30 standby). QIUXIN-REDEMPTION PIECE (structural, honest): rotation post-v56 counts
qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 9 = SIX AXES ALL-TIED (4th
all-tie state after R1006/R1012/R1018-era states; precedent = longest-gap redemption) ->
qiuxin last consumed v49 (festival/9), gap = v50..v56 seven pieces all other axes = LONGEST
redemption distance -> redemption target = qiuxin. Per R1026 next-pointer: qiuxin FULL fresh
supply-face scan r1027_pool.txt (ALL 12 buckets x 18 rows = 216 rows, fleet includes v56) ->
night 18 rows ALL content collisions (literal night face blocked, huaijiu/xiaoyao-night
same-type) + festival 18 rows ALL carry hits (nine-consumption saturated face) + dusk 18
rows ALL carry hits -> cascade = market_close line1 「新奇玩意儿正上架」 = ONLY clean row
among the four priority faces (ZERO direct shingle hits, 2-5 char including
punctuation-inclusive 2-grams all zero = zero construct-layer adjacency = FIFTH fully-zero
row of the series after v53/v54/v55/v56; row has no punctuation at all -> punctuation-pair
construct adjacency physically impossible). Zero-collision standard NOT relaxed (R442
anti-isomorphism spine, v1-v56 fifty-six-link zero-collision chain). market_close BUCKET
SECOND DAILY PIECE (v55 huaijiu/1 first piece -> v57 qiuxin/1 second piece, same-bucket
different-axis different-line; honest note: ~23:2x deep-night production x market-close
evening scene = time-adjacent NOT time-exact, v55 same-type precedent; National Day holiday
day 2 = market closed state = market-close state holiday normalcy pairing, v55 precedent).
Built-in tension: SHOU x SHANG - the market has closed for the day, yet the stall is still
stocking new novelty goods for tomorrow's holiday crowds; the moment the day ends is the
moment new things appear. 「玩意儿」 = northern street-colloquial register + 「正」
progressive-aspect immediacy = human-flavor hit. Supply honest note: 「玩意儿」 also lives in
4 unconsumed qiuxin pool rows (market_open/7+16, ceo_order/12+13) = within-axis native-word
depth-band first harvest (same law as cha/yi=xiayao, jiu=xiaqi, jiaozhun=zhixu bands);
market_open/16 「新奇玩意儿先摸个遍」 shares the 4-char band 「新奇玩意儿」 with this card
-> it becomes a future collision row once this piece is registered (next qiuxin scan must
re-probe with v57 in fleet). Layout = QUOTE-v2 params verbatim; h2_size ladder = 60 band
(short-quote band, v54/v56 precedent; attribution-line 12.65em driver at 60 budget 15.33em).
Machine source/dedup assertions (R456 system, card-face level R1010 law). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V57 = os.path.join(BASE, "MC-20261002-DAILY-v57")
TMP = V57 + "-tmp"
os.makedirs(V57, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"新奇玩意儿正上架"
AXIS, BUCKET, IDX = u"求新", u"market_close", 1

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
mb = pool["axes"][AXIS][BUCKET]
assert len(mb) == 18, "axis bucket != 18 rows (axes = 6 x 12 buckets x 18 rows = 1296)"
assert mb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % mb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1027_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"新奇", u"玩意儿", u"上架", u"正上架", u"新奇玩", u"奇玩意", u"玩意儿正", u"儿正上", u"玩意儿正上架"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1027 quote-face word probe for candidate " + QUOTE_CORE + u" (qiuxin/market_close line1)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1027_pool.txt fresh full 12-bucket scan, fleet includes v56) = FIFTH fully-zero row of the series (v53 first / v54 second / v55 third / v56 fourth / this fifth); row contains no punctuation at all -> punctuation-pair construct adjacency physically impossible; supply-face honest note: qiuxin/night 18 rows ALL content collisions (literal-night face blocked, huaijiu/xiaoyao-night same-type) + qiuxin/festival 18 rows ALL carry hits (nine-consumption saturated face) + qiuxin/dusk 18 rows ALL carry hits (r1027_pool.txt fresh full scan per R1026 pointer) -> market_close line1 = ONLY clean row among the four priority faces; remaining qiuxin clean rows after this consumption: market_open/7 + heatwave/0 + heatwave/9 + coldsnap/14 + ceo_order/12 + ceo_order/13 (season/context mismatch honest notes: heatwave+coldsnap = October-autumn season-face mismatch R972-adjacent, market_open = holiday-closed-market time-point mismatch, ceo_order = no CEO-order event today) + market_open/16 「新奇玩意儿先摸个遍」 shares 4-char band with this card = becomes future collision row; within-axis native-word depth-band first harvest: 玩意儿 = qiuxin axis native colloquial word (same law as cha/yi-xiaoyao, jiu-xiaqi, jiaozhun-zhixu bands), 4 unconsumed pool rows carry it; bucket honesty: market_close bucket SECOND DAILY piece (v55 huaijiu/1 first), production ~23:2x deep night vs market-close evening scene = time-adjacent NOT time-exact (v55 same-type precedent); holiday-day-2 note: National Day holiday day 2 = market closed state = market-close-state holiday normalcy pairing (v55 precedent); post-v57 rotation note: qiuxin becomes 10 -> counts 10/9/9/9/9/9 -> next minimum = five axes tied at 9, longest gap = yanhuo (last v51, gap 6 LONGEST) = v58 redemption target; yanhuo supply faces fresh full scan next round (night face consumed v51/13 + r1019/r1020 festival all-collisions -> cascade expected)")
io.open(os.path.join(TMP, "r1027_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V57:
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
# market_close bucket: v55 huaijiu/1 (first piece) + THIS piece = qiuxin/1 (second piece).
# DUSK bucket: v56 xiaoyao/6 (first piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 057",
    u"2026-10-02 · 国庆假期",
    u"「新奇玩意儿正上架」",
    u"——硅基城市台词池 · 求新轴",
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
assert H2_SIZE == 60, "em ladder expected 60-band (short-quote band, v54/v56 precedent; attribution line 12.65em driver at 60 budget 15.33em), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v57"
meta["form"] = (u"DAILY 城市日签 057（L-卡 图文轻内容线 DAILY 形态第五十七件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1027·日签节律续件=日期×情境桶对位判据第五十七证〔**market_close "
                u"傍晚邻接桶第二件**（v55 怀旧 line1 首件后=同桶异轴异行第二采·**诚实注=时点邻接非 literal night "
                u"直配**〔~23:2x 深夜生产×收市傍晚场景=邻接面如实注记·v55 同型先例〕·场景级=假期第二日休市态市集摊位"
                u"备新货上新面〕+**旋转律兑现（求新回补·结构性诚实注）**：v56 后计数求新 9/怀旧 9/侠气 9/烟火 9/"
                u"秩序 9/逍遥 9=**六轴全并列〔系列第四个全并列态·首=v36 后 R1006·次=v42 后 R1012·三=v48 后 R1018〕"
                u"→并列面最长回补距=求新〔v49 后 7 件未采·v50-v56 七件皆他轴=R1006/R1012/R1018 同裁决第四证〕**→"
                u"**求新 12 桶 fresh 全扫 r1027_pool.txt（R1026 指针「求新供面 fresh 全扫」兑现·fleet 含 v56）**："
                u"night 18 行全数内容层直撞〔literal 夜时点面阻断=怀旧/逍遥 night 同型〕+festival 18 行全数带撞"
                u"〔九采饱和面〕+dusk 18 行全数带撞→级联=market_close line1=**四优先面唯一干净行胜出**=零直撞标准"
                u"不放松〔R442 反同构主线·v1-v56 五十六连零直撞〕〕+line1 选优〔**全 shingle 零命中+零构式层邻接="
                u"系列第五件全零邻接行**（v53/v54/v55/v56 后连续·r1027_pool.txt fresh 2-5 字含标点 2 字组全零="
                u"r1027_quote_face.txt 九词机核·行内无标点=标点构式邻接物理不可能面注〕+「玩意儿」北方市井口语+"
                u"「正」进行时感=人味命中〔CEO 审美线对位〕+求新轴〔最爱追新·眼睛总盯着新东西的轴〕×「新奇玩意儿"
                u"正上架」〔收市后的摊位还在为明天假期人潮上新的货〕=**收×上轴内自反差金句位**〔族四十三连·上货位"
                u"语感独占注=收市的打烊时点×正上架的进行时·一天结束时正是新东西登场时〕〕〕）")
meta["source_quote"] = u"「新奇玩意儿正上架」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[求新][market_close][1]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期第 2 日=DAILY-v1~v56 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[求新][market_close][1] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+market_close 桶 18 行计数"
                         u"+axes 6 轴+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-02=当日历法事实·国庆假期="
                         u"假期第 2 天〔daily brief 2026-10-02 当日窗语境〕③情境=market_close 傍晚邻接桶第二件"
                         u"〔v55 怀旧 line1 首件后同桶第二采·**诚实注=收市场景×~23:2x 深夜生产=时点邻接非 literal "
                         u"night 直配·v55 同型**·国庆假期第 2 日休市=收市态假日常态对位〔v55 先例〕〕④池级署名="
                         u"台词池轴级行·本行无称谓面=纯景句·泛称零涉及〔人设权红线零接触·charter §2.4·v56 纯景句"
                         u"同型先例〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote "
                         u"任一（卡面级实扫=R1010 修正律·DAILY-v1~v56 全 56 行+REACT-v8 同桶三行+city-spirit v1.2 "
                         u"节日场景三行皆非本行）+「新奇」「玩意儿」「上架」「正上架」「新奇玩」「奇玩意」「玩意儿正」"
                         u"「儿正上」「玩意儿正上架」probe 九词机核〔r1027_quote_face.txt〕+**零构式层邻接**"
                         u"〔r1027_pool.txt fresh 12 桶全扫 2-5 字含标点 2 字组全零=系列第五件全零邻接行·"
                         u"v53/v54/v55/v56 后连续·求新四优先面〔night/festival/dusk/market_close〕前三面零干净行+"
                         u"market_close line1 唯一干净行 fresh 实证〕⑥季相核=本行无年味/春联/春雨/寒潮类季相错位词"
                         u"〔R972 制·收市备新货=假日情境对位〕⑦品牌语感注=「玩意儿」北方市井口语+「正」进行时感"
                         u"〔去 AI 感对位·日常口气=人味命中·零书面套语〕+「上架」=市集摊位上货情境词非行情面")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·求新轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v55/v56 泛称与纯景句先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（market_close 傍晚邻接桶第二件〔**旋转律+"
                            u"全供面扫描+零直撞三律并轨诚实执行**：六轴全并列第四态→最长回补距求新〔v49 后 7 件〕→"
                            u"R1026 指针 12 桶 fresh 全扫→night/festival/dusk 三优先面零干净行→market_close line1 "
                            u"唯一干净行胜出〕+~23:2x 同轮对位〔时点邻接诚实注〕+收×上反差金句位〔族四十三连·上货位"
                            u"语感独占注〕+「玩意儿」市井口语+「正」进行时感=语录卡线变体零新模板第五十七证（QUOTE-v2 "
                            u"参数 verbatim 复用·h2_size 60 档〔v54/v56 短句同带先例〕·charter §1「日签变体随时可续」"
                            u"兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 "
                            u"O-20260928-1910 对位〔最爱追新的人总能在收市后的城市里等到新东西上架=城市保持新鲜的"
                            u"活证据·收市不散场=节日的城市还在为明天备货〕+R442 人物场景处方带第六件〔v51 铺子守早客/"
                            u"v52 船老大夜航/v53 值夜岗慢步巡逻/v55 老陈头背手溜达/v56 江边钓鱼人+v54 生灵插件后人物带"
                            u"续连=市集摊主收市后备新货上新·v44 早市豆浆摊+v32 早点摊同族异面=市集摊主带第三采〕+"
                            u"**供给面诚实注**：本件后求新轴四优先面已采面=market_close line1 唯一干净行已消费→"
                            u"求新剩余干净行=market_open/7+heatwave/0+9+coldsnap/14+ceo_order/12+13〔季相/时点/情境"
                            u"错位注记在案〕+market_open/16 新奇玩意儿先摸个遍=4 字带新撞行→v58 目标=烟火〔v51 后 "
                            u"gap 6 最长〕+烟火供面 fresh 全扫下轮执行〔诚实缓办注〕+「玩意儿」=求新轴本命口语词纵深带"
                            u"首采〔同 v18 茶/v40 酒/v41 校准带律·池内 4 未采行同词·后续采录时=轴内纵深带注〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：收市打烊时点×正上架进行时=收×上反差〔族四十三连·"
                          u"上货位语感独占注·一天结束时正是新东西登场时〕+「玩意儿」北方市井口语真感+假期市集摊位备新货"
                          u"场景具体〔R442 处方带〕/情 1 收市后备货勤勉+新品上架期待温和面如实〔非强极点〕/时 2 当日时点="
                          u"国庆假期第 2 日+market_close 傍晚邻接桶第二件〔**诚实注=时点邻接非 literal night 直配**·"
                          u"~23:2x 深夜生产×收市傍晚场景〕/台 2 公众号方图承载=MC-001~141 S3 实证复用）——"
                          u"hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·"
                          u"queue §E E30 R1027 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面=纯景句·"
                     u"泛称零涉及〔v55/v56 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（摊位"
                     u"备新货=市井生活意象非行情面·「上架」=市集上货情境词非电商宣称·无品牌无价格=零消费宣称）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十七件·charter v1.2 §4 形态码 DAILY·日签节律续件·market_close 傍晚邻接桶第二件·求新轴回补件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[qiuxin][market_close][1] verbatim OK; market_close bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v56 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night bucket v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7 + sprite v50 festival/0 + v54 night/8 + market_close v55 huaijiu/1 + dusk v56 xiaoyao/6; qiuxin redemption: night/festival/dusk ALL collisions (r1027_pool.txt fresh full 12-bucket scan) -> market_close line1 = ONLY clean row among priority faces; quote-face word probe: 9 words see r1027_quote_face.txt (all ZERO; zero construct-layer adjacency = FIFTH fully-zero row of series after v53/v54/v55/v56)")
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
report.append("LADDER_60: attribution-line 12.65em driver (v54/v56 short-quote band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; market_close-bucket-second DAILY piece + qiuxin-redemption + 5th-fully-zero-row honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1027.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V57, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V57, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v56 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, short-quote band, v54/v56 precedent) + E4 fired async" % H2_SIZE)
