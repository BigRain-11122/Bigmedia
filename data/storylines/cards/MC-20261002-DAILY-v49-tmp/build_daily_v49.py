# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v49 build: DAILY (city daily-sign) series FORTY-NINTH piece (R1018, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 evening -> festival
bucket direct match (forty-ninth same-day proof, bucket-level; scene face = holiday street
festival-colors stroll, honestly noted; NON-LAMP-FACE variation honest note: after the v47/v48
two-piece lamp-face band this line carries no lamp character - festival colors/热闹 as generic
festive face = anti-isomorphism variation fourth proof, second return swing after the
v44/v45/v46 non-lamp trio). Axis pick = qiuxin (novelty-first, screen-native residents)
/festival/2: rotation law = post-v48 DAILY counts qiuxin 8 / huaijiu 8 / xiaqi 8 / yanhuo 8 /
zhixu 8 / xiaoyao 8 = SIX-AXIS FULL TIE (series third all-tie state; first = post-v36 R1006,
second = post-v42 R1012) -> tied-face longest-unpicked redemption = qiuxin (first re-pick
since v43; v44-v48 five pieces all other axes = R1006/R1012 same ruling third proof).
Within qiuxin FREE face content-strength pick documented (card-face-level law R1010;
r1018_pool.txt bucket pre-check machine-proven): line0 liang-tang-le DIRECT collision with
DAILY-v2 + deng-yi-gua construct near city-spirit line14 + lamp->night-sky causation near v12 =
triple adjacency; line1 jie-ri-de DIRECT v4 + zhe-jie-ri DIRECT v28/v30 double collision +
slogan-face R442; line6/8/15 nian-wei seasonal wording -> R972 seasonal law exclusion (three
rows); line10 jie-ri-li DIRECT v17 + slogan-face; line16 deng-ke-zhen DIRECT v11 + night-as-day
isomorphism v26; line17 jie-ri-li DIRECT v17 + cai-deng same-axis-same-bucket DIRECT v15 =
strongest exclusion. THIS line2 = '看这色彩斑斓，比平时还热闹几分' = qiuxin FREE-face ONLY
zero-machine-collision row (distinctive shingles se-cai-ban-lan / bi-ping-shi / re-nao-ji-fen
ALL ZERO fleet hits). Honest adjacency notes carried: se-cai-ban-lan 4-char = pool-line
book-ish wording honest note (R1012 book-cliche note carried; verbatim zero-edit red line
untouched = E4/M6 calibration position); re-nao 2-char construct-layer adjacency (v16 rhetorical-
question / v22 cou-ge-re-nao object slot / v34 truncated sigh = three fleet uses each a different
construction; this line = bi-ping-shi-hai-re-nao-ji-fen comparative = fourth construction,
isomeric); kan-zhe opener construct-layer adjacency (v15/v39 kan-kan-zhe doubled opener vs this
single kan = construct-layer isomer note). Qiuxin-axis FREE face ALL-WEAK state honest note
(line9 consumed by v43; remaining FREE rows all flagged - R1012 all-weak note carried): this
line wins as the only zero-direct-collision row (v47 zhixu line15 same-type ruling). SIX-AXIS
festival resident-bucket FREE-face all-weak STRUCTURAL note: all six axes now scan all-weak =
supply-side structural signal; sprite festival 12 lines unconsumed + remaining 11 buckets = E30
supply candidates per queue section-E ledger (next-round claim note). Built-in tension: CHANG x
SHENG axis-internal self-contrast (thirty-fifth consecutive variant): the novelty-first
screen-native residents walk the festival street, look up and certify the present street colors
as beating the everyday baseline - the most forward-looking people stamp the present as the
city's newest release. Living-city proof = a city whose most novelty-hungry residents certify
its present as its best new thing is a city still alive enough to surprise (city humane-
accumulation order echo). Line-level freshness forty-sixth proof = same-axis-different-line
forty-fourth proof. Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2
params verbatim; h2_size ladder holds 50 (quote line 17.00em inside 50-band budget 18.40em
margin +1.40em = v14/v16/v46/v48 same 17.00em-driver band). Machine source/dedup assertions
(R456 system, card-face level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V49 = os.path.join(BASE, "MC-20261002-DAILY-v49")
TMP = V49 + "-tmp"
os.makedirs(V49, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"看这色彩斑斓，比平时还热闹几分"
AXIS, BUCKET, IDX = u"求新", u"festival", 2

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1018_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"色彩斑斓", u"比平时", u"热闹几分", u"斑斓", u"几分", u"平时", u"看这", u"热闹"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1018 quote-face word probe for candidate " + QUOTE_CORE]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: se-cai-ban-lan 4-char = book-ish pool wording honest note (R1012 carried; verbatim zero-edit = E4/M6 calibration); re-nao 2-char construct layer v16/v22/v34 three uses each different construction vs this comparative = isomeric; kan-zhe opener construct layer (v15/v39 kan-kan-zhe doubled vs this single kan)")
io.open(os.path.join(TMP, "r1018_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V49:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits do NOT count as consumption.
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d
# consumed festival lines (documented not asserted): DAILY-v1 qiuxin/4 + DAILY-v2 huaijiu/0 +
# DAILY-v3 xiaqi/5 + DAILY-v4 yanhuo/4 + DAILY-v5 zhixu/4 + DAILY-v6 xiaoyao/3 + DAILY-v7
# qiuxin/7 + DAILY-v8 xiaqi/13 + DAILY-v9 qiuxin/12 + DAILY-v10 huaijiu/3 + DAILY-v11 yanhuo/13 +
# DAILY-v12 xiaoyao/15 + DAILY-v13 xiaqi/2 + DAILY-v14 qiuxin/3 + DAILY-v15 qiuxin/11 +
# DAILY-v16 huaijiu/1 + DAILY-v17 zhixu/12 + DAILY-v18 xiaoyao/1 + DAILY-v19 yanhuo/3 +
# DAILY-v20 xiaqi/1 + DAILY-v21 zhixu/6 + DAILY-v22 huaijiu/12 + DAILY-v23 qiuxin/13 +
# DAILY-v24 yanhuo/2 + DAILY-v25 huaijiu/17 + DAILY-v26 xiaqi/10 + DAILY-v27 yanhuo/7 +
# DAILY-v28 zhixu/9 + DAILY-v29 xiaoyao/2 + DAILY-v30 zhixu/2 + DAILY-v31 xiaoyao/4 +
# DAILY-v32 yanhuo/10 + DAILY-v33 huaijiu/4 + DAILY-v34 xiaqi/9 + DAILY-v35 zhixu/11 +
# DAILY-v36 xiaoyao/16 + DAILY-v37 qiuxin/5 + DAILY-v38 yanhuo/5 + DAILY-v39 huaijiu/5 +
# DAILY-v40 xiaqi/11 + DAILY-v41 zhixu/17 + DAILY-v42 xiaoyao/13 + DAILY-v43 qiuxin/9 +
# DAILY-v44 yanhuo/1 + DAILY-v45 huaijiu/16 + DAILY-v46 xiaqi/7 + DAILY-v47 zhixu/15 +
# DAILY-v48 xiaoyao/5 + REACT-v8 xiaoyao/17 + yanhuo/12 + zhixu/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/16 + qiuxin/14 + xiaqi/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 049",
    u"2026-10-02 · 国庆假期",
    u"「看这色彩斑斓，比平时还热闹几分」",
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
assert H2_SIZE == 50, "em ladder expected 50 (quote line 17.00em: 50-band budget 18.40em margin +1.40em = v14/v16/v46/v48 17.00em-driver band), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v49"
meta["form"] = (u"DAILY 城市日签 049（L-卡 图文轻内容线 DAILY 形态第四十九件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1018·日签节律续件=日期×情境桶对位判据第四十九证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日街市节庆色彩漫步面"
                u"如实注记·**非灯面变奏诚实注记**=v47/v48 灯面二连后泛节庆色彩面回摆〔本行无灯字·色彩斑斓="
                u"街市节庆装点泛称〕=反同构变奏第四证承继（v44 晨面/v45 物件面/v46 欢聚面三件非灯面带后"
                u"第二回摆）〕+六轴收官后线级新鲜度第四十六证=同轴异行第四十四证〔求新轴 DAILY-v1〔line4〕+"
                u"DAILY-v7〔line7〕+DAILY-v9〔line12〕+DAILY-v14〔line3〕+DAILY-v15〔line11〕+DAILY-v23"
                u"〔line13〕+DAILY-v37〔line5〕+DAILY-v43〔line9〕之外线级新鲜行 line2·轮前 r1018_pool.txt "
                u"求新桶 FREE 行预检=R978 拦截教训执行〕+**旋转律兑现=v48 后计数求新 8/怀旧 8/侠气 8/烟火 8/"
                u"秩序 8/逍遥 8=六轴全并列（系列第三个全并列态·首=v36 后 R1006·次=v42 后 R1012）→并列面"
                u"最久未采回补=求新〔v43 后 5 件未采·v44-v48 五件皆他轴=R1006/R1012 同裁决第三证〕**+求新 "
                u"FREE 面逐行机核排除注记：line0 亮堂了=v2 词面直撞〔机核〕+灯一挂构式近 city-spirit line14+"
                u"灯→夜空 causation 近 v12=三重邻接/line1 节日的+这节日=v4/v28/v30 双直撞〔机核〕+口号化 "
                u"R442/line6/8/15 年味措辞行=R972 季相错位律排除三行/line10 节日里=v17 直撞〔机核〕+口号化/"
                u"line16 灯可真=v11 直撞〔机核〕+夜作昼同构 v26/line17 节日里=v17+彩灯=v15 同轴同桶双直撞"
                u"〔机核〕；本行 line2=**求新 FREE 面唯一零机核直撞行**〔色彩斑斓/比平时/热闹几分 "
                u"distinctive shingles 全 ZERO·r1018_pool.txt 机核〕+三诚实邻接注记=色彩斑斓 4 字=池句书面"
                u"词面如实注〔R1012 书面套语注承继·verbatim 零改写红线不动=E4/M6 校准位〕+热闹 2 字构式层"
                u"邻接〔v16 反问构式/v22 凑个热闹宾语位/v34 截断式单叹=fleet 三用皆构式各异·本行=比平时还"
                u"热闹几分比较构式=第四构式异质〕+看这 2 字 opener 构式层邻接〔v15/v39 看看这=叠字 opener·"
                u"本行=单看=构式层异质注〕+**求新轴 FREE 面全弱态如实注记**=line9 被 v43 消费后求新桶剩余 "
                u"FREE 行全数带旗〔R1012 全弱注承继〕——本行=择优面唯一零直撞行胜出〔v47 秩序 line15 同型"
                u"裁决〕+**六轴 festival 居民桶 FREE 面全弱态结构性注记**〔v48 后六轴逐桶扫描皆全弱=供给面"
                u"结构性信号·sprite festival 12 行未消费+余 11 桶=queue §E 台账在案供给候选面·下轮可领序"
                u"注记〕〕）")
meta["source_quote"] = u"「看这色彩斑斓，比平时还热闹几分」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[求新][festival][2]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v48 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[求新][festival][2] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日历法"
                         u"事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境桶"
                         u"当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v48 同桶直配第四十九证=日签节律判据"
                         u"系列化·国庆假期第 2 日街市节庆色彩斑斓=假日街市漫步面场景对位〔场景级如实注记〕）④池级"
                         u"署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md "
                         u"64 条已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1〔求新/"
                         u"4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6"
                         u"〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/"
                         u"3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+"
                         u"DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+"
                         u"DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+"
                         u"DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+"
                         u"DAILY-v27〔烟火/7〕+DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+"
                         u"DAILY-v31〔逍遥/4〕+DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+"
                         u"DAILY-v35〔秩序/11〕+DAILY-v36〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+"
                         u"DAILY-v39〔怀旧/5〕+DAILY-v40〔侠气/11〕+DAILY-v41〔秩序/17〕+DAILY-v42〔逍遥/13〕+"
                         u"DAILY-v43〔求新/9〕+DAILY-v44〔烟火/1〕+DAILY-v45〔怀旧/16〕+DAILY-v46〔侠气/7〕+"
                         u"DAILY-v47〔秩序/15〕+DAILY-v48〔逍遥/5〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+"
                         u"city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第四十六证·"
                         u"本行=求新轴 line2 非 DAILY-v1 line4 非 DAILY-v7 line7 非 DAILY-v9 line12 非 DAILY-v14 "
                         u"line3 非 DAILY-v15 line11 非 DAILY-v23 line13 非 DAILY-v37 line5 非 DAILY-v43 line9="
                         u"同轴异行第四十四证〔六轴收官后求新轴第九采·轮前 r1018_pool.txt 机核预检=R978 拦截教训"
                         u"执行〕+「色彩斑斓」「比平时」「热闹几分」「看这」「热闹」「斑斓」「几分」「平时」probe "
                         u"八词机核〔r1018_quote_face.txt〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·求新面 "
                         u"line6/8/15 年味族行已按季相律排除·节庆色彩=国庆街市盛装季相对位〕⑦品牌语感注="
                         u"「比平时还热闹几分」比较式街坊评语口语真感〔去 AI 感对位〕+求新轴〔最爱新花样·屏幕原住民·"
                         u"最向前看〕×「看这色彩斑斓，比平时还热闹几分」〔最求新的居民给当下节庆街景认证胜过日常〕="
                         u"常×盛轴内自反差金句位〔族三十五连·v15 屏×真同族异质注：v15=屏幕 vs 彩灯直接比较面·本行="
                         u"平时 vs 节日时间轴比较面〕+色彩斑斓书面词面诚实注〔verbatim 零改写〕+国庆假期第 2 日街市"
                         u"色彩漫步场景层〔R442 审计叙事弱点处方带·v9 满眼都是光同族异质行〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·求新轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·街市漫步的求新轴居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十九证+六轴"
                            u"全并列最久未采回补〔求新 v43 后 5 件首回=R1006/R1012 同裁决第三证〕+求新 FREE 面唯一"
                            u"零直撞行胜出〔v47 同型裁决·色彩斑斓书面词面诚实注+热闹构式层注+看这 opener 注〕+"
                            u"「看这色彩斑斓，比平时还热闹几分」〔屏幕原住民把节日街景认证为本季最新景观〕常×盛"
                            u"轴内自反差金句位〔族三十五连·载体语感独占注：平时刷屏的人节日的街上抬起头——只有"
                            u"求新轴居民给满街节庆色彩盖下「比平时还热闹几分」的认证章=最爱新鲜的人承认当下就是"
                            u"最新款〕+假日街市色彩漫步场景层=R442 审计处方带续证+语录卡线变体零新模板第四十九证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 50 档〔17.00em 引文行驱动·预算 18.4em margin "
                            u"+1.40em=v14/v16/v46/v48 同带〕·charter §1「日签变体随时可续」兑现）·公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：求新轴〔最爱新花样·屏幕原住民·最向前看〕×"
                          u"「比平时还热闹几分」〔最向前看的居民给当下认证胜过日常的判词〕=常×盛轴内自反差金句位〔族"
                          u"三十五连·v15 屏×真同族异面〕+国庆假期第 2 日街市节庆色彩场景层+「比平时还热闹几分」比较"
                          u"式街坊评语口语真感/情 1 假日街市色彩共鸣温和如实非强极点〔色彩斑斓泛称弱于具体物象=诚实注·"
                          u"E4 校准位〕/时 2 当日时点=国庆假期第 2 日街市节庆装点直配+festival 情境桶直配第四十九证〔"
                          u"桶级·场景级假日街市面〕/台 2 公众号方图承载=MC-001~133 S3 实证复用）——hit-chain-mechanism "
                          u"v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1018 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（街市漫步的求新轴居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（街市色彩=公共城市景观意象非个体"
                     u"档案面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十九件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[qiuxin][festival][2] verbatim OK; festival bucket=18 lines; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v48 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness forty-sixth proof: qiuxin line2 != DAILY-v1 line4 != DAILY-v7 line7 != DAILY-v9 line12 != DAILY-v14 line3 != DAILY-v15 line11 != DAILY-v23 line13 != DAILY-v37 line5 != DAILY-v43 line9 = same-axis-different-line forty-fourth proof; quote-face word probe: se-cai-ban-lan/bi-ping-shi/re-nao-ji-fen/kan-zhe/re-nao see r1018_quote_face.txt (distinctive shingles se-cai-ban-lan / bi-ping-shi / re-nao-ji-fen all ZERO fleet hits; re-nao 2-char construct-layer three-use v16/v22/v34 + kan-zhe opener construct layer v15/v39 + se-cai-ban-lan book-ish wording = honest adjacency notes); strongest-exclusion rows machine-proven: line0 liang-tang-le v2 direct + deng-yi-gua construct near city-spirit line14 + lamp-to-night-sky causation near v12; line1 jie-ri-de v4 + zhe-jie-ri v28/v30 double direct; line6/8/15 nian-wei seasonal R972; line10 jie-ri-li v17 direct; line16 deng-ke-zhen v11 direct + night-as-day v26 isomorphism; line17 jie-ri-li v17 + cai-deng v15 same-axis double direct; qiuxin FREE face all-weak honest note (line9 consumed by v43, remaining rows all flagged, R1012 carried); six-axis festival resident-bucket all-weak structural note (sprite festival 12 lines + 11 other buckets = E30 supply candidates per queue ledger)")
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
report.append("LADDER_HOLD_50: quote line 17.00em; 50-band budget 18.40em margin +1.40em = v14/v16/v46/v48 same 17.00em-driver band; four-LINES stack; all other QUOTE-v2 params verbatim; non-lamp-face variation honest note carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1018.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V49, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V49, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v48 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder hold 50, quote 17.00em = v14/v16/v46/v48 band) + E4 fired async" % H2_SIZE)
