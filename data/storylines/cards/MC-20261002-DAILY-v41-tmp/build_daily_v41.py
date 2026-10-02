# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v41 build: DAILY (city daily-sign) series FORTY-FIRST piece (R1010, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (forty-first same-day proof). Axis pick = zhixu (order-keeper,
calibration-native residents) /festival/17: rotation law = post-v40 DAILY counts qiuxin 7 /
huaijiu 7 / xiaqi 7 / yanhuo 7 / zhixu 6 / xiaoyao 6 -> TWO-WAY TIE at 6 (zhixu/xiaoyao) ->
tie broken by longest-unconsumed redemption = zhixu last picked v35, five pieces ago
(v36-v40 five pieces all other axes) = longest gap among tied axes (xiaoyao v36 four ago)
-> zhixu redemption due. Within zhixu FREE face content-strength pick documented
(weakness notes: line0 'dengshi yi Gua, nianwei gengzu le' + line8 'Gua denglong zhen
xiqing, nianweir zu le' = nian-wei seasonal wording rows -> R972 EXCLUDED; line13
'yanhuoqi nong le, nian cai renao' = nian-face seasonal band -> R972 EXCLUDED; line3
'anquan diyi, jieri ye de yanjie' + line5 'jieri li ye yao shike tixing ziji zhuyi anquan'
= safety-slogan zero-person-zero-scene rows (R442 weakness); line10 'shou guiju, ye shi wei
chengshi hao' = generic advice zero concrete scene; line15 'denglong gao Gua zhen xiqi' =
lantern-family saturated (v21/v26/v30 lamp-joy band) + zero scene; line7 'jiaozhun le
dengguang cai anxin, jieri li ye de jiangjiu guiju' = jiaozhun+light+anxin three-word
same-face near-dup v5 [zhixu/4 'jiaozhun hao meizhan deng, xinli cai tashi'] = SAME axis
SAME bucket near-theme-family repeat = strongest exclusion in the FREE set; THIS line17 =
'jiaozhun le shijian ye de diaohao xinqing' = zhun-xin pairing face = series-FIRST
construction (the resident who calibrates the whole city's time admits the mood needs
tuning too) + 'diao' same-hand dual-register note (jiaozhun/diaohao = technical tuning x
emotional tuning, one hand) + honest adjacency notes: 'ye de' concessive construct band
THIRD consecutive [v32 yanhuo/10 zaodian tan ye de chen renao + v40 xiaqi/11 jiuguan li de
jiuxiang ye de peishang zhe xie deng + THIS = construct-level adjacency only, three
different theme families: livelihood-riding-festival / jianghu-flavor-yields-to-lamp /
post-language-yields-to-mood]; xinqing/diaohao = zero quote-face word adjacency
(r1010_quote_face.txt fleet-wide source_quote scan NONE); jiaozhun = zhixu axis native
register axis-internal depth second face [v5 lamp-calibration face + THIS =
time-x-mood face, same law as R1005 xiaoyao 'xian' band / v40 xiaqi 'jiu' band].
Scene layer: National-Day day-2 night, the city clock-tower timekeeper calibrates the
whole city's time as usual (the city clock takes no holiday), steps down from the tower,
looks at the festival lamps newly hung along the street, and admits the mood needs
tuning too = clock-tower-timekeeping scene layer (R442 audit weakness prescription band;
v11 canteen-master + v32 breakfast-stall + v40 tavern-door = market-livelihood family,
clock-tower timekeeping = post-keeping brand-new theme family, zero prior use).
Built-in tension: zhun x xin axis-internal self-contrast (v15 screen-x-real ... v39
present-x-past / v40 wine-x-lamp / THIS precision-x-mood = same structural gold-sentence
family, twenty-SEVENTH consecutive variant). Axis-exclusive register note: only the
resident whose job is calibrating the city's time would carry the word 'diao' from the
clock to their own mood - the novelty-seeker looks at lamps for new tricks, the nostalgic
for the old days, the ease-lover as ordinary scenery, the bold for whether wine pairs well
= cannot say this line = axis-exclusive register slot. Living-city proof = even the most
precision-keeping city leaves a notch for mood-tuning = the rules grow human flavor
(city humane-accumulation order echo). Line-level freshness thirty-eighth proof =
same-axis-different-line thirty-sixth proof. Quote verbatim + card framing (R285 QUOTE
precedent). Layout = QUOTE-v2 params verbatim; h2_size stays 60 (quote line 13.00em fits
60-band budget 15.33em margin +2.33em = zero-template default band, v38/v39 same-band
precedent). Machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V41 = os.path.join(BASE, "MC-20261002-DAILY-v41")
TMP = V41 + "-tmp"
os.makedirs(V41, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"校准了时间也得调好心情"
AXIS, BUCKET, IDX = u"秩序", u"festival", 17

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V41:
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
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 041",
    u"2026-10-02 · 国庆假期",
    u"「校准了时间也得调好心情」",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 13.00em fits 60-band budget 15.33em margin +2.33em (zero-template default band, v38/v39 same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v41"
meta["form"] = (u"DAILY 城市日签 041（L-卡 图文轻内容线 DAILY 形态第四十一件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1010·日签节律续件=日期×情境桶对位判据第四十一证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十八证=同轴异行第三十六证〔秩序轴 "
                u"DAILY-v5〔line4〕+DAILY-v17〔line12〕+DAILY-v21〔line6〕+DAILY-v28〔line9〕+DAILY-v30〔line2〕+"
                u"DAILY-v35〔line11〕之外线级新鲜行 line17·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·"
                u"旋转律兑现=v40 后计数求新 7/怀旧 7/侠气 7/烟火 7/秩序 6/逍遥 6=**二轴并列最少（秩序/逍遥）"
                u"→并列面最久未采回补=秩序 v35 后 5 件首回〔v36-v40 五件皆他轴=并列轴中最长回补距·逍遥 v36 后 4 件"
                u"短于秩序〕·并列面内容强度择优如实注记〔秩序 FREE 面弱项：line0「灯饰一挂，年味更足了」+line8"
                u"「挂灯笼真喜庆，年味儿足了」=年味措辞行→R972 季相错位排除两行/line13「烟火气浓了，年才热闹」"
                u"年字面季相带→R972 排除/line3「安全第一，节日也得严谨」+line5「节日里也要时刻提醒自己注意安全」"
                u"=安全口号零人物零场景〔R442 弱点正中〕/line10「守规矩，也是为城市好」泛化劝勉零具体场景/line15"
                u"「灯笼高挂真喜气」灯笼主题族饱和〔v21/v26/v30 灯喜带〕+零人物零场景/line7「校准了灯光才安心，"
                u"节日里也得讲究规矩」校准+灯+安心三词同面近 v5〔秩序/4「校准好每盏灯，心里才踏实」=同轴同桶"
                u"近主题族重复面=FREE 面最强排除〕；本行 line17=「校准了时间也得调好心情」=准×心配位面**系列首见"
                u"构式**（把全城时间校准好的人承认心情也要调好）+「调」字同手双寄存器注=校准/调好=技术调音×情绪"
                u"调音同一只手=系列首见构式核心+诚实邻接注记：「也得」让步式构式带三连〔v32 烟火/10「早点摊也得"
                u"趁热闹」+v40 侠气/11「酒馆里的酒香，也得配上这些灯」+本行=构式层邻接非主题族重复〔v32=生计趁"
                u"热闹面/v40=江湖味道配灯面/本行=岗位语言让位心情面=异题族各面〕+心情/调好=引文面零词邻"
                u"〔r1010_quote_face.txt 实证=fleet 全 source_quote 扫描零命中〕+校准=秩序轴本命寄存器轴内主题纵深"
                u"带注〔v5 校准灯面+本行=校准时间×心情面=第二面·同 R1005 逍遥「闲」字带律/v40 侠气「酒」字带律〕+"
                u"钟台守时人=具体场景面〔R442 审计叙事弱点处方带续证·v11 食堂师傅/v32 早点摊/v40 酒馆门口=市井"
                u"生计族·钟台守时=岗位坚守族全新主题族零前采〕〕〕+秩序轴〔守规矩·重条理·逐盏校准·把城市调得"
                u"妥妥当当的居民〕×「校准了时间也得调好心情」（把全城时间校准好的人承认自己心情也得调一调）="
                u"准×心轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/"
                u"v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/"
                u"v31 舞×炉/v32 劳×欢/v33 派×小/v34 义×邻/v35 细×重/v36 浓×闲/v37 老俗×新招/v38 闹×思/v39 今×昔/"
                u"v40 酒×灯/本行 准×心=族二十七连·配位语感独占注=只有把全城时间校准好的人才会把「调」字从钟表"
                u"用到自己心情上·求新的看灯看花样·念旧的看灯看当年·逍遥的看灯看寻常·侠气的看灯看配不配酒香="
                u"说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「校准了时间也得调好心情」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][festival][17]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v40 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][festival][17] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v40 同桶直配第四十一证=日签节律判据"
                         u"系列化·节日钟台守时照常校准=当日对位）④池级署名=台词池行无居民名〔人设权红线零接触·"
                         u"charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 cards.json 任一"
                         u"（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+"
                         u"DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8"
                         u"〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12"
                         u"〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16"
                         u"〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20"
                         u"〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24"
                         u"〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+DAILY-v28"
                         u"〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+DAILY-v32"
                         u"〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35〔秩序/11〕+DAILY-v36"
                         u"〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+DAILY-v39〔怀旧/5〕+DAILY-v40"
                         u"〔侠气/11〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行"
                         u"〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第三十八证·本行=秩序轴 line17 非 DAILY-v5 "
                         u"line4 非 DAILY-v17 line12 非 DAILY-v21 line6 非 DAILY-v28 line9 非 DAILY-v30 line2 非 "
                         u"DAILY-v35 line11 非 REACT-v8 line14 非 city-spirit v1.2 line16=同轴异行第三十六证"
                         u"〔六轴收官后秩序轴第七采·轮前 r1010_pool.txt 秩序桶 FREE 行预检=R978 拦截教训执行·v35 行"
                         u"已 USED 复核〕+心情/调好=引文面零词邻〔r1010_quote_face.txt 实证〕⑥季相核=本行无「年味」"
                         u"措辞亦无春联/春雨类季相错位词〔R972 制·秩序面 line0/8/13 年味年字面行已按季相律回避·校准"
                         u"时间/调好心情=全季相公共岗位措辞与国庆假期时点对位〕⑦品牌语感注=「也得调好」让步式口语="
                         u"守时人自劝式放松的市井真感〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+秩序轴〔守"
                         u"规矩·逐盏校准·把城市调得妥妥当当〕×校准了时间也得调好心情〔岗位语言让位给人话〕=准×心"
                         u"金句位（把全城时间校准好的人承认自己心情也得调一调）+国庆假期第 2 日夜里钟台守时人照常"
                         u"校准全城时间×街上满挂节日灯=钟台守时场景层〔R442 审计叙事弱点处方带续证·v11 食堂师傅/"
                         u"v32 早点摊/v40 酒馆门口=市井生计族·钟台守时=岗位坚守族全新主题族零前采〕+真城生命感方向"
                         u"对位=最讲准的城市也懂得给心情留一格调节=规矩里长着人味〔城市人文积累令 O-20260928-1910 "
                         u"对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·守着全城时间的居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十一证+二轴并列"
                            u"最久未采回补〔秩序 v35 后 5 件首回=并列轴中最长回补距·弱项注记后本行胜出·准×心配位面="
                            u"系列首见构式+「调」字同手双寄存器〕+「校准了时间也得调好心情」〔把全城时间校准好的人"
                            u"承认心情也要调好=准×心〕准×心轴内自反差金句位〔族二十七连·配位语感独占注〕+钟台守时"
                            u"场景层=R442 审计处方带续证+「也得调好」让步式岗位口语=人味命中〔CEO 审美线对位·国庆"
                            u"假期语境直配·城市的钟不放假×守时的人也别绷太紧=岗位坚守面〕+最讲准的城市懂得给心情留"
                            u"一格=城市人文积累令对位〔真城生命感〕）+语录卡线变体零新模板第四十一证（QUOTE-v2 参数"
                            u"verbatim 复用·h2_size 60=零模板默认档直配〔13.00em 引文行入 60 档预算 15.33em margin "
                            u"+2.33em=v38/v39 同档先例〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 "
                            u"7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：秩序轴〔守规矩·重条理·逐盏校准·把城市调得"
                          u"妥妥当当的居民〕×校准了时间也得调好心情〔最讲准的人承认心情也要调=岗位语言让位给"
                          u"人话〕=准×心轴内自反差金句位〔族二十七连·配位语感独占注〕+国庆假期第 2 日夜里钟台守时"
                          u"人照常校准全城时间×街上满挂节日灯=钟台守时场景层+「调」字同手双寄存器口语真感/情 1 "
                          u"节日岗位温和共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日夜钟台校准=秩序场景当日对位+"
                          u"festival 情境桶直配第四十一证+池句让步语气常青/台 2 公众号方图承载=MC-001~125 S3 实证"
                          u"复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 "
                          u"DAILY·queue §E E30 R1010 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（守着全城时间的居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（校准时间=岗位意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十一件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[zhixu][festival][17] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v40 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-eighth proof: zhixu line17 != DAILY-v5 line4 != DAILY-v17 line12 != DAILY-v21 line6 != DAILY-v28 line9 != DAILY-v30 line2 != DAILY-v35 line11 != REACT-v8 line14 != city-spirit-v1.2 line16 = same-axis-different-line thirty-sixth proof; quote-face word adjacency: xinqing/diaohao NONE fleet-wide (r1010_quote_face.txt)")
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
report.append("LADDER_STAY_60: quote line 13.00em fits 60-band budget 15.33em margin +2.33em (zero-template default band, v38/v39 same-band precedent); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1010.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V41, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V41, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v40 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (zero-template default band 60) + E4 fired async" % H2_SIZE)
