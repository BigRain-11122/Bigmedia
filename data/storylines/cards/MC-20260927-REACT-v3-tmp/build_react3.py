# -*- coding: utf-8 -*-
"""MC-20260927-REACT-v3 build: REACT series 3rd piece (R456, backlog #59 daily-hot claim;
R455 M0 pick = zhihu 2026-09-27 #8 financial-freedom x market_close bucket).
Hot topic verbatim relay (metadata desensitized off-card) x SiliconCity pool reactions
(market_close single-bucket 3-axis mapping, R309 law reuse) + census C-00025
ferry-captain creed wrap row (verbatim, job-level attribution).
M1 source machine-verify (pools.json verbatim + bucket index + anchor creed field +
daily-brief hot line) + em budget ladder with ZERO-MARGIN EXCLUSION (R293/R310)
+ vertical stack budget law (R381). Template = REACT v2 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V2 = os.path.join(BASE, "MC-20260926-REACT-v2")
V3 = os.path.join(BASE, "MC-20260927-REACT-v3")
TMP = V3 + "-tmp"
os.makedirs(V3, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V2, "cards.json"), encoding="utf-8"))

# --- M1 sources (verbatim chain) ---
POOLS = os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json")
ANCHOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00025.md")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")

HOT_RANK = 8
HOT_TITLE = u"财务自由的感觉是怎样的？"
CREED = u"船稳，人心才稳。"
POOL_TARGETS = [
    (u"逍遥轴", u"交易盘了，咱就图个心宽"),
    (u"烟火轴", u"刚赚的这份钱，得给孩子买点糖"),
    (u"像素灵池", u"喵呜一声，今日利润喜上眉梢"),
]

verify = []


def vlog(s):
    verify.append(s)


# 1) daily-brief hot line (rank + title verbatim)
daily_txt = io.open(DAILY, encoding="utf-8").read()
hot_needle = u"%d. %s" % (HOT_RANK, HOT_TITLE)
assert hot_needle in daily_txt, "daily brief hot line not found"
vlog(u"DAILY   %s  FOUND  (heat/rank metadata desensitized, README-ledger only)" % hot_needle)

# 2) census anchor creed field (C-00025, non-honor seat, registered field)
anchor_txt = io.open(ANCHOR, encoding="utf-8").read()
assert (u"**信条** 「%s」" % CREED) in anchor_txt, "C-00025 creed field mismatch"
vlog(u"ANCHOR  C-00025  creed field verbatim  「%s」  (non-honor seat, registered field)" % CREED)

# 3) pool lines verbatim + bucket index (walk whole pools.json, structure-agnostic)
pools = json.load(io.open(POOLS, encoding="utf-8"))


def find_line(target):
    hits = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [k])
        elif isinstance(node, list):
            for idx, ln in enumerate(node):
                if isinstance(ln, str) and ln == target:
                    hits.append((list(path), idx))

    walk(pools, [])
    return hits


pool_refs = []
for axis_label, target in POOL_TARGETS:
    hits = find_line(target)
    assert hits, "pool line not found verbatim: " + target
    path, idx = hits[0]
    bucket = path[-1]
    pool_refs.append((axis_label, target, bucket, idx))
    vlog(u"POOL    %s/%d  ->  %s「%s」" % ("/".join(path), idx, axis_label, target))

react_refs = u"／".join(u"%s %s/%d「%s」" % (a, b, i, t) for a, t, b, i in pool_refs)
vlog(u"REACT   single-bucket discipline: market_close bucket, 3-axis mapping (R309 law reuse)")

LINES = [
    u"城市速报 003",
    u"今日热点 · 知乎热榜 2026-09-27",
    HOT_TITLE,
] + [u"%s：「%s」" % (a, t) for a, t, b, i in pool_refs] + [u"渡轮船长信条：「%s」" % CREED]

SUBS_LINE = u"热点转述自知乎热榜·反应与信条皆取自虚构城市档案"

# --- em budget ladder (parametric pre-fit law; zero-margin exclusion R293/R310) ---
frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2

# --- vertical stack budget (R381 hard law) ---
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

meta = cfg["meta"]
meta["topic"] = "MC-20260927-REACT-v3"
meta["form"] = (u"REACT 热点城市反应版 003（L-卡 P0 形态第三位·L5 城市响应层媒体供给件·#59 按日热点随轮领"
                u"第二续件·R309 双律复用）——知乎热榜 2026-09-27 热点转述×硅基城市台词池反应×渡轮信条收束")
meta["source_facts"] = (u"热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-09-27 第 8 条问题标题 verbatim "
                        u"转述「%s」（来源=data/intel/daily/2026-09-27.md zhihu-hot·热度值 309 万与排名元数据不入卡面"
                        u"只入 README 记账）②反应行=BigLife 台词池 market_close 情境桶 verbatim 三条轴位映射"
                        u"（%s——**单桶纪律**=财务自由收市后自由感情境→market_close 桶·编辑选材 3 轴位=轴位映射律）"
                        u"③收束行=万人卡 C-00025 陆海峰信条 verbatim「%s」（渡轮船长·职业级署名不指名=REACT 署名律兼容·"
                        u"已登记字段 verbatim 零新增人格·人设权红线照守）"
                        % (HOT_TITLE, react_refs, CREED))
meta["source_pointer"] = (u"data/intel/daily/2026-09-27.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json "
                          u"台词池 market_close 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/"
                          u"C-00025.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席·CENSUS-v16 F-035 同源字段"
                          u"跨形态复用）")
meta["attribution_rule"] = (u"署名=轴级/池级/职业级（逍遥轴/烟火轴/像素灵池/渡轮船长·charter v1.2 署名律禁虚构居民名·"
                            u"人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-09-27 第 8 条·转述面合规=逐条来源链+不标题党）")
meta["triple_label"] = (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——"
                        u"热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落）+AIGC 角标＝常驻每帧 "
                        u"[AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = (u"速报体裁+轴位映射=编辑选材面（market_close 桶候选→3 轴位对位判断：逍遥=收市后自由感直配位"
                           u"〔财务自由×图个心宽=逍遥轴喝茶钓鱼收市城格直解〕／烟火=赚到钱给家人花的暖意位"
                           u"〔财务自由的家庭烟火解·给孩子买糖=自由的小额兑现〕／像素灵=城市自有灵物对利润的镜像反应位="
                           u"IP 专属面）+渡轮信条收束（财务自由×「船稳，人心才稳」=自由感×稳感对仗金句级收束+语录↔图鉴↔速报"
                           u"跨形态同句复用链〔C-00025 信条 CENSUS-v16 后速报形态首用〕）+系列「城市速报」与「城市语录」"
                           u"「城市图鉴」「城市盘点」平行连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；"
                           u"热点择优判据留痕=映射对位优先于纯热度（#8 309 万 market_close 桶位级直配入选·九条未选理由=R455 "
                           u"择优留痕全量注记：#1 中美战略=政治敏感面回避律／#2-#4 亚运乒乓男足=竞技面无映射桶〔R309/R313 "
                           u"注记维持〕／#5 可燃冰=零专属情境桶〔池 12 桶无能源面〕／#6 寻亲 58 年=真实人物隐私面回避+"
                           u"festival 桶灯笼主体弱对位／#7 鸡转头=sprite 桶无鸡位弱对位／#9 早餐月卡 369 元=market_open "
                           u"与 R313 单桶+主题族双重复〔系列同构规避=R442 审计弱点面〕／#10 网红负债 650 万=真实人物隐私面+"
                           u"弱对位）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔大众梦想话题×量化之城收市后喝茶钓鱼城格反差+"
                        u"market_close 收市场景=事实性赛博意象+像素灵「喵呜一声，今日利润喜上眉梢」城市自有灵物对利润的"
                        u"镜像反应+渡轮信条「船稳，人心才稳」自由感×稳感对仗金句级收束·知乎热榜当日热议=具体稀缺性〕/情 1 "
                        u"财务向往温和共鸣非强极点〔G4 投资理财人群+G2 超级个体野心家双群对位〕/时 2 当日热点=速报时效本体"
                        u"〔热榜在飞·时效窗=本形态存在理由〕/台 2 公众号方图承载=MC-001~044 S3 实证复用·速报=热点类大众"
                        u"流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                        u"production open）")
meta["red_line"] = (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=平台问题标题 verbatim 转述"
                    u"零改写零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00025 指针"
                    u"README 双落〕／脱敏（热度值 309 万/平台排名等元数据不入卡面=README 记账·零仓位/密钥/token 量/"
                    u"未公开财务面）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布")
meta["line"] = u"L-卡 图文轻内容线（REACT 形态第三件·charter v1.2 §4 形态码·#59 按日热点随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build) ---
report = list(verify)
report.append(u"")
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append(u"H1 size %d budget %.2fem | H2 size %d budget %.2fem (ladder pick, zero-margin exclusion margin>=%.1fem)"
              % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM))
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
report.append(u"VERT stack bottom est %.0fpx vs subs top %dpx gap %+.0fpx (need >=%dpx) (R381 vertical law)"
              % (vb, SUBS_TOP, SUBS_TOP - vb, GAP_MIN))
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
io.open(os.path.join(TMP, "em-check-r456.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V3, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V3, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
