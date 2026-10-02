# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v48 build: DAILY (city daily-sign) series FORTY-EIGHTH piece (R1017, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 evening -> festival
bucket direct match (forty-eighth same-day proof, bucket-level; scene face = holiday-night
riverside lantern-reflection stroll, honestly noted; lamp-face succession after the v47 lamp-face
return honestly noted: the surviving non-lamp candidate line9 lost on documented content-strength
grounds, NOT law-level exclusion). Axis pick = xiaoyao (most-relaxed, leisure-first residents)
/festival/5: rotation law = post-v47 DAILY counts qiuxin 8 / huaijiu 8 / xiaqi 8 / yanhuo 8 /
zhixu 8 / xiaoyao 7 = xiaoyao UNIQUE minimum (no tie) -> single-minimum-axis rotation law direct
 redemption = xiaoyao (first re-pick since v42; v43-v47 five pieces all other axes = longest
redemption distance). Within xiaoyao FREE face content-strength pick documented (card-face-level
law R1010; r1017_pool.txt bucket pre-check + r1017_wordface.txt 2-char machine probe): line0/6/8/
14 = nian-wei seasonal wording -> R972 seasonal law exclusion (four rows); line12 '云淡风轻好时节'
= yun-dan-feng-qing DIRECT collision with DAILY-v29 + REACT-v4 (machine-proven); line10 '茶香灯影
话桑麻' = cha-xiang + deng-ying DOUBLE direct collision with DAILY-v18 (machine-proven); line7
'茶室里喝杯热茶，心里暖和' = xin-li + nuan-he DOUBLE direct collision with DAILY-v24 (machine-
proven) + tea-room near-theme vs v36; line11 '鱼儿上钩喜出望外' = shang-gou DIRECT collision with
REACT-v4 quote (machine-proven) + fishing motif; line9 '钓竿一甩乐逍遥' = zero direct collision
BUT same-axis-same-bucket SAME THEME near-isomorphism with DAILY-v6 (闲来垂钓乐悠悠) + diao single-
char motif triple adjacency (v6/REACT-v4/SPIRIT) = documented content-strength weakness, loses.
THIS line5 = '灯影交错映江面，好个逍遥自在天' = FREE-face ZERO-direct-collision row (distinctive
collocations deng-ying-jiao-cuo / ying-jiang-mian / xiao-yao-zi-zai-tian ALL ZERO fleet hits).
Honest adjacency notes carried: deng-ying 2-char MOTIF-layer single adjacency (v18 only; same-
family-different-face: v18 = indoor tea-and-lampshadow ease scene vs this = riverside whole-vista
lamp-reflection scene; the collocation deng-ying-jiao-cuo itself = ZERO fleet hit); hao-ge 2-char
construct-layer adjacency (v18 好个安逸节 / v42 好个梦 - R1012 two-char construct-layer law);
jiang-mian = census geography-label layer (CENSUS-v16/v17 城区行, not a quote face). Built-in
tension: SHENG x XIAXIANG axis-internal self-contrast (thirty-fourth consecutive variant): the
most leisure-loving residents meet the city's grandest light spectacle and pronounce the whole
night a casual 'what a carefree world' (register exclusive note: tourists crowd the riverside
for camera spots, photographers adjust tripods - only the xiaoyao residents look at the
interlacing lantern reflections on the water and file the whole city's festive night as
ordinary good weather). Living-city proof = a city whose most at-ease residents treat its
grandest spectacle as everyday comfort is a city at peace with itself (city humane-accumulation
order echo). Line-level freshness forty-fifth proof = same-axis-different-line forty-third
proof. Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim;
h2_size ladder drops to 50 (quote line 17.00em inside 50-band budget 18.40em margin +1.40em =
v14/v16/v46 same 17.00em-driver band). Machine source/dedup assertions (R456 system, card-face
level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V48 = os.path.join(BASE, "MC-20261002-DAILY-v48")
TMP = V48 + "-tmp"
os.makedirs(V48, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"灯影交错映江面，好个逍遥自在天"
AXIS, BUCKET, IDX = u"逍遥", u"festival", 5

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1017_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"灯影", u"交错", u"映江面", u"好个", u"逍遥自在", u"自在天"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1017 quote-face word probe for candidate " + QUOTE_CORE]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: deng-ying 2-char MOTIF layer single hit (v18 indoor scene; collocation deng-ying-jiao-cuo itself ZERO); hao-ge construct layer (v18/v42); jiang-mian census geography-label layer (CENSUS-v16/v17)")
io.open(os.path.join(TMP, "r1017_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V48:
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
# REACT-v8 xiaoyao/17 + yanhuo/12 + zhixu/14 (source_facts) + city-spirit v1.2 festival-scene
# trio zhixu/16 + qiuxin/14 + xiaqi/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 048",
    u"2026-10-02 · 国庆假期",
    u"「灯影交错映江面，好个逍遥自在天」",
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
assert H2_SIZE == 50, "em ladder expected 50 (quote line 17.00em: 50-band budget 18.40em margin +1.40em = v14/v16/v46 17.00em-driver band), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v48"
meta["form"] = (u"DAILY 城市日签 048（L-卡 图文轻内容线 DAILY 形态第四十八件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1017·日签节律续件=日期×情境桶对位判据第四十八证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日夜江畔灯影漫步面"
                u"如实注记·**灯面承继诚实注记**=v47 灯面回摆后灯面承继——逍遥轴 FREE 非灯面候选 line9 存在但"
                u"内容强度弱项落选（同轴同桶同主题近同构于 v6〔闲来垂钓乐悠悠〕+钓字 motif 三重邻接）=择优面"
                u"如实入账非法级排除〕+六轴收官后线级新鲜度第四十五证=同轴异行第四十三证〔逍遥轴 DAILY-v6"
                u"〔line3〕+DAILY-v12〔line15〕+DAILY-v18〔line1〕+DAILY-v29〔line2〕+DAILY-v31〔line4〕+"
                u"DAILY-v36〔line16〕+DAILY-v42〔line13〕之外线级新鲜行 line5·另 REACT-v8〔line17〕亦非本行·"
                u"轮前 r1017_pool.txt 逍遥桶 FREE 行预检+r1017_wordface.txt 2 字词面机核=R978 拦截教训执行〕"
                u"+旋转律兑现=v47 后计数求新 8/怀旧 8/侠气 8/烟火 8/秩序 8/逍遥 7=**逍遥唯一最少（无并列）→"
                u"单最少轴轮换律直接兑现**〔v42 后 5 件未采·v43-v47 五件皆他轴=最长回补距〕+FREE 面内容强度"
                u"择优如实注记〔逍遥 FREE 面逐行机核排除：line0/6/8/14 年味措辞行=R972 季相错位律排除四行/"
                u"line12 云淡风轻=v29 词面直撞+REACT-v4 同词〔机核〕/line10 茶香+灯影=v18 双词面直撞〔机核〕/"
                u"line7 心里+暖和=v24 双词面直撞〔机核〕+茶室喝茶面近 v36/line11 上钩=REACT-v4 词面直撞〔机核〕"
                u"+垂钓 motif/line9 钓竿一甩=零直撞但同轴同桶同主题近同构 v6+钓字 motif 三重邻接=内容强度弱项"
                u"落选；本行 line5=**FREE 面零直撞行**〔灯影交错/映江面/逍遥自在天 distinctive 搭配三词全 "
                u"ZERO〕+诚实邻接注记=灯影 2 字 motif 层单邻接〔v18 茶香伴着灯影摇·同族异面：v18=室内茶香灯影"
                u"安逸面·本行=江面灯影全景自在面·**灯影交错搭配本身 fleet 零命中**〕+好个 2 字构式层邻接〔v18 "
                u"好个安逸节/v42 好个梦·R1012 两字构式层注记律〕+江面=图鉴城区行地理标签层〔CENSUS-v16/v17 "
                u"城区行「江面与光桥」·非引文面〕〕）")
meta["source_quote"] = u"「灯影交错映江面，好个逍遥自在天」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][festival][5]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v47 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][festival][5] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日历法"
                         u"事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境桶"
                         u"当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v47 同桶直配第四十八证=日签节律判据"
                         u"系列化·国庆假期第 2 日夜江畔灯影交错=假日夜江畔漫步面场景对位〔场景级如实注记〕）④池级"
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
                         u"DAILY-v47〔秩序/15〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 "
                         u"节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第四十五证·本行=逍遥轴 line5 "
                         u"非 DAILY-v6 line3 非 DAILY-v12 line15 非 DAILY-v18 line1 非 DAILY-v29 line2 非 "
                         u"DAILY-v31 line4 非 DAILY-v36 line16 非 DAILY-v42 line13 非 REACT-v8 line17=同轴异行"
                         u"第四十三证〔六轴收官后逍遥轴第八采·轮前 r1017_pool.txt+r1017_wordface.txt 机核预检="
                         u"R978 拦截教训执行〕+「灯影」「交错」「映江面」「好个」「逍遥自在」「自在天」probe 六词"
                         u"机核〔r1017_quote_face.txt〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·逍遥面 "
                         u"line0/6/8/14 年味族行已按季相律排除·灯影江面=国庆夜江畔灯景季相对位〕⑦品牌语感注="
                         u"「好个逍遥自在天」满足式松弛口语真感〔去 AI 感对位〕+逍遥轴〔最松弛·闲适至上·最会过"
                         u"日子〕×「好个逍遥自在天」〔把全城最大灯景当自家天气的判词〕=盛×闲轴内自反差金句位〔族"
                         u"三十四连·v18 闹×闲同族异面注：v18=室内茶香安逸面·本行=江天全景自在面〕+国庆假期第 2 日"
                         u"夜江畔灯影漫步场景层〔R442 审计叙事弱点处方带·v42 灯街漫步同族异质行〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·江畔漫步的逍遥轴居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十八证+单最少"
                            u"轴轮换律直接兑现〔逍遥 v42 后 5 件首回〕+FREE 面逐行机核排除注记后本行胜出〔零直撞"
                            u"行·灯影 motif 层诚实注+好个构式层注+江面地理标签层注+灯面承继诚实注〕+「灯影交错"
                            u"映江面，好个逍遥自在天」〔最会过日子的居民把全城最大灯景当自家天气〕盛×闲轴内"
                            u"自反差金句位〔族三十四连·载体语感独占注：游客挤到江边抢灯景机位、摄影爱好者调"
                            u"三脚架——只有逍遥轴居民看灯影在江面上交错，把整座城的盛装夜说成一句「好个逍遥"
                            u"自在天」=把盛景当日常的松弛本色〕+假日夜江畔灯影漫步场景层=R442 审计处方带续证+"
                            u"语录卡线变体零新模板第四十八证（QUOTE-v2 参数 verbatim 复用·h2_size 50 档〔17.00em "
                            u"引文行驱动·预算 18.4em margin +1.40em=v14/v16/v46 同带先例〕·charter §1「日签变体"
                            u"随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：逍遥轴〔最松弛·闲适至上·最会过日子〕×"
                          u"「好个逍遥自在天」〔把全城最大灯景当自家天气的判词〕=盛×闲轴内自反差金句位〔族三十四"
                          u"连·v18 闹×闲同族异面〕+国庆假期第 2 日夜江畔灯影漫步场景层+「好个逍遥自在天」满足式松弛"
                          u"口语真感/情 1 假日夜江畔松弛共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日夜江畔灯景"
                          u"直配+festival 情境桶直配第四十八证〔桶级·场景级假日夜江畔面〕/台 2 公众号方图承载="
                          u"MC-001~132 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R1017 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（江畔漫步的逍遥轴居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（江面灯影=公共城市景观意象非个体"
                     u"档案面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十八件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][festival][5] verbatim OK; festival bucket=18 lines; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v47 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness forty-fifth proof: xiaoyao line5 != DAILY-v6 line3 != DAILY-v12 line15 != DAILY-v18 line1 != DAILY-v29 line2 != DAILY-v31 line4 != DAILY-v36 line16 != DAILY-v42 line13 != REACT-v8 line17 = same-axis-different-line forty-third proof; quote-face word probe: deng-ying/jiao-cuo/ying-jiang-mian/hao-ge/xiao-yao-zi-zai/zi-zai-tian see r1017_quote_face.txt (distinctive collocations deng-ying-jiao-cuo / ying-jiang-mian / xiao-yao-zi-zai-tian all ZERO fleet hits; deng-ying 2-char motif single adjacency v18 + hao-ge construct layer v18/v42 + jiang-mian census geo-label layer = honest adjacency notes); strongest-exclusion rows machine-proven: line0/6/8/14 nian-wei seasonal R972; line12 yun-dan-feng-qing v29+REACT-v4 direct; line10 cha-xiang+deng-ying v18 double direct; line7 xin-li+nuan-he v24 double direct; line11 shang-gou REACT-v4 direct; line9 zero-direct but same-axis-same-bucket same-theme near-isomorphism v6 + diao motif triple adjacency = content-strength loser, documented")
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
report.append("LADDER_DROP_50: quote line 17.00em; 50-band budget 18.40em margin +1.40em = v14/v16/v46 same 17.00em-driver band; four-LINES stack; all other QUOTE-v2 params verbatim; lamp-face succession honest note carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1017.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V48, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V48, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v47 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder drop 50, quote 17.00em = v14/v16/v46 band) + E4 fired async" % H2_SIZE)
