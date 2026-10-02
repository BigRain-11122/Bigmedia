# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v27 build: DAILY (city daily-sign) series TWENTY-SEVENTH piece (R996, queue
section-E E30 standby redemption). Day context 2026-10-02 = National Day holiday day 2 ->
festival bucket direct match (twenty-seventh same-day proof). Axis pick = yanhuo (street-fire /
market-stall residents who treat neighbors as family)/festival/7: after six-axis closure
(v1-v6), freshness criterion = line-level only; this line zero fleet consumption (city-spirit
NOT_IN pre-check + all cards.json scan asserted; consumed festival lines for yanhuo axis =
DAILY-v4 line4 + DAILY-v11 line13 + DAILY-v19 line3 + DAILY-v24 line2 + REACT-v8 line12 ->
line7 fresh). Built-in tension: 晚上早点回家，别冻着了 (the most quotidian family caring
phrase) said by the axis that loves street bustle the most, on the brightest festival night =
bustle-x-homecoming axis-internal self-contrast (v15 screen-x-real / v16 past-x-present /
v17 rule-x-joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-
steady / v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time
/ v26 hard-x-soft = same structural gold-sentence family, thirteenth consecutive variant).
Scene layer: festival lamp-sea blazing outside + the caring call to come home early = concrete
home-street scene (R442 audit weakness prescription band). Plain speech ("早点回家" "别冻着
了" colloquial caring) = anti-AI-flavor authenticity. Living-city proof = the residents who
love the bustle the most are the first to think of people going home warm on a chilly October
night - the city's warmth lives in its street-fire voice (city humane-accumulation order
echo). Sixth yanhuo-axis DAILY consumption (v4/v11/v19/v24 + this + REACT-v8 line12 outside
DAILY) = same-axis-different-line twenty-second proof. Quote verbatim + card framing (R285
QUOTE precedent). Layout = QUOTE-v2 params verbatim (zero-new-template law, twenty-seventh
proof; single-line quote with comma = v17 design precedent, four-LINES stack = v19/v22
isomorphic). Em budget ladder + zero-margin exclusion (R293) + vertical stack law (R381) +
machine source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V27 = os.path.join(BASE, "MC-20261002-DAILY-v27")
TMP = V27 + "-tmp"
os.makedirs(V27, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"晚上早点回家，别冻着了"
AXIS, BUCKET, IDX = u"烟火", u"festival", 7

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V27:
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
# DAILY-v26 xiaqi/festival/10 +
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 027",
    u"2026-10-02 · 国庆假期",
    u"「晚上早点回家，别冻着了」",
    u"——硅基城市台词池 · 烟火轴",
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
meta["topic"] = "MC-20261002-DAILY-v27"
meta["form"] = (u"DAILY 城市日签 027（L-卡 图文轻内容线 DAILY 形态第二十七件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R996·日签节律续件=日期×情境桶对位判据第二十七证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第二十四证=同轴异行第二十二证〔烟火轴 "
                u"DAILY-v4〔line4〕+DAILY-v11〔line13〕+DAILY-v19〔line3〕+DAILY-v24〔line2〕之外线级新鲜行 "
                u"line7·轴面 v6 收官耗尽后线级新鲜度=唯一面·R975 收口注承接〕+烟火轴〔市井烟火气最重·菜场摊头"
                u"是主场·把街坊当家人·最爱往人堆里凑热闹〕×「晚上早点回家，别冻着了」（最家常的家人式叮嘱）"
                u"=闹×归轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/"
                u"v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软=族十三连〕+节日灯海最亮"
                u"的夜里×催人回家的叮嘱=灯再亮不如家里那盏=夜×家场景层〔v24 灯→心里头同族异质行〕〕）")
meta["source_quote"] = u"「晚上早点回家，别冻着了」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][festival][7]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v26 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][festival][7] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行带逗号=v17 设计排版先例·build 脚本内断言=池行逐字"
                         u"在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位·"
                         u"DAILY-v1~v26 同桶直配第二十七证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+"
                         u"DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+"
                         u"DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+"
                         u"DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+"
                         u"DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+"
                         u"DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+"
                         u"REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+"
                         u"求新/14+侠气/0〕皆非本行=线级新鲜度第二十四证·本行=烟火轴 line7 非 DAILY-v4 line4 非 "
                         u"DAILY-v11 line13 非 DAILY-v19 line3 非 DAILY-v24 line2=同轴异行第二十二证〔六轴收官后"
                         u"烟火轴第六采·轮前 city-spirit NOT_IN 预检复证=r996_pool_scan.txt 全桶预检 FREE 59 行="
                         u"R978 拦截教训执行〕⑥国庆语境核=本行无「年味」措辞（夜里凉提醒=十月秋夜真实体感=季相"
                         u"对位·年味类行=过年语境与国庆时点错位·选材排除·R972 制承继）⑦品牌语感注=「早点回家」"
                         u"「别冻着了」中国家庭最高频关心话=大众口语真感=人味命中〔去 AI 感/制作感双对位·CEO 趣律"
                         u"缺趣=不合格对位〕+烟火轴〔市井烟火气最重·最爱往人堆里凑热闹〕×「晚上早点回家，别冻着"
                         u"了」〔最往回收的家人式叮嘱〕=闹×归轴内自反差（最爱热闹的市井居民在节日最亮的夜里先"
                         u"想到的是人回家夜里凉）+灯再亮不如家里那盏=夜×家场景层〔v24 灯→心里头同族异质行〕="
                         u"具体场景面〔R442 审计叙事弱点处方带〕+真城生命感方向对位=最爱热闹的居民最先心疼人"
                         u"〔城市人文积累令 O-20260928-1910 对位·节日灯海越亮城市越暖=城市在变暖的活证据〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第二十七证+烟火轴"
                            u"质量选优=「晚上早点回家〔最往回收的家人式叮嘱〕×别冻着了〔十月秋夜真实体感〕」闹×归"
                            u"轴内自反差金句位〔族十三连〕+夜×家场景层=v24 灯→心里头同族异质行·具体场景面=R442 "
                            u"审计处方带续证+「早点回家」「别冻着了」大众口语真感=人味命中〔CEO 审美线对位〕+最爱"
                            u"热闹的居民最先心疼人=城市人文积累令对位〔真城生命感·灯再亮不如家里那盏〕）+语录卡线"
                            u"变体零新模板第二十七证（QUOTE v2 参数 verbatim 复用·charter §1「日签变体随时可续」"
                            u"兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：晚上早点回家，别冻着了〔最家常的家人式叮嘱〕×"
                          u"最爱往人堆里凑热闹的烟火轴=闹×归轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 "
                          u"闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×"
                          u"旧光/v26 硬×软=族十三连〕+灯再亮不如家里那盏=夜×家场景层〔v24 灯→心里头同族异质行〕+"
                          u"「早点回家」「别冻着了」大众口语真感/情 1 家人式关怀温和共鸣如实非强极点/时 2 当日时点="
                          u"国庆假期第 2 日夜里灯海=节日场景当日对位+十月秋夜体感季相对位+festival 情境桶直配"
                          u"第二十七证+池句节日语气常青/台 2 公众号方图承载=MC-001~111 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R996 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（烟火轴居民=轴级群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（回家叮嘱=家人式群像关怀面非个体档案面·"
                     u"夜里体感=季节气候描述面非居民私人档案）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第二十七件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][festival][7] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v26 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness twenty-fourth proof: yanhuo line7 != DAILY-v4 line4 != DAILY-v11 line13 != DAILY-v19 line3 != DAILY-v24 line2 = same-axis-different-line twenty-second proof")
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
io.open(os.path.join(TMP, "em-check-r996.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V27, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V27, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v26 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (QUOTE-v2 param match=%s) + E4 fired async" % (H2_SIZE, H2_SIZE == 60))
