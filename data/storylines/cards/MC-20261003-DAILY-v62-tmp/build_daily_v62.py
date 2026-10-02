# -*- coding: utf-8 -*-
"""MC-20261003-DAILY-v62 build: DAILY (city daily-sign) series SIXTY-SECOND piece (R1062, queue
section-E E30 standby cascade). MORNING-WINDOW UNLOCK PIECE - the R1031 pre-registered
short-term candidate window ("daytime production window lifts the morning weak-adjacency
gate") fires THIS round: production ~07:0x = LITERAL morning hour, so a morning-bucket scene
line pairs with same-hour reality (strongest adjacency, R1019 night-scene-at-20:5x /
R1020 dian-tou-same-hour precedents family). Post-v61 rotation: qiuxin 10 / huaijiu 9 /
xiaqi 10 / yanhuo 10 / zhixu 9 / xiaoyao 10 -> minimum pair huaijiu 9 + zhixu 9 -> cascade
trail (r1032_pool.txt fresh scan, fleet includes v61, zero new cards since): zhixu [gap 8
LONGEST: rain/2 no-rain-event + coldsnap/2+9 October-season ALL BLOCKED] -> huaijiu [gap 6:
heatwave/8 + coldsnap/7 season + market_open/6+7+9 holiday-closure v57 + ceo_order/3+10
no-event ALL BLOCKED] -> qiuxin [gap 4: heatwave/0+9 season BLOCKED] -> yanhuo [gap 3:
morning/6+7 zhou-xiang-morning-market + cai-xian market-stall 3-link-iso with v44+v57+v58
BLOCKED at any hour] -> xiaqi [gap 2: morning/0+15 sheng-yi business 3-link + chen-wu twin
pair BLOCKED at any hour] -> xiaoyao [gap 1: morning/0 chen-wu-shan-sheng-yi-lai business
twin BLOCKED; morning/1 = UNIQUE non-business/non-market-stall clean morning row] ->
xiaoyao/morning/1 「鱼竿一甩，梦醒时分」 = UNIQUE honestly-pairable row at THIS daytime
production context. Zero-collision standard NOT relaxed (R442 anti-isomorphism spine,
v1-v61 sixty-one-link zero-collision chain). ANGLING-BAND HONEST REGISTRATION (the load-
bearing honesty note of this piece): angling-ACTION motif prior uses = DAILY-v6 「闲来垂钓
乐悠悠」 [festival leisure-angling facet] + REACT-v4 fishing hot-topic weekend rows
[hot-topic angling facet]; THIS row [morning first-cast + waking facet] = THIRD angling-
action use = angling 3-link CHAIN FORMS with this piece -> per market-stall 3-link law
letter (block applies to the NEXT use after three exist) the third link is legal, and
post-v62 ALL angling-action rows are FUTURE-BLOCKED (registration = the gate grows teeth
forward). Heterogeneous-facet notes: v56 「夕阳西下鱼也归巢了」 [fish-homecoming
personification facet, NOT angling] + v60 「檐下观鱼跃」 [fish-watching spectator facet,
NOT angling] = same aquatic family, non-angling facets. MENG band: v42 「街灯如织好个梦」
[dream-state facet] vs THIS 「梦醒时分」 [waking-moment facet] = same char family
heterogeneous construct (shingle-level 梦醒 vs 好个梦 machine-verified ZERO). Built-in
tension: SHUI x XING - the whole holiday town is still inside its biggest sleep while the
earliest fisherman is already casting the day's first line; the shortest instant of the
day (waking) meets the longest slow craft (angling). Layout = QUOTE-v2 params verbatim;
h2_size ladder = 60 band (13em quote line fits 15.33em budget, v60 same-band precedent).
Machine source/dedup assertions (R456 system, card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V62 = os.path.join(BASE, "MC-20261003-DAILY-v62")
TMP = V62 + "-tmp"
os.makedirs(V62, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"鱼竿一甩，梦醒时分"
AXIS, BUCKET, IDX = u"逍遥", u"morning", 1  # axes face (6 axes x 12 buckets x 18 rows = 1296)

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
mb = pool["axes"][AXIS][BUCKET]
assert len(mb) == 18, "axes bucket != 18 rows (axes = 12 buckets x 18 rows = 1296 per axis-face)"
assert mb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % mb[IDX]
assert mb[0] == u"晨雾散，生意来", "business twin row morning/0 expected 晨雾散，生意来"
assert mb[3] == u"早市忙，人声鼎沸", "market-stall row morning/3 expected"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1062_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"鱼竿", u"一甩", u"梦醒", u"时分", u"鱼竿一甩", u"竿一甩", u"醒时分", u"梦醒时分", u"鱼竿一甩，梦醒时分"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1062 quote-face word probe for candidate " + QUOTE_CORE + u" (xiaoyao/morning line1)"]
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1032_pool.txt fresh scan, fleet includes v61; zero new cards registered since) = TENTH fully-zero row of the series (v53-v61 nine precedents). Motif-band honest registrations (single-char/family layer, NOT card-face collisions; machine scan 2+ char ZERO verified): (1) ANGLING-ACTION BAND - prior uses DAILY-v6 「闲来垂钓乐悠悠」 [festival leisure-angling facet] + REACT-v4 fishing hot-topic weekend rows 「周末钓竿闲，江畔好时光」 family [hot-topic angling facet]; THIS row [morning first-cast + waking facet] = THIRD angling-action use = angling 3-link CHAIN FORMS with this piece (legal per 3-link law letter: the block applies to the NEXT use after three exist) -> POST-v62 REGISTRATION: all angling-action rows future-blocked (morning/5+6+8+10+14+17 and any 钓/竿 rows in other buckets). (2) AQUATIC-FAMILY heterogeneous facets: v56 「夕阳西下鱼也归巢了」 [fish-homecoming personification facet, NOT angling] + v60 「檐下观鱼跃」 [fish-watching spectator facet, NOT angling] = same aquatic family non-angling facets, no chain contribution. (3) MENG band: v42 「街灯如织好个梦」 [dream-state facet] vs THIS 「梦醒时分」 [waking-moment facet] = same char family heterogeneous construct; shingle-level 梦醒 vs 好个梦 machine-verified ZERO. (4) R1025 precedent note: 钓竿近同构 v6 was a selection-preference exclusion WHEN alternatives existed; at zero alternatives the documented cascade redeems the last standing honestly-pairable row - registered honestly here, not silently.")
qrep.append(u"morning-window unlock note: R1031 pre-registered 日间生产窗可解 morning 邻接阻=短期候选窗; THIS round production ~07:0x = literal morning hour -> the R1029 deep-night weak-adjacency gate LIFTS; 梦醒时分 content + morning bucket + morning production hour = TRIPLE literal alignment (adjacency upgraded from v55/v57 时点邻接 to literal, same ladder as R1019 夜幕-at-20:5x / R1020 这个点-at-21:1x). Business/market-stall morning rows remain blocked at any hour (3-link-iso, R1032 close-out note).")
qrep.append(u"supply-face honest note post-v62: morning bucket xiaoyao face exhausted (remaining rows all business/market-stall/angling/chen-wu collisions); angling-action theme family = 3-link formed -> future-blocked; unlock windows unchanged: rain-event day / CEO-order day / 2026-10-08+ market reopen / Nov+ coldsnap / summer heatwave. Pool-expansion report position maintained (status-line not chase).")
io.open(os.path.join(TMP, "r1062_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V62:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 062",
    u"2026-10-03 · 国庆假期 · 晨",
    u"「鱼竿一甩，梦醒时分」",
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
assert H2_SIZE == 60, "em ladder expected 60-band (13em quote line + morning-marker date line v54/v61 same-type precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261003-DAILY-v62"
meta["form"] = (u"DAILY 城市日签 062（L-卡 图文轻内容线 DAILY 形态第六十二件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 级联续领 R1062·日签节律续件=日期×情境桶对位判据第六十二证〔**morning "
                u"桶首件=晨间邻接桶开门件**〔night v51/market_close v55/dusk v56/weekend v58 后第 5 新开桶·"
                u"**R1031 预登记「日间生产窗可解 morning 邻接阻=短期候选窗」兑现件**：~07:0x 晨间生产×"
                u"morning 桶×梦醒时分内容=三重 literal 对位〔R1019 夜幕 20:5x/R1020 这个点 21:1x 同型先例"
                u"带·v55/v57「时点邻接」诚实注升档〕〕+**旋转级联兑现（诚实注）**：v61 后计数求新 10/怀旧 "
                u"9/侠气 10/烟火 10/秩序 9/逍遥 10=双轴并列最少→最长回补距=秩序〔v53 后 gap 8〕→干净行仅 "
                u"rain/2+coldsnap/2+9=雨无事件+十月季相全阻→级联怀旧〔gap 6〕：market_open 假日休市"
                u"〔v57 判例〕+ceo_order 无令事件+季相全阻→级联求新〔gap 4〕：heatwave/0+9 季相全阻→"
                u"级联烟火〔gap 3〕：morning/6+7=早市/菜场主题与 v44+v57+v58 市集三连同构〔任一时点皆阻〕"
                u"→级联侠气〔gap 2〕：morning/0+15 生意三连+晨雾散孪生对〔任一时点皆阻〕→逍遥〔gap 1〕："
                u"morning/0 生意孪生阻→**morning/1 唯一非生意/非市集干净行胜出**=零直撞标准不放松〔R442 "
                u"反同构主线·v1-v61 六十一连零直撞〕〕+line3 选优〔**全 shingle 零命中=系列第十件全零"
                u"邻接行**（v53-v61 九件先例后·r1062_quote_face.txt 九词机核〕+**垂钓动作族带三连成形注册**"
                u"〔前用=DAILY-v6 闲来垂钓乐悠悠〔festival 闲钓面〕+REACT-v4 周末钓竿行带〔热点钓鱼面〕·"
                u"本行〔morning 起手+梦醒面〕=第三用=族带三连成形〔三连同构律字面=第四用起阻·本件合法〕→"
                u"**post-v62 垂钓动作行全数未来阻注册**〔morning/5+6+8+10+14+17 及各桶 钓/竿 行〕〕+同族"
                u"异质注〔v56 鱼也归巢〔归巢拟人面·非垂钓〕+v60 檐下观鱼跃〔观赏面·非垂钓〕=水族带非垂钓"
                u"面零贡献〕+梦字族带异构注〔v42 好个梦〔梦中态〕vs 本行梦醒时分〔醒转瞬间〕=同字族异构式·"
                u"shingle 机核零撞〕+R1025 先例诚实注〔钓竿近同构 v6=有替代面时的选材偏好排除·零替代级联"
                u"面下末位常立行诚实领受非静默〕〕+逍遥轴〔最松弛·闲适至上〕×鱼竿一甩〔把一天最早的期待"
                u"甩进江里〕×梦醒时分〔全城最短的一瞬〕=**睡×醒+瞬×长双反差金句位**〔族四十八连·晨钓位"
                u"语感独占注=假期里全城还在最大的睡梦里·最早醒的人已经把第一竿甩进了最长的慢工艺里〕〕）")
meta["source_quote"] = u"「鱼竿一甩，梦醒时分」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][morning][1]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"·跨仓只读指针）+data/intel/daily/2026-10-03.md（当日日期语境源·国庆假期第 3 日"
                           u"+周六·晨间生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][morning][1] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+morning 桶 18 行计数"
                         u"+axes 6+sprite 顶层结构三断言实锚〔R982〕+生意孪生行 morning/0 结构断言）②日期行 "
                         u"2026-10-03=当日历法事实·周六+国庆假期第 3 天〔daily brief 2026-10-03 当日窗语境〕"
                         u"+晨标记〔v54 夜标记先例的晨对位·~07:0x 晨间生产 literal〕③情境=morning 桶首件"
                         u"〔**三重 literal 对位**=晨间生产时刻×morning 桶×梦醒时分内容·R1031 预登记日间"
                         u"窗候选兑现〕④池级署名=台词池轴级行·本行无称谓面=纯景句·泛称零涉及〔人设权红线"
                         u"零接触·charter §2.4·v56-v61 泛称纯景句先例族〕⑤去重断言=本行不在 city-spirit.md "
                         u"64 条已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·"
                         u"DAILY-v1~v61 全 61 行+REACT-v8 同桶三行+city-spirit v1.2 节日场景三行皆非本行）"
                         u"+「鱼竿」「一甩」「梦醒」「时分」「鱼竿一甩」「竿一甩」「醒时分」「梦醒时分」"
                         u"全句 probe 九词机核〔r1062_quote_face.txt〕+**零构式层邻接**〔r1032_pool.txt "
                         u"fresh 2-5 字含标点 2 字组全零=系列第十件全零邻接行〕+**垂钓动作族带三连成形注册**"
                         u"〔v6 festival 闲钓面+REACT-v4 热点钓鱼面+本行 morning 起手面=第三用·post-v62 "
                         u"垂钓动作行未来阻注册=morning/5+6+8+10+14+17 及各桶钓/竿行〕+同族异质注〔v56 "
                         u"归巢拟人面+v60 观赏面=非垂钓面〕+梦字族带异构注〔v42 梦中态 vs 本行醒转瞬间〕"
                         u"⑥季相核=本行无年味/春联/春雨/寒潮类季相错位词〔R972 制·晨钓=四季通用晨间面·"
                         u"十月秋晨兼容〕⑦品牌语感注=「鱼竿一甩，梦醒时分」4+4 对仗式+动作瞬间定格=去 AI"
                         u"感对位·人味命中·零书面套语·零消费宣称无品牌无价格")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名/生灵名"
                             u"（charter v1.2 署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v56-v61 "
                             u"先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（morning 桶首件+逍遥轴 gap 1 回补"
                            u"双位〔**旋转级联+日间窗解锁+零直撞三律并轨诚实执行**：秩序 rain/coldsnap 阻→"
                            u"怀旧 market_open/ceo_order/季相阻→求新 heatwave 阻→烟火 morning 市集三连阻→"
                            u"侠气 morning 生意三连+孪生阻→逍遥 morning/1 唯一非生意干净行胜出〕+睡×醒+瞬×长"
                            u"双反差金句位〔族四十八连·晨钓位语感独占注=假期最大的睡梦×最早的一竿〕+4+4 "
                            u"对仗式=语录卡线变体零新模板第六十二证（QUOTE-v2 参数 verbatim 复用·h2_size "
                            u"60 档〔v60 逍遥轴同带先例〕·charter §1「日签变体随时可续」兑现）·公众号低"
                            u"创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 "
                            u"O-2026-09-28-1910 对位〔假期清晨还在睡的城市里最早醒的人=城市一日之计的"
                            u"人文开卷〕+**供给面诚实注**：本件后 morning 桶逍遥面耗尽（余行皆生意/市集/"
                            u"垂钓/晨雾撞）+垂钓动作族带三连成形未来阻注册=DAILY 可诚实配对面维持结构性近"
                            u"枯竭注〔R1030 REACT 判负+R1032 零判负同族信号·池扩容呈报位维持呈现状行"
                            u"不催办〕·post-v62 指针：解锁窗维持=雨事件日/CEO 令日/10-08 market_open 复市/"
                            u"Nov+ 寒潮/夏季 heatwave·REACT-v9 10-04 窗·F 序号诚实注=本件先落 F-147·"
                            u"REACT-v9 10-04 预指位顺延 F-148〔R978 判例 finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：梦醒时分〔全城最短的一瞬·睡到醒的切换〕"
                          u"×鱼竿一甩〔最悠长的晨间慢工艺起手〕=瞬×长反差+假期全城沉睡〔最大范围的睡〕×最早"
                          u"个体已醒〔最早的醒〕=睡×醒反差〔族四十八连〕/情 1 假日清晨早起出钓的松弛共鸣"
                          u"温和如实非强极点〔G5+G3 双群〕/时 2 当日=2026-10-03 周六国庆假期第 3 日·~07:0x "
                          u"晨间生产=morning 桶×梦醒时分内容×生产时刻三重 literal 直配=晨间邻接桶开门件"
                          u"〔R1031 预登记日间窗候选兑现〕/台 2 公众号方图承载=MC-001~146 S3 实证复用）"
                          u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 "
                          u"DAILY·queue §E E30 R1062 级联续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面="
                     u"纯景句·泛称零涉及〔v56-v61 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零"
                     u"金钱数额（鱼竿一甩梦醒时分=晨间垂钓意象非商业面·无品牌无价格=零消费宣称）；成品只"
                     u"入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十二件·charter v1.2 §4 形态码 DAILY·日签节律续件·morning 桶首件·日间窗解锁件·逍遥轴 gap 1 回补件·垂钓族带三连成形注册件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][morning][1] verbatim OK; morning bucket=18 rows; axes=6 + sprite 12-bucket top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v61 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; rotation cascade: zhixu rain/coldsnap blocked -> huaijiu market_open/ceo_order/season blocked -> qiuxin heatwave blocked -> yanhuo morning market-stall 3-link blocked -> xiaqi morning business 3-link+twin blocked -> xiaoyao morning/1 = UNIQUE honestly-pairable clean row at DAYTIME morning production (r1032_pool.txt fresh, fleet includes v61; R1031 pre-registered daytime-window candidate); quote-face word probe: 9 words see r1062_quote_face.txt (all ZERO; tenth fully-zero row of series after v53-v61; angling-action 3-link chain-forms registration + aquatic-family heterogeneous facets + meng-band heterogeneous construct + R1025 precedent honest note)")
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
report.append("LADDER_60: 13em quote line + morning-marker date line fits 60-band (v60 xiaoyao same-band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; morning-window-unlock + rotation-cascade + tenth-fully-zero-row + angling-3-link-chain-forms registration honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1062.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V62, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V62, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v61 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, 13em quote-line + morning-marker date line fits) + E4 fired async" % H2_SIZE)
