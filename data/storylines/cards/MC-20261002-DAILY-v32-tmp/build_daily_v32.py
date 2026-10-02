# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v32 build: DAILY (city daily-sign) series THIRTY-SECOND piece (R1001, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-second same-day proof). Axis pick = yanhuo (market-life /
crowd-loving street residents)/festival/10: rotation law = post-v31 DAILY counts qiuxin 6 /
huaijiu 5 / xiaqi 5 / yanhuo 5 / zhixu 5 / xiaoyao 5 -> five-way tie at five consumptions
(qiuxin 6 most) -> within-tie content-strength pick documented (huaijiu FREE face
theme-saturated: umbrella-motif line [2] sibling of v22 consumed umbrella line, [10]
sentiment near-duplicate of v24 consumed line; yanhuo line10 = brand-new series theme
family - breakfast-stall vendor slot zero prior consumption + literal yanhuoqi hit on
CEO aesthetic line + R442 concrete-scene prescription) + yanhuo first return five pieces
after v27 (v30 zhixu / v31 xiaoyao two most recent picks avoided = alternation diversity
maintained). This line zero fleet consumption (city-spirit NOT_IN pre-check + all
cards.json scan asserted; consumed festival lines for yanhuo axis = DAILY-v4 line4 +
DAILY-v11 line13 + DAILY-v19 line3 + DAILY-v24 line2 + DAILY-v27 line7 + REACT-v8 line12
-> line10 fresh). Built-in tension:
早点摊也得趁热闹，多卖点包子 (everyone else takes the festival crowd-heat to the
lanterns; the breakfast-stall owner takes the same crowd-heat to the steamer - the
festival's liveliness flows into the most daily of livelihoods = joy through labor's eye)
= 劳×欢 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17 rule-x-
joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady /
v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time /
v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle /
v30 dress-x-proper / v31 dance-x-furnace = same structural gold-sentence family,
eighteenth consecutive variant). Axis-exclusive register note: only a resident whose days
are lived inside the market steam says the festival as a sales boom - the lantern-watchers
cannot say this line = axis-exclusive register slot. Scene layer: National Day holiday
morning crowd pouring out to see the lanterns + the breakfast stall set up as always,
steam rising, extra baozi sold = concrete stall-front peak-season scene (R442 audit
weakness prescription band; v11 canteen cook overtime / v19 market cabbage sibling
scenes noted). Plain speech ("也得" concession + "多卖点" vendor-quantifier = colloquial
authenticity) = anti-AI-flavor authenticity. Living-city proof = the festival's joy is not
only for lantern-watchers - it flows into the most daily livelihood, the crowd-heat
becomes the stall's peak season = living evidence (city humane-accumulation order echo).
Line-level freshness twenty-ninth proof = same-axis-different-line twenty-seventh proof.
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim;
h2_size ladder step-down to notch 50 (quote line 16.00em > 15.33em budget at 60; 18.40em
budget at 50 with margin +2.40em = v29/v31 same-family step-down, third series proof).
Machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V32 = os.path.join(BASE, "MC-20261002-DAILY-v32")
TMP = V32 + "-tmp"
os.makedirs(V32, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"早点摊也得趁热闹，多卖点包子"
AXIS, BUCKET, IDX = u"烟火", u"festival", 10

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V32:
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
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 032",
    u"2026-10-02 · 国庆假期",
    u"「早点摊也得趁热闹，多卖点包子」",
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
assert H2_SIZE == 50, "em ladder front-fit: 16.00em quote line > 15.33em budget at 60 -> step-down notch 50 (v29/v31 same-family precedent, margin +2.40em), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v32"
meta["form"] = (u"DAILY 城市日签 032（L-卡 图文轻内容线 DAILY 形态第三十二件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1001·日签节律续件=日期×情境桶对位判据第三十二证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第二十九证=同轴异行第二十七证〔烟火轴 "
                u"DAILY-v4〔line4〕+DAILY-v11〔line13〕+DAILY-v19〔line3〕+DAILY-v24〔line2〕+DAILY-v27〔line7〕"
                u"+REACT-v8〔line12〕之外线级新鲜行 line10·轴面 v6 收官耗尽后线级新鲜度=唯一面·R975 收口注承接·"
                u"旋转律兑现=v31 后计数求新 6/怀旧 5/侠气 5/烟火 5/秩序 5/逍遥 5=五轴并列最少 5 采·并列面内内容强度"
                u"择优如实注记〔怀旧 FREE 行主题饱和：伞 motif 行〔line2〕与 v22 已采修伞铺行同景近重复·line10 与 "
                u"v24 已采行「心里头也暖和了」情绪近重复·本行=早点摊摊主位系列全新主题族零前采+烟火气人味=CEO "
                u"审美线字面命中+R442 具体场景处方双命中〕·v30 秩序/v31 逍遥双最近采避开=轮换多样性维持·烟火 v27 "
                u"后 5 件首回〕〕+烟火轴〔最爱往人堆里凑热闹的市井居民：逛菜场·下馆子·摆早点摊〕×「早点摊也得"
                u"趁热闹，多卖点包子」（别人趁热闹看灯·摊主趁热闹开蒸笼=节日的欢腾流进最日常的生计=生计视角的"
                u"节日语感）=劳×欢轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/"
                u"v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/"
                u"v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉=族十八连·摊主位语感独占注=日子过在蒸汽里的人把节日"
                u"过成旺季·看灯的人说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「早点摊也得趁热闹，多卖点包子」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][festival][10]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v31 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][festival][10] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v31 同桶直配第三十二证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+"
                         u"REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+"
                         u"求新/14+侠气/0〕皆非本行=线级新鲜度第二十九证·本行=烟火轴 line10 非 DAILY-v4 line4 非 "
                         u"DAILY-v11 line13 非 DAILY-v19 line3 非 DAILY-v24 line2 非 DAILY-v27 line7 非 REACT-v8 "
                         u"line12=同轴异行第二十七证〔六轴收官后烟火轴第六采·轮前 city-spirit NOT_IN 预检复证="
                         u"r1001_pool_scan.txt 全桶预检 FREE 54 行=R978 拦截教训执行·v31 行已 USED 复核〕⑥国庆"
                         u"语境核=本行无「年味」措辞（R972 制·早点摊/包子=节日人潮饮食面公共措辞与国庆时点相对位）"
                         u"⑦品牌语感注=「也得」让步式+「多卖点」生意人量词=大众口语真感·把节日的热闹说成生意的旺季="
                         u"生计视角独占语感〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+烟火轴〔最爱往人堆里"
                         u"凑热闹的市井居民〕×「早点摊也得趁热闹，多卖点包子」〔节日的欢腾流进最日常的生计〕=劳×欢"
                         u"轴内自反差（别人趁热闹看灯·摊主趁热闹开蒸笼·同一片节日热闹两副市井过法=欢腾被过成了旺季）"
                         u"+国庆假期早晨出门看灯人潮×早点摊蒸汽照常升起多卖几笼包子=摊前旺季场景层=具体场景面〔R442 "
                         u"审计叙事弱点处方带·v11 食堂师傅加班/v19 菜场白菜同族异质行注·摊主位=系列全新主题族零前采〕"
                         u"+真城生命感方向对位=节日的快乐不只属于看灯的人也流进最日常的生计里·城市的热闹能变成摊主"
                         u"生意的人潮=城市在运转的活证据（城市人文积累令 O-20260928-1910 对位）")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十二证+烟火轴"
                            u"五轴并列最少 5 采内内容强度择优〔摊主位=系列全新主题族·CEO 审美线字面命中+R442 具体"
                            u"场景处方双命中·v27 后 5 件首回〕+「早点摊也得趁热闹，多卖点包子」〔节日的欢腾流进"
                            u"最日常的生计=生计视角的节日语感〕劳×欢轴内自反差金句位〔族十八连·摊主位语感独占注〕"
                            u"+摊前旺季场景层=R442 审计处方带续证+「也得」「多卖点」口语真感=人味命中〔CEO 审美线"
                            u"对位·烟火气字面命中〕+节日快乐流进最日常的生计=城市人文积累令对位〔真城生命感〕）+"
                            u"语录卡线变体零新模板第三十二证（QUOTE-v2 参数 verbatim 复用·h2_size 梯档降 50="
                            u"16.00em 行长驱动〔v29/v31 同型降档第三证·18.40em 预算 margin +2.40em·R293 零余量"
                            u"排除+R301-313 梯档律〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 "
                            u"7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：早点摊〔每天天不亮开工的最日常生计·薄利小买卖〕"
                          u"×趁热闹〔节日的欢腾人潮〕=劳×欢轴内自反差金句位〔族十八连·摊主位语感独占注〕+国庆假期"
                          u"早晨看灯人潮×早点摊蒸汽照常升起=摊前旺季场景层+「也得」「多卖点」口语真感/情 1 生意"
                          u"人视角的节日温和共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日人潮=节日场景当日对位+"
                          u"festival 情境桶直配第三十二证+池句节日语气常青/台 2 公众号方图承载=MC-001~116 S3 "
                          u"实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 "
                          u"形态码 DAILY·queue §E E30 R1001 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（烟火轴居民=轴级群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（多卖点包子=生意口语量词非价格数额·早点摊="
                     u"市井生计群像场景非个体档案面）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十二件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][festival][10] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v31 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness twenty-ninth proof: yanhuo line10 != DAILY-v4 line4 != DAILY-v11 line13 != DAILY-v19 line3 != DAILY-v24 line2 != DAILY-v27 line7 != REACT-v8 line12 = same-axis-different-line twenty-seventh proof")
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
report.append("LADDER_STEPDOWN: quote line 16.00em > 15.33em budget at 60 -> notch 50 (v29/v31 same-family precedent = third series step-down; budget 18.40em margin +2.40em); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1001.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V32, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V32, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v31 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder step-down to 50, v29/v31 family third proof) + E4 fired async" % H2_SIZE)
