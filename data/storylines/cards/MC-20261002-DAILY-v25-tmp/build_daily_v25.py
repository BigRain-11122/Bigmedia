# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v25 build: DAILY (city daily-sign) series TWENTY-FIFTH piece (R994, queue
section-E E30 standby redemption). Day context 2026-10-02 = National Day holiday day 2 ->
festival bucket direct match (twenty-fifth same-day proof). Axis pick = huaijiu (nostalgia
/ old-things residents)/festival/17: after six-axis closure (v1-v6), freshness criterion =
line-level only; this line zero fleet consumption (city-spirit NOT_IN pre-check + all
cards.json scan asserted; consumed festival lines for huaijiu axis = DAILY-v2 line0 +
DAILY-v10 line3 + DAILY-v16 line1 + DAILY-v22 line12 -> line17 fresh). Built-in tension:
这灯串儿 (the most in-season festival dressing, hung fresh each year) x 得有几十年光景了
(the deepest time depth) = new-season-x-old-time axis-internal self-contrast (v15
screen-x-real / v16 past-x-present / v17 rule-x-joy / v18 bustle-x-ease / v19 plain-x-
festival / v20 rest-x-busy / v21 joy-x-steady / v22 old-x-bustle / v23 new-x-craft / v24
bustle-x-heart = same structural gold-sentence family, eleventh consecutive variant).
Same-family heterogeneous note: v10 archive-house lamp (institutional archive) x this
street lamp-string (living street archive) = city-memory band; plain speech ("串儿"
"得有…了" "光景" colloquial) = anti-AI-flavor authenticity + street lamp-string scene =
concrete scene (R442 audit weakness prescription band). Living-city proof = the most
nostalgic residents read decades of time in the freshest festival dressing - the city's
memory lives on the street (city humane-accumulation order echo). Fifth huaijiu-axis
DAILY consumption (v2/v10/v16/v22 + this) = same-axis-different-line twentieth proof.
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params verbatim
(zero-new-template law, twenty-fifth proof; single-line quote = v19/v22 short-sentence
data-layer variant). Em budget ladder + zero-margin exclusion (R293) + vertical stack law
(R381) + machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V25 = os.path.join(BASE, "MC-20261002-DAILY-v25")
TMP = V25 + "-tmp"
os.makedirs(V25, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"这灯串儿得有几十年光景了"
AXIS, BUCKET, IDX = u"怀旧", u"festival", 17

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V25:
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
# DAILY-v23 qiuxin/festival/13 + DAILY-v24 yanhuo/festival/2 +
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 025",
    u"2026-10-02 · 国庆假期",
    u"「这灯串儿得有几十年光景了」",
    u"——硅基城市台词池 · 怀旧轴",
]

SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]  # QUOTE-v2 own size 60 first = zero-template change
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
assert H2_SIZE == 60, "zero-template law: expected QUOTE-v2 h2_size 60, got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v25"
meta["form"] = (u"DAILY 城市日签 025（L-卡 图文轻内容线 DAILY 形态第二十五件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R994·日签节律续件=日期×情境桶对位判据第二十五证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第二十二证=同轴异行第二十证〔怀旧轴 "
                u"DAILY-v2〔line0〕+DAILY-v10〔line3〕+DAILY-v16〔line1〕+DAILY-v22〔line12〕之外线级新鲜行 "
                u"line17·轴面 v6 收官耗尽后线级新鲜度=唯一面·R975 收口注承接〕+怀旧轴〔最爱念旧·最珍藏往年"
                u"时光〕×几十年光景〔最长的时间纵深〕=新时×旧光轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×"
                u"情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心=族十一连〕〕）")
