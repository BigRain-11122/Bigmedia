# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v46 build: DAILY (city daily-sign) series FORTY-SIXTH piece (R1015, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (forty-sixth same-day proof, bucket-level; scene face = holiday street-
fellowship gathering cheer honestly noted, THIRD non-lamp face after v44 morning-market and
v45 at-home old-objects = anti-homogenization variation continuation). Axis pick = xiaqi
(hearty street-fellowship, the hardiest mutual-aid residents) /festival/7: rotation law =
post-v45 DAILY counts qiuxin 8 / huaijiu 8 / xiaqi 7 / yanhuo 8 / zhixu 7 / xiaoyao 7 = THREE
axes tied at minimum (xiaqi/zhixu/xiaoyao) -> tie-break by longest-since-last-pick
redemption = xiaqi (first re-pick since v40; v41-v45 five pieces all other axes = longest
redemption distance in the tie). Within xiaqi FREE face content-strength pick documented
(card-face-level law R1010 corrected scanning; r1015_pool.txt FREE-face precheck +
r1015_quote_face.txt word-face machine probe): line3 'da huo er huan ju yi tang, jie ri fen
wei zhen shi hao' = jie-ri-fen-wei v28 wordface DIRECT collision (machine-proven) + slogan-
ish zero-scene R442; line4 'chuan shang hao zi xiang lian tian, jie ri xi qing le wu bian' =
chuan-shang v20 two-char collision + xi-qing v19 adjacency + generic blessing tail; line6
'deng yi gua qi, nian wei er jiu nong le' = nian-wei seasonal R972 + lamp face; line8 'gua ge
hong deng long, nian wei er geng nong le' = nian-wei seasonal + deng-long saturation + lamp
face; line12 'chuan zhang shuo, chu hai ye de you hao xin qing' = chuan-zhang CENSUS-v16
'du-lun-chuan-zhang' card-face cross-series collision (machine-proven) + generic xin-qing;
line14 'jie ri deng shi zhen re nao, ye ye dou neng jian xing xing' = re-nao v32 four-use
saturation + xing-xing v43 night-sky motif direct repeat + lamp face; line15 'deng long yi
gua, xi qing jiu lai la' = deng-long-yi-gua v21 four-char family collision + xi-qing v19
adjacency + deng-long eight-piece saturation; line16 'jiu lou li wai dou piao xiang, chuan
zhang men xin qing fei yang' = chuan-zhang CENSUS-v16 collision + piao-xiang v40 jiu-xiang
adjacency + generic xin-qing; line17 'jie ri li zan men duo zou dong, jiang hu yi qi zui
jiang xin yong' = jiang-hu-yi-qi v3 FOUR-char direct collision (machine-proven) + zou-dong
v34 chuan-men adjacency. THIS line7 = 'da huo er le he le he, yi nian dao tou lei bu huai' =
the ONLY FREE row with ZERO machine wordface flag on probe words (da-huo-er/le-he/yi-nian-
dao-tou/lei-bu-huai; r1015_quote_face.txt) and ZERO seasonal wording and ZERO four-char
collision and NON-lamp face (third non-lamp = anti-homogenization variation continuation).
Honest notes carried: 'le-he-le-he' reduplication = construct-layer band adjacency (v43
chuan-chuan-de / v34 chuan-chuan-men / v35 zhan-zhan = different-word families, R1012
xing-xing two-char law); lei x le tension = v32 lao x huan same-family different-face
honest note (v32 kitchen-labor-missing-family face vs THIS rest-day gathering-cheer face =
same family different scene row); zero explicit festival word = festival bucket catalog =
holiday generic face (v38/v44/v45 precedent), day-match compensation = date line
'2026-10-02 - National Day holiday' + holiday street-gathering scene framing. Scene layer:
National-Day day-2 holiday, xiaqi-axis street folks off work gather at the street corner,
patting shoulders laughing it off saying a-whole-year-of-toil-cannot-wear-us-down = holiday
gathering-cheer scene (R442 weakness prescription band; THIRD non-lamp face of the series
run). Built-in tension: LEI x LE axis-internal self-contrast (thirty-second consecutive
variant): the hardiest hearty residents, hardened by a whole year of toil, spend the
holiday laughing it off together = the toughest crowd laughs loudest (register exclusive
note: scholars archive, nostalgics keep, only the street-hardiest know the best use of a
holiday is a room full of da-huo-er laughter that washes the year's toil away). Living-city
proof = a city whose crowd laughs off its toil is a city whose spirit cannot be worn down
(city humane-accumulation order echo). Line-level freshness forty-third proof = same-axis-
different-line forty-first proof. Quote verbatim + card framing (R285 QUOTE precedent).
Layout = QUOTE-v2 params verbatim; h2_size ladder picks 50 (quote line 17.00em: 60-band
budget 15.33em fails -> 50-band budget 18.40em margin +1.40em = v14 18.0em@50 / v16
16.10em@50 precedent band). Machine source/dedup assertions (R456 system, card-face level
R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V46 = os.path.join(BASE, "MC-20261002-DAILY-v46")
TMP = V46 + "-tmp"
os.makedirs(V46, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"大伙儿乐呵乐呵，一年到头累不坏"
AXIS, BUCKET, IDX = u"侠气", u"festival", 7

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1015_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"大伙儿", u"乐呵", u"一年到头", u"累不坏"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1015 quote-face word probe for candidate " + QUOTE_CORE]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
io.open(os.path.join(TMP, "r1015_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V46:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits do NOT count as consumption.
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d
# consumed festival lines (documented not asserted): DAILY-v1 qiuxin/festival/4 +
# DAILY-v2 huaijiu/festival/0 + DAILY-v3 xiaqi/festival/5 + DAILY-v4 yanhuo/festival/4 +
# DAILY-v5 zhixu/festival/4 + DAILY-v6 xiaoyao/festival/3 + DAILY-v7 qiuxin/festival/7 +
# DAILY-v8 xiaqi/festival/13 + DAILY-v9 qiuxin/festival/12 + DAILY-v10 huaijiu/festival/3 +
# DAILY-v11 yanhuo/festival/13 + DAILY-v12 xiaoyao/festival/15 + DAILY-v13 xiaqi/festival/2 +
# DAILY-v14 qiuxin/festival/3 + DAILY-v15 qiuxin/festival/11 + DAILY-v16 huaijiu/festival/1 +
# DAILY-v17 zhixu/festival/12 + DAILY-v18 xiaoyao/festival/1 + DAILY-v19 yanhuo/festival/3 +
# DAILY-v20 xiaqi/festival/1 + DAILY-v21 zhixu/festival/6 + DAILY-v22 huaijiu/festival/12 +
# DAILY-v23 qiuxin/festival/13 + DAILY-v24 yanhuo/festival/2 + DAILY-v25 huaijiu/festival/17 +
# DAILY-v26 xiaqi/festival/10 + DAILY-v27 yanhuo/festival/7 + DAILY-v28 zhixu/festival/9 +
# DAILY-v29 xiaoyao/festival/2 + DAILY-v30 zhixu/festival/2 + DAILY-v31 xiaoyao/festival/4 +
# DAILY-v32 yanhuo/festival/10 + DAILY-v33 huaijiu/festival/4 + DAILY-v34 xiaqi/festival/9 +
# DAILY-v35 zhixu/festival/11 + DAILY-v36 xiaoyao/festival/16 + DAILY-v37 qiuxin/festival/5 +
# DAILY-v38 yanhuo/festival/5 + DAILY-v39 huaijiu/festival/5 + DAILY-v40 xiaqi/festival/11 +
# DAILY-v41 zhixu/festival/17 + DAILY-v42 xiaoyao/festival/13 + DAILY-v43 qiuxin/festival/9 +
# DAILY-v44 yanhuo/festival/1 + DAILY-v45 huaijiu/festival/16 + REACT-v8 xiaoyao/festival/17 +
# yanhuo/festival/12 + zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio
# zhixu/festival/16 + qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 046",
    u"2026-10-02 · 国庆假期",
    u"「大伙儿乐呵乐呵，一年到头累不坏」",
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
assert H2_SIZE == 50, "em ladder expected 50 (quote line 17.00em: 60-band 15.33em fails, 50-band budget 18.40em margin +1.40em = v14 18.0em@50 / v16 16.10em@50 precedent band), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v46"
meta["form"] = (u"DAILY 城市日签 046（L-卡 图文轻内容线 DAILY 形态第四十六件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1015·日签节律续件=日期×情境桶对位判据第四十六证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日街坊欢聚歇工面如实"
                u"注记〔灯面之外的假日欢聚面·v44 早市晨面+v45 老物件面后**第三件非灯面=反同构变奏第三证**·R442 "
                u"系列同构弱点正面处方·日期行「2026-10-02 · 国庆假期」承节日面〕〕+六轴收官后线级新鲜度第四十三证="
                u"同轴异行第四十一证〔侠气轴 DAILY-v3〔line5〕+DAILY-v8〔line13〕+DAILY-v13〔line2〕+DAILY-v20"
                u"〔line1〕+DAILY-v26〔line10〕+DAILY-v34〔line9〕+DAILY-v40〔line11〕之外线级新鲜行 line7·轮前 "
                u"r1015_pool.txt 侠气桶 FREE 行预检=R978 拦截教训执行·v40 行已 USED 复核〕+旋转律兑现=v45 后计数"
                u"求新 8/怀旧 8/侠气 7/烟火 8/秩序 7/逍遥 7=三轴并列最少（侠气/秩序/逍遥）→并列面最久未采回补="
                u"侠气〔v40 后 5 件未采·v41-v45 五件皆他轴=并列轴中最长回补距〕·FREE 面内容强度择优如实注记"
                u"〔侠气 FREE 面逐行机核排除：line3「大伙儿欢聚一堂，节日氛围真是好」=节日氛围 **v28 词面直撞**"
                u"〔r1015_pool.txt 机核〕+口号化零人物零场景 R442/line4「船上号子响连天，节日喜庆乐无边」=船上 "
                u"**v20 词面直撞**+喜庆 v19 邻接+乐无边祝福套语尾/line6「灯一挂起，年味儿就浓了」=年味季相 R972+"
                u"灯面/line8「挂个红灯笼，年味儿更浓了」=年味季相+红灯笼灯笼饱和+灯面/line12「船长说，出海也得"
                u"有好心情」=船长 **CENSUS-v16「渡轮船长」卡面跨系列词面直撞**〔机核〕+心情泛化词/line14「节日灯饰"
                u"真热闹，夜夜都能见星星」=热闹 v32 四用饱和+星星 **v43 夜空星星 motif 直撞**+灯饰灯面/line15"
                u"「灯笼一挂，喜庆就来啦」=灯笼一挂 **v21「挂上灯笼」四字族直撞**+喜庆 v19 邻接+灯笼八件饱和/"
                u"line16「酒楼里外都飘香，船长们心情飞扬」=船长 CENSUS-v16 直撞+飘香 v40 酒香邻接+心情泛化词/"
                u"line17「节日里咱们多走动，江湖义气最讲信用」=江湖义气 **v3 四字直撞**〔机核〕+走动 v34 串门"
                u"邻接族；本行 line7=「大伙儿乐呵乐呵，一年到头累不坏」=**FREE 面唯一零机核词面旗行**〔大伙儿/"
                u"乐呵/一年到头/累不坏=fleet 卡面+source_quote 扫描·probe 词面 r1015_quote_face.txt 机核〕+零季相词+"
                u"零四字直撞+非灯面〔v44 后第三件非灯面=反同构变奏第三证〕+「乐呵乐呵」叠词构式层诚实邻接注记="
                u"v43 串串的/v34 串串门/v35 盏盏叠词构式带异词族〔R1012「星星」两字同律=构式层如实注记非主题族"
                u"重复〕+累×乐张力 v32 劳×欢同族异面诚实注记〔v32=灶头劳作怀人面 vs 本行=歇工欢聚扛事面=同族异质"
                u"行〕+「累不坏」口语真感=人味命中+零显性节日钩〔festival 桶编目=节日通用面·v38/v44/v45 零节日钩"
                u"先例·假日街坊欢聚面场景补偿〕〕）")
meta["source_quote"] = u"「大伙儿乐呵乐呵，一年到头累不坏」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[侠气][festival][7]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v45 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[侠气][festival][7] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v45 同桶直配第四十六证=日签节律判据"
                         u"系列化·国庆假期第 2 日街坊歇工欢聚=假日欢聚面场景对位〔场景级如实注记：灯面之外的假日"
                         u"街坊欢聚面·第三件非灯面〕）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕"
                         u"⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote 任一（卡面级"
                         u"实扫=R1010 修正律·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/"
                         u"4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9"
                         u"〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/"
                         u"2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+"
                         u"DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22"
                         u"〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/"
                         u"10〕+DAILY-v27〔烟火/7〕+DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+"
                         u"DAILY-v31〔逍遥/4〕+DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35"
                         u"〔秩序/11〕+DAILY-v36〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+DAILY-v39〔怀旧/"
                         u"5〕+DAILY-v40〔侠气/11〕+DAILY-v41〔秩序/17〕+DAILY-v42〔逍遥/13〕+DAILY-v43〔求新/9〕+"
                         u"DAILY-v44〔烟火/1〕+DAILY-v45〔怀旧/16〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+"
                         u"city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第四十三证·本行="
                         u"侠气轴 line7 非 DAILY-v3 line5 非 DAILY-v8 line13 非 DAILY-v13 line2 非 DAILY-v20 line1 非 "
                         u"DAILY-v26 line10 非 DAILY-v34 line9 非 DAILY-v40 line11=同轴异行第四十一证〔六轴收官后侠气轴"
                         u"第八采·轮前 r1015_pool.txt 侠气桶 FREE 行预检=R978 拦截教训执行〕+「大伙儿」「乐呵」「一年"
                         u"到头」「累不坏」probe 四词机核〔r1015_quote_face.txt〕⑥季相核=本行无年味/春联/春雨类季相"
                         u"错位词〔R972 制·侠气面 line6/8 年味行已按季相律排除·乐呵欢聚=全季相公共措辞与国庆假日"
                         u"时点对位〕⑦品牌语感注=「乐呵乐呵」「累不坏」大众口语叠词真感〔去 AI 感对位〕+侠气轴"
                         u"〔街坊义气·豪爽担当〕×大伙儿乐呵乐呵（最能扛事的大伙儿把一年辛苦笑着放下）=累×乐轴内"
                         u"自反差金句位+国庆假期第 2 日街坊歇工欢聚场景层〔R442 审计叙事弱点处方带·第三件非灯面="
                         u"反同构变奏第三证〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·侠气轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·乐呵欢聚的侠气轴街坊=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十六证+三轴"
                            u"并列最少最久未采回补=侠气赎回〔v40 后 5 件首回〕+FREE 面逐行机核排除注记后本行胜出"
                            u"〔唯一零机核词面旗行·乐呵乐呵叠词构式层诚实邻接注+累×乐 v32 劳×欢同族异面注〕+「大伙儿"
                            u"乐呵乐呵，一年到头累不坏」〔最硬朗的大伙儿假日里笑声最响〕累×乐轴内自反差金句位〔族"
                            u"三十二连·载体语感独占注：文人把感悟写成集子、念旧的人把岁月收进柜子——只有最扛事的"
                            u"大伙儿知道，假日最好的过法是一屋子乐呵乐呵，把一年的辛苦笑着放下〕+假日街坊欢聚歇工"
                            u"场景层=R442 审计处方带续证+v44 后第三件非灯面=反同构变奏第三证+「乐呵乐呵」「累不坏」"
                            u"大众口语=人味命中〔CEO 审美线对位·城市人文积累令对位·笑声压过辛苦=城市精气神磨不"
                            u"坏面〕）+语录卡线变体零新模板第四十六证（QUOTE-v2 参数 verbatim 复用·h2_size 50 回摆档"
                            u"〔17.00em 引文行·60 档 15.33em 排除→50 档预算 18.40em margin +1.40em=v14 18.0em@50/"
                            u"v16 16.10em@50 先例带内〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：侠气轴〔街坊义气·豪爽担当〕×大伙儿乐呵乐呵"
                          u"〔最能扛事的大伙儿把一年辛苦笑着放下〕=累×乐轴内自反差金句位〔族三十二连〕+国庆假期"
                          u"第 2 日街坊歇工欢聚场景层+「乐呵乐呵」「累不坏」口语叠词真感/情 1 假日欢聚松弛共鸣如实"
                          u"非强极点/时 2 当日时点=国庆假期第 2 日欢聚面直配+festival 情境桶直配第四十六证〔桶级·"
                          u"场景级假日欢聚面注记〕/台 2 公众号方图承载=MC-001~130 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1015 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（乐呵欢聚的侠气轴街坊=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（欢聚乐呵=公共生活意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十六件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaqi][festival][7] verbatim OK; festival bucket=18 lines; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v45 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness forty-third proof: xiaqi line7 != DAILY-v3 line5 != DAILY-v8 line13 != DAILY-v13 line2 != DAILY-v20 line1 != DAILY-v26 line10 != DAILY-v34 line9 != DAILY-v40 line11 = same-axis-different-line forty-first proof; quote-face word probe: da-huo-er/le-he/yi-nian-dao-tou/lei-bu-huai see r1015_quote_face.txt; strongest-exclusion rows machine-proven: line3 jie-ri-fen-wei v28 collision; line4 chuan-shang v20 + xi-qing v19; line6 nian-wei seasonal + lamp; line8 nian-wei + hong-deng-long; line12 chuan-zhang CENSUS-v16 cross-series; line14 re-nao v32 saturation + xing-xing v43 motif; line15 deng-long-yi-gua v21 family + xi-qing v19; line16 chuan-zhang CENSUS-v16 + piao-xiang v40; line17 jiang-hu-yi-qi v3 four-char")
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
report.append("LADDER_DROP_50: quote line 17.00em; 60-band budget 15.33em excluded (17.00>15.13); 50-band budget 18.40em margin +1.40em = v14 18.0em@50 / v16 16.10em@50 precedent band; all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1015.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V46, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V46, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v45 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder drop 60->50, quote 17.00em driver) + E4 fired async" % H2_SIZE)
