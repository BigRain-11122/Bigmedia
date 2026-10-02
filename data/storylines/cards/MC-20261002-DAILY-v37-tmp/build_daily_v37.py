# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v37 build: DAILY (city daily-sign) series THIRTY-SEVENTH piece (R1006, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-seventh same-day proof). Axis pick = qiuxin (novelty-first
residents)/festival/5: rotation law = post-v36 DAILY counts qiuxin 6 / huaijiu 6 / xiaqi 6
/ yanhuo 6 / zhixu 6 / xiaoyao 6 -> SIX-WAY TIE at 6 (first full-tie state) -> tie broken by
longest-unconsumed redemption = qiuxin last picked v23, thirteen pieces ago (v24-v36 all
other axes). Within qiuxin FREE face content-strength pick documented (weakness notes: line0
'deng yi gua qilai, yekong dou liangtang le' double adjacency [liangtang word-level repeat of
consumed v2 huaijiu line0 'zhe lao po xiao ye liangtang le' + lamp-lights-night-sky causation
scene adjacency v12 xiaoyao line15 'deng gua de zhen gao, kan dejian xingxing le'], line1
'zhe jieri de qifen, de yong denglong hongtu chulai' slogan-zero-person-zero-scene R442
weakness + jieri-qifen word-face repeat v28 zhixu line9 + hongtu bookish, line2 'kan zhe
secai banlan, bi pingshi hai renao jifen' secai-banlan bookish set-phrase + renao tail-word
adjacency v22/v34 + 'bi pingshi hai...' festival-heat comparison construction same-family as
v16 'nian na you jinnianiban renao', line9 'zhe dengchuanchuan de, jiu xiang yekong de
xingxing' dengchuan word-level near-duplicate v25 'zhe dengchuanr de you jishinian guangjing
le' + night-sky-stars scene repeat v12, line10 'jieri li, de you dianr renao de qifen'
slogan-abstract-zero-scene R442 weakness + 'jieri li' opener repeat consumed v17 zhixu
line12, line16 'zhe deng ke zhen liang, gen baizhou shide' strongest-dup face = night-as-day
construction near-duplicate of consumed v26 xiaqi line10 'jiner zhe deng duo piaoliang, gen
baitian yiyang ming', line17 'jieri li de you dian xinyi, women zai jia dian caideng'
triple adjacency ['jieri li' opener repeat v17 + caideng word-face repeat consumed v15 qiuxin
line11 same-axis-same-bucket + 'zan/wo-men' adjacency v21]; THIS line5 = qi-dai (anticipation)
slot brand-new series theme family zero prior consumption [lantern motif = qiuxin axis-native
depth band noted NOT cross-axis dup: v1 zhibojian-lantern = showcase face / v7 xiaoshihou
jiyi = backward-memory face / v14 xinseng denglong = craft-handover face / v23 shouyi
jingzhi = craft-evaluation face / THIS = variation-anticipation face = series-first 'zhao'
as craft-measure-word construction] + 'laoshu x xinzhao' axis-internal self-contrast: the
oldest festival craft x the newest forward expectation = the novelty-first resident holds
the BIGGEST renewal expectation toward the OLDEST tradition. Mild adjacency documented
honestly: 'jinnian' word also in consumed v16 [wang-x-jin] = temporal-depth family, distinct
face = THIS projects anticipation forward not memory backward; novelty vocabulary = axis
core register (same-band law as zhixu festival-praise trio v21/v28/v30 and xiaoyao 'xian'
band). This line zero fleet consumption (city-spirit NOT_IN pre-check + all cards.json scan
asserted; consumed festival lines for qiuxin axis = DAILY-v1 line4 + DAILY-v7 line7 +
DAILY-v9 line12 + DAILY-v14 line3 + DAILY-v15 line11 + DAILY-v23 line13 + REACT-v8 none-qiuxin
trio + city-spirit v1.2 qiuxin/festival/14 -> line5 fresh). Built-in tension:
今年的灯笼花样，肯定又要多出几招来 (while the nostalgic mourn the old and the rule-keepers
steady it, the novelty-first resident bets the oldest craft will out-do itself this year)
= 老俗×新招 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17
rule-x-joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady
/ v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time /
v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle / v30
dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy / v33 style-x-small / v34 yi-x-lin
/ v35 fine-x-heavy / v36 thick-x-ease
= same structural gold-sentence family, twenty-third consecutive variant). Axis-exclusive
register note: only a resident whose whole ethos is the next new thing says trust as
anticipation of MORE - the nostalgic dreads change, the order-keeper steadies it, the
ease-lover ignores it = axis-exclusive register slot. Scene layer: pre-festival lantern
market, the novelty-first resident stops at the lantern-craft stall eyeing this year's new
patterns, certain the old craft has new acts coming = concrete person-at-stall scene (R442
audit weakness prescription band; v7 backward-looking novelty sibling = axis temporal
depth pair, forward-looking half). Plain speech ('keneng bu' certainty + 'ji zhao' craft
measure word = artisan-market folk register) = anti-AI-flavor authenticity. Living-city
proof = a city that turns its oldest custom into a show with new acts every year keeps the
tradition alive = the tradition itself is alive (city humane-accumulation order echo).
Line-level freshness thirty-fourth proof = same-axis-different-line thirty-second proof.
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim;
h2_size ladder step-down 46 (quote line 19.00em over 50-band budget 18.40em -> 46 budget
20.00em margin +1.00em = v33 same-band precedent, ladder length-driven law). Machine
source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V37 = os.path.join(BASE, "MC-20261002-DAILY-v37")
TMP = V37 + "-tmp"
os.makedirs(V37, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"今年的灯笼花样，肯定又要多出几招来"
AXIS, BUCKET, IDX = u"求新", u"festival", 5

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V37:
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
# DAILY-v35 zhixu/festival/11 + DAILY-v36 xiaoyao/festival/16 + REACT-v8 xiaoyao/festival/17 +
# yanhuo/festival/12 + zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio
# zhixu/festival/16 + qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 037",
    u"2026-10-02 · 国庆假期",
    u"「今年的灯笼花样，肯定又要多出几招来」",
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
assert H2_SIZE == 46, "em ladder front-fit: quote line 19.00em over 60/50 budgets (15.33/18.40) -> step-down to 46 (budget 20.00em margin +1.00em = v33 same-band precedent, ladder length-driven law), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v37"
meta["form"] = (u"DAILY 城市日签 037（L-卡 图文轻内容线 DAILY 形态第三十七件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1006·日签节律续件=日期×情境桶对位判据第三十七证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十四证=同轴异行第三十二证〔求新轴 "
                u"DAILY-v1〔line4〕+DAILY-v7〔line7〕+DAILY-v9〔line12〕+DAILY-v14〔line3〕+DAILY-v15〔line11〕+"
                u"DAILY-v23〔line13〕之外线级新鲜行 line5·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·"
                u"旋转律兑现=v36 后计数求新 6/怀旧 6/侠气 6/烟火 6/秩序 6/逍遥 6=**六轴全并列（系列首个全并列态）"
                u"→并列面最久未采回补=求新 v23 后 13 件首回〔v24-v36 十三件皆他轴〕·并列面内容强度择优如实注记"
                u"〔求新 FREE 面弱项：line0「灯一挂起来，夜空都亮堂了」双邻接〔「亮堂」词面重复已采 v2〔怀旧 "
                u"line0「老破小也亮堂了」〕+灯→夜空 causation 场景邻接 v12〔逍遥 line15「灯挂得真高，看得见星星"
                u"了」〕〕+line1「这节日的气氛，得用灯笼烘托出来」口号化零人物零场景〔R442 弱点正中〕+「节日气氛」"
                u"词面重复 v28+「烘托」书面感+line2「色彩斑斓」书面套语+「热闹」尾词 v22/v34 邻接+「比平时还…」"
                u"节日热度比较构式 v16 同族+line9「灯串」词面近重复 v25+夜空星星场景重复 v12+line10 口号化抽象"
                u"〔R442〕+「节日里」opener 重复 v17+line16「跟白昼似的」≈v26「跟白天一样明」夜作昼面同构近重复"
                u"=最强重复面+line17 三重邻接〔「节日里」opener v17+「彩灯」词面 v15 同轴同桶+「咱」v21〕；本行="
                u"期待位系列全新主题族零前采〔灯笼 motif=求新轴本位纵深带注非跨轴重复：v1 直播间灯笼=展示面/v7 "
                u"灯笼像小时候记忆=记忆对照面/v14 新灯笼给小孙子=手艺传承面/v23 灯笼手艺精致=工艺评价面/本行="
                u"花样翻新期待面=系列首见「招」作手艺量词构式〕+「肯定又要」「多出几招」灯市行话口语真感·轻度邻接"
                u"如实注记：「今年」词面亦在已采 v16〔往×今〕=时间纵深族·异质面=本行期待向前投影非记忆向后对照·"
                u"翻新构面与轴核心词汇「最爱新花样」=轴本位纵深注〔同 v21/v28/v30 秩序轴夸节三连带律·逍遥闲字带律〕"
                u"〕〕+求新轴〔最爱新花样·最向前看·屏幕原住民的居民〕×「今年的灯笼花样，肯定又要多出几招来」"
                u"（最老的手艺年年有新看头=最爱向前看的人对最老的传统抱最大的翻新期待）=老俗×新招轴内自反差金句位"
                u"〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 "
                u"新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×"
                u"炉/v32 劳×欢/v33 派×小/v34 义×邻/v35 细×重/v36 浓×闲=族二十三连·期待位语感独占注=只有把新"
                u"东西当信仰的人才会用「肯定」对老手艺下注·念旧的怕变样·讲规矩的求稳妥·逍遥的不关心=说不出"
                u"这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「今年的灯笼花样，肯定又要多出几招来」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[求新][festival][5]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v36 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[求新][festival][5] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行长句排版=v33 同型设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v36 同桶直配第三十七证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
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
                         u"DAILY-v36〔逍遥/16〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日"
                         u"场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第三十四证·本行=求新轴 line5 非 "
                         u"DAILY-v1 line4 非 DAILY-v7 line7 非 DAILY-v9 line12 非 DAILY-v14 line3 非 DAILY-v15 "
                         u"line11 非 DAILY-v23 line13 非 city-spirit v1.2 line14=同轴异行第三十二证〔六轴收官后"
                         u"求新轴第七采·轮前 city-spirit NOT_IN 预检复证=r1006_pool_scan.txt 全桶预检 FREE 48 行="
                         u"R978 拦截教训执行·v36 行已 USED 复核〕⑥季相核=本行无「年味」措辞亦无春雨/春联类季相"
                         u"错位词（R972 制·求新面 line6/line8/line15 年味行已按季相律回避·今年/灯笼花样/几招=全季相"
                         u"公共措辞与国庆灯市场景对位）⑦品牌语感注=「肯定又要」「多出几招来」灯市行话口语真感+"
                         u"「招」作手艺量词=通感行话化收束〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+求新轴"
                         u"〔最爱新花样·最向前看〕×翻新期待〔把老手艺当年年更新的节目单〕=老俗×新招金句位（最老的"
                         u"传统遇上最大的翻新期待）+节前灯市求新轴市民驻足扎灯师傅摊前盯今年新样式=期待场景层"
                         u"=具体人物×具体动作场景面〔R442 审计叙事弱点处方带续证·v7 灯笼像小时候记忆=轴内前后向"
                         u"纵深双证注〔v7 向后看记忆面+本行向前看期待面〕·期待位=系列全新主题族零前采〕+真城生命感"
                         u"方向对位=把最老的节俗办成年年有新看头的城市=传统活着的证据〔城市人文积累令 O-20260928-1910"
                         u"对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·求新轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·看新样式的市民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十七证+六轴"
                            u"全并列最久未采回补〔求新 v23 后 13 件首回=系列最长回补距·弱项注记后本行胜出·期待位="
                            u"系列全新主题族·R442 具体人物场景处方+灯市行话口语真感双命中〕+「今年的灯笼花样，肯定"
                            u"又要多出几招来」〔最爱向前看的人对最老的传统抱最大翻新期待=老俗×新招〕老俗×新招轴内"
                            u"自反差金句位〔族二十三连·期待位语感独占注〕+期待场景层=R442 审计处方带续证+「肯定又"
                            u"要」「多出几招」灯市口语=人味命中〔CEO 审美线对位·国庆灯市场景直配〕+把最老的节俗"
                            u"办成年年有新看头的城市=传统活着的证据=城市人文积累令对位〔真城生命感〕）+语录卡线"
                            u"变体零新模板第三十七证（QUOTE-v2 参数 verbatim 复用·h2_size 梯档降 46=19.00em 行长驱动"
                            u"〔50 档预算 18.40em 不容→46 档预算 20.00em margin +1.00em=v33 同构档·R293 零余量排除+"
                            u"R301-313 梯档律〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：求新轴〔最爱新花样·最向前看·屏幕原住民的"
                          u"居民〕×翻新期待〔把老手艺当年年更新的节目单=系列首见「招」作手艺量词构式〕=老俗×新招轴内"
                          u"自反差金句位〔族二十三连·期待位语感独占注〕+节前灯市求新轴市民驻足扎灯摊前盯今年新样式="
                          u"期待场景层+「肯定又要」「多出几招」灯市行话口语真感/情 1 期待振奋明亮共鸣如实非强极点/"
                          u"时 2 当日时点=国庆假期第 2 日节前灯市看新样=求新场景当日对位+festival 情境桶直配第三"
                          u"十七证+池句期待语气常青/台 2 公众号方图承载=MC-001~121 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R1006 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（看新样式的市民=群像称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（看灯市新样=公共节俗生活面非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十七件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[qiuxin][festival][5] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v36 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-fourth proof: qiuxin line5 != DAILY-v1 line4 != DAILY-v7 line7 != DAILY-v9 line12 != DAILY-v14 line3 != DAILY-v15 line11 != DAILY-v23 line13 != city-spirit-v1.2 line14 = same-axis-different-line thirty-second proof")
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
report.append("LADDER_STEP_DOWN_46: quote line 19.00em over 60/50 budgets (15.33/18.40em) -> 46 notch budget 20.00em margin +1.00em = v33 same-band precedent (19.00em quote, step-down from 50-band, ladder length-driven law); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1006.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V37, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V37, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v36 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder step-down 46 = v33 band) + E4 fired async" % H2_SIZE)
