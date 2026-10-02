# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v43 build: DAILY (city daily-sign) series FORTY-THIRD piece (R1012, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (forty-third same-day proof). Axis pick = qiuxin (novelty-seeker,
screen-native, forward-most residents) /festival/9: rotation law = post-v42 DAILY counts
qiuxin 7 / huaijiu 7 / xiaqi 7 / yanhuo 7 / zhixu 7 / xiaoyao 7 = ALL-SIX-AXES TIED
(series SECOND all-tie state; first = post-v36 R1006) -> tie-break by longest-since-last-pick
redemption = qiuxin (first re-pick since v37; v38-v42 five pieces all other axes = longest
redemption distance in the tie; R1006 all-tie precedent same ruling = qiuxin redemption).
Within qiuxin FREE face content-strength pick documented (weakness notes: line0 'deng yi gua
qilai, yekong dou liangtang le' = 'liangtang' direct word-face repeat v2 [huaijiu/0] +
'deng yi gua' SAME-AXIS construct near line14 [qiuxin/14 pre-consumed 'zhe denglong yi gua']
= double adjacency incl. same-axis construct face; line1 'zhe jieride qifen, deiyong
denglong hongtuo chulai' = slogan-zero-scene [R442 direct hit] + 'jieri qifen' near v28 +
'dei' construct band fourth run [v28/v32/v40/v41] + 'hongtuo' bookish; line2 'kan zhe
secai banlan, bi pingshi hai renao jifen' = 'secai banlan' bookish cliche [human-warmth
loss] + 'renao' tail third use v22/v34 + comparison construct v16 family; line6 + line8 +
line15 = nian-wei seasonal wording rows -> R972 EXCLUDED three rows [R1011 xiaoyao-face
same-law four-row precedent]; line10 'jierili, dei youdianr renaode qifen' = slogan
zero-scene R442 + 'jierili' opener v17 same word-face + 'dei' band; line16 'zhe deng ke
zhen liang, gen baizhou shide' = night-as-day SAME construct v26 ['gen baitian yiyang
ming'] = strongest repeat face [R1006 note carried]; line17 'jierili dei youdian xinyi,
zanmen zai jiadian caideng' = triple adjacency ['jierili' v17 + 'caideng' SAME-AXIS
SAME-BUCKET direct repeat v15 = strongest exclusion + 'zan' v21]; THIS line9 = 'zhe
dengchuanchuande, jiu xiang yekongde xingxing' = the ONLY FREE row with ZERO same-axis
theme-word-face repeat + festival hook present (dengchuan = National-Day lamp strings) +
concrete street scene (whole-street lamp strings strung like stars) + 'chuanchuande'
reduplicated street-oral warmth = human-warmth hit; all adjacencies at cross-axis/motif/
construct level honestly noted: 'dengchuan' = v25 cross-axis near word-face [v25
dengchuan-er vs THIS dengchuanchuande = same root different construct different theme];
'xingxing' = v12 cross-axis motif family [v12 lamp-high sees-stars causation face vs THIS
lamp-strings-as-stars simile face = same family different theme]; 'yekong' = fleet
source_quote ZERO hits (r1012_quote_face.txt machine proof); 'jiuxiang' = v39 cross-axis +
city-spirit simile construct band + 'xiangjile' v7 same-axis simile CONSTRUCT-level
adjacency [construct band, same law as v18 'haoge' / v32 'yede' bands]; 'chuanchuan' =
v34 reduplication construct band [series-positive construct, v35 'zhanzhan' same law];
'zhe deng' opener = fleet-wide opener construct band [v10/v23/v25/v26/v39 = construct
level, not theme face]. Scene layer: National-Day day-2 night, the novelty-seeker walks
out to see the newly hung festival lamp strings, looks up at the whole street's strings
strung one after another like stars strung down onto the street = lamp-string
star-gazing scene layer (R442 audit weakness prescription band; v12 lamp-hung-high
sees-stars = same-family different-theme row, v12 = single-lamp look-up face, THIS =
whole-street strings face, zero prior use). Built-in tension: xin x gu axis-internal
self-contrast (v15 screen-x-real ... v42 bustle-x-dream / THIS new-x-ancient = same
structural gold-sentence family, twenty-NINTH consecutive variant; the newest people give
the city's newest festival lamps their highest praise by likening them to the oldest
stars in the sky = novelty-exclusive register slot: the nostalgic remembers, the
rule-keeper checks mounting, the bold pairs wine, the ease-lover calls it a dream - only
the novelty-seeker reaches for the sky's oldest reference = axis-exclusive register
note; same-axis depth-band second face: v7 lamp-x-memory TIME face vs THIS lamp-x-stars
SPACE face, same axis-depth-band law as v36 cha / v40 jiu / v41 jiaozhun). Living-city
proof = man-made festival beauty rated against natural stars = the city's festival
light has caught up with the sky (city humane-accumulation order echo). Line-level
freshness fortieth proof = same-axis-different-line thirty-eighth proof. Quote verbatim +
card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size stays 60
(quote line 15.00em fits 60-band budget 15.33em margin +0.33em = thinnest in-band margin
still above the 0.2em floor, R293 zero-margin exclusion NOT triggered; v42 10.40em
+4.93em same-band precedent). Machine source/dedup assertions (R456 system).
All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V43 = os.path.join(BASE, "MC-20261002-DAILY-v43")
TMP = V43 + "-tmp"
os.makedirs(V43, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"这灯串串的，就像夜空的星星"
AXIS, BUCKET, IDX = u"求新", u"festival", 9

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V43:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        assert QUOTE_CORE not in io.open(cj, encoding="utf-8").read(), "line already consumed by %s" % d
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
# DAILY-v41 zhixu/festival/17 + DAILY-v42 xiaoyao/festival/13 +
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 043",
    u"2026-10-02 · 国庆假期",
    u"「这灯串串的，就像夜空的星星」",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 15.00em fits 60-band budget 15.33em margin +0.33em (thinnest in-band margin, >=0.2em floor per R293, v42 same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v43"
meta["form"] = (u"DAILY 城市日签 043（L-卡 图文轻内容线 DAILY 形态第四十三件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1012·日签节律续件=日期×情境桶对位判据第四十三证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第四十证=同轴异行第三十八证〔求新轴 "
                u"DAILY-v1〔line4〕+DAILY-v7〔line7〕+DAILY-v9〔line12〕+DAILY-v14〔line3〕+DAILY-v15〔line11〕+"
                u"DAILY-v23〔line13〕+DAILY-v37〔line5〕之外线级新鲜行 line9·轴面 v6 收官耗尽后线级新鲜度=唯一面"
                u"〔R975 收口注承接〕·旋转律兑现=v42 后计数求新 7/怀旧 7/侠气 7/烟火 7/秩序 7/逍遥 7=**六轴全并列"
                u"（系列第二个全并列态·首个=v36 后 R1006）→并列面最久未采回补=求新〔v37 后 5 件未采·v38-v42 五件"
                u"皆他轴=并列轴中最长回补距·R1006 全并列先例同裁决=求新赎回〕·FREE 面内容强度择优如实注记〔求新 "
                u"FREE 面弱项：line0「灯一挂起来，夜空都亮堂了」=「亮堂」词面直重 v2〔怀旧/0〕+「灯一挂」同轴构式"
                u"近邻 line14〔求新/14 前采「这灯笼一挂」=同轴构式面〕=双邻接/line1「这节日的气氛，得用灯笼烘托"
                u"出来」=口号化零人物零场景〔R442 弱点正中〕+「节日气氛」词面近 v28+「得」构式带四连〔v28/v32/"
                u"v40/v41〕+「烘托」书面感/line2「看这色彩斑斓，比平时还热闹几分」=「色彩斑斓」书面套语〔人味"
                u"缺失〕+「热闹」尾词三用 v22/v34+比较构式 v16 族/line6+line8+line15=「年味儿」措辞行→R972 季相"
                u"错位排除三行〔R1011 逍遥面同律四行先例〕/line10「节日里，得有点儿热闹的气氛」=口号化零场景 "
                u"R442+「节日里」opener v17 同词面/line16「这灯可真亮，跟白昼似的」=夜作昼同构 v26〔「跟白天一样"
                u"明」〕=FREE 面最强重复面〔R1006 注记承继〕/line17「节日里得有点新意，咱们再加点彩灯」=三重邻接"
                u"〔「节日里」v17+「彩灯」同轴同桶直重 v15=最强排除+「咱」v21〕；本行 line9=「这灯串串的，就像"
                u"夜空的星星」=FREE 面唯一无同轴主题词面重复行+节日钩 ✓〔灯串=国庆灯饰季相对位〕+街景 ✓〔满街"
                u"灯串连缀如星〕+「串串的」叠词口语真感=人味命中〔CEO 审美线对位〕+全邻接皆跨轴/motif/构式层"
                u"如实注记：「灯串」=v25 跨轴词面近邻〔v25=灯串儿儿化档口面 vs 本行=灯串串叠词观星面=同词根"
                u"异构式异题族〕+「星星」=v12 跨轴 motif 族邻接〔v12=灯挂高看得见星星 causation 面 vs 本行=灯串"
                u"比星 simile 面=同族异质面〕+「夜空」=fleet source_quote 零命中〔r1012_quote_face.txt 机核〕+"
    u"「就像」=v39 跨轴+city-spirit 明喻构式带+「像极了」v7 同轴明喻构式层邻接〔构式带·v18「好个」/v32「也得」"
                u"带同律〕+「串串」=v34 叠词构式带〔系列正面构式带·v35「盏盏」同律〕+「这灯」opener=fleet 广带"
                u"构式层〔v10/v23/v25/v26/v39 同 opener 族=构式层非主题面〕〕〕）")
meta["source_quote"] = u"「这灯串串的，就像夜空的星星」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[求新][festival][9]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v42 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[求新][festival][9] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v42 同桶直配第四十三证=日签节律判据"
                         u"系列化·国庆灯饰观灯=当日对位）④池级署名=台词池行无居民名〔人设权红线零接触·charter "
                         u"§2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 cards.json 任一（build "
                         u"脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+"
                         u"DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8"
                         u"〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12"
                         u"〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16"
                         u"〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20"
                         u"〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24"
                         u"〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+DAILY-v28"
                         u"〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+DAILY-v32"
                         u"〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35〔秩序/11〕+DAILY-v36"
                         u"〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+DAILY-v39〔怀旧/5〕+DAILY-v40"
                         u"〔侠气/11〕+DAILY-v41〔秩序/17〕+DAILY-v42〔逍遥/13〕+REACT-v8 同桶三行〔逍遥/17+"
                         u"烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行="
                         u"线级新鲜度第四十证·本行=求新轴 line9 非 DAILY-v1 line4 非 DAILY-v7 line7 非 DAILY-v9 "
                         u"line12 非 DAILY-v14 line3 非 DAILY-v15 line11 非 DAILY-v23 line13 非 DAILY-v37 line5="
                         u"同轴异行第三十八证〔六轴收官后求新轴第八采·轮前 r1012_pool.txt 求新桶 FREE 行预检="
                         u"R978 拦截教训执行·v37 行已 USED 复核〕+「夜空」=fleet source_quote 零词邻+「灯串」"
                         u"「星星」「就像」「串串」=跨轴/motif/构式层词面预检〔r1012_quote_face.txt 实证="
                         u"source_quote 级词面预检 R1010/R1011 面承继〕⑥季相核=本行无「年味」措辞亦无春联/春雨类"
                         u"季相错位词〔R972 制·求新面 line6/8/15 年味行已按季相律排除·灯串=全季相公共节日灯饰"
                         u"措辞与国庆时点对位〕⑦品牌语感注=「串串的」叠词口语〔v34 串串门/v35 盏盏 叠词带同律〕"
                         u"=观灯人抬头脱口而出的市井真感〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+求新轴"
                         u"〔最爱新花样·屏幕原住民·最向前看〕×这灯串串的就像夜空的星星〔把人间新灯比作天上"
                         u"最旧的星〕=新×古金句位+国庆假期第 2 日夜求新居民出门看新挂节日灯串抬头看满街灯串连缀"
                         u"如星=灯串观星场景层〔R442 审计叙事弱点处方带续证·v12 灯挂得高看得见星星=同族异质行·"
                         u"v12=仰望单灯面 vs 本行=满街灯串连缀面〕+真城生命感方向对位=最爱新的人群给城市人造"
                         u"节日灯饰的最高赞美是自然星空=城市的人造节日美追平了自然〔城市人文积累令 O-20260928-1910"
                         u"对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·求新轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·出门看灯串的求新居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十三证+六轴全并列"
                            u"并列面最久未采回补=求新赎回〔系列第二个全并列态·R1006 先例同裁决〕+弱项注记后本行胜出"
                            u"〔FREE 面唯一无同轴主题词面重复行+全邻接跨轴/motif/构式层如实注记〕+「这灯串串的，"
                            u"就像夜空的星星」〔把人间新灯比作天上最旧的星=新×古〕新×古轴内自反差金句位〔族二十九连·"
                            u"语感独占注〕+灯串观星场景层=R442 审计处方带续证+「串串的」叠词口语=人味命中〔CEO 审美线"
                            u"对位·国庆假期语境直配·城市的人造节日美追平自然星空=追新人真感面〕+最爱新的人群把最高"
                            u"赞美给最旧的星=城市人文积累令对位〔真城生命感〕）+语录卡线变体零新模板第四十三证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 60=零模板默认档直配〔15.00em 引文行入 60 档"
                            u"预算 15.33em margin +0.33em=带内最薄余量档·≥0.2em 地板律内·R293 零余量排除线不触发·"
                            u"v42 同档先例 10.40em +4.93em 对照〕·charter §1「日签变体随时可续」兑现）·公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：求新轴〔最爱新花样·屏幕原住民·最向前看的居民〕×"
                          u"这灯串串的就像夜空的星星〔最爱新的人群给节日新灯的最高赞美是把它比作天上最旧的星星〕="
                          u"新×古轴内自反差金句位〔族二十九连·语感独占注〕+国庆假期第 2 日夜出门看新挂灯串抬头看"
                          u"满街灯串连缀如星=灯串观星场景层+「串串的」叠词口语真感/情 1 节日观灯温和共鸣如实非强"
                          u"极点/时 2 当日时点=国庆假期第 2 日夜灯饰直配+festival 情境桶直配第四十三证+池句观景"
                          u"语气常青/台 2 公众号方图承载=MC-001~127 S3 实证复用）——hit-chain-mechanism v1.0 "
                          u"§2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1012 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（出门看灯串的求新居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（灯串星星=城市公共灯景意象非个体"
                     u"档案面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十三件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[qiuxin][festival][9] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v42 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness fortieth proof: qiuxin line9 != DAILY-v1 line4 != DAILY-v7 line7 != DAILY-v9 line12 != DAILY-v14 line3 != DAILY-v15 line11 != DAILY-v23 line13 != DAILY-v37 line5 = same-axis-different-line thirty-eighth proof; quote-face word adjacency: yekong ZERO fleet source_quote hits (r1012_quote_face.txt); dengchuan=v25 cross-axis near (different construct); xingxing=v12 cross-axis motif family; jiuxiang/xiangjile simile construct band v39/v7; chuanchuan reduplication band v34")
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
report.append("LADDER_STAY_60: quote line 15.00em fits 60-band budget 15.33em margin +0.33em (thinnest in-band margin, >=0.2em floor per R293, v42 same-band precedent 10.40em +4.93em); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1012.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V43, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V43, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v42 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (zero-template default band 60) + E4 fired async" % H2_SIZE)
