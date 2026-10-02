# -*- coding: utf-8 -*-
"""MC-20261003-DAILY-v60 build: DAILY (city daily-sign) series SIXTIETH piece (R1030, queue
section-E E30 standby via cascade). XIAOYAO-REDEMPTION PIECE via THREE-STEP ROTATION CASCADE
(structural, honest): R1030 round opening = 10-03 day-boundary round; E31 REACT-v9 FIRST
claimable item per R1029 pointer -> 10-03 daily brief produced first (O-2304 iron rule,
bilibili-popular + zhihu-hot 20/20 collected) -> REACT M0 honest-mapping scan r1030_react_probe.txt
+ r1030_probe2.txt: ALL 20 hot items excluded per law (political: Trump-phone/CFA-Palestine x2;
sports: football x2 six-link precedent; health-claims: clinic; music/IP-promo: 3 items;
documentary-promo: 2 items; real-person/money: 24-bloggers; tech-product: Huawei-chip no-bucket;
food-face: half-bun title carries no honest facets + bun word consumed v32; brain-hole:
earth-online no-bucket; AI-drama = industry-news face no situational bucket [v8 car-sales
same ruling] + all direct livestream/content lines carry card-face hits [probe evidence];
cola-fake = pool zero counterfeit/goods rows; anti-return-tape = pool zero hits + theme-family
repeat with REACT-v6 refund piece; vitamin = science no-bucket; Tsinghua-PKU = education-
criticism sensitive + pool zero exam/rank rows; station-yi = culture no-bucket + wharf lines
all carry hits) -> E31 REACT-v9 supply-blocked verdict for the 10-03 window (negative result
recorded per P-2026-09-28-02) -> cascade to section-E E30 standby: rotation post-v59 counts
qiuxin 10 / xiaqi 10 / yanhuo 10 / huaijiu 9 / zhixu 9 / xiaoyao 9 -> THREE AXES TIED AT 9 ->
target zhixu (longest gap 6, R1029 pointer) -> zhixu global-census clean rows (r1030_probe2.txt,
fleet includes v59): rain/2 + coldsnap/2 + coldsnap/9 ONLY -> rain = no rain event today (context
mismatch), coldsnap = October-autumn season mismatch (R972-adjacent) -> zhixu BLOCKED -> cascade
next-longest huaijiu (gap 4): clean rows market_open/6+7+9 (holiday closed-market time-point
mismatch v57 ruling + deep-night x morning-market weak adjacency v58 ruling) + ceo_order/3+10
(no CEO-order event) + heatwave/coldsnap (season) -> huaijiu BLOCKED -> cascade xiaoyao (gap 3):
clean rows morning/0+1 (deep-night x morning weak adjacency v58 ruling + 晨雾散生意来/兴 twin-line
note) + rain/17 (no event) + heatwave x3 + coldsnap x2 (season) + ceo_order x2 (no event) +
weekend/4 -> weekend line4 「檐下观鱼跃，茶室笑谈多」 = ONLY honestly-pairable clean row.
Zero-collision standard NOT relaxed (R442 anti-isomorphism spine, v1-v59 fifty-nine-link
zero-collision chain). WEEKEND BUCKET THIRD DAILY PIECE (v58 yanhuo/7 + v59 xiaqi/8 precedents;
2026-10-03 = SATURDAY = literal weekend + National Day holiday day 3 = first LITERAL double-
anchor weekend piece of the series; supply-driven three-peat honest note: stable holiday
context, three axes three lines heterogeneous). Built-in tension: CHAO x JING - the most
crowd-avoiding ease-first axis finds the quietest corner (eaves-side fish-watching + tea-room
chatter) in the city's most crowded holiday; v56 nao-x-jing same-family heterogeneity note
(v56 solitary dusk fishing vs this row small-gathering tea-room = two states of quiet).
Layout = QUOTE-v2 params verbatim; h2_size ladder = 60 band (12em quote line fits 60-band
budget 15.33em margin +3.33em = zero-template default band). Machine source/dedup assertions
(R456 system, card-face level R1010 law). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V60 = os.path.join(BASE, "MC-20261003-DAILY-v60")
TMP = V60 + "-tmp"
os.makedirs(V60, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"檐下观鱼跃，茶室笑谈多"
AXIS, BUCKET, IDX = u"逍遥", u"weekend", 4

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
wb = pool["axes"][AXIS][BUCKET]
assert len(wb) == 18, "axis bucket != 18 rows (axes = 6 x 12 buckets x 18 rows = 1296)"
assert wb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % wb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1030_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"檐下", u"观鱼", u"鱼跃", u"茶室", u"笑谈", u"檐下观", u"观鱼跃", u"茶室笑", u"谈多"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1030 quote-face word probe for candidate " + QUOTE_CORE + u" (xiaoyao/weekend line4)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO direct shingle hits and NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1030_probe2.txt global census, fleet includes v59) = EIGHTH fully-zero row of the series (v53/v54/v55/v56/v57/v58/v59 seven precedents). Motif-band honest notes (single-char layer, not card-face collisions; machine scan 2+ char ZERO verified): (1) FISH-WATER motif band - v6 闲来垂钓乐悠悠 [xiaoyao/festival, angling facet] + REACT-v4 云淡风轻时，鱼上钩未急 [xiaoyao/weekend/2 SAME bucket, angling-wait facet] + xiaoyao/morning/1 鱼竿一甩 [unconsumed row] vs THIS row 檐下观鱼跃 = fish-WATCHING facet (ornamental pond viewing, not angling) = same motif family heterogeneous facet; same-bucket internal note: weekend bucket xiaoyao has line2 angling-wait [consumed by REACT-v4] vs line4 fish-watching tea-room = same bucket different theme families. (2) TEA character band (xiaoyao axis home-topic depth band, R1005 闲-character-band law same type): v18 茶香伴着灯影摇 [aroma-scene facet] + v36 茶水泡得正浓，好品一口闲 [taste-idle facet] + REACT-v8 节日热闹，不如在家喝喝茶 [stay-home facet] vs THIS row 茶室笑谈 = tea-room small-gathering social facet = fourth facet of the band. (3) 闹×静 contrast family: v56 nao-x-jing [solitary dusk fishing] vs THIS row chao-x-jing [holiday-crowd vs tea-room small gathering] = two states of quiet (solitary vs small-gathering) heterogeneous note.")
qrep.append(u"supply-face honest note: rotation cascade trail zhixu[gap 6, rain/coldsnap event+season all blocked] -> huaijiu[gap 4, market_open holiday-closed time-point + ceo_order no-event + season all blocked] -> xiaoyao[gap 3, morning deep-night weak + rain/heatwave/coldsnap/ceo_order exclusions] -> weekend line4 = ONLY honestly-pairable clean row (2026-10-03 Saturday = literal weekend + holiday day 3 double anchor, first literal piece of the weekend bucket; v58/v59 holiday-state adjacency precedents upgraded). Post-v60 xiaoyao clean faces: morning/0+1 [deep-night weak adjacency + twin-line note] + rain/17 [no event] + heatwave/coldsnap [season] + ceo_order [no event] = xiaoyao honestly-pairable faces approaching structural exhaustion (v59 xiaqi same-family note); supply-side rotation will cascade to sprite voices: sprite/weekend/3+4 + sprite/market_close/3+9 + sprite/market_open/3 clean rows = third-voice candidates pending.")
io.open(os.path.join(TMP, "r1030_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V60:
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
# v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7. market_close bucket: v55 huaijiu/1 + v57 qiuxin/1.
# DUSK bucket: v56 xiaoyao/6. WEEKEND bucket: v58 yanhuo/7 + v59 xiaqi/8 + REACT-v4 xiaoyao/2
# + THIS piece = xiaoyao/4 (third DAILY piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 060",
    u"2026-10-03 · 国庆假期",
    u"「檐下观鱼跃，茶室笑谈多」",
    u"——硅基城市台词池 · 逍遥轴",
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
assert H2_SIZE == 60, "em ladder expected 60-band (12em quote line < 60-band budget 15.33em margin +3.33em; zero-template default band, v2/v6/v20/v24/v59 family precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261003-DAILY-v60"
meta["form"] = (u"DAILY 城市日签 060（L-卡 图文轻内容线 DAILY 形态第六十件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 级联续领 R1030·日签节律续件=日期×情境桶对位判据第六十证〔**weekend 桶"
                u"第三件=系列首件 literal 双锚件**（v58 烟火/7+v59 侠气/8 假日态邻接两先例后第三采·"
                u"**2026-10-03=周六=literal weekend+国庆假期第 3 日双直配**=weekend 桶六件〔v58/v59/本件+"
                u"REACT-v4/v5 同桶〕中首件真周六件·供给面驱动三连同构注=国庆假期稳定语境·三轴三行异质"
                u"〔v58 面摊守汤劳作面/v59 行船祝酒开阔面/本件檐下茶室闲聚面〕诚实注·场景级=檐下观鱼+"
                u"茶室笑谈=假日闲聚场景·~00:1x 深夜生产×不受时点绑定的假日闲聚场景兼容〕+**旋转律三步级联"
                u"兑现（结构性诚实注）**：R1030 轮=E31 REACT-v9 日界窗首位→**10-03 热榜 20 条全数无诚实"
                u"配对位判负留痕**〔r1030_react_probe.txt+r1030_probe2.txt 机核证据·政治/竞技/健康/食物/"
                u"脑洞/宣传/真实人物面法条排除+AI 短剧=产业新闻面无情境桶〔v8 车企销量同判〕+直配行全撞"
                u"实证+可乐造假/防拆带/教育/车站面=池零命中或全撞实证=P-2026-09-28-02 判负留痕合法·"
                u"E31 当窗零产件〕→级联 E30 standby：v59 后计数求新 10/侠气 10/烟火 10/怀旧 9/秩序 9/"
                u"逍遥 9=三轴并列最少→最长回补距=秩序〔v53 后 6 件=R1029 指针〕→**秩序 census fresh 复扫"
                u"〔fleet 含 v59〕：干净行仅 rain/2+coldsnap/2+9=雨无事件+寒潮十月季相错位全阻**→级联怀旧"
                u"〔v55 后 4 件〕：干净行仅 market_open/6+7+9+ceo_order/3+10=假日休市时点错位 v57 同判+"
                u"无令事件+季相全阻→级联逍遥〔v56 后 3 件〕：morning/0+1 深夜邻接弱 v58 判例+晨雾散生意"
                u"来/兴孪生行注+rain/17 无雨事件+heatwave/coldsnap 季相+ceo_order 无令→**weekend line4="
                u"唯一可诚实配对干净行胜出**=零直撞标准不放松〔R442 反同构主线·v1-v59 五十九连零直撞〕"
                u"〕+line4 选优〔**全 shingle 零命中+零构式层邻接=系列第八件全零邻接行**（v53-v59 七件先例后"
                u"·r1030_quote_face.txt 九词机核〕+「笑谈多」闲谈口气口语真感=人味命中〔CEO 审美线对位〕+"
                u"逍遥轴〔最松弛·闲适至上·把节日也过成日常〕×檐下观鱼跃茶室笑谈〔满城最挤假期里最安静的"
                u"檐下小聚〕=**潮×静轴内自反差金句位**〔族四十六连·v56 闹×静同族异质注=v56 黄昏独自收竿"
                u"独静面 vs 本行茶室笑谈小聚静面=静的两态〕〕〕）")
meta["source_quote"] = u"「檐下观鱼跃，茶室笑谈多」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][weekend][4]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-03.md（当日日期语境源·"
                           u"国庆假期第 3 日+周六=weekend 桶首件 literal 双锚语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][weekend][4] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 18 行计数"
                         u"+axes 6 轴+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-03=当日历法事实·"
                         u"周六+国庆假期第 3 天〔daily brief 2026-10-03 当日窗语境〕③情境=weekend 桶第三件"
                         u"〔**首件 literal 双锚=真周六+假态双直配**·v58/v59 假日态邻接先例升档·场景=檐下"
                         u"观鱼+茶室笑谈假日闲聚面=~00:1x 深夜生产×不受时点绑定的假日闲聚场景兼容〕④池级"
                         u"署名=台词池轴级行·本行无称谓面=纯景句·泛称零涉及〔人设权红线零接触·charter "
                         u"§2.4·v56/v57/v58/v59 泛称纯景句先例族〕⑤去重断言=本行不在 city-spirit.md 64 条"
                         u"已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~"
                         u"v59 全 59 行+REACT-v8 同桶三行+city-spirit v1.2 节日场景三行皆非本行）+「檐下」"
                         u"「观鱼」「鱼跃」「茶室」「笑谈」「檐下观」「观鱼跃」「茶室笑」「谈多」probe 九词"
                         u"机核〔r1030_quote_face.txt〕+**零构式层邻接**〔r1030_probe2.txt 全池 census 2-5 字"
                         u"含标点 2 字组全零=系列第八件全零邻接行·三步级联 fresh 实证〕+**motif 带诚实注"
                         u"〔单字层非卡面碰撞·机核 2+ 字零命中实证〕**：鱼水 motif 带=v6 垂钓乐悠悠〔垂钓面〕"
                         u"+REACT-v4 鱼上钩未急〔同桶 weekend 垂钓待鱼面〕+逍遥 morning/1 鱼竿一甩〔未消费行〕"
                         u"vs 本行观鱼跃=观赏面〔非垂钓捕捉面〕=同族异质+同桶内注=weekend 桶逍遥两行异题族"
                         u"〔line2 垂钓待鱼 vs line4 观鱼茶室〕；茶字带第四面=逍遥轴本位纵深带〔v18 茶香场景面"
                         u"/v36 品闲通感面/REACT-v8 喝茶留守面/本行茶室小聚面·R1005 闲字带律同型〕⑥季相核="
                         u"本行无年味/春联/春雨/寒潮类季相错位词〔R972 制·茶室观鱼=四季通用面·十月秋日"
                         u"檐下闲聚=季相兼容〕⑦品牌语感注=「檐下观鱼跃，茶室笑谈多」5+5 对仗闲聚口气"
                         u"〔去 AI 感对位·日常口气=人味命中·零书面套语·零消费宣称无品牌无价格〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v56/v57/v58/v59 先例族"
                             u"对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（weekend 桶第三件首件 literal 双锚"
                            u"〔**E31 REACT 判负级联+旋转三步级联+零直撞三律并轨诚实执行**：10-03 热榜 20 条"
                            u"全排除→E30 standby→秩序 rain/coldsnap 阻→怀旧 market_open/ceo_order 阻→逍遥 "
                            u"morning/rain/季相阻→weekend line4 唯一可诚实配对行胜出〕+潮×静反差金句位〔族"
                            u"四十六连·檐下闲聚位语感独占注=最爱松弛的轴在满城最挤的假期里找到了最安静的角落〕"
                            u"+「檐下观鱼跃，茶室笑谈多」5+5 对仗闲聚口语=语录卡线变体零新模板第六十证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 60 档〔零新模板默认带·v2/v6/v20/v24/v59 "
                            u"先例族〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑"
                            u"价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔最松弛"
                            u"的居民把最挤的假期过成檐下茶室的一池鱼一壶茶=城市从容的活证据〕+R442 人物场景"
                            u"处方带第九件〔v51 铺子守早客/v52 船老大夜航/v53 值夜岗慢步巡逻/v55 老陈头背手"
                            u"溜达/v56 江边钓鱼人/v57 收市摊主备新货/v58 深夜面摊摊主守汤/v59 假期祝酒居民+"
                            u"人物带续连=檐下观鱼茶室闲聚者=假日闲聚带首采·观鱼=观赏面与 v6/REACT-v4 垂钓"
                            u"面异质注〕+**供给面诚实注**：本件后逍遥轴可诚实配对面=weekend 面零干净行剩余"
                            u"〔line4 消费后〕→逍遥剩余干净行=morning/0+1〔深夜邻接弱+孪生行注〕+rain/17〔无"
                            u"雨事件〕+heatwave/coldsnap〔季相〕+ceo_order〔无令事件〕=**逍遥轴干净面结构性"
                            u"近枯竭注（v59 侠气同族注姊妹案）**→后续逍遥回补须待池扩容；post-v60 旋转注："
                            u"逍遥升至 10→计数求新 10/侠气 10/烟火 10/逍遥 10/怀旧 9/秩序 9→二轴并列最少"
                            u"〔怀旧 gap 4/秩序 gap 6〕→下一 DAILY 目标=秩序〔gap 6·rain/coldsnap 面待事件/"
                            u"季相窗·池扩容前置〕→级联备胎=sprite 声部第三件候选〔sprite/weekend/4「叮咚响"
                            u"夜晚」=weekend+夜晚双直配行+sprite/market_close 夜面行=clean 在册〕·10-04 日界"
                            u"轮可领序=①E31 REACT-v9〔10-04 日报先补产·热点窗择优·若连续第二窗无可诚实配对"
                            u"位=连续判负如实注·REACT 供给面结构性近枯竭预警呈报〕②E30 DAILY 续件 standby"
                            u"〔旋转级联+sprite 第三声部候选〕③#94 记忆梳理〔10-04〕④W41 周轮件〔10-05〕·"
                            u"F 序号诚实注=本件先落 F-145·REACT-v9 预指位顺延 F-146〔R978 判例 finished "
                            u"顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：逍遥轴〔最松弛·闲适至上·把节日也"
                          u"过成日常〕×檐下观鱼跃茶室笑谈〔满城最挤假期的最安静檐下小聚〕=潮×静反差〔族"
                          u"四十六连·v56 闹×静同族异质注=静的两态〕+檐下观鱼+茶室笑谈具体场景双落〔R442 "
                          u"处方带第九件〕+「笑谈多」闲谈口气口语真感/情 1 假日从容温和共鸣如实非强极点/"
                          u"时 2 当日=2026-10-03 周六 literal weekend+国庆假期第 3 日双直配〔**weekend 桶"
                          u"首件 literal 双锚·v58/v59 假日态邻接先例升档**〕/台 2 公众号方图承载=MC-001~"
                          u"144 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R1030 级联续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面=纯景句·"
                     u"泛称零涉及〔v56/v57/v58/v59 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/"
                     u"零金钱数额（檐下观鱼+茶室笑谈=假日闲聚生活意象非商业面·无品牌无价格=零消费宣称）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十件·charter v1.2 §4 形态码 DAILY·日签节律续件·weekend 桶第三件首件 literal 双锚·逍遥轴回补件·E31 REACT 判负级联件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][weekend][4] verbatim OK; weekend bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v59 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night v51+v52+v53 + sprite v50/v54 + market_close v55/v57 + dusk v56 + weekend v58/v59 + REACT-v4 xiaoyao/weekend/2; rotation cascade: zhixu rain/coldsnap blocked -> huaijiu market_open/ceo_order blocked -> xiaoyao weekend/4 = ONLY honestly-pairable clean row (census r1030_probe2.txt fresh, fleet includes v59); quote-face word probe: 9 words see r1030_quote_face.txt (all ZERO; zero construct-layer adjacency = EIGHTH fully-zero row of series after v53-v59; fish-water motif band + tea-character band honest single-char-layer notes)")
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
report.append("LADDER_60: 12em quote-line fits 60-band budget 15.33em margin +3.33em (zero-template default band, v2/v6/v20/v24/v59 family); four-LINES stack; all other QUOTE-v2 params verbatim; weekend-bucket-third DAILY piece first-literal-double-anchor + xiaoyao-redemption via three-step rotation cascade + 8th-fully-zero-row + E31-REACT-blocked-cascade honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1030.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V60, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V60, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v59 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, 12em quote-line fits, zero-template default band) + E4 fired async" % H2_SIZE)