meta["source_quote"] = u"「这灯串儿得有几十年光景了」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][festival][17]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v24 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][festival][17] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行=短句数据层变体〔v19/v22 先例〕·build 脚本内断言=池行逐字"
                         u"在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位·"
                         u"DAILY-v1~v24 同桶直配第二十五证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+"
                         u"DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+"
                         u"DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+"
                         u"DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+"
                         u"DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+"
                         u"DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+"
                         u"city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第二十二证·"
                         u"本行=怀旧轴 line17 非 DAILY-v2 line0 非 DAILY-v10 line3 非 DAILY-v16 line1 非 "
                         u"DAILY-v22 line12=同轴异行第二十证〔六轴收官后怀旧轴第五采·轮前 city-spirit NOT_IN 预检"
                         u"复证=r994_pool_scan.txt 全桶预检 FREE 61 行=R978 拦截教训执行〕⑥国庆语境核=本行无「年味」"
                         u"措辞（灯串=国庆灯饰季相对位·年味类行=过年语境与国庆时点错位·选材排除·R972 制承继）"
                         u"⑦品牌语感注=「串儿」「得有…了」「光景」大众口语真感=人味命中〔去 AI 感/制作感双对位·CEO "
                         u"趣律缺趣=不合格对位〕+怀旧轴〔最应季最当令的节日装点〕×几十年光景〔最长的时间纵深〕="
                         u"新时×旧光轴内自反差（最念旧的居民在最新的节日装点里读出最长的时光=城市记忆活在街面）+"
                         u"街边灯串=具体场景面〔R442 审计叙事弱点处方带·v10 档案馆〔institutional archive〕×本件"
                         u"〔street living archive〕=城市记忆带同族异质行〕+真城生命感方向对位=最念旧的居民把节日"
                         u"灯串看成几十年活档案〔城市人文积累令 O-20260928-1910 对位·街面记忆不进博物馆=城市在"
                         u"积累的活证据〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第二十五证+怀旧轴"
                            u"质量选优=「这灯串儿〔最应季的节日装点·年年新挂〕×得有几十年光景了〔最长的时间纵深〕」"
                            u"新时×旧光轴内自反差金句位〔族十一连〕+街边灯串=具体场景面=R442 审计处方带续证+「串儿」"
                            u"「得有…了」「光景」大众口语真感=人味命中〔CEO 审美线对位〕+最念旧的居民把节日灯串看成"
                            u"几十年活档案=城市人文积累令对位〔真城生命感〕）+语录卡线变体零新模板第二十五证"
                            u"（QUOTE v2 参数 verbatim 复用·charter §1「日签变体随时可续」兑现）·公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：这灯串儿〔最应季最当令的节日装点·年年"
                          u"新挂〕×得有几十年光景了〔最长的时间纵深〕=新时×旧光轴内自反差金句位〔v15 屏×真/v16 往×今"
                          u"/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心"
                          u"=轴内自反差金句位族十一连〕+「串儿」「得有…了」大众口语真感/情 1 时间纵深温和共鸣如实"
                          u"非强极点/时 2 当日时点=国庆假期第 2 日〔街边挂灯串=节日场景当日对位〕+festival 情境桶直配"
                          u"第二十五证+池句节日语气常青/台 2 公众号方图承载=MC-001~108 S3 实证复用）——"
                          u"hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·"
                          u"queue §E E30 R994 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（怀旧轴居民=轴级群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（灯串=公共设施群像面非个体档案面·几十年光景="
                     u"物件时间描述面非居民私人档案）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第二十五件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[huaijiu][festival][17] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v24 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness twenty-second proof: huaijiu line17 != DAILY-v2 line0 != DAILY-v10 line3 != DAILY-v16 line1 != DAILY-v22 line12 = same-axis-different-line twentieth proof")
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
report.append(u"H1 %d budget %.2fem | H2 %d budget %.2fem (ladder pick, margin>=%.1fem) | VERT stack bottom %.0fpx vs subs top %dpx gap %+.0fpx (need >=%d) R381" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM, vb, SUBS_TOP, SUBS_TOP - vb, GAP_MIN))
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
io.open(os.path.join(TMP, "em-check-r994.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V25, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V25, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v24 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (QUOTE-v2 param match=%s) + E4 fired async" % (H2_SIZE, H2_SIZE == 60))
