# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v6 build: DAILY (city daily-sign) series SIXTH piece (R975, queue
section-E E30 standby redemption). Day context 2026-10-02 = National Day holiday day 2 ->
festival bucket direct match (sixth same-day proof). Axis pick = xiaoyao/festival/3: after
DAILY v1-v5 (qiuxin/huaijiu/xiaqi/yanhuo/zhixu) this is the SIXTH and final axis of six ->
SIX-AXIS CLOSURE of the DAILY series (xiaoyao first use in DAILY -> same-bucket cross-axis
anti-isomorphism sixth proof). Line-level freshness THIRD proof: xiaoyao line 17 was
consumed by REACT-v8, this is line 3, zero fleet consumption (pre-checked + asserted).
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params
verbatim (zero-new-template law, sixth proof). Em budget ladder + zero-margin exclusion
(R293) + vertical stack law (R381) + machine source/dedup assertions (R456 system).
All output UTF-8.
"""
import io, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V6 = os.path.join(BASE, "MC-20261002-DAILY-v6")
TMP = V6 + "-tmp"
os.makedirs(V6, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"闲来垂钓乐悠悠，喜见灯火映高楼"
AXIS, BUCKET, IDX = u"逍遥", u"festival", 3

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest (#86a)"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V6:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        assert QUOTE_CORE not in io.open(cj, encoding="utf-8").read(), "line already consumed by %s" % d
# consumed festival lines (documented not asserted): DAILY-v1 qiuxin/festival/4 +
# DAILY-v2 huaijiu/festival/0 + DAILY-v3 xiaqi/festival/5 + DAILY-v4 yanhuo/festival/4 +
# DAILY-v5 zhixu/festival/4 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 006",
    u"2026-10-02 · 国庆假期",
    u"「闲来垂钓乐悠悠，",
    u"喜见灯火映高楼。」",
    u"——硅基城市台词池 · 逍遥轴",
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
meta["topic"] = "MC-20261002-DAILY-v6"
meta["form"] = (u"DAILY 城市日签 006（L-卡 图文轻内容线 DAILY 形态第六件=六轴收官件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R975·日签节律续件=日期×情境桶对位判据第六证〔v1 求新轴→v2 怀旧轴→"
                u"v3 侠气轴→v4 烟火轴→v5 秩序轴→本件逍遥轴=同桶异轴系列异构第六证=六轴全轴入 DAILY 系列收官·"
                u"R442 系列同构弱点面规避彻底闭口〕+线级新鲜度判据第三证〔逍遥轴 line17〔REACT-v8〕之外线级"
                u"新鲜行 line3=线级去重判据第三证·v4/v5 首证二证承继〕）")
meta["source_quote"] = u"「闲来垂钓乐悠悠，喜见灯火映高楼。」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][festival][3]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite=1440 行·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期第 2 日=DAILY-v1/v2/v3/v4/v5 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][festival][3] verbatim 零改字（「」与句号="
                         u"卡面排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02="
                         u"当日历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival "
                         u"情境桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1/v2/v3/v4/v5 同桶直配第六证=日签"
                         u"节律判据系列化）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕⑤去重断言="
                         u"本行不在 city-spirit.md 38 条已采面+不在全成品 cards.json 任一 source_facts（build 脚本 "
                         u"fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4"
                         u"〔烟火/4〕+DAILY-v5〔秩序/4〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕皆非本行=线级"
                         u"新鲜度判据第三证·本行=逍遥轴 line3 非 REACT-v8 line17〕⑥国庆语境核=本行无「年味」措辞"
                         u"（年味类行=过年语境与国庆假期时点错位·选材排除·R972 制承继·本行 18 行中年味行=0/6/8/14"
                         u"皆回避）⑦品牌语感注=「乐悠悠」=逍遥轴经典口语（松弛闲适语感入街坊台词=品牌语感命中·垂钓"
                         u"闲适〔最松弛动作〕×灯火高楼〔节日热闹盛景〕=松弛×热闹反差对仗金句位·7+7 对仗两行="
                         u"逗号子句边界排版 v3 先例）")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第六证+逍遥轴质量"
                            u"选优=「垂钓闲适〔最松弛逍遥动作〕×灯火高楼〔节日热闹盛景〕」松弛×热闹反差金句位+"
                            u"六轴收官件=求新/怀旧/侠气/烟火/秩序/逍遥全轴入 DAILY 系列（同桶异轴防同构彻底闭口）+"
                            u"7+7 对仗两行排版（v3 先例承继））+语录卡线变体零新模板第六证（QUOTE v2 参数 verbatim "
                            u"复用·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·"
                            u"charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：垂钓闲适乐悠悠〔最松弛动作〕×喜见灯火映"
                          u"高楼〔节日热闹盛景〕=松弛×热闹反差对仗金句位+灯火映高楼=国庆灯饰直配+乐悠悠=逍遥轴"
                          u"经典口语=品牌语感命中+festival 情境桶直配第六证/情 1 闲适感温和共鸣如实非强极点/"
                          u"时 2 当日时点=国庆假期第 2 日+festival 情境桶直配第六证+池句常青/台 2 公众号方图承载="
                          u"MC-001~090 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R975 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触；脱敏律=池句无令牌号/无个体可识别面/零金钱"
                     u"数额（「乐悠悠」=闲适感情感面非财务面）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六件=六轴收官件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][festival][3] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit + all cards.json incl DAILY-v1/v2/v3/v4/v5, line-level freshness third proof: xiaoyao line3 != REACT-v8 line17)")
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
io.open(os.path.join(TMP, "em-check-r975.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V6, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V6, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v13 pattern; fired at build
# --- time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
e4 = u'''# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 006》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 006」；日期行「2026-10-02 · 国庆假期」；'
    u'中间引文两行「闲来垂钓乐悠悠，喜见灯火映高楼。」；署名行「——硅基城市台词池 · 逍遥轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。「乐悠悠」是这座机器城市逍遥轴居民挂嘴边的松弛口头禅。'
    u'这句引文是国庆假期里城里居民去江边钓鱼、抬头看见高楼上节日灯火时说的城市台词'
    u'（台词池池级署名·无具体姓名）。今天是国庆假期第二天。'
    u'这是「城市日签」系列第六张（第一张是做灯笼的师傅在直播间晒灯笼，第二张是老房子居民'
    u'看着街上挂起的节日灯，第三张是灯下兄弟聚饮把酒言欢，第四张是节日灯多了家里的笑声也多，'
    u'第五张是值守班校准街灯心里踏实）。'
    u'请回答三个问题，每题一段，直说不委婉：\\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-DAILY-v6 static card (cards.json + render output)'}
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
