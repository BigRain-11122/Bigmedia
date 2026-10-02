# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v30 build: DAILY (city daily-sign) series THIRTIETH piece (R999, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirtieth same-day proof). Axis pick = zhixu (order / rules-and-
calibration residents)/festival/2: rotation law = post-v29 counts qiuxin 6 / huaijiu 5 /
xiaqi 5 / yanhuo 5 / zhixu 4 / xiaoyao 4 -> zhixu tied-least plus least-recently-consumed
(v28 zhixu vs v29 xiaoyao) -> alternating redemption of the two least-consumed axes, zhixu
fifth DAILY consumption, first return two pieces after v28. This line zero fleet
consumption (city-spirit NOT_IN pre-check + all cards.json scan asserted; consumed festival
lines for zhixu axis = DAILY-v5 line4 + DAILY-v17 line12 + DAILY-v21 line6 + DAILY-v28
line9 + REACT-v8 line14 + city-spirit v1.2 line16 -> line2 fresh). Built-in tension:
这节日灯挂得真妥当 (everyone else praises festival lamps as pretty; the order axis gives
its workmanship-acceptance verdict "妥当" - the rules axis enjoying the festival in its
own professional inspection voice) = 装×妥 axis-internal self-contrast (v15 screen-x-real
/ v16 past-x-present / v17 rule-x-joy / v18 bustle-x-ease / v19 plain-x-festival / v20
rest-x-busy / v21 joy-x-steady / v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart
/ v25 new-season-x-old-time / v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-
maintain / v29 ease-x-bustle = same structural gold-sentence family, sixteenth consecutive
variant; zhixu festival-praise trio noted: v21 joy-x-steady + v28 joy-x-maintain + v30
dress-x-proper = same-axis theme-depth band). Scene layer: National Day lamp-sea all over
the city + the order residents walking the street checking the lamp hangs and pronouncing
their acceptance word = concrete inspection-acceptance scene (R442 audit weakness
prescription band; v5 calibrating street lamps / v28 patrol-watch sibling scenes noted).
Plain speech ("挂得""真妥当" = the order axis's own acceptance-register authenticity)
= anti-AI-flavor authenticity, 妥当 = machine-register word entering daily praise =
brand-voice exclusive slot (v5 校准 sibling). Living-city proof = the rules-strictest
residents praising the festival dress-up with an acceptance verdict = lamps hung properly
is living evidence the city runs its own festival in good order (city humane-accumulation
order echo). Line-level freshness twenty-seventh proof = same-axis-different-line
twenty-fifth proof. Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2
params verbatim, h2_size back to notch 60 after v29's one-off ladder step-down (quote line
11.0em < 15.33em budget at 60; three-line stack = v19/v22/v27/v28 isomorphic +229px).
Machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V30 = os.path.join(BASE, "MC-20261002-DAILY-v30")
TMP = V30 + "-tmp"
os.makedirs(V30, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"这节日灯挂得真妥当"
AXIS, BUCKET, IDX = u"秩序", u"festival", 2

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V30:
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
# DAILY-v29 xiaoyao/festival/2 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/festival/16 +
# qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 030",
    u"2026-10-02 · 国庆假期",
    u"「这节日灯挂得真妥当」",
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
assert H2_SIZE == 60, "em ladder front-fit: expected notch 60 return (11.0em line vs 15.33em budget), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v30"
meta["form"] = (u"DAILY 城市日签 030（L-卡 图文轻内容线 DAILY 形态第三十件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R999·日签节律续件=日期×情境桶对位判据第三十证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第二十七证=同轴异行第二十五证〔秩序轴 "
                u"DAILY-v5〔line4〕+DAILY-v17〔line12〕+DAILY-v21〔line6〕+DAILY-v28〔line9〕之外线级新鲜行 "
                u"line2·轴面 v6 收官耗尽后线级新鲜度=唯一面·R975 收口注承接·旋转律兑现=秩序轴与逍遥轴并列最少"
                u"消费〔各 4 采·v29 后计数：求新 6/怀旧 5/侠气 5/烟火 5/秩序 4/逍遥 4〕·v28 后 2 件首回=双最少"
                u"轴交替轮换制〕+秩序轴〔最讲规矩·安全安稳第一·验收思维的城市居民〕×「这节日灯挂得真妥当」"
                u"（把满城节日盛装当工程验收来夸的秩序轴本行语感）=装×妥轴内自反差金句位〔v15 屏×真/v16 往×今"
                u"/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心"
                u"/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧=族十六连·秩序轴夸节日三连注："
                u"v21 喜×稳+v28 喜×护+v30 装×妥=同轴主题纵深带〕〕）")
meta["source_quote"] = u"「这节日灯挂得真妥当」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][festival][2]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v29 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][festival][2] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v29 同桶直配第三十证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕"
                         u"+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第二十七证"
                         u"·本行=秩序轴 line2 非 DAILY-v5 line4 非 DAILY-v17 line12 非 DAILY-v21 line6 非 "
                         u"DAILY-v28 line9 非 REACT-v8 line14 非 city-spirit v1.2 line16=同轴异行第二十五证〔六轴"
                         u"收官后秩序轴第五采·轮前 city-spirit NOT_IN 预检复证=r999_pool_scan.txt 全桶预检 FREE "
                         u"56 行=R978 拦截教训执行〕⑥国庆语境核=本行无「年味」措辞（R972 制·灯挂=国庆红旗红灯笼"
                         u"城市盛装季相对位）⑦品牌语感注=「真妥当」=秩序轴最本行的验收词入日常夸赞=机器语感独占位"
                         u"〔v5 校准同族·去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+秩序轴〔最讲规矩·验收"
                         u"思维的城市居民〕×「这节日灯挂得真妥当」〔把满城节日盛装当工程验收来夸〕=装×妥轴内自反差"
                         u"（别人夸灯漂亮好看·规矩轴夸灯挂得妥当=用自己最本行的验收词给节日盛装打分）+满城国庆灯海"
                         u"×秩序轴居民巡看灯挂给出验收词=验收场景层=具体场景面〔R442 审计叙事弱点处方带·v5 校准街灯"
                         u"/v28 巡街值守同族异质行注〕+真城生命感方向对位=最讲规矩的居民用验收标准夸节日灯=灯挂得"
                         u"妥当就是城市把自己的节日也办得井井有条的活证据（城市人文积累令 O-20260928-1910 对位）")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十证+秩序轴"
                            u"旋转律兑现〔与逍遥轴并列最少消费各 4 采·v28 后 2 件首回=双最少轴交替轮换制〕+"
                            u"「这节日灯挂得真妥当」〔把满城节日盛装当工程验收来夸的秩序轴本行语感〕装×妥轴内"
                            u"自反差金句位〔族十六连·秩序轴夸节日三连注：v21 喜×稳+v28 喜×护+v30 装×妥=同轴主题"
                            u"纵深带〕+验收场景层=R442 审计处方带续证+「真妥当」验收词口语真感=人味命中〔CEO "
                            u"审美线对位·机器语感独占位 v5 校准同族〕+灯挂得妥当=城市把节日办得井井有条的活证据"
                            u"=城市人文积累令对位〔真城生命感〕）+语录卡线变体零新模板第三十证（QUOTE-v2 参数 "
                            u"verbatim 复用·h2_size 回归 60 档=v29 单发降档 50 后回归〔11.0em 行长 < 15.33em 预算"
                            u"·R293 零余量排除+R301-313 梯档律·三行栈=v19/v22/v27/v28 同构〕·charter §1「日签"
                            u"变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：这节日灯挂得真妥当〔把满城节日盛装当工程"
                          u"验收来夸的秩序轴本行语感〕×最讲规矩·验收思维的秩序轴=装×妥轴内自反差金句位〔v15 屏×真"
                          u"/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×"
                          u"手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归/v28 喜×护/v29 闲×喧=族十六连〕+满城"
                          u"国庆灯海×秩序轴居民巡看灯挂给出验收词=验收场景层+「真妥当」验收词口语真感/情 1 温和安心"
                          u"共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日灯海=节日场景当日对位+festival 情境桶直配"
                          u"第三十证+池句节日语气常青/台 2 公众号方图承载=MC-001~114 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R999 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（秩序轴居民=轴级群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（灯挂=城市公共装点群像场景非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[zhixu][festival][2] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v29 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness twenty-seventh proof: zhixu line2 != DAILY-v5 line4 != DAILY-v17 line12 != DAILY-v21 line6 != DAILY-v28 line9 != REACT-v8 line14 != city-spirit v1.2 line16 = same-axis-different-line twenty-fifth proof")
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
report.append("LADDER_RETURN: quote line 11.0em < 15.33em budget -> notch 60 returns after v29's one-off step-down to 50 (28+1+1 profile); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r999.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V30, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V30, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v29 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder return to 60) + E4 fired async" % H2_SIZE)
