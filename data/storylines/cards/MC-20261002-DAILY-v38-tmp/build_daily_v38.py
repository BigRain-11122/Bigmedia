# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v38 build: DAILY (city daily-sign) series THIRTY-EIGHTH piece (R1007, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-eighth same-day proof). Axis pick = yanhuo (market-fireworks
residents)/festival/5: rotation law = post-v37 DAILY counts qiuxin 7 / huaijiu 6 / xiaqi 6
/ yanhuo 6 / zhixu 6 / xiaoyao 6 -> FIVE-WAY TIE at 6 (huaijiu/xiaqi/yanhuo/zhixu/xiaoyao)
-> tie broken by longest-unconsumed redemption = yanhuo last picked v32, six pieces ago
(v33-v37 five pieces all other axes) = longest gap among tied axes -> yanhuo redemption due.
Within yanhuo FREE face content-strength pick documented (weakness notes: line1 're-teng de
doujiang peishang youtiao, yi zhengtian dou jingshen' breakfast-stall theme-family near-dup
v32 [zaodian-baozi stall-livelihood band] + ZERO festival hook = weak day-context evidence
[DAILY criterion = date x bucket direct match, no festival face = thin 38th proof], line8
'deng gua de zhen gao a, haoxiang tianshang dou kuai liang le' strongest-dup face vs consumed
v12 xiaoyao line15 'deng gua de zhen gao, kan dejian xingxing le' [same opener + lamp-height
x sky-bright causation], line9 'zhe jieri qifen, bi guonian hai renao ne' triple adjacency
[jieri-qifen word-face near v28 jieri-fenwei + renao tail-word v22/v34 + bi-guonian
comparison-construction family v16] + slogan-zero-person-zero-scene R442 weakness, line11
'caichang ayimen zhehui de duo dian dengchuan huiqu' double adjacency [caichang theme-family
near-dup v19 + dengchuan word-face v25], line15 'gua shang denglong duo xiqing a'
'gua-shang-denglong' word-face v21 + lantern-hang theme family saturated [v0/v6/v14/v21/v26]
+ slogan-ish short exclamation, line16 're-tengteng de baozi lai yi fen?' baozi word-face
DIRECT repeat v32 = strongest-dup face, line17 'zhe jieride denglong ke zhen piaoliang'
'zhe...ke zhen...' evaluation construction near-dup consumed v23 'zhe denglong ke zhen
jingzhi' = same-construction strongest face; THIS line5 = si-nian (missing-someone) slot
brand-new series theme family zero prior consumption [jia-ren x ni double-addressee
progressive construction series-first + zhu-tangyuan = kitchen-steam scene = yanhuo-qi
literal hit] + mild adjacency documented honestly: family-face v27 [v27=di-zhu exhort face
vs THIS=si-nian missing face = same family-depth band distinct faces] + tangyuan = festival
food imagery note [pool line catalogued in festival bucket = BigLife festival-general face;
National-Day long holiday = homecoming-reunion peak = missing-home universal alignment; zero
'nian-wei' wording = R972 rule passed]. Built-in tension:
煮汤圆的时候，想家人也想你 (while the whole city crowds the festival streets, the
market-fireworks resident stands at the stove with white steam rising and puts the heart into
the most private longing) = nao x si axis-internal self-contrast (v15 screen-x-real / v16
past-x-present / v17 rule-x-joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy
/ v21 joy-x-steady / v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25
new-season-x-old-time / v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain /
v29 ease-x-bustle / v30 dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy / v33
style-x-small / v34 yi-x-lin / v35 fine-x-heavy / v36 thick-x-ease / v37 old-custom-x-new-trick
= same structural gold-sentence family, twenty-fourth consecutive variant). Axis-exclusive
register note: only the resident whose whole ethos is the crowd's warmth says the tenderest
sentence alone at the stove - the nostalgic remembers, the order-keeper patrols, the
ease-lover sips tea = the crowd-lover alone turns festival heat into private longing =
axis-exclusive register slot. Scene layer: National-Day day-2 kitchen, pot of tangyuan
steaming, the market-fireworks resident stirring and thinking of family far away and a
special someone = concrete person-at-stove scene (R442 audit weakness prescription band;
v27 family exhort sibling = family band distinct faces: v27 = street exhort face, THIS =
stove-side missing face). Plain speech ('xiang jia-ren ye xiang ni' double-addressee
progressive folk register) = anti-AI-flavor authenticity. Living-city proof = a city whose
loudest crowd-lover keeps a private tenderness = the festival is not only street heat but
also home warmth (city humane-accumulation order echo). Line-level freshness thirty-fifth
proof = same-axis-different-line thirty-third proof. Quote verbatim + card framing (R285
QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size 60 zero-template default (quote
line 15.00em within 60-band budget 15.33em margin +0.33em, thin-but-legal notch >= 0.2em
margin rule). Machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V38 = os.path.join(BASE, "MC-20261002-DAILY-v38")
TMP = V38 + "-tmp"
os.makedirs(V38, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"煮汤圆的时候，想家人也想你"
AXIS, BUCKET, IDX = u"烟火", u"festival", 5

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V38:
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
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 038",
    u"2026-10-02 · 国庆假期",
    u"「煮汤圆的时候，想家人也想你」",
    u"——硅基城市台词池 · 烟火轴",
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
meta["topic"] = "MC-20261002-DAILY-v38"
meta["form"] = (u"DAILY 城市日签 038（L-卡 图文轻内容线 DAILY 形态第三十八件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1007·日签节律续件=日期×情境桶对位判据第三十八证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十五证=同轴异行第三十三证〔烟火轴 "
                u"DAILY-v4〔line4〕+DAILY-v11〔line13〕+DAILY-v19〔line3〕+DAILY-v24〔line2〕+DAILY-v27〔line7〕+"
                u"DAILY-v32〔line10〕之外线级新鲜行 line5·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·"
                u"旋转律兑现=v37 后计数求新 7/怀旧 6/侠气 6/烟火 6/秩序 6/逍遥 6=**五轴并列最少（怀旧/侠气/烟火/"
                u"秩序/逍遥）→并列面最久未采回补=烟火 v32 后 6 件首回〔v33-v37 五件皆他轴=并列轴中最长回补距〕·"
                u"并列面内容强度择优如实注记〔烟火 FREE 面弱项：line1「热腾的豆浆配上油条，一整天都精神」早点摊"
                u"主题族近重复 v32〔早点摊/包子=摊位生计带〕+零节日钩=festival 对位证据薄〔DAILY 判据=日期×情境桶"
                u"对位·无节日面=第三十八证弱〕/line8「灯挂得真高啊，好像天上都快亮了」≈v12〔逍遥 line15「灯挂得"
                u"真高，看得见星星了」〕=同 opener+灯高×天亮 causation 同构=最强重复面/line9「这节日气氛，比过年还"
                u"热闹呢」三邻接〔节日气氛词面近 v28 节日氛围+热闹尾词 v22/v34+比过年比较构式 v16 往×今族〕+口号化"
                u"零人物零场景〔R442 弱点正中〕/line11「菜场阿姨们这回得多买点灯串回去」双邻接〔菜场主题族近重复 "
                u"v19+灯串词面 v25〕/line15「挂上灯笼多喜庆啊」挂上灯笼词面 v21+灯笼一挂主题族饱和〔v0/v6/v14/"
                u"v21/v26〕+口号化短叹/line16「热腾腾的包子来一份？」包子词面直接重复 v32=最强重复面/line17「这"
                u"节日的灯笼可真漂亮」这…可真…评价构式近重复 v23〔这灯笼可真精致〕=同构最强面；本行=思念位系列"
                u"全新主题族零前采〔家人×你双落递进构式系列首见+煮汤圆=厨房蒸汽场景=烟火气字面命中〕+轻度邻接"
                u"如实注记：家人面 v27〔v27=叮嘱面 vs 本行=思念面=家人族纵深带异质面〕+汤圆=节令食物意象注"
                u"〔池行编目 festival 桶=BigLife 节日通用面·国庆长假=返乡团圆高峰=想家通用对位·无「年味」措辞="
                u"R972 制核过〕〕〕+烟火轴〔最爱往人堆里凑热闹·市井烟火气最重·菜场摊头是主场的居民〕×「煮汤圆"
                u"的时候，想家人也想你」（满城凑热闹的人把心思落在最私人的牵挂上）=闹×思轴内自反差金句位〔v15 "
                u"屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手"
                u"艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉/v32 "
                u"劳×欢/v33 派×小/v34 义×邻/v35 细×重/v36 浓×闲/v37 老俗×新招=族二十四连·思念位语感独占注=只"
                u"有把人堆的暖当信仰的人才会一个人在灶前说这句话·念旧的在心里记·讲规矩的在街上守·逍遥的在茶馆"
                u"坐=说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「煮汤圆的时候，想家人也想你」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][festival][5]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v37 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][festival][5] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v37 同桶直配第三十八证=日签节律判据"
                         u"系列化·长假想家团圆面=当日对位）④池级署名=台词池行无居民名〔人设权红线零接触·charter "
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
                         u"〔逍遥/16〕+DAILY-v37〔求新/5〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+"
                         u"city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第三十五证·"
                         u"本行=烟火轴 line5 非 DAILY-v4 line4 非 DAILY-v11 line13 非 DAILY-v19 line3 非 DAILY-v24 "
                         u"line2 非 DAILY-v27 line7 非 DAILY-v32 line10 非 REACT-v8 line12=同轴异行第三十三证〔六轴"
                         u"收官后烟火轴第七采·轮前 city-spirit NOT_IN 预检复证=R978 拦截教训执行·v37 行已 USED "
                         u"复核〕⑥季相核=本行无「年味」措辞亦无春联/春雨类季相错位词（R972 制·烟火面 line0/6/14 "
                         u"年味行已按季相律回避·汤圆=节令食物意象注：池行编目 festival 桶=BigLife 节日通用面·国庆"
                         u"长假返乡团圆高峰=想家通用对位·煮汤圆=厨房团圆面全季相公共意象）⑦品牌语感注=「想家人"
                         u"也想你」双落递进构式=家人×心上人双思念落点系列首见〔去 AI 感/制作感双对位·CEO 趣律缺趣="
                         u"不合格对位〕+烟火轴〔最爱往人堆里凑·市井烟火气最重〕×灶前思念〔把节日的热闹熬进一锅"
                         u"白汽腾腾的家常〕=闹×思金句位（最爱凑热闹的人在最私人的时刻想最私的人）+国庆假期第 2 日"
                         u"灶头煮汤圆白汽腾腾=思念场景层=具体人物×具体动作场景面〔R442 审计叙事弱点处方带续证·"
                         u"v27 家人叮嘱=家人族纵深带异质面注〔v27 街面叮嘱面+本行灶前思念面〕·思念位=系列全新主题"
                         u"族零前采〕+真城生命感方向对位=最热闹的城市装得下最私人的牵挂=城市不只养热闹也养软处"
                         u"〔城市人文积累令 O-20260928-1910 对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·煮汤圆的居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十八证+五轴"
                            u"并列最久未采回补〔烟火 v32 后 6 件首回=并列轴中最长回补距·弱项注记后本行胜出·"
                            u"思念位=系列全新主题族·R442 具体人物场景处方+双落递进口语真感双命中〕+「煮汤圆的"
                            u"时候，想家人也想你」〔最爱凑热闹的人在最私人的时刻想最私的人=闹×思〕闹×思轴内"
                            u"自反差金句位〔族二十四连·思念位语感独占注〕+灶前思念场景层=R442 审计处方带续证+"
                            u"「想家人也想你」双落递进口语=人味命中〔CEO 审美线对位·国庆长假想家语境直配·烟火"
                            u"气字面命中〕+最热闹的城市装得下最私人的牵挂=城市不只养热闹也养软处=城市人文积累"
                            u"令对位〔真城生命感〕）+语录卡线变体零新模板第三十八证（QUOTE-v2 参数 verbatim 复用·"
                            u"h2_size 60 零模板默认档〔15.00em 引文行入 60 档预算 15.33em margin +0.33em=薄而合法"
                            u"正余量档·R293 零余量排除不触发〕·charter §1「日签变体随时可续」兑现）·公众号低"
                            u"创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：烟火轴〔最爱往人堆里凑热闹·市井烟火气最重·"
                          u"菜场摊头是主场〕×灶前思念〔煮一锅汤圆把节日的热闹熬成最私人的牵挂=家人×你双落递进构式"
                          u"系列首见〕=闹×思轴内自反差金句位〔族二十四连·思念位语感独占注〕+国庆假期第 2 日灶头"
                          u"煮汤圆白汽腾腾=思念场景层+「想家人也想你」双落递进口语真感/情 1 长假想家温和共鸣"
                          u"如实非强极点/时 2 当日时点=国庆假期第 2 日长假想家团圆面=烟火场景当日对位+festival "
                          u"情境桶直配第三十八证+池句思念语气常青/台 2 公众号方图承载=MC-001~122 S3 实证复用）"
                          u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·"
                          u"queue §E E30 R1007 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（煮汤圆的居民=群像称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（煮汤圆想家人=家庭生活私感面但非个体可"
                     u"识别档案面=公共情感群像口径）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十八件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][festival][5] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v37 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-fifth proof: yanhuo line5 != DAILY-v4 line4 != DAILY-v11 line13 != DAILY-v19 line3 != DAILY-v24 line2 != DAILY-v27 line7 != DAILY-v32 line10 != REACT-v8 line12 = same-axis-different-line thirty-third proof")
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
report.append("LADDER_ZERO_TEMPLATE_60: quote line 15.00em within 60-band budget 15.33em margin +0.33em (thin-but-legal >=0.2em notch, zero-template default band, v2/v24 same-band); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1007.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V38, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V38, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v37 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (zero-template 60 band) + E4 fired async" % H2_SIZE)
