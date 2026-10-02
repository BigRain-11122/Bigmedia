# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v47 build: DAILY (city daily-sign) series FORTY-SEVENTH piece (R1016, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival bucket
direct match (forty-seventh same-day proof, bucket-level; scene face = holiday street lantern
inspection-and-praise scene honestly noted, lamp-face RETURN after the v44/v45/v46 three-piece
non-lamp run = honest note, NOT concealed regression: the zhixu FREE non-lamp rows are ALL
law-level excluded this round). Axis pick = zhixu (order-loving, acceptance-inspection minded
residents) /festival/15: rotation law = post-v46 DAILY counts qiuxin 8 / huaijiu 8 / xiaqi 8 /
yanhuo 8 / zhixu 7 / xiaoyao 7 = TWO axes tied at minimum (zhixu/xiaoyao) -> tie-break by
longest-since-last-pick redemption = zhixu (first re-pick since v41; v42-v46 five pieces all
other axes = longest redemption distance in the tie). Within zhixu FREE face content-strength
pick documented (card-face-level law R1010 corrected scanning; r1016_quote_face.txt word-face
machine probe): line0 'deng shi yi gua, nian wei geng zu le' = nian-wei seasonal R972 (SPIRIT
hit) + deng-shi-yi-gua v21 four-char-family adjacency + lamp face; line1 'shou gui ju cai neng
rang cheng shi geng an wen' = shou-gui-ju city-spirit#47 wordface DIRECT collision (machine-
proven) + slogan zero-scene zero-holiday-hook R442; line3 'an quan di yi, jie ri ye de yan jin'
= an-quan-di-yi v35 FOUR-char direct collision (machine-proven) + bookish yan-jin; line5
'jie ri li ye yao shi ke ti xing zi ji zhu yi an quan' = jie-ri-li v17 opening THREE-char
direct collision (machine-proven) + flat redundant R1004 pre-judgment + safety-theme v35
territory; line7 'jiao zhun le deng guang cai an xin, jie ri li ye de jiang jiu gui ju' =
jiao-zhun v5/v41/CENSUS-v2 TRIPLE collision (machine-proven) + an-xin REACT-v8 + jie-ri-li
v17 + lamp face; line8 'gua deng long zhen xi qing, nian weir le zu le' = nian-wei seasonal
R972 + xi-qing v19 adjacency (machine-proven) + deng-long saturation + lamp face; line10
'shou gui ju, ye shi wei cheng shi hao' = shou-gui-ju city-spirit#47 DIRECT collision +
slogan-abstract R1004 pre-judgment; line13 'yan huo qi nong le, nian cai re nao' = re-nao
FIVE-piece saturation (v16/v22/v32/v34/REACT-v8 machine-proven) + nian-cai-re-nao seasonal
R1004 honest avoidance + yan-huo-qi cross-axis wordface. THIS line15 = 'deng long gao gua
zhen xi qi' = the ONLY FREE row with ZERO direct wordface collision on its distinctive
probe words (gao-gua / zhen-xi-qi / xi-qi all ZERO fleet hits, r1016_quote_face.txt) and
ZERO seasonal wording and ZERO four-char collision. Honest notes carried: deng-long 2-char
construct-layer saturation (7 DAILY pieces + SPIRIT) = R1012 xing-xing two-char law honest
adjacency note (collocation deng-long-gao-gua itself = ZERO fleet hit, unlike the excluded
deng-long-yi-gua v21 four-char family); zhen-xi-qi adjacency to v21 xi-yang-yang / v19
xi-qing = same-family different-face honest note (xi-qi itself ZERO); lamp-face return after
three non-lamp pieces = axis-redemption constraint honest note (zhixu FREE non-lamp rows all
law-level excluded this round; the only zero-direct-collision row IS a lamp row - logged, not
concealed). Scene layer: National-Day day-2 holiday street, zhixu-axis residents walk the
street as usual, look up at the lanterns hung high all over the city, and hand out their
inspector-style verdict: zhen xi qi = lantern-inspection praise scene (R442 weakness
prescription band; v30 'hung-just-right' acceptance note = same-axis acceptance-register
depth trio v21 xi-x-wen + v30 zhuang-x-tuo + v47 gua-x-xi). Built-in tension: YAN x XI
axis-internal self-contrast (thirty-third consecutive variant): the most rule-loving
acceptance-minded residents, whose daily job is checking everything is in order, give the
festival their most emotional word of praise = the strictest verdict-giver says the warmest
word (register exclusive note: tourists say piao-liang, children shout hao-kan - only the
residents who inspect the street every day turn festivity itself into something worth an
acceptance pass). Living-city proof = a city whose order-keepers love its festivity is a
city whose rules and joy are on the same side (city humane-accumulation order echo).
Line-level freshness forty-fourth proof = same-axis-different-line forty-second proof.
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim;
h2_size ladder stays 60 (quote line 9.00em inside 60-band budget 15.33em margin +6.33em =
v21/v30 short-quote single-line band; four-LINES stack = v28 same-structure band). Machine
source/dedup assertions (R456 system, card-face level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V47 = os.path.join(BASE, "MC-20261002-DAILY-v47")
TMP = V47 + "-tmp"
os.makedirs(V47, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"灯笼高挂真喜气"
AXIS, BUCKET, IDX = u"秩序", u"festival", 15

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1016_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"灯笼", u"高挂", u"真喜气", u"喜气"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1016 quote-face word probe for candidate " + QUOTE_CORE]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
io.open(os.path.join(TMP, "r1016_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V47:
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
# DAILY-v44 yanhuo/festival/1 + DAILY-v45 huaijiu/festival/16 + DAILY-v46 xiaqi/festival/7 +
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 047",
    u"2026-10-02 · 国庆假期",
    u"「灯笼高挂真喜气」",
    u"——硅基城市台词池 · 秩序轴",
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
assert H2_SIZE == 60, "em ladder expected 60 (quote line 9.00em: 60-band budget 15.33em margin +6.33em = v21/v30 short-quote single-line band), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v47"
meta["form"] = (u"DAILY 城市日签 047（L-卡 图文轻内容线 DAILY 形态第四十七件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1016·日签节律续件=日期×情境桶对位判据第四十七证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日街面灯笼巡查验收赞叹面"
                u"如实注记·**灯面回摆诚实注记**=v44 晨面+v45 物件面+v46 欢聚面三件非灯面后灯面回摆——秩序轴 FREE "
                u"非灯面行本轮全数法级排除（年味季相 line0/8+守规矩 #47 词面直撞 line1/10+安全第一 v35 四字直撞 "
                u"line3+节日里 v17 三字直撞 line5+校准三重直撞 line7）→唯一零直撞行即灯面行=轴赎回约束下的诚实"
                u"回摆如实入账非同构倒退隐瞒·日期行「2026-10-02 · 国庆假期」承节日面〕〕+六轴收官后线级新鲜度"
                u"第四十四证=同轴异行第四十二证〔秩序轴 DAILY-v5〔line4〕+DAILY-v17〔line12〕+DAILY-v21〔line6〕+"
                u"DAILY-v28〔line9〕+DAILY-v30〔line2〕+DAILY-v35〔line11〕+DAILY-v41〔line17〕之外线级新鲜行 "
                u"line15·另 REACT-v8〔line14〕+city-spirit#47〔line16〕亦非本行·轮前 r1016 池预检=R978 拦截教训执行〕"
                u"+旋转律兑现=v46 后计数求新 8/怀旧 8/侠气 8/烟火 8/秩序 7/逍遥 7=两轴并列最少（秩序/逍遥）→并列面"
                u"最久未采回补=秩序〔v41 后 5 件未采·v42-v46 五件皆他轴=并列轴中最长回补距〕·FREE 面内容强度择优"
                u"如实注记〔秩序 FREE 面逐行机核排除：line0「灯饰一挂，年味更足了」=年味季相 R972〔SPIRIT 命中〕+"
                u"灯饰一挂 v21 四字族邻接+灯面/line1「守规矩才能让城市更安稳」=守规矩 **city-spirit#47 词面直撞**"
                u"〔机核〕+口号化零场景零节日钩 R442/line3「安全第一，节日也得严谨」=安全第一 **v35 四字直撞**"
                u"〔机核〕+严谨书面感/line5「节日里也要时刻提醒自己注意安全」=节日里 **v17 开头三字直撞**〔机核〕+"
                u"冗长语感平〔R1004 预判〕+安全主题 v35 领地/line7「校准了灯光才安心，节日里也得讲究规矩」=校准 "
                u"**v5/v41/CENSUS-v2 三重直撞**〔机核〕+安心 REACT-v8+节日里 v17+灯面/line8「挂灯笼真喜庆，年味儿"
                u"足了」=年味儿季相 R972+喜庆 v19 邻接〔机核〕+灯笼饱和+灯面/line10「守规矩，也是为城市好」=守规矩 "
                u"#47 直撞〔机核〕+口号化抽象〔R1004 预判〕/line13「烟火气浓了，年才热闹」=热闹 **五重饱和**〔v16/"
                u"v22/v32/v34/REACT-v8 机核〕+年才热闹年味族季相〔R1004 诚实回避承继〕+烟火气跨轴词面；本行 line15="
                u"「灯笼高挂真喜气」=**FREE 面唯一零直撞行**〔高挂/真喜气/喜气 probe 三词 fleet 零命中〔r1016_quote_"
                u"face.txt 机核〕+零季相词+零四字直撞〕+诚实邻接注记=灯笼 **2 字构式层饱和**〔7 件+SPIRIT·R1012 星星"
                u"两字同律=构式层注记非主题族重复·**灯笼高挂搭配本身=fleet 零命中**≠被排除的灯笼一挂 v21 四字族〕+"
                u"真喜气 vs v21 喜洋洋/v19 喜庆=**同族异面诚实邻接**〔喜气词本身 ZERO 命中〕+灯面回摆=轴赎回约束诚实"
                u"注记〔非灯面行全数法级排除后唯一零直撞行·如实入账〕〕）")
meta["source_quote"] = u"「灯笼高挂真喜气」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][festival][15]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v46 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][festival][15] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日历法"
                         u"事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境桶"
                         u"当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v46 同桶直配第四十七证=日签节律判据"
                         u"系列化·国庆假期第 2 日街面灯笼高挂=假日街面巡查验收面场景对位〔场景级如实注记：灯面"
                         u"回摆=v44/v45/v46 三件非灯面后秩序轴约束下诚实回摆〕）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 "
                         u"lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/"
                         u"13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+"
                         u"DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+"
                         u"DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35〔秩序/11〕+"
                         u"DAILY-v36〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+DAILY-v39〔怀旧/5〕+"
                         u"DAILY-v40〔侠气/11〕+DAILY-v41〔秩序/17〕+DAILY-v42〔逍遥/13〕+DAILY-v43〔求新/9〕+"
                         u"DAILY-v44〔烟火/1〕+DAILY-v45〔怀旧/16〕+DAILY-v46〔侠气/7〕+REACT-v8 同桶三行〔逍遥/17+"
                         u"烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级"
                         u"新鲜度第四十四证·本行=秩序轴 line15 非 DAILY-v5 line4 非 DAILY-v17 line12 非 DAILY-v21 "
                         u"line6 非 DAILY-v28 line9 非 DAILY-v30 line2 非 DAILY-v35 line11 非 DAILY-v41 line17 非 "
                         u"REACT-v8 line14 非 city-spirit#47 line16=同轴异行第四十二证〔六轴收官后秩序轴第八采·轮前"
                         u"池预检=R978 拦截教训执行〕+「灯笼」「高挂」「真喜气」「喜气」probe 四词机核〔r1016_quote_"
                         u"face.txt〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·秩序面 line0/8/13 年味族行已"
                         u"按季相律排除·灯笼=国庆红旗红灯笼城市盛装季相对位·v21 先例〕⑦品牌语感注=「真喜气」验收式"
                         u"赞叹口语真感〔去 AI 感对位〕+秩序轴〔最讲规矩·验收思维·安全安稳第一〕×「真喜气」〔最感性"
                         u"的节日赞叹词〕=严×喜轴内自反差金句位+国庆假期第 2 日街面灯笼巡查验收场景层〔R442 审计"
                         u"叙事弱点处方带·v30 同族异质行=验收语感纵深带三连（v21 喜×稳+v30 装×妥+v47 挂×喜）〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·巡街验收的秩序轴居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十七证+两轴"
                            u"并列最少最久未采回补=秩序赎回〔v41 后 5 件首回〕+FREE 面逐行机核排除注记后本行胜出"
                            u"〔唯一零直撞行·灯笼 2 字构式层饱和诚实邻接注+真喜气同族异面注+灯面回摆=轴赎回约束"
                            u"诚实注记〕+「灯笼高挂真喜气」〔最讲规矩的验收人把最高赞词给了节日的喜庆〕严×喜轴内"
                            u"自反差金句位〔族三十三连·载体语感独占注：游客看灯说漂亮、孩子看灯喊好看——只有"
                            u"天天巡查街面的秩序轴居民，把节日的喜庆本身当成一件值得验收的事，「真喜气」三个字"
                            u"是他们盖下的验收章〕+假日街面灯笼巡查验收场景层=R442 审计处方带续证+验收语感纵深带"
                            u"三连〔v21 喜×稳+v30 装×妥+v47 挂×喜=同轴验收语感主题带〕+「真喜气」口语真感=人味"
                            u"命中〔CEO 审美线对位·城市人文积累令对位·规矩与喜庆同在一侧=城市在变好的活证据〕）"
                            u"+语录卡线变体零新模板第四十七证（QUOTE-v2 参数 verbatim 复用·h2_size 60 短句档"
                            u"〔9.00em 引文行·60 档预算 15.33em margin +6.33em=v21/v30 短句单行先例带〕·charter §1"
                            u"「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化"
                            u"合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：秩序轴〔最讲规矩·验收思维·安全安稳第一〕×"
                          u"「真喜气」〔最感性的节日赞叹词〕=严×喜轴内自反差金句位〔族三十三连〕+国庆假期第 2 日"
                          u"街面灯笼巡查验收场景层+「真喜气」验收式口语真感/情 1 假日街面温馨共鸣如实非强极点/"
                          u"时 2 当日时点=国庆假期第 2 日城市盛装面直配+festival 情境桶直配第四十七证〔桶级·场景级"
                          u"灯面回摆诚实注记〕/台 2 公众号方图承载=MC-001~131 S3 实证复用）——hit-chain-mechanism "
                          u"v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1016 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（巡街验收的秩序轴居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（街面灯笼=公共城市装点意象非个体"
                     u"档案面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十七件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[zhixu][festival][15] verbatim OK; festival bucket=18 lines; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v46 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness forty-fourth proof: zhixu line15 != DAILY-v5 line4 != DAILY-v17 line12 != DAILY-v21 line6 != DAILY-v28 line9 != DAILY-v30 line2 != DAILY-v35 line11 != DAILY-v41 line17 != REACT-v8 line14 != city-spirit#47 line16 = same-axis-different-line forty-second proof; quote-face word probe: deng-long/gao-gua/zhen-xi-qi/xi-qi see r1016_quote_face.txt (distinctive collocation words gao-gua/zhen-xi-qi/xi-qi all ZERO fleet hits; deng-long 2-char construct-layer saturation honest note per R1012 two-char law); strongest-exclusion rows machine-proven: line0 nian-wei seasonal SPIRIT + lamp; line1+10 shou-gui-ju city-spirit#47 collision; line3 an-quan-di-yi v35 four-char; line5 jie-ri-li v17 opening; line7 jiao-zhun v5/v41/CENSUS-v2 triple + an-xin REACT-v8; line8 nian-wei-r seasonal + xi-qing v19; line13 re-nao five-piece saturation + nian-cai-re-nao R1004 seasonal avoidance")
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
report.append("LADDER_STAY_60: quote line 9.00em; 60-band budget 15.33em margin +6.33em = v21/v30 short-quote single-line band; four-LINES stack; all other QUOTE-v2 params verbatim; lamp-face return honest note carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1016.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V47, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V47, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v46 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder stay 60, quote 9.00em short-line band) + E4 fired async" % H2_SIZE)
