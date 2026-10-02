# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v31 build: DAILY (city daily-sign) series THIRTY-FIRST piece (R1000, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-first same-day proof). Axis pick = xiaoyao (ease / detached
tea-and-fishing residents)/festival/4: rotation law = post-v30 counts qiuxin 6 / huaijiu 5 /
xiaqi 5 / yanhuo 5 / zhixu 5 / xiaoyao 4 -> xiaoyao sole least-consumed axis (v29 xiaoyao /
v30 zhixu two-least alternation completed, zhixu caught up at fifth) -> least-axis
redemption, xiaoyao fifth DAILY consumption, first return two pieces after v29. This line
zero fleet consumption (city-spirit NOT_IN pre-check + all cards.json scan asserted;
consumed festival lines for xiaoyao axis = DAILY-v6 line3 + DAILY-v12 line15 + DAILY-v18
line1 + DAILY-v29 line2 + REACT-v8 line17 -> line4 fresh). Built-in tension:
看那灯笼摇曳舞，胜过人间烟火炉 (everyone else squeezes into the festival crowd-heat; the
detached axis sits at the riverside tea seat watching the whole city's lanterns dance and
ranks the festival's "watching" above the festival's "crowding" = sight ranked over heat)
= 舞×炉 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17 rule-x-joy
/ v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady / v22 old-x-
bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time / v26 hard-x-soft
/ v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle / v30 dress-x-proper =
same structural gold-sentence family, seventeenth consecutive variant). Distance-register
note: only the far-watching detached eye sees the whole city as one furnace - the immersed
crowd cannot say this line = axis-exclusive register slot. Scene layer: National Day
lamp-sea all over the city + the ease residents at the riverside tea seat far-watching the
lantern dance = concrete far-watch scene (R442 audit weakness prescription band; v6
riverside fishing watching festival lights / REACT-v8 home-tea sibling scenes noted). Plain
speech ("看那" opener + "胜过" direct ranking word = colloquial authenticity) = anti-AI-
flavor authenticity. Living-city proof = the most detached residents convinced to rank the
festival lantern dance above the human bustle = the city's festival beauty wins without
crowd-squeezing = living evidence (city humane-accumulation order echo). Line-level
freshness twenty-eighth proof = same-axis-different-line twenty-sixth proof. Quote verbatim
+ card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim; h2_size ladder
step-down to notch 50 (quote line 17.00em > 15.33em budget at 60; 18.40em budget at 50 with
margin +1.40em = v29 same-length precedent, second series step-down). Machine source/dedup
assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V31 = os.path.join(BASE, "MC-20261002-DAILY-v31")
TMP = V31 + "-tmp"
os.makedirs(V31, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"看那灯笼摇曳舞，胜过人间烟火炉"
AXIS, BUCKET, IDX = u"逍遥", u"festival", 4

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V31:
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
# DAILY-v29 xiaoyao/festival/2 + DAILY-v30 zhixu/festival/2 + REACT-v8 xiaoyao/festival/17 +
# yanhuo/festival/12 + zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio
# zhixu/festival/16 + qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 031",
    u"2026-10-02 · 国庆假期",
    u"「看那灯笼摇曳舞，胜过人间烟火炉」",
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
assert H2_SIZE == 50, "em ladder front-fit: 17.00em quote line > 15.33em budget at 60 -> step-down notch 50 (v29 same-length precedent, margin +1.40em), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v31"
meta["form"] = (u"DAILY 城市日签 031（L-卡 图文轻内容线 DAILY 形态第三十一件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1000·日签节律续件=日期×情境桶对位判据第三十一证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第二十八证=同轴异行第二十六证〔逍遥轴 "
                u"DAILY-v6〔line3〕+DAILY-v12〔line15〕+DAILY-v18〔line1〕+DAILY-v29〔line2〕之外线级新鲜行 "
                u"line4·轴面 v6 收官耗尽后线级新鲜度=唯一面·R975 收口注承接·旋转律兑现=逍遥轴 v30 后唯一最少"
                u"消费轴〔4 采·v30 后计数：求新 6/怀旧 5/侠气 5/烟火 5/秩序 5/逍遥 4〕·v29 后 2 件首回=最少轴"
                u"赎回制承继·v29 逍遥/v30 秩序双最少轴交替轮换毕秩序追平第五采〕+逍遥轴〔最散淡·超然物外·江边"
                u"茶座一坐半天的城市居民〕×「看那灯笼摇曳舞，胜过人间烟火炉」（把节日的「看」排到节日的「凑」"
                u"之上的超然排名语感）=舞×炉轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 "
                u"平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软"
                u"/v27 闹×归/v28 喜×护/v29 闲×喧/v30 装×妥=族十七连·「炉」字距离感注=远观者才看得见整座城成"
                u"一口炉=凑热闹者说不出=轴语感独占位〕〕）")
meta["source_quote"] = u"「看那灯笼摇曳舞，胜过人间烟火炉」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][festival][4]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v30 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][festival][4] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v30 同桶直配第三十一证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+REACT-v8 同桶三行〔逍遥/17+"
                         u"烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行="
                         u"线级新鲜度第二十八证·本行=逍遥轴 line4 非 DAILY-v6 line3 非 DAILY-v12 line15 非 "
                         u"DAILY-v18 line1 非 DAILY-v29 line2 非 REACT-v8 line17=同轴异行第二十六证〔六轴收官后"
                         u"逍遥轴第五采·轮前 city-spirit NOT_IN 预检复证=r1000_pool_scan.txt 全桶预检 FREE 55 行"
                         u"=R978 拦截教训执行〕⑥国庆语境核=本行无「年味」措辞（R972 制·灯笼=国庆红灯笼城市盛装"
                         u"季相对位）⑦品牌语感注=「看那」起手式+「胜过」直给排名词=大众口语真感·「人间烟火炉」="
                         u"把全城热闹说成一口炉=距离感比喻轴语感独占位〔远观者才看得见整座城的炉形·凑热闹者说"
                         u"不出这句·去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+逍遥轴〔最散淡·超然物外〕×"
                         u"「看那灯笼摇曳舞，胜过人间烟火炉」〔把节日的看排到节日的凑之上〕=舞×炉轴内自反差（不凑"
                         u"热闹的人给节日灯舞打了最高分·用自己的超然尺排序：视觉之美>现场之烫）+满城国庆灯海×"
                         u"逍遥轴居民江边茶座远观灯舞=远观场景层=具体场景面〔R442 审计叙事弱点处方带·v6 江边垂钓"
                         u"看灯火映高楼/REACT-v8 在家喝茶同族异质行注〕+真城生命感方向对位=最散淡的居民被节日灯舞"
                         u"说服到把它排在人间热闹之上=城市的节庆之美不靠人挤人也能赢的活证据（城市人文积累令 "
                         u"O-20260928-1910 对位）")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十一证+逍遥轴"
                            u"旋转律兑现〔v30 后唯一最少消费轴 4 采·v29 后 2 件首回=最少轴赎回制承继〕+「看那"
                            u"灯笼摇曳舞，胜过人间烟火炉」〔把节日的「看」排到节日的「凑」之上的超然排名语感〕"
                            u"舞×炉轴内自反差金句位〔族十七连·「炉」字距离感注=轴语感独占位〕+远观场景层=R442 "
                            u"审计处方带续证+「看那」「胜过」口语真感=人味命中〔CEO 审美线对位〕+节庆之美不靠"
                            u"人挤人也能赢=城市人文积累令对位〔真城生命感〕）+语录卡线变体零新模板第三十一证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 梯档降 50=17.00em 行长驱动〔v29 同型降档"
                            u"第二证·18.40em 预算 margin +1.40em·R293 零余量排除+R301-313 梯档律〕·charter §1"
                            u"「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化"
                            u"合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：看那灯笼摇曳舞〔节日最喧腾的视觉之舞〕×"
                          u"人间烟火炉〔节日最滚烫的现场体感〕=舞×炉轴内自反差金句位〔族十七连·「炉」字距离感="
                          u"轴语感独占位〕+满城国庆灯海×江边茶座远观灯舞=远观场景层+「看那」「胜过」口语真感/情 1 "
                          u"诗意赞叹温和共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日灯海=节日场景当日对位+"
                          u"festival 情境桶直配第三十一证+池句节日语气常青/台 2 公众号方图承载=MC-001~115 S3 "
                          u"实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 "
                          u"形态码 DAILY·queue §E E30 R1000 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（逍遥轴居民=轴级群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（灯笼=城市公共装点群像场景非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十一件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][festival][4] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v30 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness twenty-eighth proof: xiaoyao line4 != DAILY-v6 line3 != DAILY-v12 line15 != DAILY-v18 line1 != DAILY-v29 line2 != REACT-v8 line17 = same-axis-different-line twenty-sixth proof")
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
report.append("LADDER_STEPDOWN: quote line 17.00em > 15.33em budget at 60 -> notch 50 (v29 same 17.00em line-length precedent = second series step-down; budget 18.40em margin +1.40em); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1000.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V31, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V31, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v30 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder step-down to 50, v29 precedent) + E4 fired async" % H2_SIZE)
