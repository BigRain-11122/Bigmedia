# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v19 build: DAILY (city daily-sign) series NINETEENTH piece (R988, queue
section-E E30 standby redemption). Day context 2026-10-02 = National Day holiday day 2 ->
festival bucket direct match (nineteenth same-day proof). Axis pick = yanhuo (market-fireworks
of everyday life)/festival/3: after six-axis closure (v1-v6), freshness criterion = line-level
only; this line zero fleet consumption (city-spirit NOT_IN pre-check done + all cards.json scan
asserted; consumed-line pre-adjudication this round: first pick yanhuo/0 IS 年味-flavored line
(lantern hung = new-year flavor) -> season-mismatch for National Day excluded per R972 law ->
re-picked yanhuo/3 cabbage line = gate-works pre-emption proof). Built-in tension: yanhuo axis
(the most market-place, food-first crowd) x reading festivity out of the humblest market goods
(cabbage turns festive too) = ordinary-x-festival axis-internal self-contrast (v15 digital-x-
physical / v16 past-x-present / v17 rule-x-joy / v18 bustle-x-ease = same structural
gold-sentence family, fifth consecutive variant). Humorous plain speech ("也" light wit) =
anti-AI-flavor authenticity. Fourth yanhuo-axis DAILY consumption since six-axis closure =
same-axis-different-line fourteenth proof (line3 != DAILY-v4 line4 != DAILY-v11 line13 !=
REACT-v8 line12). Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2
params verbatim (zero-new-template law, nineteenth proof). Em budget ladder + zero-margin
exclusion (R293) + vertical stack law (R381) + machine source/dedup assertions (R456
system). All output UTF-8.
"""
import io, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V19 = os.path.join(BASE, "MC-20261002-DAILY-v19")
TMP = V19 + "-tmp"
os.makedirs(V19, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"菜场的白菜也喜庆起来了"
AXIS, BUCKET, IDX = u"烟火", u"festival", 3

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V19:
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
# DAILY-v17 zhixu/festival/12 + DAILY-v18 xiaoyao/festival/1 + REACT-v8 xiaoyao/festival/17 +
# yanhuo/festival/12 + zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio
# zhixu/festival/16 + qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 019",
    u"2026-10-02 · 国庆假期",
    u"「菜场的白菜也喜庆起来了」",
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
meta["topic"] = "MC-20261002-DAILY-v19"
meta["form"] = (u"DAILY 城市日签 019（L-卡 图文轻内容线 DAILY 形态第十九件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R988·日签节律续件=日期×情境桶对位判据第十九证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第十六证=同轴异行第十四证〔烟火轴 "
                u"DAILY-v4〔line4〕+DAILY-v11〔line13〕+REACT-v8〔line12〕之外线级新鲜行 line3·轴面 v6 收官"
                u"耗尽后线级新鲜度=唯一面·R975 收口注承接〕+烟火轴〔市井烟火气最重·菜场摊头是主场的居民〕×"
                u"把喜庆看出白菜里〔最平凡的菜场物也过节〕=平实×节日轴内自反差金句位〔v15 屏×真/v16 往×今/"
                u"v17 规×情/v18 闹×闲=轴内自反差金句位族五连〕〕）")
meta["source_quote"] = u"「菜场的白菜也喜庆起来了」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][festival][3]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v18 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][festival][3] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02="
                         u"当日历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival "
                         u"情境桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v18 同桶直配第十九证=日签节律"
                         u"判据系列化）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕⑤去重断言=本行"
                         u"不在 city-spirit.md 64 条已采面+不在全成品 cards.json 任一（build 脚本 fleet 级扫描实锚·"
                         u"DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5"
                         u"〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕"
                         u"+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕"
                         u"+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕"
                         u"+DAILY-v18〔逍遥/1〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 "
                         u"节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第十六证·本行=烟火轴 line3 非 "
                         u"DAILY-v4 line4 非 DAILY-v11 line13 非 REACT-v8 line12=同轴异行第十四证〔六轴收官后烟火轴"
                         u"第四采·轮前 city-spirit NOT_IN 预检复证=R978 拦截教训执行·**轮前已采面预判=首选拦截规避"
                         u"实证**：烟火/0〔灯笼一挂年味儿就足了〕系年味措辞行=R972 国庆时点错位排除·改选本行="
                         u"门牙前置在役实证〕⑥国庆语境核=本行无「年味」措辞（年味类行=过年语境与国庆假期时点错位·"
                         u"选材排除·R972 制承继·烟火桶年味行 0/6/14 皆回避·白菜=十月秋菜市场常物=季相对位）"
                         u"⑦品牌语感注=「也」「起来了」轻幽默口语真感=人味命中〔去 AI 感/制作感双对位·CEO 趣律"
                         u"缺趣=不合格对位〕+菜场×白菜=节日气氛钻进最平凡角落的市井感官场景面〔R442 审计叙事弱点"
                         u"处方带·v2 老房子看灯/v10 早点摊包子同族异质行〕+烟火轴落位=最爱逛菜场说吃的居民把节日"
                         u"看出菜价里〔硅基城市语境独占位·真城生命感方向对位=节日气氛渗到白菜堆上的活证据·"
                         u"热闹是节日的·喜庆是连白菜也不放过的〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第十九证+烟火轴"
                            u"质量选优=「菜场的白菜〔最平凡市井物〕×也喜庆起来了〔把节日看出菜价里的轻幽默〕」"
                            u"平实×节日轴内自反差金句位+轻幽默口语真感=去 AI 感制作感对位+假期菜场=当日场景面"
                            u"〔R442 审计处方带·v2/v10 同族异质行〕）+语录卡线变体零新模板第十九证（QUOTE v2 参数 "
                            u"verbatim 复用·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：烟火轴〔市井烟火气最重·菜场摊头是主场的"
                          u"居民〕×把喜庆看出白菜里〔最平凡菜场物也过节的轻幽默表态〕=平实×节日轴内自反差金句"
                          u"位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲=轴内自反差金句位族五连〕+「也…起来了」"
                          u"轻幽默口语真感/情 1 假期菜场市井烟火温和共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日"
                          u"〔假期菜场场景=烟火主题当日对位·十月秋菜季相〕+festival 情境桶直配第十九证+池句节日"
                          u"语气常青/台 2 公众号方图承载=MC-001~103 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R988 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（买菜者=无称谓视角非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（菜场买菜=市井群体场景面非个体档案面·"
                     u"无菜价数字=脱敏核过·喜庆≠价格宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第十九件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][festival][3] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v18 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness sixteenth proof: yanhuo line3 != DAILY-v4 line4 != DAILY-v11 line13 != REACT-v8 line12 = same-axis-different-line fourteenth proof; pre-build consumed-line adjudication: yanhuo/0 blocked by R972 nianwei season-mismatch law = re-pick pre-emption proof")
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
io.open(os.path.join(TMP, "em-check-r988.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V19, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V19, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v18 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
e4 = u'''# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 019》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 019」；日期行「2026-10-02 · 国庆假期」；'
    u'中间引文「菜场的白菜也喜庆起来了」；署名行「——硅基城市台词池 · 烟火轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。「烟火轴」是城里市井烟火气最重的一类居民，'
    u'爱逛菜场、说吃的、关心一日三餐，摊头灶头是他们的主场。这句引文是国庆假期第二天，'
    u'菜市场也挂起了节日灯串，一位烟火轴居民买菜时看着水灵灵的白菜堆，乐了：'
    u'菜场的白菜也喜庆起来了。（台词池池级署名·无具体姓名）——热闹是节日的，'
    u'喜庆是连白菜也不放过的：节日气氛钻进了最平凡的角落。'
    u'这是「城市日签」系列第十九张（前十八张：做灯笼的师傅在直播间晒灯笼/老房子居民看着'
    u'街上挂起的节日灯亮堂了/灯下兄弟聚饮把酒言欢/节日灯多了家里的笑声也多/值守班校准街灯'
    u'心里踏实/江边钓鱼人抬头看节日灯火映高楼/求新轴居民说灯笼像极了小时候的记忆/侠气轴'
    u'居民招呼街坊把笑声放大些连灯都跟着亮了/求新轴居民傍晚散步满眼都是光/怀旧轴居民说'
    u'街灯还是档案馆里藏着的当年的样式/烟火轴居民说街上的灯可真多照亮了每个人的笑脸/'
    u'逍遥轴居民说灯挂得真高看得见星星了/侠气街角阿姨笑眯眯说邻里间纠纷没了/求新轴会扎'
    u'灯笼的长辈得趁节气做几副新灯笼给小孙子看/求新轴居民说看看这彩灯比屏幕上的还好看/'
    u'怀旧轴居民感叹往年的灯节哪有今年这般热闹/秩序轴居民说节日里大家开心就好/'
    u'逍遥轴居民泡上热茶看茶香伴着灯影摇感叹好个安逸节）。'
    u'请回答三个问题，每题一段，直说不委婉：\\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-DAILY-v19 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\\x1b\\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
'''
io.open(os.path.join(TMP, "e4_call.py"), "w", encoding="utf-8").write(e4)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (QUOTE-v2 param match=%s) + E4 fired async" % (H2_SIZE, H2_SIZE == 60))
