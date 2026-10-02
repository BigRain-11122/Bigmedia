# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v28 build: DAILY (city daily-sign) series TWENTY-EIGHTH piece (R997, queue
section-E E30 standby redemption). Day context 2026-10-02 = National Day holiday day 2 ->
festival bucket direct match (twenty-eighth same-day proof). Axis pick = zhixu (order /
rules-and-calibration residents)/festival/9: rotation law = zhixu axis only 3 DAILY
consumptions so far (v5/v17/v21, last one seven pieces ago) = due axis; this line zero fleet
consumption (city-spirit NOT_IN pre-check + all cards.json scan asserted; consumed festival
lines for zhixu axis = DAILY-v5 line4 + DAILY-v17 line12 + DAILY-v21 line6 + REACT-v8 line14
+ city-spirit line16 -> line9 fresh). Built-in tension: 这节日氛围，得好好维护 (the order axis
loving the festival in its own infrastructural way - treating the city's joy as a public
asset worth upkeep) = 喜×护 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present
/ v17 rule-x-joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-
steady / v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time
/ v26 hard-x-soft / v27 bustle-x-homecoming = same structural gold-sentence family,
fourteenth consecutive variant; v21 joy-x-steady = adjacent-pair sibling line noted). Scene
layer: holiday lamp-sea all over the city + the order residents on their rounds treating the
festive atmosphere like a system worth maintaining = concrete duty scene (R442 audit
weakness prescription band). Plain speech ("得好好维护" = the order axis's own colloquial
work-voice) = anti-AI-flavor authenticity. Living-city proof = even joy has keepers in this
city - the rules-and-calibration residents love the festival the way they know best
(city humane-accumulation order echo). Fourth zhixu-axis DAILY consumption = same-axis-
different-line twenty-third proof. Quote verbatim + card framing (R285 QUOTE precedent).
Layout = QUOTE-v2 params verbatim (zero-new-template law, twenty-eighth proof; single-line
quote with comma = v17 design precedent, four-LINES stack = v19/v22/v27 isomorphic). Em
budget ladder + zero-margin exclusion (R293) + vertical stack law (R381) + machine
source/dedup assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V28 = os.path.join(BASE, "MC-20261002-DAILY-v28")
TMP = V28 + "-tmp"
os.makedirs(V28, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"这节日氛围，得好好维护"
AXIS, BUCKET, IDX = u"秩序", u"festival", 9

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V28:
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
# DAILY-v26 xiaqi/festival/10 + DAILY-v27 yanhuo/festival/7 +
# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts) +
# city-spirit v1.2 festival-scene trio zhixu/festival/16 + qiuxin/festival/14 +
# xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 028",
    u"2026-10-02 · 国庆假期",
    u"「这节日氛围，得好好维护」",
    u"——硅基城市台词池 · 秩序轴",
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
meta["topic"] = "MC-20261002-DAILY-v28"
meta["form"] = (u"DAILY 城市日签 028（L-卡 图文轻内容线 DAILY 形态第二十八件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R997·日签节律续件=日期×情境桶对位判据第二十八证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第二十五证=同轴异行第二十三证〔秩序轴 "
                u"DAILY-v5〔line4〕+DAILY-v17〔line12〕+DAILY-v21〔line6〕之外线级新鲜行 line9·轴面 v6 收官耗尽"
                u"后线级新鲜度=唯一面·R975 收口注承接·旋转律=秩序轴 DAILY 仅 3 采最欠轮换之一·v21 后 7 件首回〕"
                u"+秩序轴〔最讲规矩最爱校准的城市规则维护者〕×「这节日氛围，得好好维护」（把满城喜庆当公共设施"
                u"来爱护的本行式疼爱）=喜×护轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 平实"
                u"×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归"
                u"=族十四连·v21 喜×稳=邻对同族异质行注〕+国庆灯海满城×秩序轴巡街值守把节日气氛当系统来维护="
                u"值守场景层〕〕）")
meta["source_quote"] = u"「这节日氛围，得好好维护」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][festival][9]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v27 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][festival][9] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行带逗号=v17 设计排版先例·build 脚本内断言=池行逐字在位实锚）"
                         u"②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）"
                         u"③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v27 同桶直配第"
                         u"二十八证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权红线零接触·charter "
                         u"§2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 cards.json 任一（build "
                         u"脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+"
                         u"DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8"
                         u"〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12"
                         u"〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16"
                         u"〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20"
                         u"〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24"
                         u"〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+REACT-v8 同桶"
                         u"三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕"
                         u"皆非本行=线级新鲜度第二十五证·本行=秩序轴 line9 非 DAILY-v5 line4 非 DAILY-v17 line12 非 "
                         u"DAILY-v21 line6=同轴异行第二十三证〔六轴收官后秩序轴第四采·轮前 city-spirit NOT_IN 预检"
                         u"复证=r997_pool_scan.txt 全桶预检 FREE 58 行=R978 拦截教训执行〕⑥国庆语境核=本行无「年味」"
                         u"措辞（R972 制·维护氛围=节日公共面措辞与国庆时点对位）⑦品牌语感注=「得好好维护」=秩序轴"
                         u"最本行的工作口语真感=人味命中〔去 AI 感/制作感双对位·CEO 趣律缺趣=不合格对位〕+秩序轴"
                         u"〔最讲规矩最爱校准的城市规则维护者〕×「这节日氛围，得好好维护」〔把满城喜庆当公共设施"
                         u"来爱护〕=喜×护轴内自反差（最讲规矩的居民爱节日的方式是给它做维护值守）+国庆灯海满城×"
                         u"巡街值守把节日气氛当系统来维护=值守场景层=具体场景面〔R442 审计叙事弱点处方带〕+真城"
                         u"生命感方向对位=城市的快乐也有人值守〔城市人文积累令 O-20260928-1910 对位·喜庆不是自发"
                         u"飘着的是有人守着的=城市在运转的活证据〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第二十八证+秩序轴"
                            u"旋转律兑现〔DAILY 仅 3 采最欠轮换之一·v21 后 7 件首回〕+「这节日氛围，得好好维护」"
                            u"〔把满城喜庆当公共设施来爱护〕喜×护轴内自反差金句位〔族十四连·v21 喜×稳邻对同族"
                            u"异质行注〕+值守场景层=R442 审计处方带续证+「得好好维护」工作口语真感=人味命中"
                            u"〔CEO 审美线对位〕+城市的快乐也有人值守=城市人文积累令对位〔真城生命感·喜庆有人守"
                            u"着=城市在运转的活证据〕）+语录卡线变体零新模板第二十八证（QUOTE v2 参数 verbatim "
                            u"复用·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·"
                            u"charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：这节日氛围，得好好维护〔把满城喜庆当公共"
                          u"设施来爱护的本行式疼爱〕×最讲规矩最爱校准的秩序轴=喜×护轴内自反差金句位〔v15 屏×真"
                          u"/v16 往×今/v17 规×情/v18 闹×闲/v19 平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×"
                          u"手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 闹×归=族十四连〕+国庆灯海满城×巡街值守把"
                          u"节日气氛当系统来维护=值守场景层+「得好好维护」工作口语真感/情 1 规矩式疼爱温和共鸣"
                          u"如实非强极点/时 2 当日时点=国庆假期第 2 日灯海=节日场景当日对位+festival 情境桶直配"
                          u"第二十八证+池句节日语气常青/台 2 公众号方图承载=MC-001~112 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R997 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（秩序轴居民=轴级群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（氛围维护=公共面群像值守关怀非个体档案"
                     u"面）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第二十八件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[zhixu][festival][9] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v27 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness twenty-fifth proof: zhixu line9 != DAILY-v5 line4 != DAILY-v17 line12 != DAILY-v21 line6 = same-axis-different-line twenty-third proof")
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
io.open(os.path.join(TMP, "em-check-r997.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V28, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V28, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v27 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (QUOTE-v2 param match=%s) + E4 fired async" % (H2_SIZE, H2_SIZE == 60))
