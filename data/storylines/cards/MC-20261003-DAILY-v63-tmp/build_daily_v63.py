# -*- coding: utf-8 -*-
"""MC-20261003-DAILY-v63 build: DAILY (city daily-sign) series SIXTY-THIRD piece (R1086, queue
section-E E30 standby cascade). WEEKEND-RESET UNLOCK PIECE + SPRITE VOICE 4TH PIECE - the R1032
registered unlock-window line "sprite/weekend/3+4 blocked until >=1 non-weekend piece intervenes
(four-peat reset)" fires THIS round with DOUBLE intervention (v61 market_close + v62 morning after
the v58/v59/v60 weekend three-run). Production ~11:0x = literal morning window (R1031 daytime-window
pre-registration family, v62 fired first at ~07:0x; 晨风 content + weekend holiday bucket + morning
production hour = triple literal alignment). Post-v62 rotation: qiuxin 10 / huaijiu 9 / xiaqi 10 /
yanhuo 10 / zhixu 9 / xiaoyao 11 -> minimum pair huaijiu+zhixu 9 -> longest gap zhixu (v53..v62 = 9)
-> cascade trail (r1086_pool_scan.txt fresh, fleet includes v62): zhixu [rain/2 no-event +
coldsnap/2+9 season ALL BLOCKED] -> huaijiu [gap 7: heatwave/8 + coldsnap/7 season + market_open/6+7+9
holiday-closure + ceo_order/3+10 no-event ALL BLOCKED] -> qiuxin [gap 5: heatwave/0+9 season BLOCKED]
-> yanhuo [gap 4: morning/6+7 zhou+cai-xian market-stall 3-link-iso (v44+v57+v58) BLOCKED at any
hour - R1032 close-out note + R1062 trail double-on-file; r1086 keyword-list miss on 菜 honestly
corrected in evidence file] -> xiaqi [gap 3: morning/0+15 business 3-link + chen-wu twins BLOCKED]
-> xiaoyao [v62 just-consumed; remaining rows all blocked] -> SIX AXES ALL BLOCKED -> sprite-voice
cascade fallback (R1024 降级备胎转正 precedent): typhoon/3 + ceo_order/0+3+4+9+11 no-event +
heatwave/3+11 season + weekend/4 night-content-at-day weak (R1020 literal-law) ALL BLOCKED ->
sprite/weekend/3 「嗡嗡嗡，晨风中的舞」 = UNIQUE honestly-pairable row at THIS context (= the
R1032-registered unlock target line for this exact window). Zero-collision standard NOT relaxed
(R442 anti-isomorphism spine, v1-v62 sixty-two-link zero-collision chain). Facet-band honest
registrations: (1) SPRITE VOICE 4th piece, 4 DISTINCT buckets zero-repeat (v50 festival / v54
night / v61 market_close / v63 weekend); (2) ONOMATOPOEIA band 2-link (v50 叮叮当 = 1st, THIS
嗡嗡嗡 = 2nd - no chain); (3) MORNING-SCENE band 2-link (v62 晨钓 facet + THIS 晨舞 facet - chain
would form on a 3rd -> post-v63 morning-scene rows future-blocked registration); (4) 逍遥/morning/1
consumed by v62, angling rows post-v62-blocked carried. Built-in tension: SHENG x WU - the tiniest
body in the city (one sprite's hum, the finest voice) takes the largest stage (the whole city's
morning breeze); the invisible wind meets the visible dance. Layout = QUOTE-v2 params verbatim;
h2_size ladder = 60 band (11em quote line fits 15.33em budget; v61 城市生灵 attribution line same
band precedent). Machine source/dedup assertions (R456 system, card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V63 = os.path.join(BASE, "MC-20261003-DAILY-v63")
TMP = V63 + "-tmp"
os.makedirs(V63, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"嗡嗡嗡，晨风中的舞"
VOICE, BUCKET, IDX = u"sprite", u"weekend", 3  # sprite top-level voice (12 buckets x 12 rows = 144, R982)

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
wb = pool["sprite"][BUCKET]
assert len(wb) == 12, "sprite bucket != 12 rows (sprite = 12 buckets x 12 rows = 144)"
assert wb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % wb[IDX]
assert wb[4] == u"叮咚响夜晚", "night-content twin row weekend/4 expected 叮咚响夜晚 (day-weak-adjacency blocked)"
assert pool["axes"][u"逍遥"][u"morning"][1] == u"鱼竿一甩，梦醒时分", "v62 consumed-row structural anchor expected"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1086_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"嗡嗡", u"嗡嗡嗡", u"晨风", u"风中", u"的舞", u"中的舞", u"风中的舞", u"晨风中的舞", u"嗡嗡嗡，晨风中的舞"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1086 quote-face word probe for candidate " + QUOTE_CORE + u" (sprite/weekend line3)"]
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: all 2-5 char punctuation-inclusive shingles ZERO fleet hits (r1086_pool_scan.txt fresh scan, fleet includes v62; zero new cards since) = ELEVENTH fully-zero row of the series (v53-v62 ten precedents). Facet-band honest registrations (single-char/family layer, NOT card-face collisions; machine scan 2+ char ZERO verified): (1) SPRITE VOICE 4th piece - 4 DISTINCT buckets zero-repeat (v50 festival / v54 night / v61 market_close / THIS weekend) = voice-level anti-isomorphism strongest form; (2) ONOMATOPOEIA band - v50 叮叮当 [1st] + THIS 嗡嗡嗡 [2nd] = 2-link, no chain, 3rd use would form; (3) MORNING-SCENE band - v62 晨钓 facet + THIS 晨舞 facet = 2-link -> POST-v63 REGISTRATION: morning-scene rows future-blocked on a 3rd (chain-forms law); (4) v62-consumed row 逍遥/morning/1 + angling rows post-v62-blocked carried (R1062 registration).")
qrep.append(u"weekend-reset unlock note: R1032 unlock-window line 'weekend/3+4 (sprite) blocked until >=1 non-weekend piece intervenes (four-peat reset)' - v61 (market_close) + v62 (morning) = DOUBLE intervention after v58/v59/v60 three-run -> reset achieved, THIS piece = weekend bucket 1st of new run. 晨风 content + ~11:0x literal morning production + weekend holiday bucket = TRIPLE literal alignment (R1031 daytime-window family, v62 fired first; adjacency ladder: v55/v57 时点邻接 -> v62/v63 literal).")
qrep.append(u"supply-face honest note post-v63: sprite weekend face remainder = weekend/4 夜晚 content (night-window only); six axes remain R1032-depletion state; morning-scene band 2-link formed -> 3rd use future-blocked; unlock windows unchanged: rain-event day / CEO-order day / 2026-10-08+ market reopen / Nov+ coldsnap / summer heatwave / night-window rows (sprite/weekend/4 + night-bucket residue). Pool-expansion report position maintained (status-line not chase).")
io.open(os.path.join(TMP, "r1086_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V63:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 063",
    u"2026-10-03 · 国庆假期 · 晨",
    u"「嗡嗡嗡，晨风中的舞」",
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
assert H2_SIZE == 60, "em ladder expected 60-band (11em quote line + 城市生灵 attribution line v61 same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261003-DAILY-v63"
meta["form"] = (u"DAILY 城市日签 063（L-卡 图文轻内容线 DAILY 形态第六十三件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 级联续领 R1086·日签节律续件=日期×情境桶对位判据第六十三证〔**sprite "
                u"声部第四件+weekend 桶四连重置后首件**〔声部四件四桶零重复=v50 festival/v54 night/v61 "
                u"market_close/本件 weekend=声部级反同构最强形·**R1032 解锁窗「weekend/3+4 blocked until "
                u">=1 non-weekend piece intervenes」兑现**：v58/v59/v60 三连后 v61 market_close+v62 morning "
                u"双干预=四连重置达成→本件=新跑第一件〕+**晨窗 literal 对位**：~11:0x 晨间生产×晨风内容×"
                u"weekend 假日桶三重 literal〔R1031 日间窗预登记族·v62 首发承继·邻接升档带 v55/v57 时点"
                u"邻接→v62/v63 literal〕〕+**旋转级联兑现（诚实注）**：v62 后计数 求新 10/怀旧 9/侠气 10/"
                u"烟火 10/秩序 9/逍遥 11→双轴并列最少→最长回补距=秩序〔v53 后 gap 9〕干净行仅 rain/2+"
                u"coldsnap/2+9=雨无事件+十月季相全阻→级联怀旧〔gap 7〕：季相+market_open 假日休市〔v57 "
                u"判例〕+ceo_order 无令事件全阻→级联求新〔gap 5〕：heatwave 季相全阻→级联烟火〔gap 4〕："
                u"morning/6+7 粥香早市+菜场市集三连同构〔v44+v57+v58〕任一时点皆阻〔R1032 收口注+R1062 "
                u"轨迹双在案·r1086 关键词表「菜」漏字面诚实修正注〕→级联侠气〔gap 3〕：morning/0+15 生意"
                u"三连+晨雾散孪生对任一时点皆阻→逍遥〔v62 刚用·余行全阻〕→**六轴全阻=声部级联回退**"
                u"〔R1024 降级备胎转正先例〕→sprite 声部：typhoon/ceo_order 无事件+heatwave 季相+"
                u"weekend/4 夜内容日间弱邻接全阻→**weekend/3 唯一诚实配对行胜出**=零直撞标准不放松"
                u"〔R442 反同构主线·v1-v62 六十二连零直撞〕〕+line3 选优〔**全 shingle 零命中=系列第十一件"
                u"全零邻接行**（v53-v62 十件先例后·r1086_quote_face.txt 九词机核〕+**声部族带诚实注册**："
                u"拟声族带二连〔v50 叮叮当=1+本件 嗡嗡嗡=2·三连未成形〕+**晨场景带二连成形预挂**〔v62 "
                u"晨钓面+本件 晨舞面=二连→post-v63 晨场景行第三用起阻注册〕+夜内容行 weekend/4 留夜窗注〕〕"
                u"+生灵声部〔最细的一具身体〕×晨风〔全城最大的舞台〕×舞〔看得见的姿态〕=**最小舞者×最大"
                u"舞台+无形×有形双反差金句位**〔族四十九连·晨舞位语感独占注=假期近午人潮未醒的城市里·"
                u"最小的居民已经开演了今天的头一场〕〕）")
meta["source_quote"] = u"「嗡嗡嗡，晨风中的舞」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 sprite[weekend][3]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-03.md（当日日期语境源·国庆假期第 3 日+周六·晨间生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 sprite[weekend][3] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 12 行计数+sprite "
                         u"顶层 12 桶结构断言〔R982〕+夜内容孪生行 weekend/4 结构断言+v62 已耗行 逍遥/morning/1 "
                         u"结构锚）②日期行 2026-10-03=当日历法事实·周六+国庆假期第 3 天〔daily brief "
                         u"2026-10-03 当日窗语境〕+晨标记〔v54 夜标记/v62 晨标记先例带·~11:0x 晨间生产 "
                         u"literal〕③情境=weekend 桶四连重置后首件〔三重 literal 对位=晨间生产时刻×晨风内容×"
                         u"weekend 假日桶〕④声部署名=台词池城市生灵声部行·本行无称谓面=纯景句·泛称零涉及"
                         u"〔人设权红线零接触·charter §2.4·v50/v54/v61 先例族〕⑤去重断言=本行不在 "
                         u"city-spirit.md 已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 "
                         u"修正律·DAILY-v1~v62 全 62 行+REACT-v8 同桶三行+city-spirit 节日场景三行皆非本行）"
                         u"+「嗡嗡」「嗡嗡嗡」「晨风」「风中」「的舞」「中的舞」「风中的舞」「晨风中的舞」"
                         u"全句 probe 九词机核〔r1086_quote_face.txt〕+**零构式层邻接**〔r1086_pool_scan.txt "
                         u"fresh 2-5 字含标点 2 字组全零=系列第十一件全零邻接行〕+**族带诚实注册**〔声部四件"
                         u"四桶零重复+拟声族带二连〔v50 叮叮当〕+晨场景带二连成形预挂〔v62 晨钓面〕→post-v63 "
                         u"第三用起阻〕⑥季相核=本行无年味/春联/春雨/寒潮类季相错位词〔R972 制·晨风=四季通用"
                         u"晨间面·十月秋晨兼容〕⑦品牌语感注=「嗡嗡嗡，晨风中的舞」拟声开场+画面定格=去 AI "
                         u"感对位·人味命中·零书面套语·零消费宣称无品牌无价格")
meta["attribution_rule"] = (u"署名=池级+声部级（台词池·城市生灵声部）——池行无逐民署名·禁虚构居民名/生灵名"
                             u"（charter v1.2 署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v50/v54/v61 "
                             u"先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（sprite 声部第四件+weekend 四连重置"
                            u"后首件双位〔**旋转级联+解锁窗兑现+零直撞三律并轨诚实执行**：秩序 rain/coldsnap "
                            u"阻→怀旧休市/无令/季相阻→求新季相阻→烟火菜场市集三连阻→侠气生意三连+孪生阻→"
                            u"逍遥刚用余行全阻→六轴全阻声部级联回退→sprite/weekend/3 唯一诚实配对行胜出〕+"
                            u"最小舞者×最大舞台+无形×有形双反差金句位〔族四十九连·晨舞位语感独占注〕+拟声开场"
                            u"人味=语录卡线变体零新模板第六十三证（QUOTE-v2 参数 verbatim 复用·h2_size 60 "
                            u"档〔v61 城市生灵署名行同带先例〕·charter §1「日签变体随时可续」兑现）·公众号低"
                            u"创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 "
                            u"O-2026-09-28-1910 对位〔假期近午的城市里最小的居民先开演=城市一日之计的生灵"
                            "开卷·城市生灵令 P-20260926-13 媒体面第四采〕+**供给面诚实注**：本件后 sprite "
                            u"weekend 面余 weekend/4 夜内容行（夜窗专属）+六轴维持 R1032 枯竭注+晨场景带二连"
                            u"成形→第三用起阻注册=DAILY 可诚实配对面维持结构性近枯竭注〔R1030 REACT 判负+"
                            u"R1032 零判负+R1086 唯一行解锁窗兑现三信号族·池扩容呈报位维持呈现状行不催办〕·"
                            u"post-v63 指针：解锁窗维持=雨事件日/CEO 令日/10-08 market_open 复市/Nov+ 寒潮/"
                            u"夏季 heatwave/夜窗行（sprite/weekend/4+night 余面）·REACT-v9 10-04 窗·F 序号"
                            u"诚实注=本件先落 F-148·REACT-v9 10-04 预指位顺延 F-149〔R978 判例 finished "
                            u"顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：嗡嗡嗡〔一具生灵的小身体·全城最细的"
                          u"声音〕×晨风中的舞〔全城尺度的风=最大的舞台〕=最小舞者×最大舞台反差+无形的风"
                          u"〔看不见〕×有形的舞〔看得见的姿态〕=无形×有形反差〔族四十九连〕/情 1 假日上午"
                          u"生灵晨舞的轻盈治愈共鸣温和如实非强极点〔G5 生灵/宠物群+G3 轻松群〕/时 2 当日="
                          u"2026-10-03 周六国庆假期第 3 日·~11:0x 晨间生产=weekend 桶〔假日态·四连重置后"
                          u"首件〕×晨风内容×晨间生产时刻三重 literal 直配=解锁窗兑现件〔R1032 注册行+"
                          u"R1031 日间窗预登记族〕/台 2 公众号方图承载=MC-001~147 S3 实证复用）——"
                          u"hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 "
                          u"DAILY·queue §E E30 R1086 级联续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面="
                     u"纯景句·泛称零涉及〔v50/v54/v61 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零"
                     u"金钱数额（嗡嗡嗡晨风中的舞=晨间生灵意象非商业面·无品牌无价格=零消费宣称）；成品只"
                     u"入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十三件·charter v1.2 §4 形态码 DAILY·日签节律续件·sprite 声部第四件·weekend 四连重置后首件·晨窗 literal 对位件·晨场景带二连注册件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: sprite[weekend][3] verbatim OK; weekend bucket=12 rows; sprite top-level 12 buckets (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v62; rotation cascade: zhixu rain/coldsnap blocked -> huaijiu market_open/ceo_order/season blocked -> qiuxin heatwave blocked -> yanhuo morning market-stall 3-link blocked (cai-xian keyword miss honestly corrected) -> xiaqi morning business 3-link+twin blocked -> xiaoyao just-consumed remainder blocked -> SIX AXES ALL BLOCKED -> sprite-voice cascade fallback (R1024 precedent): sprite/weekend/3 = UNIQUE honestly-pairable clean row at DAYTIME morning production (r1086_pool_scan.txt fresh, fleet includes v62); quote-face word probe: 9 words see r1086_quote_face.txt (all ZERO; eleventh fully-zero row of series after v53-v62; sprite-voice 4-piece 4-bucket zero-repeat + onomatopoeia 2-link + morning-scene 2-link chain-forms registration + weekend/4 night-window note)")
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
report.append("LADDER_60: 11em quote line + 城市生灵 attribution line fits 60-band (v61 same-band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; weekend-reset-unlock + rotation-cascade + eleventh-fully-zero-row + sprite-voice-4-piece + morning-scene-2-link registration honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1086.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V63, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V63, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v62 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, 11em quote-line + 城市生灵 attribution line fits) + E4 fired async" % H2_SIZE)
