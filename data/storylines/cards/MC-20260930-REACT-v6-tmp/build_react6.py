# -*- coding: utf-8 -*-
"""MC-20260930-REACT-v6 build: REACT series 6th piece (R716, queue E3 daily-hot claim;
M0 pick = zhihu-hot 2026-09-30 #9 cilantro-refund-dispute x morning bucket triple-face
direct fit (vegetable-price fair-deal line / small-dispute-early-settle line / vendor-rules
line); morning bucket = 6th distinct bucket in series (v1 rain / v2 market_open /
v3 market_close / v4-v5 weekend) - bucket freshness. P-1 anti-cliche line-selection law v2
pilot FINAL piece 2/2 (queue SD): prefer atypical-subject lines, heterogeneous structures
within bucket, no same-axis same-structure across consecutive pieces, creed wrap row weight
upgraded; sprite position consciously dropped after 5-piece streak (sprite/morning lines
are ambient shop-opening sounds, off-argument for dispute/rules theme) - honest note.
Hot topic verbatim prefix-substring relay (full zhihu title + heat metadata desensitized,
README-ledger only) x SiliconCity pool reactions (morning single-bucket 3-axis mapping,
R309 law reuse) + census C-00015 QUANT-city risk-officer creed wrap row (verbatim,
job-level attribution) + C-00010 vendor anchor as city-annals mutual proof.
M1 source machine-verify (daily hot line + anchor creed/job/district + companion anchor
job + pool lines verbatim) + em budget ladder with ZERO-MARGIN EXCLUSION (R293/R310)
+ vertical stack budget law (R381). Template = REACT v5 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V5 = os.path.join(BASE, "MC-20260929-REACT-v5")
V6 = os.path.join(BASE, "MC-20260930-REACT-v6")
TMP = V6 + "-tmp"
os.makedirs(V6, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V5, "cards.json"), encoding="utf-8"))

# --- M1 sources (verbatim chain) ---
POOLS = os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json")
ANCHOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00015.md")
ANCHOR_VENDOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00010.md")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-09-30.md")

HOT_RANK = 9
HOT_TITLE_FULL = u"8.59 元香菜遭「仅退款」，商家驱车千里跨省讨回，如何评价？电商商家维权成本这么高，症结在哪？"
HOT_TITLE = u"8.59 元香菜遭「仅退款」，商家驱车千里跨省讨回"
CREED = u"红灯是为所有人亮的，包括我。"
JOB_LABEL = u"风控官"
POOL_TARGETS = [
    (u"烟火轴", u"青菜萝卜两厢情愿，咱这价格明镜儿似的"),
    (u"侠气轴", u"邻里间，小纠纷早化解"),
    (u"秩序轴", u"摊贩出摊了，规矩不能少，日子得按部就班"),
]

verify = []


def vlog(s):
    verify.append(s)


# 1) daily-brief hot line (rank + FULL title verbatim; card face = verbatim prefix substring,
#    short-label discipline R631 precedent; full title + heat metadata README-ledger only)
daily_txt = io.open(DAILY, encoding="utf-8").read()
hot_needle = u"%d. %s" % (HOT_RANK, HOT_TITLE_FULL)
assert hot_needle in daily_txt, "daily brief hot line not found"
assert HOT_TITLE in HOT_TITLE_FULL, "card hot line must be verbatim substring of full title"
vlog(u"DAILY   %s  FOUND  (zhihu-hot source; card face = verbatim prefix substring, full title + heat metadata desensitized, README-ledger only)" % hot_needle)

# 2) census anchor creed field (C-00015, non-honor seat, registered field)
anchor_txt = io.open(ANCHOR, encoding="utf-8").read()
assert (u"**信条** 「%s」" % CREED) in anchor_txt, "C-00015 creed field mismatch"
assert (u"**职业** %s" % JOB_LABEL) in anchor_txt, "C-00015 job field mismatch"
assert u"QUANT 城 · 风控高地" in anchor_txt, "C-00015 district field mismatch"
assert u"手写展示锚" in anchor_txt, "C-00015 provenance (P-0 sample anchor) missing"
vlog(u"ANCHOR  C-00015  creed field verbatim  「%s」  (job=%s, QUANT city risk-control height, non-honor seat P-0, registered field)" % (CREED, JOB_LABEL))

# 2b) companion anchor C-00010 (city-native morning-market vendor texture proof)
vendor_txt = io.open(ANCHOR_VENDOR, encoding="utf-8").read()
assert u"**职业** 数据粥铺摊主" in vendor_txt, "C-00010 vendor job field mismatch"
assert u"早点摊" in vendor_txt, "C-00010 breakfast-stall wording mismatch"
assert u"开档" in vendor_txt, "C-00010 stall jargon mismatch"
vlog(u"ANCHOR  C-00010  morning-market vendor in census (job=数据粥铺摊主, stall jargon 开档/收摊 registered) - city-annals mutual proof for morning-bucket vendor texture")

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
    assert bucket == u"morning", "pool line bucket mismatch: " + bucket
    pool_refs.append((axis_label, target, bucket, idx))
    vlog(u"POOL    %s/%d  ->  %s「%s」" % ("/".join(path), idx, axis_label, target))

react_refs = u"／".join(u"%s %s/%d「%s」" % (a, b, i, t) for a, t, b, i in pool_refs)
vlog(u"REACT   single-bucket discipline: morning bucket, 3-axis mapping (R309 law reuse; P-1 anti-cliche v2 applied; sprite position dropped - honest note)")

LINES = [
    u"城市速报 006",
    u"今日热点 · 知乎热榜 2026-09-30",
    HOT_TITLE,
] + [u"%s：「%s」" % (a, t) for a, t, b, i in pool_refs] + [u"%s信条：「%s」" % (JOB_LABEL, CREED)]

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
meta["topic"] = "MC-20260930-REACT-v6"
meta["form"] = (u"REACT 热点城市反应版 006（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第五续件·"
                u"R309 双律复用·**P-1 反套路化选句律 v2 试点终判件 2/2**·知乎源线第 3 用）——知乎热榜热点转述×"
                u"硅基城市台词池 morning 情境桶反应×QUANT 城风控官信条收束")
meta["source_facts"] = (u"热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-09-30 第 9 条标题 verbatim 前段子串"
                        u"转述「%s」（全题=「%s」·来源=data/intel/daily/2026-09-30.md zhihu-hot·排名与 168 万热度"
                        u"元数据不入卡面只入 README 记账=脱敏律·知乎源线第 3 用〔v1 天气律 CEO 行/v3 财务自由后第 3 用〕·"
                        u"短标签口径纪律=R631 verbatim 子串先例）②反应行=BigLife 台词池 morning 情境桶 verbatim 三条轴位映射"
                        u"（%s——**单桶纪律**=早市场景→morning 桶〔系列第 6 个不同桶=v1 rain/v2 market_open/v3 market_close/"
                        u"v4-v5 weekend 后 morning 首用·桶新鲜度=反套路化正面证据〕·城志互证=万人卡 C-00010 顾阿凤职业字段"
                        u"「数据粥铺摊主——早点摊的赛博后身」+语言字段摊头行话「开档」「收摊」=早市摊主城市原住纹理在册·"
                        u"morning 桶摊主口气池句有城志根〔收束行锚与摊主互证链真实在档〕·编辑选材 3 轴位=轴位映射律+"
                        u"**P-1 反套路化选句律 v2 终判件应用**〔优先非典型主语句=烟火句青菜萝卜俗谚主语/侠气句邻里间场景三拍/"
                        u"秩序句摊贩事件句·三句结构全异质=俗谚判断/三拍短句/事件规矩论·禁同轴位连件同句式=v5 求新/秩序/sprite→"
                        u"v6 烟火/侠气/秩序·保留轴秩序句式全异〔v5 秩序=日境陪玩陈述 vs v6 秩序=摊贩规矩论〕·烟火轴=v2 后首归·"
                        u"侠气轴=v2 后首归·**sprite 位自觉弃用注记**=v1-v5 连用 sprite 观战位 5 连=潜在套路位·sprite/morning "
                        u"行全为开店环境音（叮叮当响开店营业忙类）离纠纷/规则论题·三轴全 on-argument=反套路化正面证据·"
                        u"收束行权重升档〕）③收束行=万人卡 C-00015 陈雅雯信条 verbatim「%s」（风控官·职业级署名不指名="
                        u"REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·非荣誉席 P-0 样板锚·QUANT 城风控高地="
                        u"规则/治理域锚=话题同域〔仅退款规则单边性×「红灯是为所有人亮的，包括我。」规则普遍性题眼="
                        u"症结所在的城志答案〕）"
                        % (HOT_TITLE, HOT_TITLE_FULL, react_refs, CREED))
meta["source_pointer"] = (u"data/intel/daily/2026-09-30.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json "
                          u"台词池 morning 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/C-00015.md "
                          u"万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）+anchors/C-00010.md 摊主锚（城志互证·"
                          u"职业/语言摊头行话断言）")
meta["attribution_rule"] = (u"署名=轴级/池级/职业级（烟火轴/侠气轴/秩序轴/风控官·charter v1.2 署名律禁虚构居民名·"
                            u"人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-09-30 第 9 条·知乎源线第 3 用·"
                            u"转述面合规=逐条来源链+不标题党+verbatim 子串零改字）")
meta["triple_label"] = (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——"
                        u"热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落）+AIGC 角标＝常驻每帧 "
                        u"[AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = (u"速报体裁+轴位映射=编辑选材面（morning 桶候选→3 轴位对位判断：烟火=公道买卖直配位"
                           u"〔「青菜萝卜两厢情愿，咱这价格明镜儿似的」=香菜 8.59 元价格争议×城里摊主两厢情愿公道自持="
                           u"买卖公平题眼正面同构位·俗谚判断句结构〕／侠气=纠纷处置直配位〔「邻里间，小纠纷早化解」="
                           u"跨省千里讨说法=纠纷未早化解的城外反例×城里调解传统早化解=纠纷治理对照位·场景三拍短句结构〕／"
                           u"秩序=规则约束直配位〔「摊贩出摊了，规矩不能少，日子得按部就班」=平台规则约束商家×城里摊贩"
                           u"规矩自律=规则两面性同构位·事件规矩论结构〕）+QUANT 城风控官信条收束（仅退款单边规则×「红灯是为"
                           u"所有人亮的，包括我。」规则普遍性=对仗金句级收束〔症结所在的城志答案：规则只在该绑住所有人时"
                           u"才成立·含说规则者自己〕+语录↔图鉴↔速报跨形态信条复用链〔C-00015 信条速报形态首用·QUANT 城风控高地="
                           u"话题同域居民档案·CENSUS-v4 同源字段跨形态复用先例〕）+系列「城市速报」与「城市语录」「城市图鉴」"
                           u"「城市盘点」平行连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；"
                           u"热点择优判据留痕=映射对位优先于纯热度第六证（zhihu #9 三面位级直配〔价格公道+纠纷处置+规则约束="
                           u"morning 桶三轴全直配·全题三问〔香菜价格/维权成本/症结〕与三轴位一一对应〕入选·未选理由全量注记："
                           u"zhihu #1 房贷贴息政策=住房金融政策评价面·政策敏感回避〔R643 养老金同型〕+池无住房桶／#2 陕西醉驾案="
                           u"具名刑案悲剧面+真实当事人隐私回避〔R455 寻亲同型〕／#3 车载冰箱使用率 5%=消费科技面·池 12 桶无"
                           u"消费电子桶〔R455 小米防窥屏/R643 注记维持·冰箱行在 heatwave 桶=跨桶弱对位〕／#4 AMD 收购 World Labs="
                           u"AI 产业新闻面·池 12 桶无科技/AI 桶〔本轮机核 ai_hit=0 实证〕／#5 亚运混接首金=竞技面无映射桶"
                           u"〔R309/R313/R455/R575/R643 五连注记维持〕／#6 那英举报式采访=媒体批评争议面·娱乐人物具名敏感／"
                           u"#7 国乒亚运=竞技面无映射桶〔维持〕／#8 银鳕鱼汞中毒=食品安全面+儿童健康邻位敏感·食物类跨桶"
                           u"弱对位〔R313 注记维持〕／#10 河虾价格=食物价格族与 v2 牛肉涨价同主题族双重复〔R455 早餐月卡/"
                           u"R643 双汇同型规避〕／bilibili #1 量筒水量=科普实验面无映射桶／#2 自学动画爆肝俩月=手作创作面·"
                           u"求新 weekend 桶 craft 行在册但 weekend 桶 v4/v5 连件已用〔桶单调性=反套路化对面·同桶注记反向应用·"
                           u"候选留档下窗〕／#3 龙泉印泥=非遗文化审美面无桶〔R643 乾隆的字同型〕／#4 长生契=剧集内容面无映射位"
                           u"〔R643 注记维持〕／#5 手绘 465 张 EVA=同 #2 手作创作族+IP 官方纪念宣传面／#6 六耳单曲=音乐面无桶"
                           u"〔R643 唐笑同型〕／#7 斯克拉奇溪=恐怖小说连载面无映射位／#8 怎么夸人=社交技巧泛题面无情境桶／"
                           u"#9 风声 1=影视宣发面无映射位／#10 消失的裂痕=剧集内容面无映射位〔R643 注记维持〕）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔8.59 元 vs 千里跨省=最小金额×最大维权成本数字反差·"
                        u"量化之城成本收益本能共振+摊主「价格明镜儿似的」公道自持×「仅退款」单边规则=公道×单边反差+"
                        u"风控官「红灯是为所有人亮的，包括我。」规则普遍性题眼金句收束·知乎热榜当日=具体稀缺性〕"
                        u"/情 1 较真公道吃瓜温和共鸣非强极点〔G5 吃瓜未来党+G1 AI 效率实操党成本收益对位副群〕"
                        u"/时 2 当日热点=速报时效本体〔知乎热榜在飞〕/台 2 公众号方图承载=MC-001~054 S3 实证复用·速报="
                        u"热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                        u"production open）")
meta["red_line"] = (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim 前段"
                    u"子串转述零改写零加感叹·全题入 README〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·"
                    u"信条=户籍卡 C-00015 指针README 双落〕／脱敏（排名/热度元数据不入卡面=README 记账·零仓位/密钥/"
                    u"token 量/未公开财务面·热点无具名当事人）；政治敏感面回避律照守（当日榜房贷贴息政策/醉驾刑案条不选）；"
                    u"成品只入库＝M5 账号物理件未开+M4 全绿前零发布")
meta["line"] = u"L-卡 图文轻内容线（REACT 形态第六件·charter v1.2 §4 形态码·#59 按日热点随轮领）"

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
io.open(os.path.join(TMP, "em-check-r716.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V6, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V6, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
