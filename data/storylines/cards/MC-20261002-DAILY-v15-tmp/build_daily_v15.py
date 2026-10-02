# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v15 build: DAILY (city daily-sign) series FIFTEENTH piece (R984, queue
section-E E30 standby redemption). Day context 2026-10-02 = National Day holiday day 2 ->
festival bucket direct match (fifteenth same-day proof). Axis pick = qiuxin/festival/11:
after six-axis closure (v1-v6), freshness criterion = line-level only; this line zero fleet
consumption (city-spirit NOT_IN check done + all cards.json scan asserted). Built-in tension:
qiuxin axis (the novelty-hungriest, screen-native, most forward-looking crowd) x saying real
festival lanterns look better than screens (the digital-native crowd conceding the physical
world wins) = digital-x-physical axis-internal self-contrast; festival eve walk-and-look
scene = same-day National Day lantern direct match. Fifth qiuxin-axis consumption since
six-axis closure = same-axis-different-line tenth proof (line11 != v1 line4 != v7 line7 !=
v9 line12 != v14 line3). Quote verbatim + card framing (R285 QUOTE precedent). Layout =
QUOTE-v2 params verbatim (zero-new-template law, fifteenth proof). Em budget ladder +
zero-margin exclusion (R293) + vertical stack law (R381) + machine source/dedup assertions
(R456 system). All output UTF-8.
"""
import io, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V15 = os.path.join(BASE, "MC-20261002-DAILY-v15")
TMP = V15 + "-tmp"
os.makedirs(V15, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"看看这彩灯，比屏幕上的还好看"
AXIS, BUCKET, IDX = u"求新", u"festival", 11

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V15:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        assert QUOTE_CORE not in io.open(cj, encoding="utf-8").read(), "line already consumed by %s" % d
# consumed festival lines (documented not asserted): DAILY-v1 qiuxin/festival/4 +
# DAILY-v2 huaijiu/festival/0 + DAILY-v3 xiaqi/festival/5 + DAILY-v4 yanhuo/festival/4 +
# DAILY-v5 zhixu/festival/4 + DAILY-v6 xiaoyao/festival/3 + DAILY-v7 qiuxin/festival/7 +
# DAILY-v8 xiaqi/festival/13 + DAILY-v9 qiuxin/festival/12 + DAILY-v10 huaijiu/festival/3 +
# DAILY-v11 yanhuo/festival/13 + DAILY-v12 xiaoyao/festival/15 + DAILY-v13 xiaqi/festival/2 +
# DAILY-v14 qiuxin/festival/3 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 015",
    u"2026-10-02 · 国庆假期",
    u"「看看这彩灯，",
    u"比屏幕上的还好看」",
    u"——硅基城市台词池 · 求新轴",
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
meta["topic"] = "MC-20261002-DAILY-v15"
meta["form"] = (u"DAILY 城市日签 015（L-卡 图文轻内容线 DAILY 形态第十五件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R984·日签节律续件=日期×情境桶对位判据第十五证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第十二证=同轴异行第十证〔求新轴 "
                u"DAILY-v1〔line4〕+DAILY-v7〔line7〕+DAILY-v9〔line12〕+DAILY-v14〔line3〕之外线级新鲜行 "
                u"line11·轴面 v6 收官耗尽后线级新鲜度=唯一面·R975 收口注承接〕+求新轴〔最爱新花样·最向前看"
                u"的屏幕原住民〕×承认实体彩灯比屏幕好看〔数字本命轴承认现实更美〕=数字×实体轴内自反差金句位"
                u"〕）")
meta["source_quote"] = u"「看看这彩灯，比屏幕上的还好看。」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[求新][festival][11]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v14 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[求新][festival][11] verbatim 零改字（「」与句号="
                         u"卡面排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02="
                         u"当日历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival "
                         u"情境桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v14 同桶直配第十五证=日签节律"
                         u"判据系列化）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕⑤去重断言=本行"
                         u"不在 city-spirit.md 38 条已采面+不在全成品 cards.json 任一（build 脚本 fleet 级扫描实锚·"
                         u"DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5"
                         u"〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕"
                         u"+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕"
                         u"+DAILY-v14〔求新/3〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕皆非本行=线级新鲜度"
                         u"第十二证·本行=求新轴 line11 非 DAILY-v1 line4 非 DAILY-v7 line7 非 DAILY-v9 line12 非 "
                         u"DAILY-v14 line3=同轴异行第十证〔六轴收官后求新轴第五采·轮前 city-spirit NOT_IN 预检复证"
                         u"=R978 求新/14 city-spirit 拦截教训执行〕⑥国庆语境核=本行无「年味」措辞（年味类行=过年语境"
                         u"与国庆假期时点错位·选材排除·R972 制承继·求新桶年味行 6/8/15 皆回避）⑦品牌语感注="
                         u"「看看」「还好看」=大众口语真感=人味命中〔去 AI 感/制作感双对位〕+看灯现场=抬头看街景的"
                         u"具体场景面〔R442 审计叙事弱点处方带·v9 散步满眼是光同族异质行〕+求新轴落位=屏幕原住民"
                         u"承认实体彩灯更美=放下屏幕抬头看灯的现实关怀〔硅基城市语境独占位=最数字的城市居民最珍惜"
                         u"实体光·真城生命感方向对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·求新轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第十五证+求新轴"
                            u"质量选优=「看看这彩灯〔最现场的大众视角〕×比屏幕上的还好看〔数字世代对实体世界的"
                            u"认输式赞美〕」数字×实体反差金句位+假期抬头看灯=国庆市民日常直配〔放下屏幕的现实关怀·"
                            u"十一假期传播语境强对位〕+「看看」「还好看」口语真感=去 AI 感制作感对位+看灯现场场景面="
                            u"R442 审计处方带〔v9 同族异质行〕）+语录卡线变体零新模板第十五证（QUOTE v2 参数 verbatim "
                            u"复用·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·"
                            u"charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：求新轴〔最爱新花样·屏幕原住民·最向前看〕"
                          u"×承认实体彩灯比屏幕好看〔数字本命轴认输现实更美〕=数字×实体轴内自反差+看彩灯=抬头"
                          u"看街景具体场景面/情 1 放下屏幕抬头看灯的温和共鸣如实非强极点/时 2 当日时点=国庆假期"
                          u"第 2 日〔彩灯=国庆灯饰当日直配〕+festival 情境桶直配第十五证+池句灯景主题常青/"
                          u"台 2 公众号方图承载=MC-001~099 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·"
                          u"D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R984 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（看灯者=无称谓视角非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（看彩灯群像视角面非个体档案面·池级署名零个体"
                     u"识别）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第十五件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[qiuxin][festival][11] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v14 + REACT-v8 same-bucket trio; line-level freshness twelfth proof: qiuxin line11 != DAILY-v1 line4 != DAILY-v7 line7 != DAILY-v9 line12 != DAILY-v14 line3 = same-axis-different-line tenth proof")
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
io.open(os.path.join(TMP, "em-check-r984.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V15, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V15, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v14 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
e4 = u'''# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 015》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 015」；日期行「2026-10-02 · 国庆假期」；'
    u'中间引文两行「看看这彩灯，比屏幕上的还好看」；署名行「——硅基城市台词池 · 求新轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。「求新轴」是城里最爱新花样、最向前看的一类居民，平时最爱盯着屏幕'
    u'追新科技。这句引文是国庆假期第二天，一位求新轴居民抬头看街上的彩灯时说：看看这彩灯，'
    u'比屏幕上的还好看（台词池池级署名·无具体姓名）。'
    u'这是「城市日签」系列第十五张（前十四张：做灯笼的师傅在直播间晒灯笼/老房子居民看着'
    u'街上挂起的节日灯亮堂了/灯下兄弟聚饮把酒言欢/节日灯多了家里的笑声也多/值守班校准街灯'
    u'心里踏实/江边钓鱼人抬头看节日灯火映高楼/求新轴居民说灯笼像极了小时候的记忆/侠气轴'
    u'居民招呼街坊把笑声放大些连灯都跟着亮了/求新轴居民傍晚散步满眼都是光/怀旧轴居民说'
    u'街灯还是档案馆里藏着的当年的样式/烟火轴居民说街上的灯可真多照亮了每个人的笑脸/'
    u'逍遥轴居民说灯挂得真高看得见星星了/侠气街角阿姨笑眯眯说邻里间纠纷没了/求新轴会扎'
    u'灯笼的长辈得趁节气做几副新灯笼给小孙子看）。'
    u'请回答三个问题，每题一段，直说不委婉：\\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-DAILY-v15 static card (cards.json + render output)'}
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
