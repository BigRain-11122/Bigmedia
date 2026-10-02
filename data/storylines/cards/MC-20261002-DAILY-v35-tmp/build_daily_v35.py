# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v35 build: DAILY (city daily-sign) series THIRTY-FIFTH piece (R1004, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-fifth same-day proof). Axis pick = zhixu (rule-and-order
residents)/festival/11: rotation law = post-v34 DAILY counts qiuxin 6 / huaijiu 6 / xiaqi 6 /
yanhuo 6 / zhixu 5 / xiaoyao 5 -> two-way tie at five consumptions -> within-tie
longest-unconsumed redemption = zhixu last picked v30, four pieces ago (v31-v34 all other
axes) vs xiaoyao v31 three pieces ago avoided; alternation law continuation (v29 xiaoyao ->
v30 zhixu -> v31 xiaoyao -> ... -> v35 zhixu = double-least-axis alternating rotation).
Within zhixu FREE face content-strength pick documented (weakness notes: line1 'shou guiju'
slogan-register zero-scene zero-festival-hook hollow-cliche risk, line3 'anquan diyi'
word-level overlap with line11 plus 'yanjin' bookish register, line5 wordy self-reminder
flat register, line7 'jiaohao le dengguang cai anxin' calibration motif near-duplicate of
consumed v5 line4 'jiaohao hao mei zhan deng, xinli cai taoshi' (same structure
calibrate->ease, R442 serial-isomorphism face), line10 slogan-register abstract zero-scene,
line13 'nian cai renao' season-law avoid (October timepoint, R972 rule, nian-family
adjacent line honestly avoided despite FREE scan mark), line15 lantern-hang pattern family
saturation (v21/v26/v30 lantern-joy band, v33 noted), line17 'jiaohao' word-level repeat of
consumed v5 line4 plus zero festival-lamp hook; THIS line11 = xunjian (lamp-by-lamp safety
inspection) slot brand-new series theme family zero prior consumption (v28 weihu slot =
ambiance-care face vs THIS = physical safety-inspection face = distinct) + doubled-noun
'zhanzhan' folk reduplication one-by-one working-procedure feel + clipped four-char
heavyweight close 'anquan diyi' (shortest-heaviest guardian promise, four-char clipped
close) + festival lamp-inspection night-duty scene direct match (holiday lamps strung city
needs its rule-keepers walking the line) = top concrete-scene pick (R442 audit
people-in-scene prescription band). Mild adjacency documented honestly: 'zhan' char also
in consumed REACT-v8 line14 (different construction: zhe zhan deng single-lamp point vs
deng-zhanzhan reduplicated every-lamp sweep). This line zero fleet consumption
(city-spirit NOT_IN pre-check + all cards.json scan asserted; consumed festival lines for
zhixu axis = DAILY-v5 line4 + DAILY-v17 line12 + DAILY-v21 line6 + DAILY-v28 line9 +
DAILY-v30 line2 + REACT-v8 line14 + city-spirit v1.2 line16 -> line11 fresh). Built-in tension:
灯盏盏都得检查，安全第一 (the residents who prize rules above all, in the end, spend the
festival on the humblest of all work - checking the lamps one by one = grand order lands in
the smallest procedure)
= 细×重 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17 rule-x-joy
/ v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady / v22
old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time / v26
hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle / v30
dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy / v33 style-x-small / v34 yi-x-lin
= same structural gold-sentence family, twenty-first consecutive variant). Axis-exclusive
register note: only a resident whose order-ethos lives in checklists and procedures says
the festival as 'every lamp gets checked' - the ease-seekers and the loyalty-keepers cannot
say this line = axis-exclusive register slot. Scene layer: National Day holiday evening,
festival lamps strung over the streets, the rule-keeper walking the line with a checklist,
lifting each lamp one by one, 'safety first' as the shortest heaviest promise = concrete
person-at-work inspection scene (R442 audit weakness prescription band; v28 street-patrol
sibling scene noted; xunjian slot = brand-new theme family). Plain speech (doubled-noun
zhanzhan + four-char clipped close anquan diyi = folk working-register authenticity) =
anti-AI-flavor authenticity. Living-city proof = the rule-keepers guarding every lamp of
the holiday city = the city's order is alive (city humane-accumulation order echo).
Line-level freshness thirty-second proof = same-axis-different-line thirtieth proof.
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim;
h2_size ladder holds notch 60 (quote line 14.00em fits 15.33em budget with +1.33em margin,
four-line stack VERT +229px = v17/v22/v34 same-structure notch band; holds from v34,
ladder length-driven law). Machine source/dedup assertions (R456 system). All output
UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V35 = os.path.join(BASE, "MC-20261002-DAILY-v35")
TMP = V35 + "-tmp"
os.makedirs(V35, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"灯盏盏都得检查，安全第一"
AXIS, BUCKET, IDX = u"秩序", u"festival", 11

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V35:
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
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 035",
    u"2026-10-02 · 国庆假期",
    u"「灯盏盏都得检查，安全第一」",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 14.00em fits 15.33em budget at 60 with margin +1.33em (four-line stack VERT +229px = v17/v22/v34 same-structure notch band; holds 60 notch from v34, ladder length-driven law), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v35"
meta["form"] = (u"DAILY 城市日签 035（L-卡 图文轻内容线 DAILY 形态第三十五件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1004·日签节律续件=日期×情境桶对位判据第三十五证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十二证=同轴异行第三十证〔秩序轴 "
                u"DAILY-v5〔line4〕+DAILY-v17〔line12〕+DAILY-v21〔line6〕+DAILY-v28〔line9〕+DAILY-v30〔line2〕"
                u"之外线级新鲜行 line11·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·旋转律兑现=v34 后"
                u"计数求新 6/怀旧 6/侠气 6/烟火 6/秩序 5/逍遥 5=双轴并列最少 5 采·并列面内最久未采回补=秩序"
                u"v30 后 4 件首回〔v31-v34 四件皆他轴〕·逍遥 v31 后 3 件次回避开=轮换多样性维持·双最少轴交替"
                u"轮换制承继〔v29 逍遥→v30 秩序→v31 逍遥→v35 秩序〕·并列面内内容强度择优如实注记〔秩序 FREE "
                u"面弱项：line1「守规矩才能让城市更安稳」口号化零场景零节日钩=空洞套话风险+line3「安全第一」"
                u"词面与本行重叠+「严谨」书面语感+line5 冗长自我提醒语感平+line7 校准 motif 近重复已采 v5 "
                u"line4〔校准好每盏灯心里才踏实=同构校准→安心·R442 系列同构面〕+line10 口号化抽象零场景+"
                u"line13「年才热闹」季相律回避〔10 月秋时点·R972 制·年味族邻接行·扫描 FREE 但季相核诚实回避〕+"
                u"line15 灯笼一挂主题族饱和〔v21/v26/v30 灯喜带·v33 已注〕+line17「校准」词面重复已采 v5 "
                u"line4 且零节日灯钩；本行=巡检位系列全新主题族零前采〔v28 维护位=氛围爱护面 vs 本行=安全"
                u"巡检面=异质〕+叠词「盏盏」逐盏排查工序感+四字格收束「安全第一」=最短最重的守护承诺·轻度"
                u"邻接如实注记：「盏」字亦在已采 REACT-v8 line14〔这盏灯单指 vs 灯盏盏叠词逐盏=不同构式〕〕〕"
                u"+秩序轴〔最讲规矩·安全安稳第一·把规矩落进工序里的居民〕×「灯盏盏都得检查，安全第一」"
                u"（最讲规矩的人把节日过成最家常的逐盏工序=大秩序落进小检查）=细×重轴内自反差金句位〔v15 "
                u"屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×"
                u"手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×"
                u"炉/v32 劳×欢/v33 派×小/v34 义×邻=族二十一连·巡检位语感独占注=把规矩落进逐盏工序·散淡的人"
                u"和豪爽的人说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「灯盏盏都得检查，安全第一」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][festival][11]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v34 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][festival][11] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v34 同桶直配第三十五证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+"
                         u"DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+REACT-v8 同桶三行〔逍遥/17+"
                         u"烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行="
                         u"线级新鲜度第三十二证·本行=秩序轴 line11 非 DAILY-v5 line4 非 DAILY-v17 line12 非 "
                         u"DAILY-v21 line6 非 DAILY-v28 line9 非 DAILY-v30 line2 非 REACT-v8 line14 非 city-spirit "
                         u"v1.2 line16=同轴异行第三十证〔六轴收官后秩序轴第六采·轮前 city-spirit NOT_IN 预检复证="
                         u"r1004_pool_scan.txt 全桶预检 FREE 51 行=R978 拦截教训执行·v34 行已 USED 复核〕⑥季相核="
                         u"本行无「年味」措辞亦无春雨/春联类季相错位词（R972 制·秩序面 line0/line8 年味行已按季相律"
                         u"回避·line13「年才热闹」邻接行亦按季相律诚实回避·检查/安全第一=全季相公共城市安全措辞"
                         u"与国庆假期值守时点对位）⑦品牌语感注=「盏盏」叠词逐盏排查工序感+「安全第一」四字格"
                         u"收束=值守师傅嘴里的口气·口语真感顶档〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+"
                         u"秩序轴〔最讲规矩·把规矩落进工序里〕×逐盏检查〔最家常的值守工序〕=细×重金句位（最讲"
                         u"规矩的人把节日过成最家常的逐盏工序=大秩序落进小检查）+国庆假期夜晚满街节日灯下值守"
                         u"员提灯逐盏巡检=巡检场景层=具体人物×具体动作场景面〔R442 审计叙事弱点处方带续证·v28 "
                         u"巡街值守同族异质行注·巡检位=系列全新主题族零前采〕+真城生命感方向对位=最讲规矩的居民"
                         u"守着满城灯火的安全=城市安稳活着的证据〔城市人文积累令 O-20260928-1910 对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·值守员=职业称谓群像面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十五证+双轴"
                            u"并列最少 5 采内最久未采回补〔秩序 v30 后 4 件首回·并列面内容强度择优弱项注记后本行"
                            u"胜出·巡检位=系列全新主题族·R442 具体人物场景处方+叠词四字格收束双命中〕+"
                            u"「灯盏盏都得检查，安全第一」〔最讲规矩的人把节日过成最家常的逐盏工序=细×重〕细×重"
                            u"轴内自反差金句位〔族二十一连·巡检位语感独占注〕+巡检场景层=R442 审计处方带续证+"
                            u"「盏盏」叠词+「安全第一」四字格收束=口语真感=人味命中〔CEO 审美线对位·国庆假期"
                            u"值守巡检直配〕+最讲规矩的居民守着满城灯火的安全=城市人文积累令对位〔真城生命感〕）"
                            u"+语录卡线变体零新模板第三十五证（QUOTE-v2 参数 verbatim 复用·h2_size 梯档守 60="
                            u"14.00em 行长驱动〔v34 60 档带后守档·60 档预算 15.33em margin +1.33em·四行栈 VERT "
                            u"+229px=v17/v22/v34 同构档·R293 零余量排除+R301-313 梯档律〕·charter §1「日签变体"
                            u"随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：秩序轴〔最讲规矩·安全安稳第一·把规矩落进"
                          u"工序里的居民〕×逐盏检查〔最家常的值守工序〕=细×重轴内自反差金句位〔族二十一连·巡检"
                          u"位语感独占注〕+国庆假期夜晚满街节日灯下值守员提灯逐盏巡检=巡检场景层+「盏盏」叠词+"
                          u"「安全第一」四字格收束=值守师傅口气口语真感/情 1 安稳守护温和共鸣如实非强极点/"
                          u"时 2 当日时点=国庆假期第 2 日夜间值守=巡检场景当日对位+festival 情境桶直配第三十五证+"
                          u"池句城市安全语气常青/台 2 公众号方图承载=MC-001~119 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R1004 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（值守员=职业称谓群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（检查=城市安全工序面非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十五件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[zhixu][festival][11] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v34 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-second proof: zhixu line11 != DAILY-v5 line4 != DAILY-v17 line12 != DAILY-v21 line6 != DAILY-v28 line9 != DAILY-v30 line2 != REACT-v8 line14 != city-spirit v1.2 line16 = same-axis-different-line thirtieth proof")
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
report.append("LADDER_HOLD_60: quote line 14.00em fits 15.33em budget at 60 with margin +1.33em -> holds notch 60 (four-line stack VERT +229px = v17/v22/v34 same-structure band; holds from v34, ladder length-driven law); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1004.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V35, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V35, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v34 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder holds 60 notch from v34 band) + E4 fired async" % H2_SIZE)
