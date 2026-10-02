# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v42 build: DAILY (city daily-sign) series FORTY-SECOND piece (R1011, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (forty-second same-day proof). Axis pick = xiaoyao (ease-lover,
idle-supreme residents) /festival/13: rotation law = post-v41 DAILY counts qiuxin 7 /
huaijiu 7 / xiaqi 7 / yanhuo 7 / zhixu 7 / xiaoyao 6 = xiaoyao UNIQUE minimum (no tie)
-> single-minimum axis redemption law direct. Within xiaoyao FREE face content-strength
pick documented (weakness notes: line0 'gua ge denglong duo xiqi, nianweir nong le' +
line6 'gua denglong le, nianweir nong le' + line8 'denghuo yi gua nianwei nong' +
line14 'denglong yi gua man, nianweir geng nong le' = nian-wei seasonal wording rows
-> R972 EXCLUDED four rows; line7 'chashi li he bei recha, xinli nuanhe' = teahouse-tea
face vs v36 'chashui pao de zheng nong, hao pin yi kou xian' = SAME axis SAME bucket
near-theme-family repeat (R1010 line7-exclusion precedent) + xinli-nuanhe near-dup
v24 = strongest exclusion in the FREE set; line5 'dengying jiaocuo ying jiangmian,
hao ge xiaoyao zizai tian' = dengying word-face same-axis v18 + jiangmian scene v6/v31
+ haoge construct v18 = triple adjacency; line9 'diaogan yi shuai le xiaoyao' +
line11 'yuer shanggou xichuwangwai' = fishing motif family repeat v6 + zero festival
hook (R1001 thin-evidence exclusion); line10 'chaxiang dengying hua sangma' =
chaxiang+dengying double word-face overlap v18 = strongest repeat face; line12
'yundan fengqing hao shijie' = yundan-fengqing direct word repeat v29 + zero festival
hook; THIS line13 = 'jiedeng ruzhi hao ge meng' = the ONLY FREE row with ZERO
same-axis word-face repeat + festival hook present (jiedeng = National-Day street
lamps) + concrete street scene (lamp-river woven like fabric) + all adjacencies at
construct/cross-axis/metaphor-family level only, honest notes: 'haoge' = v18
['chaxiang ban zhe dengying yao, haoge anyijie'] SQFACE construct-level adjacency
(fourth documented construct-band note, same law as v32/v40/v41 'yede' band);
'ruzhi' = zhi-metaphor family cross-bucket with city-spirit qiuxin/14 zhi-jin-si-bei
(metaphor family only, verbatim zero hit); 'jiedeng' contiguous word = fleet source_quote
ZERO hits (v24/v11 use 'jie shang de deng' non-contiguous = motif-level only);
'meng' = fleet zero hits (r1011_quote_face.txt machine proof). Scene layer:
National-Day day-2 night, the ease-lover strolls into the festival lamp street,
sees the whole street's lamps woven like a bolt of fabric flowing river-wise,
narrows eyes and calls it a dream = lamp-street-stroll scene layer (R442 audit
weakness prescription band; v9 walk-out-seeing-light-everywhere = same-family
different-theme row, THIS = woven-lamp-river dream-view face, zero prior use).
Built-in tension: nao x meng axis-internal self-contrast (v15 screen-x-real ... v41
zhun-x-xin / THIS bustle-x-dream = same structural gold-sentence family, twenty-EIGHTH
consecutive variant; the busiest festival spectacle becomes, in the most relaxed
resident's eyes, a dream = ease-exclusive register slot: the rule-keeper checks each
lamp, the nostalgic remembers, the novelty-seeker hunts new tricks, the bold checks
wine pairing - only the ease-lover can call the whole street a dream = axis-exclusive
register note). Living-city proof = a city whose festival street is beautiful enough
to be mistaken for a dream = the most relaxed residents are also moved = the holiday
polish reaches even those who never chase crowds (city humane-accumulation order
echo). Line-level freshness thirty-ninth proof = same-axis-different-line
thirty-seventh proof. Quote verbatim + card framing (R285 QUOTE precedent). Layout =
QUOTE-v2 params verbatim; h2_size stays 60 (quote line ~10.40em fits 60-band budget
15.33em margin ~+4.9em = zero-template default band, v38/v39/v41 same-band precedent).
Machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V42 = os.path.join(BASE, "MC-20261002-DAILY-v42")
TMP = V42 + "-tmp"
os.makedirs(V42, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"街灯如织好个梦"
AXIS, BUCKET, IDX = u"逍遥", u"festival", 13

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V42:
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
# DAILY-v41 zhixu/festival/17 +
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 042",
    u"2026-10-02 · 国庆假期",
    u"「街灯如织好个梦」",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 10.40em fits 60-band budget 15.33em margin +4.93em (zero-template default band, v38/v39/v41 same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v42"
meta["form"] = (u"DAILY 城市日签 042（L-卡 图文轻内容线 DAILY 形态第四十二件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1011·日签节律续件=日期×情境桶对位判据第四十二证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十九证=同轴异行第三十七证〔逍遥轴 "
                u"DAILY-v6〔line3〕+DAILY-v12〔line15〕+DAILY-v18〔line1〕+DAILY-v29〔line2〕+DAILY-v31〔line4〕+"
                u"DAILY-v36〔line16〕之外线级新鲜行 line13·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·"
                u"旋转律兑现=v41 后计数求新 7/怀旧 7/侠气 7/烟火 7/秩序 7/逍遥 6=**逍遥唯一最少（无并列）"
                u"→单最少轴轮换律直接兑现**·FREE 面内容强度择优如实注记〔逍遥 FREE 面弱项：line0「挂个灯笼多喜气，"
                u"年味儿浓了」+line6「挂灯笼了，年味儿浓了」+line8「灯火一挂年味浓」+line14「灯笼一挂满，年味儿"
                u"更浓了」=年味措辞行→R972 季相错位排除四行/line7「茶室里喝杯热茶，心里暖和」=茶室喝茶面 vs "
                u"v36「茶水泡得正浓，好品一口闲」**同轴同桶近主题族重复面**〔R1010 line7 排除先例〕+心里暖和"
                u"近 v24=FREE 面最强排除/line5「灯影交错映江面，好个逍遥自在天」=灯影词面 v18 同轴+江面场景 v6/v31+"
                u"好个构式 v18=三重邻接/line9「钓竿一甩乐逍遥」+line11「鱼儿上钩喜出望外」=垂钓 motif 族重复 v6+"
                u"零节日钩〔R1001 证据薄排除〕/line10「茶香灯影话桑麻」=茶香+灯影双词面重叠 v18=最强重复面/"
                u"line12「云淡风轻好时节」=云淡风轻词面直重 v29+零节日钩；本行 line13=「街灯如织好个梦」=FREE 面"
                u"唯一无同轴词面重复行+节日钩 ✓〔街灯=国庆灯饰季相对位〕+街景 ✓〔灯河如织绵延〕+全邻接皆构式/"
                u"跨轴/喻族层如实注记：「好个」=v18「好个安逸节」SQFACE 构式层邻接〔构式带第二现·「也得」带三连"
                u"〔v32/v40/v41〕同律〕+「如织」=织喻族跨桶邻接 city-spirit 求新/14 织金丝被〔喻族层·verbatim 零命中〕"
                u"+「街灯」连续词=fleet source_quote 零词邻〔v24/v11 用「街上的灯」非连续街灯=motif 层邻接〕+「梦」"
                u"=fleet 零词邻〔r1011_quote_face.txt 实证〕〕〕+逍遥轴〔最松弛·闲适至上·把节日也过成日常的居民〕×"
                u"「街灯如织好个梦」（最闲的人把满城最热闹的节日灯街看成一场好梦）=闹×梦轴内自反差金句位"
                u"〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/"
                u"v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉/v32 劳×欢/"
                u"v33 派×小/v34 义×邻/v35 细×重/v36 浓×闲/v37 老俗×新招/v38 闹×思/v39 今×昔/v40 酒×灯/v41 准×心/"
                u"本行 闹×梦=族二十八连·配位语感独占注=只有把闲看得比什么都重的人才会把整条街的灯说成一场梦"
                u"·求新的看灯看新花样·念旧的看灯看当年·秩序的看灯查挂得妥不妥当·侠气的看灯配不配酒香=说不出这句"
                u"=轴语感独占位〕〕）")
meta["source_quote"] = u"「街灯如织好个梦」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][festival][13]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v41 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][festival][13] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v41 同桶直配第四十二证=日签节律判据"
                         u"系列化·国庆灯街漫步=当日对位）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕"
                         u"⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 cards.json 任一（build 脚本 fleet "
                         u"级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+"
                         u"DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9"
                         u"〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13"
                         u"〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17"
                         u"〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+DAILY-v21"
                         u"〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+DAILY-v25"
                         u"〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+DAILY-v28〔秩序/9〕+DAILY-v29"
                         u"〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+DAILY-v32〔烟火/10〕+DAILY-v33"
                         u"〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35〔秩序/11〕+DAILY-v36〔逍遥/16〕+DAILY-v37"
                         u"〔求新/5〕+DAILY-v38〔烟火/5〕+DAILY-v39〔怀旧/5〕+DAILY-v40〔侠气/11〕+DAILY-v41"
                         u"〔秩序/17〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行"
                         u"〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第三十九证·本行=逍遥轴 line13 非 DAILY-v6 "
                         u"line3 非 DAILY-v12 line15 非 DAILY-v18 line1 非 DAILY-v29 line2 非 DAILY-v31 line4 非 "
                         u"DAILY-v36 line16 非 REACT-v8 line17=同轴异行第三十七证〔六轴收官后逍遥轴第七采·轮前 "
                         u"r1011_pool.txt 逍遥桶 FREE 行预检=R978 拦截教训执行·v36 行已 USED 复核〕+「好个」=v18 "
                         u"SQFACE 构式层词邻+「如织」「街灯」「梦」=fleet source_quote 零词邻〔r1011_quote_face.txt "
                         u"实证=source_quote 级词面预检 R1010 面承继〕⑥季相核=本行无「年味」措辞亦无春联/春雨类"
                         u"季相错位词〔R972 制·逍遥面 line0/6/8/14 年味行已按季相律排除·街灯如织=全季相公共节日"
                         u"灯街措辞与国庆时点对位〕⑦品牌语感注=「好个梦」截断式单叹口语〔v34「热闹」截断式收尾"
                         u"同构〕=闲人眯眼叹一声的市井真感〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+"
                         u"逍遥轴〔最松弛·闲适至上〕×街灯如织好个梦〔把节日盛装看成梦〕=闹×梦金句位+国庆假期第 2 日"
                         u"夜里逍遥居民散步进节日灯街看满街街灯如织连成灯河眯眼说好个梦=灯街漫步场景层〔R442 审计"
                         u"叙事弱点处方带续证·v9 散步满眼是光=同族异质行·本行=织灯河梦景面全新主题族零前采〕+真城"
                         u"生命感方向对位=最闲的人也被节日灯街美得说成梦=城市的节日连不凑热闹的人也打动〔城市人文"
                         u"积累令 O-20260928-1910 对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·散步进灯街的逍遥居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十二证+单最少轴"
                            u"轮换律直接兑现〔逍遥唯一最少 6 采无并列·弱项注记后本行胜出·FREE 面唯一无同轴词面重复行"
                            u"+全邻接构式/跨轴/喻族层如实注记〕+「街灯如织好个梦」〔把满城最热闹的节日灯街看成一场"
                            u"好梦=闹×梦〕闹×梦轴内自反差金句位〔族二十八连·配位语感独占注〕+灯街漫步场景层=R442 审计"
                            u"处方带续证+「好个梦」截断式单叹口语=人味命中〔CEO 审美线对位·国庆假期语境直配·城市的"
                            u"节日美得像梦=闲人真感面〕+最闲的人也被节日打动=城市人文积累令对位〔真城生命感〕）+"
                            u"语录卡线变体零新模板第四十二证（QUOTE-v2 参数 verbatim 复用·h2_size 60=零模板默认档"
                            u"直配〔10.40em 引文行入 60 档预算 15.33em margin +4.93em=v38/v39/v41 同档先例〕·"
                            u"charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 "
                            u"自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：逍遥轴〔最松弛·闲适至上·把节日也过成日常的"
                          u"居民〕×街灯如织好个梦〔最闲的人把最热闹的节日灯街看成一场梦〕=闹×梦轴内自反差金句位"
                          u"〔族二十八连·配位语感独占注〕+国庆假期第 2 日夜里灯街漫步看满街街灯如织连成灯河=灯街"
                          u"漫步场景层+「好个梦」截断式单叹口语真感/情 1 节日闲适温和共鸣如实非强极点/时 2 当日"
                          u"时点=国庆假期第 2 日夜灯街直配+festival 情境桶直配第四十二证+池句闲叹语气常青/台 2 公众"
                          u"号方图承载=MC-001~126 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1011 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（散步进灯街的逍遥居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（街灯如织=城市公共灯景意象非个体"
                     u"档案面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十二件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][festival][13] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v41 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-ninth proof: xiaoyao line13 != DAILY-v6 line3 != DAILY-v12 line15 != DAILY-v18 line1 != DAILY-v29 line2 != DAILY-v31 line4 != DAILY-v36 line16 != REACT-v8 line17 = same-axis-different-line thirty-seventh proof; quote-face word adjacency: haoge=v18 SQFACE construct-level (documented), ruzhi/jiedeng/meng ZERO fleet source_quote hits (r1011_quote_face.txt)")
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
report.append("LADDER_STAY_60: quote line 10.40em fits 60-band budget 15.33em margin +4.93em (zero-template default band, v38/v39/v41 same-band precedent); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1011.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V42, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V42, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v41 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (zero-template default band 60) + E4 fired async" % H2_SIZE)
