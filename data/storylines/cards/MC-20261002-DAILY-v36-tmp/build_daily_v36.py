# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v36 build: DAILY (city daily-sign) series THIRTY-SIXTH piece (R1005, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-sixth same-day proof). Axis pick = xiaoyao (ease-and-leisure
residents)/festival/16: rotation law = post-v35 DAILY counts qiuxin 6 / huaijiu 6 / xiaqi 6
/ yanhuo 6 / zhixu 6 / xiaoyao 5 -> xiaoyao the UNIQUE least-consumed axis (no tie) ->
longest-unconsumed redemption = xiaoyao last picked v31, four pieces ago (v32-v35 all other
axes). Within xiaoyao FREE face content-strength pick documented (weakness notes: line5
'dengying jiaocuo ying Jiangmian, hao ge xiaoyao zizai tian' triple adjacency [deng-ying
word-level repeat of consumed v18 'chaxiang banzhe dengying yao' + Jiang-mian scene repeat
v6/v31 + 'hao ge...tian' exclamatory construction repeat v18 'hao ge anyi jie'], line7
'xinli nuanhe' near-duplicate of consumed v24 yanhuo line2 'xinlitou ye nuanhe le' + hot-tea
motif REACT-v8 'zai jia he he cha', line9 'diaogan yi shuai le xiaoyao' fishing-motif scene
duplicate of consumed v6 'xianlai chu diao', line10 'chaxiang dengying hua sangma'
chaxiang+dengying double word-level overlap with consumed v18 [strongest dup face], line11
'yu er shanggou' fishing-scene duplicate of v6 family, line12 'yundan fengqing hao shijie'
yundan-fengqing word-level repeat of consumed v29 'yundan fengqing rizichang', line13
'jiedeng ruzhi hao ge meng' weave metaphor already consumed by city-spirit qiuxin line14
'ese xiang zhi le ceng jinsi' + jiedeng motif v24/v11 adjacency + 'hao ge...meng' v18
construction family; THIS line16 = pin-xian (sipping leisure itself) slot brand-new series
theme family zero prior consumption [tea motif = axis-native register, NOT cross-axis dup:
v18 chaxiang-ban-dengying = scene face / v29 yundan-fengqing = mood face / REACT-v8 zaijia-hecha
= contrast face / THIS = tasting leisure itself = gustatory synesthesia face, series-first
construction 'xian' as tasteable object] + nong [the most concrete physical concentration]
x xian [the most abstract felt ease] = shi-xu (solid-x-void) axis-internal self-contrast
gold-sentence slot + 'pao de zheng nong' 'hao pin yi kou' teahouse-goer folk register).
Mild adjacency documented honestly: 'xian' char also in consumed v18 [nao-x-xian] and v29
[xian-x-xuan] = axis-internal theme-depth band (xiaoyao = the ease-first axis, 'xian' is its
core vocabulary; same-band law as zhixu festival-praise trio v21/v28/v30), distinct face =
THIS line turns ease from a state into the thing being tasted. This line zero fleet
consumption (city-spirit NOT_IN pre-check + all cards.json scan asserted; consumed festival
lines for xiaoyao axis = DAILY-v6 line3 + DAILY-v12 line15 + DAILY-v18 line1 + DAILY-v29
line2 + DAILY-v31 line4 + REACT-v8 line17 -> line16 fresh). Built-in tension:
茶水泡得正浓，好品一口闲 (while the whole city rushes the festival, the most at-ease
resident brews it stronger and sips the leisure itself)
= 浓×闲 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17 rule-x-joy
/ v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady / v22
old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time / v26
hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle / v30
dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy / v33 style-x-small / v34 yi-x-lin
/ v35 fine-x-heavy
= same structural gold-sentence family, twenty-second consecutive variant). Axis-exclusive
register note: only a resident whose whole ethos is sipping time slowly says leisure as
something you taste - the rule-keepers and the loyalty-keepers cannot say this line =
axis-exclusive register slot. Scene layer: National Day holiday afternoon, whole city
rushing the lamp-festival bustle, the teahouse regular with a freshly-stewed strong cup,
eyes half-closed, one unhurried sip = concrete person-at-ease scene (R442 audit weakness
prescription band; v18 tea-scene sibling noted; pin-xian slot = brand-new theme family).
Plain speech ('pao de zheng nong' + 'hao pin yi kou' = teahouse working-register
authenticity) = anti-AI-flavor authenticity. Living-city proof = the city that runs the
festival at full boil also keeps one quiet seat where leisure itself is on the menu =
the city's ease is alive (city humane-accumulation order echo). Line-level freshness
thirty-third proof = same-axis-different-line thirty-first proof. Quote verbatim + card
framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size ladder holds
notch 60 (quote line 14.00em fits 15.33em budget with +1.33em margin, four-line stack VERT
+229px = v17/v22/v34/v35 same-structure notch band; holds from v34, ladder length-driven
law). Machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V36 = os.path.join(BASE, "MC-20261002-DAILY-v36")
TMP = V36 + "-tmp"
os.makedirs(V36, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"茶水泡得正浓，好品一口闲"
AXIS, BUCKET, IDX = u"逍遥", u"festival", 16

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V36:
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
# DAILY-v35 zhixu/festival/11 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/festival/16 +
# qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 036",
    u"2026-10-02 · 国庆假期",
    u"「茶水泡得正浓，好品一口闲」",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 14.00em fits 15.33em budget at 60 with margin +1.33em (four-line stack VERT +229px = v17/v22/v34/v35 same-structure notch band; holds 60 notch from v34, ladder length-driven law), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v36"
meta["form"] = (u"DAILY 城市日签 036（L-卡 图文轻内容线 DAILY 形态第三十六件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1005·日签节律续件=日期×情境桶对位判据第三十六证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十三证=同轴异行第三十一证〔逍遥轴 "
                u"DAILY-v6〔line3〕+DAILY-v12〔line15〕+DAILY-v18〔line1〕+DAILY-v29〔line2〕+DAILY-v31〔line4〕"
                u"之外线级新鲜行 line16·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·旋转律兑现=v35 后"
                u"计数求新 6/怀旧 6/侠气 6/烟火 6/秩序 6/逍遥 5=逍遥唯一最少 5 采（无并列）→最久未采回补=逍遥"
                u"v31 后 4 件首回〔v32-v35 四件皆他轴〕·单最少轴轮换律直接兑现·并列面内容强度择优如实注记〔逍遥 "
                u"FREE 面弱项：line5「灯影交错映江面，好个安逸自在天」三重邻接〔灯影词面重复已采 v18「茶香伴着"
                u"灯影摇」+江面场景重复 v6/v31+「好个…天」感叹构式重复 v18「好个安逸节」〕+line7「心里暖和」近"
                u"重复已采 v24〔烟火 line2「心里头也暖和了」〕+热茶 motif 邻接 REACT-v8「在家喝喝茶」+line9 垂钓 "
                u"motif 场景重复已采 v6〔闲来垂钓〕+line10「茶香灯影」双词面重叠已采 v18〔最强重复面〕+line11 垂钓"
                u"场景 v6 同族+line12「云淡风轻」词面重复已采 v29〔云淡风轻日子长〕+line13「如织」织喻已被 "
                u"city-spirit 采〔求新 line14「夜色就像织了层金丝」〕+街灯 motif v24/v11 邻接+「好个…梦」v18 构式"
                u"族；本行=品闲位系列全新主题族零前采〔茶 motif=逍遥轴本位纵深带注非跨轴重复：v18 茶香伴灯影="
                u"场景面/v29 云淡风轻=心境面/REACT-v8 在家喝茶=对比面/本行=品味闲本身=通感味觉化系列首见「闲」作"
                u"物宾语构式〕+「泡得正浓」「好品一口」茶客口语真感·轻度邻接如实注记：「闲」字亦在已采 v18〔闹×"
                u"闲〕+v29〔闲×喧〕=轴内主题纵深带〔逍遥=闲适本位轴·闲字=轴核心词汇·同 v21/v28/v30 秩序轴夸节日"
                u"三连带律〕·异质面=本行把闲从状态变成品味对象〕〕〕+逍遥轴〔最松弛·闲适至上·把「闲」看得比"
                u"什么都重的居民〕×「茶水泡得正浓，好品一口闲」（满城赶节日的热闹里最松弛的人把闲当茶细细品="
                u"最浓的茶泡出最淡的日子）=浓×闲轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 "
                u"平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 "
                u"闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉/v32 劳×欢/v33 派×小/v34 义×邻/v35 细×重="
                u"族二十二连·品闲位语感独占注=只有把时间泡在茶里的人才会把闲当东西品·讲规矩的人和讲义气的人"
                u"说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「茶水泡得正浓，好品一口闲」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][festival][16]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v35 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][festival][16] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v35 同桶直配第三十六证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+"
                         u"DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35〔秩序/11〕+"
                         u"REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+"
                         u"求新/14+侠气/0〕皆非本行=线级新鲜度第三十三证·本行=逍遥轴 line16 非 DAILY-v6 line3 非 "
                         u"DAILY-v12 line15 非 DAILY-v18 line1 非 DAILY-v29 line2 非 DAILY-v31 line4 非 REACT-v8 "
                         u"line17=同轴异行第三十一证〔六轴收官后逍遥轴第六采·轮前 city-spirit NOT_IN 预检复证="
                         u"r1005_pool_scan.txt 全桶预检 FREE 49 行=R978 拦截教训执行·v35 行已 USED 复核〕⑥季相核="
                         u"本行无「年味」措辞亦无春雨/春联类季相错位词（R972 制·逍遥面 line0/line6/line8/line14 "
                         u"年味行已按季相律回避·茶水/品闲=全季相公共闲适措辞与国庆假期喝茶场景对位）⑦品牌语感注="
                         u"「泡得正浓」「好品一口」茶客口语真感+「品一口闲」=通感味觉化收束〔去 AI 感/制作感双对位·"
                         u"CEO 趣律缺趣=不合格对位〕+逍遥轴〔最松弛·闲适至上〕×品闲〔把闲当茶品〕=浓×闲金句位"
                         u"（最浓的茶泡出最淡的日子）+国庆假期满城赶热闹的午后茶馆里老茶客眯眼啜一口浓茶=品闲场景层"
                         u"=具体人物×具体动作场景面〔R442 审计叙事弱点处方带续证·v18 茶香灯影同族异质行注·品闲位="
                         u"系列全新主题族零前采〕+真城生命感方向对位=把节日开到最满档的城市也永远留得住一把慢椅"
                         u"子=城市的闲适活着的证据〔城市人文积累令 O-20260928-1910 对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·老茶客=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十六证+单最少"
                            u"轴最久未采回补〔逍遥 v31 后 4 件首回·弱项注记后本行胜出·品闲位=系列全新主题族·R442 "
                            u"具体人物场景处方+茶客口语真感双命中〕+「茶水泡得正浓，好品一口闲」〔最松弛的人把闲当"
                            u"茶品=浓×闲〕浓×闲轴内自反差金句位〔族二十二连·品闲位语感独占注〕+品闲场景层=R442 "
                            u"审计处方带续证+「泡得正浓」「好品一口」茶客口语=人味命中〔CEO 审美线对位·国庆假期"
                            u"喝茶场景直配〕+把节日开到最满档的城市也留得住一把慢椅子=城市人文积累令对位〔真城"
                            u"生命感〕）+语录卡线变体零新模板第三十六证（QUOTE-v2 参数 verbatim 复用·h2_size 梯档"
                            u"守 60=14.00em 行长驱动〔v34 60 档带后守档·60 档预算 15.33em margin +1.33em·四行栈 "
                            u"VERT +229px=v17/v22/v34/v35 同构档·R293 零余量排除+R301-313 梯档律〕·charter §1「日签"
                            u"变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：逍遥轴〔最松弛·闲适至上·把「闲」看得比什么"
                          u"都重的居民〕×品闲〔把闲当茶细细品=通感味觉化系列首见构式〕=浓×闲轴内自反差金句位〔族"
                          u"二十二连·品闲位语感独占注〕+国庆假期满城赶热闹的午后茶馆老茶客眯眼啜浓茶=品闲场景层+"
                          u"「泡得正浓」「好品一口」茶客口语真感/情 1 闲适松弛温和共鸣如实非强极点/时 2 当日时点="
                          u"国庆假期第 2 日午后茶馆闲坐=逍遥场景当日对位+festival 情境桶直配第三十六证+池句闲适"
                          u"语气常青/台 2 公众号方图承载=MC-001~120 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1005 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（老茶客=群像称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（品茶=闲适生活面非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十六件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][festival][16] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v35 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-third proof: xiaoyao line16 != DAILY-v6 line3 != DAILY-v12 line15 != DAILY-v18 line1 != DAILY-v29 line2 != DAILY-v31 line4 != REACT-v8 line17 = same-axis-different-line thirty-first proof")
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
report.append("LADDER_HOLD_60: quote line 14.00em fits 15.33em budget at 60 with margin +1.33em -> holds notch 60 (four-line stack VERT +229px = v17/v22/v34/v35 same-structure band; holds from v34, ladder length-driven law); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1005.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V36, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V36, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v35 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder holds 60 notch from v34 band) + E4 fired async" % H2_SIZE)
