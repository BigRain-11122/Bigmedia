# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v44 build: DAILY (city daily-sign) series FORTY-FOURTH piece (R1013, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (forty-fourth same-day proof, bucket-level; scene face = holiday-morning
street-breakfast honestly noted, first non-lamp scene after the v39/v40/v42/v43 lamp run =
anti-homogenization variation). Axis pick = yanhuo (market-crowd, street-warmth heaviest,
crowding-is-destiny residents) /festival/1: rotation law = post-v43 DAILY counts qiuxin 8 /
huaijiu 7 / xiaqi 7 / yanhuo 7 / zhixu 7 / xiaoyao 7 = FIVE axes tied at minimum
(huaijiu/xiaqi/yanhuo/zhixu/xiaoyao) -> tie-break by longest-since-last-pick redemption =
yanhuo (first re-pick since v38; v39-v43 five pieces all other axes = longest redemption
distance in the tie). Within yanhuo FREE face content-strength pick documented
(card-face-level law R1010 corrected scanning; r1013_pool.txt FREE-face precheck +
r1013_quote_face.txt word-face machine probe): line8 'deng gua de zhen gao a, haoxiang
tianshang dou kuai liang le' = 'deng gua de zhen gao' FIVE-CHAR VERBATIM collision with v12
['deng gua de zhen gao, kan dejian xingxing le'] = strongest exclusion (machine-proven);
line11 'caichang ayimen zhehui dei duomaidian dengchuan huiqu' = caichang same-axis
same-bucket direct repeat v19 + ayi v13 + dengchuan v25/v43 in-window immediate adjacency
(triple); line9 'zhe jieri qifen, biguonian hai renao ne' = renao same-axis direct repeat
v32 [fourth use after v22/v34] + jieri qifen v28 + bi-comparison construct v16; line15
'gua shang denglong duo xiqing a' = guashangdenglong FOUR-CHAR verbatim collision v21 +
xiqing same-axis direct repeat v19; line16 'retengteng de baozi lai yifen?' = baozi
same-axis direct repeat v32; line17 'zhe jieride denglong ke zhen piaoliang' =
denglong-ke-zhen FOUR-CHAR construct collision v23 + deng-ler eight-piece saturation;
line0/6/14 = nian-wei seasonal wording rows -> R972 EXCLUDED three rows; THIS line1 =
'reteng de doujiang peishang youtiao, yizhengtian dou jingshen' = the ONLY FREE row with
ZERO card-face/source_quote word-face repeat (doujiang/youtiao/reteng/yizhengtian/jingshen
fleet source_quote zero hits r1013_quote_face.txt; v38 full-file hit = meta weakness-note
NARRATIVE false hit, v38 form-field once quoted THIS line as passed-over candidate = R1010
whole-file trap same type, card-face-level scan zero consumption). Honest weakness notes
carried: zaodian/hot-food theme-family adjacency v32 [zaodiantan/baozi = stall-livelihood
band] + v38 [zhutangyuan kitchen-steam home face vs THIS street-market steam face = same
family different scene]; zero explicit festival word = festival bucket catalog = holiday
generic face (v38 holiday-reunion precedent), day-match compensation = date line
'2026-10-02 - National Day holiday' + holiday-morning breakfast-stall scene framing.
Scene layer: National-Day day-2 early morning, market-crowd residents out for holiday
breakfast, hot soy-milk with fresh fried dough sticks at the street stall = holiday
morning-market steam scene (R442 weakness prescription band; first morning face + first
non-lamp face of the series run). Built-in tension: nao x chen axis-internal self-contrast
(thirtieth consecutive variant): the crowd-loving, festivity-is-destiny residents locate
the whole city's festival energy at one hot breakfast = the festive city's energy has a
morning root (axis-exclusive register note: the nostalgic sees the past in lamps, the
rule-keeper hangs them right, the bold pairs wine, the ease-lover calls it a dream, the
novelty-seeker likens them to stars - only the market-crowd regular knows the city's
festival warmth starts steaming at the breakfast stall). Living-city proof = man-made
festivity is not rootless: it rises from the first hot mouthful of the morning market
(city humane-accumulation order echo; renao-you-gen = renjian yanhuo literal hit). Line-
level freshness forty-first proof = same-axis-different-line thirty-ninth proof. Quote
verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size
drops to 50 (quote line 18.00em, 60-band budget 15.33em FAIL -> 50-band budget 18.40em
margin +0.40em >= 0.2em floor per R293, v40 16.00em same-band precedent, v43 +0.33em
thinnest precedent). Machine source/dedup assertions (R456 system, card-face level R1010).
All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V44 = os.path.join(BASE, "MC-20261002-DAILY-v44")
TMP = V44 + "-tmp"
os.makedirs(V44, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"热腾的豆浆配上油条，一整天都精神"
AXIS, BUCKET, IDX = u"烟火", u"festival", 1

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V44:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits (v38 form-field once quoted THIS line as a passed-over
        # candidate) do NOT count as consumption.
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
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 044",
    u"2026-10-02 · 国庆假期",
    u"「热腾的豆浆配上油条，一整天都精神」",
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
assert H2_SIZE == 50, "em ladder front-fit: quote line 18.00em fails 60-band (15.33em) -> 50-band budget 18.40em margin +0.40em (>=0.2em floor per R293; v40 16.00em same-band precedent; v43 +0.33em thinnest precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v44"
meta["form"] = (u"DAILY 城市日签 044（L-卡 图文轻内容线 DAILY 形态第四十四件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1013·日签节律续件=日期×情境桶对位判据第四十四证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日早晨早市过早面如实注记"
                u"〔灯面之外的节日早晨面·v39 灯火/v40 酒香配灯/v42 街灯/v43 灯串四连灯带后首件非灯面=反同构变奏"
                u"·R442 系列同构弱点正面处方·日期行「2026-10-02 · 国庆假期」承节日面〕〕+六轴收官后线级新鲜度"
                u"第四十一证=同轴异行第三十九证〔烟火轴 DAILY-v4〔line4〕+DAILY-v11〔line13〕+DAILY-v19〔line3〕+"
                u"DAILY-v24〔line2〕+DAILY-v27〔line7〕+DAILY-v32〔line10〕+DAILY-v38〔line5〕+REACT-v8〔line12〕"
                u"之外线级新鲜行 line1·轮前 r1013_pool.txt 烟火桶 FREE 行预检=R978 拦截教训执行·v38 行已 USED 复核〕+"
                u"旋转律兑现=v43 后计数求新 8/怀旧 7/侠气 7/烟火 7/秩序 7/逍遥 7=五轴并列最少（怀旧/侠气/烟火/"
                u"秩序/逍遥）→并列面最久未采回补=烟火〔v38 后 5 件未采·v39-v43 五件皆他轴=并列轴中最长回补距〕·"
                u"FREE 面内容强度择优如实注记〔烟火 FREE 面全弱态=本行胜出注记：line8「灯挂得真高啊，好像天上都"
                u"快亮了」=「灯挂得真高」v12 五字 verbatim 直撞〔r1013_quote_face.txt 机核〕=最强排除/line11「菜场"
                u"阿姨们这回得多买点灯串回去」=菜场同轴同桶直重 v19+阿姨 v13+灯串 v25/v43 窗内即邻=三重/line9"
                u"「这节日气氛，比过年还热闹呢」=热闹同轴直重 v32〔四用·v22/v34 在先〕+节日气氛 v28+比构式 v16/"
                u"line15「挂上灯笼多喜庆啊」=挂上灯笼 v21 四字直撞+喜庆 v19 同轴直重/line16「热腾腾的包子来一份？」"
                u"=包子 v32 同轴直重/line17「这节日的灯笼可真漂亮」=灯笼可真 v23 四字构式直撞+灯笼八件饱和/"
                u"line0+line6+line14=年味儿季相排除三行〔R972〕；本行 line1=「热腾的豆浆配上油条，一整天都精神」"
                u"=FREE 面唯一零卡面词面重复行〔豆浆/油条/热腾/一整天/精神=fleet source_quote 零命中"
                u"〔r1013_quote_face.txt 机核〕·v38 全文件命中=meta 弱项注记叙述面假命中〔v38 form 字段曾引本行"
                u"全文为落选候选注记=R1010 整文匹配陷阱同型·卡面级实扫定谳零消费〕〕+弱项如实注记=早点/热食主题族"
                u"邻接 v32〔早点摊/包子=摊位生计带〕+v38〔煮汤圆白汽=灶头家用蒸汽面 vs 本行=早市街头蒸汽面=同族"
                u"异质〕+零节日钩〔festival 桶编目=节日通用面·v38 假日团圆对位先例·假日晨面场景补偿〕+「一整天"
                u"都精神」市井大白话口语真感=人味命中〔CEO 审美线对位〕〕）")
meta["source_quote"] = u"「热腾的豆浆配上油条，一整天都精神」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][festival][1]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v43 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][festival][1] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v43 同桶直配第四十四证=日签节律判据"
                         u"系列化·国庆假期第 2 日早晨早市过早=假日晨面场景对位〔场景级如实注记：灯面之外的节日"
                         u"早晨面〕）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕⑤去重断言=本行"
                         u"不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote 任一（**卡面级实扫="
                         u"R1010 修正律**·v38 全文件命中=meta 弱项注记叙述面假命中如实注记非卡面消费·DAILY-v1"
                         u"〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+"
                         u"DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10"
                         u"〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14"
                         u"〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18"
                         u"〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22"
                         u"〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26"
                         u"〔侠气/10〕+DAILY-v27〔烟火/7〕+DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30"
                         u"〔秩序/2〕+DAILY-v31〔逍遥/4〕+DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34"
                         u"〔侠气/9〕+DAILY-v35〔秩序/11〕+DAILY-v36〔逍遥/16〕+DAILY-v37〔求新/5〕+DAILY-v38"
                         u"〔烟火/5〕+DAILY-v39〔怀旧/5〕+DAILY-v40〔侠气/11〕+DAILY-v41〔秩序/17〕+DAILY-v42"
                         u"〔逍遥/13〕+DAILY-v43〔求新/9〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+"
                         u"city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第四十一证·"
                         u"本行=烟火轴 line1 非 DAILY-v4 line4 非 DAILY-v11 line13 非 DAILY-v19 line3 非 DAILY-v24 "
                         u"line2 非 DAILY-v27 line7 非 DAILY-v32 line10 非 DAILY-v38 line5 非 REACT-v8 line12="
                         u"同轴异行第三十九证〔六轴收官后烟火轴第九采·轮前 r1013_pool.txt 烟火桶 FREE 行预检="
                         u"R978 拦截教训执行〕+「豆浆」「油条」「热腾」「一整天」「精神」=fleet source_quote 零词邻"
                         u"〔r1013_quote_face.txt 机核〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·烟火面 "
                         u"line0/6/14 年味行已按季相律排除·豆浆油条=全季相公共早餐措辞与国庆早晨时点对位〕"
                         u"⑦品牌语感注=「一整天都精神」市井大白话〔口语真感·去 AI 感对位〕+烟火轴〔最爱往人堆里"
                         u"凑·市井烟火气最重〕×热豆浆油条〔满城赶热闹的人一天的精神从早市一口热乎来〕=闹×晨金句位+"
                         u"国庆假期第 2 日早晨早市过早场景层〔R442 审计叙事弱点处方带·灯带四连后首件晨市场景="
                         u"反同构〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·早市过早的烟火轴居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十四证+五轴"
                            u"并列最少最久未采回补=烟火赎回〔v38 后 5 件首回〕+FREE 面全弱态如实注记后本行胜出"
                            u"〔唯一零卡面词面重复行·v38 meta 叙述面假命中定谳〕+「热腾的豆浆配上油条，一整天都"
                            u"精神」〔满城赶热闹的人一天的精神从早市一口热乎里来〕闹×晨轴内自反差金句位〔族三十连·"
                            u"晨源语感独占注：怀旧的人从灯里看到从前·守规矩的人把灯挂得妥当·豪爽的人用酒香配灯·"
                            u"松弛的人叫它一场梦·追新的人把它比作星星——只有往人堆里凑的人知道节日的热闹从大清早"
                            u"一碗热豆浆开始冒汽〕+早市过早场景层=R442 审计处方带续证+灯带四连后反同构变奏+"
                            u"「一整天都精神」市井大白话=人味命中〔CEO 审美线对位·城市人文积累令对位·热闹有根="
                            u"人间烟火字面命中〕）+语录卡线变体零新模板第四十四证（QUOTE-v2 参数 verbatim 复用·"
                            u"h2_size 50 梯档〔18.00em 引文行入 50 档预算 18.40em margin +0.40em≥0.2em 地板律·"
                            u"R293 零余量排除线不触发·v40 16.00em 同带先例〕·charter §1「日签变体随时可续」兑现）"
                            u"·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：烟火轴〔最爱往人堆里凑·市井烟火气最重·"
                          u"热闹是本命〕×热腾的豆浆配上油条一整天都精神〔满城赶热闹的人一天的精神是从早市一口"
                          u"热乎里来的〕=闹×晨轴内自反差金句位〔族三十连〕+国庆假期第 2 日早晨早市过早场景层+"
                          u"「一整天都精神」口语真感/情 1 假日晨市温暖共鸣如实非强极点/时 2 当日时点=国庆假期"
                          u"第 2 日早晨早市直配+festival 情境桶直配第四十四证〔桶级·场景级假日晨面注记〕/台 2 "
                          u"公众号方图承载=MC-001~128 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1013 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（早市过早的烟火轴居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（豆浆油条=市井早餐公共意象非个体"
                     u"档案面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十四件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][festival][1] verbatim OK; festival bucket=18 lines; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; v38 whole-file hit = meta weakness-note NARRATIVE false hit, zero card-face consumption; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v43 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness forty-first proof: yanhuo line1 != DAILY-v4 line4 != DAILY-v11 line13 != DAILY-v19 line3 != DAILY-v24 line2 != DAILY-v27 line7 != DAILY-v32 line10 != DAILY-v38 line5 != REACT-v8 line12 = same-axis-different-line thirty-ninth proof; quote-face word adjacency: doujiang/youtiao/reteng/yizhengtian/jingshen ZERO fleet source_quote hits (r1013_quote_face.txt); strongest-exclusion rows machine-proven: line8 deng-gua-de-zhen-gao 5-char verbatim v12; line15 guashang-denglong 4-char v21 + xiqing v19; line17 denglong-ke-zhen 4-char v23; line16 baozi v32; line9 renao v32; line11 caichang v19+ayi v13+dengchuan v25/v43")
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
report.append("LADDER_DROP_50: quote line 18.00em fails 60-band (budget 15.33em) -> 50-band budget 18.40em margin +0.40em (>=0.2em floor per R293; v40 16.00em same-band precedent; v43 +0.33em thinnest precedent); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1013.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V44, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V44, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v43 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder drop from 60 zero-template default to 50, quote 18.00em driver) + E4 fired async" % H2_SIZE)
