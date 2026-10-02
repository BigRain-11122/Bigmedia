# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v33 build: DAILY (city daily-sign) series THIRTY-THIRD piece (R1002, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-third same-day proof). Axis pick = huaijiu (old-times-loving
residents)/festival/4: rotation law = post-v32 DAILY counts qiuxin 6 / yanhuo 6 / huaijiu 5 /
xiaqi 5 / zhixu 5 / xiaoyao 5 -> four-way tie at five consumptions -> within-tie
content-strength pick documented (xiaqi FREE-face weakness notes: line17 'jianghu yiqi'
word-level repeat of consumed v3 line, line14 star motif near-duplicate of consumed v12
line, line11 'ye dei' clause wording near-duplicate of consumed v32 line (consecutive
pieces same clause = template feel), line7 labor-x-joy structural slot same as v32 (R442
serial-isomorphism face); huaijiu FREE-face saturation notes: line2 umbrella motif
near-duplicate of v22 (R1001 documented), line7 spring-rain season-law mismatch (October
autumn timepoint, R972 analog), line9 lantern-craft family near v14/v23, line10 warm-heart
sentiment near v24, line11 archive near v10, line5 back-to-old-times depth family near
v16/v25, line14 steady-life sentiment near v21, line13 'niannianduoyu' spring-couplet
wording nianwei adjacency avoid; THIS line4 = laokele slot brand-new series theme family
zero prior consumption + R442 concrete-persona prescription hit (laokele = Shanghai
local-chronicle persona slot) + word-face new-x-old self-contrast ('laokele' old-school
gentleman x 'xiaoquexing' modern borrowed word) + huaijiu first return seven pieces after
v25 = longest-unconsumed axis redemption). This line zero fleet consumption (city-spirit
NOT_IN pre-check + all cards.json scan asserted; consumed festival lines for huaijiu axis =
DAILY-v2 line0 + DAILY-v10 line3 + DAILY-v16 line1 + DAILY-v22 line12 + DAILY-v25 line17
-> line4 fresh). Built-in tension:
老克勒们最爱的，还是这传统的小确幸 (the most style-and-swagger-obsessed old Shanghai
gentlemen, in the end, claim the festival as their own tiny certain happiness - the
grandest persona settles into the smallest everyday joy = style x smallness)
= 派×小 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17 rule-x-
joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady /
v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time /
v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle /
v30 dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy = same structural gold-sentence
family, nineteenth consecutive variant). Axis-exclusive register note: only a resident
whose days are worn inside old-time style says the festival as a 'small certain
happiness' - the trend-chasers cannot say this line = axis-exclusive register slot.
Scene layer: National Day holiday evening, festival lamps strung across the streets, the
old-school gentleman stops under the lamps and takes the whole city's festival as his own
xiaoquexing = concrete gentleman-under-lamps scene (R442 audit weakness prescription
band; v10 archive / v16 lantern-festival nostalgia sibling scenes noted). Plain speech
("们最爱的" crowd-possessive + "还是" preference-concession = colloquial authenticity) =
anti-AI-flavor authenticity. Living-city proof = the most style-obsessed old residents
finally count the city's festival as their own small happiness = the city in old-time
texture is alive (city humane-accumulation order echo). Line-level freshness thirtieth
proof = same-axis-different-line twenty-eighth proof. Quote verbatim + card framing
(R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size ladder step-down to
notch 46 (quote line 19.00em > 18.40em budget at 50; 20.00em budget at 46 with margin
+1.00em = step-down from v29/v31/v32 50-notch band, v13-era 46-notch family). Machine
source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V33 = os.path.join(BASE, "MC-20261002-DAILY-v33")
TMP = V33 + "-tmp"
os.makedirs(V33, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"老克勒们最爱的，还是这传统的小确幸"
AXIS, BUCKET, IDX = u"怀旧", u"festival", 4

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V33:
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
# DAILY-v32 yanhuo/festival/10 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/festival/16 +
# qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 033",
    u"2026-10-02 · 国庆假期",
    u"「老克勒们最爱的，还是这传统的小确幸」",
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
assert H2_SIZE == 46, "em ladder front-fit: 19.00em quote line > 18.40em budget at 50 -> step-down notch 46 (budget 20.00em, margin +1.00em; step-down from v29/v31/v32 50-notch band, v13-era 46-notch family), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v33"
meta["form"] = (u"DAILY 城市日签 033（L-卡 图文轻内容线 DAILY 形态第三十三件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1002·日签节律续件=日期×情境桶对位判据第三十三证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十证=同轴异行第二十八证〔怀旧轴 "
                u"DAILY-v2〔line0〕+DAILY-v10〔line3〕+DAILY-v16〔line1〕+DAILY-v22〔line12〕+DAILY-v25〔line17〕"
                u"之外线级新鲜行 line4·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·旋转律兑现=v32 后"
                u"计数求新 6/烟火 6/怀旧 5/侠气 5/秩序 5/逍遥 5=四轴并列最少 5 采·并列面内内容强度择优如实注记"
                u"〔侠气 FREE 面弱项：line17「江湖义气」与 v3 已采行词面重复+line14 星星 motif 与 v12 已采行情绪"
                u"近重复+line11「也得」句式与 v32 连件措辞近重复+line7 劳×欢结构位与 v32 同构〔R442 系列同构"
                u"弱点面〕；怀旧 FREE 面饱和：line2 伞 motif 与 v22 同景近重复〔R1001 已注〕+line7 春雨季相错位"
                u"〔10 月秋时点·R972 季相律同型〕+line9 布灯手艺与 v14/v23 手艺族近重复+line10 心里暖和与 v24 "
                u"情绪近重复+line11 档案馆与 v10 同景近重复+line5 回到从前与 v16/v25 时间纵深族近重复+line14 "
                u"日子踏实与 v21 稳当族近重复+line13「年年有余」春联措辞年味邻接回避·本行=老克勒位系列全新主题族"
                u"零前采+R442 具体人物处方+词面新×旧自反差〕·v30 秩序/v31 逍遥/v32 烟火三最近采避开=轮换多样性"
                u"维持·怀旧 v25 后 7 件首回=最久未采轴回补〕〕+怀旧轴〔最爱念旧·守着老物件·念着往年时光的居民〕×"
                u"「老克勒们最爱的，还是这传统的小确幸」（最讲腔调做派的老派绅士把满城节日认成自己的小确幸=派头"
                u"落进小日子的节日语感）=派×小轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 "
                u"平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 "
                u"闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉/v32 劳×欢=族十九连·老克勒位语感独占注=把满城"
                u"节日灯海过成自己的小确幸·赶新潮的人说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「老克勒们最爱的，还是这传统的小确幸」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][festival][4]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v32 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][festival][4] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v32 同桶直配第三十三证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+"
                         u"DAILY-v32〔烟火/10〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 "
                         u"节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第三十证·本行=怀旧轴 line4 "
                         u"非 DAILY-v2 line0 非 DAILY-v10 line3 非 DAILY-v16 line1 非 DAILY-v22 line12 非 "
                         u"DAILY-v25 line17=同轴异行第二十八证〔六轴收官后怀旧轴第六采·轮前 city-spirit NOT_IN "
                         u"预检复证=r1002_pool_scan.txt 全桶预检 FREE 53 行=R978 拦截教训执行·v32 行已 USED 复核〕"
                         u"⑥季相核=本行无「年味」措辞亦无春雨/春联类季相错位词（R972 制·怀旧面 line7 春雨行已按"
                         u"季相律回避·老克勒/小确幸=全季相公共措辞与国庆时点相对位）⑦品牌语感注=「们最爱的」群众"
                         u"所属式+「还是」偏好让步式=老派口语真感·最讲派头的做派最后落在最小的日常快乐上=派头×"
                         u"小日子语感独占〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+老克勒〔上海地方志人物"
                         u"位·洋泾浜借词 colour/class 音译·最讲腔调做派的老派绅士群像〕×「小确幸」〔现代语词·"
                         u"最小最朴素的日常快乐〕=词面新×旧自反差（最老派的人群说着最新的词=城市把新词接进旧时光的"
                         u"活证据）+国庆假期傍晚满街节日灯串×老派绅士驻足灯下把满城节日当成自己的小确幸=绅士看灯"
                         u"场景层=具体人物×具体场景面〔R442 审计叙事弱点处方带·v10 档案馆/v16 灯节感叹同族异质行注·"
                         u"老克勒位=系列全新主题族零前采〕+真城生命感方向对位=最念旧的居民把当下节日过成自己的"
                         u"小确幸〔城市人文积累令 O-20260928-1910 对位·老物件接新快乐=城市记忆活着的证据〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·老克勒=人群称谓群像面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十三证+怀旧轴"
                            u"四轴并列最少 5 采内内容强度择优〔侠气 FREE 面弱项+怀旧面饱和注记后本行胜出·老克勒位="
                            u"系列全新主题族·R442 具体人物处方+词面新×旧自反差双命中·v25 后 7 件首回=最久未采轴"
                            u"回补〕+「老克勒们最爱的，还是这传统的小确幸」〔最讲派头的做派落进最小的日常快乐="
                            u"派头×小日子〕派×小轴内自反差金句位〔族十九连·老克勒位语感独占注〕+绅士看灯场景层="
                            u"R442 审计处方带续证+「们最爱的」「还是」老派口语真感=人味命中〔CEO 审美线对位·地方"
                            u"志人物趣味〕+最念旧居民把当下节日过成小确幸=城市人文积累令对位〔真城生命感〕）+"
                            u"语录卡线变体零新模板第三十三证（QUOTE-v2 参数 verbatim 复用·h2_size 梯档降 46="
                            u"19.00em 行长驱动〔v29/v31/v32 50 档带后降档·46 档预算 20.00em margin +1.00em·R293 "
                            u"零余量排除+R301-313 梯档律〕·charter §1「日签变体随时可续」兑现）·公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：老克勒〔最讲腔调做派的老上海绅士派头·"
                          u"人群称谓〕×小确幸〔现代语词·最小最朴素的日常快乐〕=派×小轴内自反差金句位〔族十九连·"
                          u"老克勒位语感独占注〕+国庆假期傍晚满街灯串×老派绅士驻足灯下=绅士看灯场景层+「们最爱的」"
                          u"「还是」老派口语真感/情 1 旧时光底色人群的当下小快乐温和共鸣如实非强极点/时 2 当日时点="
                          u"国庆假期第 2 日灯海=节日场景当日对位+festival 情境桶直配第三十三证+池句节日语气常青/"
                          u"台 2 公众号方图承载=MC-001~117 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1002 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（老克勒=人群称谓群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（小确幸=生活语感词非平台指标·老克勒=地方志"
                     u"人群称谓非个体档案面）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十三件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[huaijiu][festival][4] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v32 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirtieth proof: huaijiu line4 != DAILY-v2 line0 != DAILY-v10 line3 != DAILY-v16 line1 != DAILY-v22 line12 != DAILY-v25 line17 = same-axis-different-line twenty-eighth proof")
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
report.append("LADDER_STEPDOWN: quote line 19.00em > 18.40em budget at 50 -> notch 46 (step-down from v29/v31/v32 50-notch band, v13-era 46-notch family; budget 20.00em margin +1.00em); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1002.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V33, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V33, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v32 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder step-down to 46, from v29/v31/v32 50-notch band) + E4 fired async" % H2_SIZE)
