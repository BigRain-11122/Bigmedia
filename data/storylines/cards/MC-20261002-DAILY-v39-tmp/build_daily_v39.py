# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v39 build: DAILY (city daily-sign) series THIRTY-NINTH piece (R1008, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-ninth same-day proof). Axis pick = huaijiu (nostalgic residents)
/festival/5: rotation law = post-v38 DAILY counts qiuxin 7 / huaijiu 6 / xiaqi 6 / yanhuo 7
/ zhixu 6 / xiaoyao 6 -> FOUR-WAY TIE at 6 (huaijiu/xiaqi/zhixu/xiaoyao) -> tie broken by
longest-unconsumed redemption = huaijiu last picked v33, six pieces ago (v34-v38 five pieces
all other axes) = longest gap among tied axes -> huaijiu redemption due. Within huaijiu FREE
face content-strength pick documented (weakness notes: line6 'deng yi Gua qi lai, nianweir
jiu zu le' + line8 'gua shang denglong, nianweir jiu zu le' + line13 'nian nian gua deng,
nian nian you yu' + line15 'denglong yi Gua nianwei nong' = nian-wei/new-year-blessing
wording rows -> R972 seasonal-misalignment EXCLUDED four rows; line7 'jiu san shang na pa
you ge xiao po dong, ye zhe de zhu chunyu' = chun-yu spring-rain seasonal mismatch + umbrella
theme-family near-dup v22 [xiu-san-pu umbrella-repair shop row] = double exclusion; line10
'kan zhe hong tong tong de, xinli ye nuanhuo le' heart-warm word-face DIRECT near-dup v24
['jie shang de deng yi liang, xinli tou ye nuanhuo le'] = lamp->heart-warm causation
strongest-dup face; line14 'zhe jieri deng yi Gua, ganjue rizi you tashi le jifen'
lamp-hang-x-life-steady causation same-structure v21 ['gua shang denglong xiyangyang, an
zhe rizi guo de wendang'] = strongest same-structure face; line2 'xiu san de shouyi huor,
rujin ke zhen shi shao le' umbrella theme-family direct near-dup v22 + shouyi-huor word-face
v23 = double adjacency; line9 'zhe bu deng de shouyi, chuan le ji beizi' shouyi word-face
v23 family + generational-passing face near v14 [make lanterns for grandson] = double
adjacency; line11 'jide lao dang'an li xie de gua deng xisu' archive theme-family near-dup
v10 [dang'anguan archive row] + slogan-zero-person-zero-scene R442 weakness; line16
'lao wu jian li cang zhe gushi' slogan-short-zero-scene R442 direct + old-object face near
v25 lamp-string-decades family; THIS line5 = denghuo x hui-dao-cong-qian = the nostalgia
axis's MOST-native register (today's lamps become a door back to the past) + festival hook
strong (denghuo in-row = 39th day-context proof) + mild adjacency documented honestly:
'kan kan zhe' opener word-face family v15 [qiuxin line11 'kan kan zhe cai deng' same opener
different construction different axis] + time-depth band v16/v25 same-family distinct-face
note [v16 = past-x-present judging face, v25 = lamp-string living-archive face, THIS =
immersive-return face = nostalgia-x-time third distinct face] + gaze-face scene weaker than
v38 stove scene (R442 honest note, absorption slot = series context). Built-in tension:
看看这灯火，就像回到了从前 (while the whole city's lamp-sea burns at its brightest NOW,
the most past-facing resident looks at the glow and is carried all the way back THEN)
= jin x xi axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17
rule-x-joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady
/ v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time /
v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle /
v30 dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy / v33 style-x-small / v34
yi-x-lin / v35 fine-x-heavy / v36 thick-x-ease / v37 old-custom-x-new-trick / v38
bustle-x-longing = same structural gold-sentence family, twenty-FIFTH consecutive variant;
v16 note = judging-comparison face vs THIS immersive-return face = same band distinct
faces). Axis-exclusive register note: only the resident whose heart lives most in the past
would read tonight's whole lamp-sea as a road back - the novelty-lover looks at lamps for
new tricks, the crowd-lover looks at lamps for the warm crowd, the order-keeper looks at
lamps for proper hanging = cannot say this line = axis-exclusive register slot. Scene
layer: National-Day day-2 night, whole-city lamp-sea, the nostalgic resident standing at the
street corner gazing at the lights, suddenly back in the old days = gaze-x-memory scene
layer (R442 audit weakness prescription band; v7 childhood-memory + v16 old-lamp-festival =
time-depth band sibling rows). Plain speech ('kan kan zhe... jiu xiang hui dao le cong qian'
folk sigh register) = anti-AI-flavor authenticity. Living-city proof = the city that
changes fastest still keeps, for its most past-facing resident, a road made of light
between tonight and the old days (city humane-accumulation order echo). Line-level
freshness thirty-sixth proof = same-axis-different-line thirty-fourth proof. Quote verbatim
+ card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size 60
zero-template default (quote line 15.00em within 60-band budget 15.33em margin +0.33em,
thin-but-legal notch >= 0.2em margin rule). Machine source/dedup assertions (R456 system).
All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V39 = os.path.join(BASE, "MC-20261002-DAILY-v39")
TMP = V39 + "-tmp"
os.makedirs(V39, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"看看这灯火，就像回到了从前"
AXIS, BUCKET, IDX = u"怀旧", u"festival", 5

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V39:
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
# DAILY-v38 yanhuo/festival/5 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/festival/16
# + qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 039",
    u"2026-10-02 · 国庆假期",
    u"「看看这灯火，就像回到了从前」",
    u"——硅基城市台词池 · 怀旧轴",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 15.00em within 60-band budget 15.33em margin +0.33em (thin-but-legal >=0.2em margin rule, zero-template default), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v39"
meta["form"] = (u"DAILY 城市日签 039（L-卡 图文轻内容线 DAILY 形态第三十九件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1008·日签节律续件=日期×情境桶对位判据第三十九证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十六证=同轴异行第三十四证〔怀旧轴 "
                u"DAILY-v2〔line0〕+DAILY-v10〔line3〕+DAILY-v16〔line1〕+DAILY-v22〔line12〕+DAILY-v25〔line17〕+"
                u"DAILY-v33〔line4〕之外线级新鲜行 line5·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·"
                u"旋转律兑现=v38 后计数求新 7/怀旧 6/侠气 6/烟火 7/秩序 6/逍遥 6=**四轴并列最少（怀旧/侠气/秩序/"
                u"逍遥）→并列面最久未采回补=怀旧 v33 后 6 件首回〔v34-v38 五件皆他轴=并列轴中最长回补距〕·并列面"
                u"内容强度择优如实注记〔怀旧 FREE 面弱项：line6「灯一挂起来，年味儿就足了」+line8「挂上灯笼，年味"
                u"儿就足了」+line13「年年挂灯，年年有余」+line15「灯笼一挂年味浓」=年味/过年祝福措辞行=R972 季相"
                u"错位排除四行/line7「旧伞上哪怕有个小破洞，也遮得住春雨」=春雨季相错位+伞主题族近 v22〔修伞铺〕="
                u"双拦截/line10「看这红彤彤的，心里也暖和了」心里也暖和词面直接近 v24〔街上的灯一亮，心里头也暖和"
                u"了〕=灯→心暖 causation 同构最强重复面/line14「这节日灯一挂，感觉日子又踏实了几分」挂灯×日子"
                u"踏实 causation 同构 v21〔挂上灯笼喜洋洋咱这日子过得稳当〕=同构最强面/line2「修伞的手艺活儿，"
                u"如今可真是少了」修伞主题族直接近 v22+手艺活儿词面 v23=双邻接/line9「这布灯的手艺，传了几辈子」"
                u"手艺词面 v23 族+传代面近 v14〔做灯笼给小孙子看〕=双邻接/line11「记得老档案里写的挂灯习俗」档案"
                u"主题族近 v10〔档案馆里藏着的〕+口号化零人物零场景〔R442 弱点正中〕/line16「老物件里藏着故事」"
                u"口号化短句零场景〔R442 正中〕+老物件光景面近 v25 灯串几十年族；本行=灯火×回到从前=怀旧轴最"
                u"本命寄存器〔今日之光作时光之门〕+节日钩=灯火在位=festival 对位第三十九证强+轻度邻接如实注记："
                u"「看看这」opener 词面族 v15〔求新 line11「看看这彩灯，比屏幕上的还好看」·同 opener 异构异轴〕+"
                u"时间纵深带 v16/v25 同族异质面注〔v16=往×今评断面·v25=灯串光景活档案面·本行=沉浸回溯面=怀旧×"
                u"时间纵深带第三面〕+内景凝视面=具体人物场景弱于 v38 灶前面〔R442 诚实注记·吸收位=系列语境〕〕〕"
                u"+怀旧轴〔最念旧·心里最活在过去的时光·最爱往年光景的居民〕×「看看这灯火，就像回到了从前」"
                u"（今天的灯成了回从前的路）=今×昔轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/"
                u"v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/"
                u"v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉/v32 劳×欢/v33 派×小/v34 义×邻/v35 细×重/"
                u"v36 浓×闲/v37 老俗×新招/v38 闹×思=族二十五连·v16 注=评断比较面 vs 本行沉浸回溯面=同带异质·"
                u"回溯位语感独占注=只有心里最活在过去的居民才会把今天满城的灯看成一条回从前的路·求新的看灯看"
                u"新花样·烟火的看灯看人堆的热乎·秩序的看灯看挂得妥不妥当=说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「看看这灯火，就像回到了从前」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][festival][5]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v38 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][festival][5] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v38 同桶直配第三十九证=日签节律判据"
                         u"系列化·满城灯海夜=当日对位）④池级署名=台词池行无居民名〔人设权红线零接触·charter "
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
                         u"〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+"
                         u"秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度"
                         u"第三十六证·本行=怀旧轴 line5 非 DAILY-v2 line0 非 DAILY-v10 line3 非 DAILY-v16 line1 非 "
                         u"DAILY-v22 line12 非 DAILY-v25 line17 非 DAILY-v33 line4=同轴异行第三十四证〔六轴收官后"
                         u"怀旧轴第七采·轮前 r1008_pool.txt 怀旧桶 FREE 行预检=R978 拦截教训执行·v38 行已 USED "
                         u"复核〕⑥季相核=本行无「年味」措辞亦无春联/春雨类季相错位词〔R972 制·怀旧面 line6/8/13/15 "
                         u"年味行+line7 春雨行已按季相律回避·「从前」=泛时间纵深词无季相错位〕⑦品牌语感注=「看看"
                         u"这…就像回到了从前」口语凝视+回溯构式=民间叹喟式语感〔去 AI 感/制作感双对位·CEO 趣律缺趣="
                         u"不合格对位〕+怀旧轴〔最念旧·心里最活在过去的时光〕×今日灯海〔最当下的满城之光〕=今×昔"
                         u"金句位（今天的灯成了回从前的路）+国庆假期第 2 日夜晚满城灯海念旧居民街口凝视出神=凝视×"
                         u"回忆场景层=内景凝视面〔R442 审计叙事弱点处方带续证·诚实注记=凝视面弱于 v38 灶前动作面·"
                         u"v7 小时候记忆〔求新〕+v16 往年灯节〔怀旧〕=时间纵深带同族异质行〕+真城生命感方向对位="
                         u"最念旧的居民在今天的灯海里仍能找到从前的路=城市的灯不只照亮今晚也连着来路〔城市人文积累"
                         u"令 O-20260928-1910 对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·看灯火的居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十九证+四轴"
                            u"并列最久未采回补〔怀旧 v33 后 6 件首回=并列轴中最长回补距·弱项注记后本行胜出·灯火×"
                            u"回到从前=怀旧轴最本命寄存器·R442 凝视面诚实注记〕+「看看这灯火，就像回到了从前」"
                            u"〔今天的灯成了回从前的路=今×昔〕今×昔轴内自反差金句位〔族二十五连·回溯位语感独占注〕"
                            u"+街口凝视回忆场景层=R442 审计处方带续证+「就像回到了从前」民间叹喟式口语=人味命中"
                            u"〔CEO 审美线对位·国庆灯海语境直配〕+城市的灯不只照亮今晚也连着来路=城市人文积累令"
                            u"对位〔真城生命感〕）+语录卡线变体零新模板第三十九证（QUOTE-v2 参数 verbatim 复用·"
                            u"h2_size 60 零模板默认档〔15.00em 引文行入 60 档预算 15.33em margin +0.33em=薄而合法"
                            u"正余量档·R293 零余量排除不触发〕·charter §1「日签变体随时可续」兑现）·公众号低"
                            u"创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：怀旧轴〔最念旧·心里最活在过去的时光·最爱"
                          u"往年光景的居民〕×今日灯海〔最当下的满城之光·今天的灯成了回从前的路〕=今×昔轴内自反差"
                          u"金句位〔族二十五连·回溯位语感独占注〕+国庆假期第 2 日夜晚满城灯海街口凝视出神=凝视×回忆"
                          u"场景层+「就像回到了从前」民间叹喟式口语真感/情 1 灯海怀旧温和共鸣如实非强极点/时 2 "
                          u"当日时点=国庆假期第 2 日满城灯海夜=怀旧场景当日对位+festival 情境桶直配第三十九证+"
                          u"池句回溯语气常青/台 2 公众号方图承载=MC-001~123 S3 实证复用）——hit-chain-mechanism "
                          u"v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1008 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（看灯火的居民=群像称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（看灯火忆从前=公共情感群像面非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十九件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[huaijiu][festival][5] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v38 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-sixth proof: huaijiu line5 != DAILY-v2 line0 != DAILY-v10 line3 != DAILY-v16 line1 != DAILY-v22 line12 != DAILY-v25 line17 != DAILY-v33 line4 = same-axis-different-line thirty-fourth proof")
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
report.append("LADDER_ZERO_TEMPLATE_60: quote line 15.00em within 60-band budget 15.33em margin +0.33em (thin-but-legal >=0.2em notch, zero-template default band, v2/v24/v38 same-band); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1008.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V39, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V39, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v38 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (zero-template 60 band) + E4 fired async" % H2_SIZE)
