# -*- coding: utf-8 -*-
"""MC-20260929-REACT-v5 build: REACT series 5th piece (R643, backlog #59 daily-hot claim;
M0 pick = bilibili-popular 2026-09-29 #3 cat-roguelike-game x weekend bucket double-axis
direct fit (cat -> sprite cat line; game -> qiuxin game line); weekend bucket 2nd
consecutive use is honest-noted (topic family differs: fishing -> game; R455 same-theme
criterion = theme family, not bucket). P-1 anti-cliche line-selection law v2 pilot piece
1/2 (queue SD): prefer atypical-subject lines, heterogeneous structures within bucket,
no same-axis same-structure across consecutive pieces; creed wrap row weight upgraded.
Hot topic verbatim relay (UP-name/rank metadata desensitized off-card) x SiliconCity pool
reactions (weekend single-bucket 3-axis mapping, R309 law reuse) + census C-00021
GAME-city primary-school student creed wrap row (verbatim, job-level attribution).
M1 source machine-verify (daily hot line + anchor creed/job + companion anchors C-00029
+ pool lines verbatim) + em budget ladder with ZERO-MARGIN EXCLUSION (R293/R310)
+ vertical stack budget law (R381). Template = REACT v4 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V4 = os.path.join(BASE, "MC-20260928-REACT-v4")
V5 = os.path.join(BASE, "MC-20260929-REACT-v5")
TMP = V5 + "-tmp"
os.makedirs(V5, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V4, "cards.json"), encoding="utf-8"))

# --- M1 sources (verbatim chain) ---
POOLS = os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json")
ANCHOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00021.md")
ANCHOR_CAT = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00029.md")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-09-29.md")

HOT_RANK = 3
HOT_TITLE = u"一猫哈气万狗哭！我把哈基米做成了肉鸽游戏！"
CREED = u"放学别走，先把今天的谜想完。"
JOB_LABEL = u"像素小学学生"
POOL_TARGETS = [
    (u"求新轴", u"周末了，手头正好，给新游戏添个皮肤"),
    (u"秩序轴", u"今日没事，正好陪孩子玩会儿"),
    (u"像素灵池", u"喵呜喵，星光下的梦"),
]

verify = []


def vlog(s):
    verify.append(s)


# 1) daily-brief hot line (rank + title verbatim, bilibili source line 2nd use)
daily_txt = io.open(DAILY, encoding="utf-8").read()
hot_needle = u"%d. %s" % (HOT_RANK, HOT_TITLE)
assert hot_needle in daily_txt, "daily brief hot line not found"
vlog(u"DAILY   %s  FOUND  (bilibili-popular source; UP-name/rank metadata desensitized, README-ledger only)" % hot_needle)

# 2) census anchor creed field (C-00021, non-honor seat, registered field)
anchor_txt = io.open(ANCHOR, encoding="utf-8").read()
assert (u"**信条** 「%s」" % CREED) in anchor_txt, "C-00021 creed field mismatch"
assert (u"**职业** %s" % JOB_LABEL) in anchor_txt, "C-00021 job field mismatch"
assert u"GAME 城 · X026 城门区" in anchor_txt, "C-00021 district field mismatch"
vlog(u"ANCHOR  C-00021  creed field verbatim  「%s」  (job=%s, GAME city, non-honor seat, registered field)" % (CREED, JOB_LABEL))

# 2b) companion anchor C-00029 (cat sprite in GAME city; cross-card mutual-proof claims)
cat_txt = io.open(ANCHOR_CAT, encoding="utf-8").read()
assert u"**物种** 像素灵·radiocat" in cat_txt, "C-00029 species field mismatch"
assert u"GAME 城 · 像素匠人巷" in cat_txt, "C-00029 district field mismatch"
assert u"最投缘=王多多" in cat_txt, "C-00029 relationship cross-link mismatch"
vlog(u"ANCHOR  C-00029  radiocat sprite in GAME city  +  relationship cross-link to C-00021 (city-annals mutual proof)")

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
    assert bucket == u"weekend", "pool line bucket mismatch: " + bucket
    pool_refs.append((axis_label, target, bucket, idx))
    vlog(u"POOL    %s/%d  ->  %s「%s」" % ("/".join(path), idx, axis_label, target))

react_refs = u"／".join(u"%s %s/%d「%s」" % (a, b, i, t) for a, t, b, i in pool_refs)
vlog(u"REACT   single-bucket discipline: weekend bucket, 3-axis mapping (R309 law reuse; P-1 anti-cliche v2 applied)")

LINES = [
    u"城市速报 005",
    u"今日热点 · B站热门 2026-09-29",
    HOT_TITLE,
] + [u"%s：「%s」" % (a, t) for a, t, b, i in pool_refs] + [u"%s信条：「%s」" % (JOB_LABEL, CREED)]

SUBS_LINE = u"热点转述自B站热门·反应与信条皆取自虚构城市档案"

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
meta["topic"] = "MC-20260929-REACT-v5"
meta["form"] = (u"REACT 热点城市反应版 005（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第四续件·"
                u"R309 双律复用·**P-1 反套路化选句律 v2 试点件 1/2**·B站源线第 2 用）——B站热门热点转述×"
                u"硅基城市台词池反应×GAME 城像素小学学生信条收束")
meta["source_facts"] = (u"热点转述律+反应抽取律 R309 双律复用：①热点行=B站热门 2026-09-29 第 3 条视频标题 verbatim "
                        u"转述「%s」（来源=data/intel/daily/2026-09-29.md bilibili-popular·UP 主名与排名元数据不入卡面"
                        u"只入 README 记账=脱敏律·B站源线第 2 用）②反应行=BigLife 台词池 weekend 情境桶 verbatim 三条"
                        u"轴位映射（%s——**单桶纪律**=周末休闲游戏情境→weekend 桶〔v4 钓鱼→v5 游戏=同桶不同主题族·"
                        u"R455 同构判据=主题族非桶·如实注记〕·城志互证=万人卡 C-00021 王多多经历字段「爹妈都在游戏楼上班」"
                        u"GAME 城游戏楼家庭锚+C-00029 咪喱物种行「像素灵·radiocat」城区行「GAME 城·像素匠人巷」关系字段"
                        u"「最投缘=王多多」像素灵猫锚=猫×游戏双面城志互证〔收束行锚与猫灵互证链真实在档〕·编辑选材 3 轴位="
                        u"轴位映射律+**P-1 反套路化选句律 v2 首用**〔优先非典型主语句=三池句全无主语口气句·同桶选结构"
                        u"异质者=求新游戏行为桶内唯一游戏直配行·sprite 猫行为桶内仅存猫行〔v4 已用 /7〕·秩序陪玩行="
                        u"日境陈述结构 vs v4 秩序建议句=结构异质·禁同轴位连件同句式=v4 逍遥/秩序/sprite→v5 求新/秩序/sprite "
                        u"两保留轴句式全异质·收束行权重升档〕）③收束行=万人卡 C-00021 王多多信条 verbatim「%s」"
                        u"（像素小学学生·职业级署名不指名=REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·"
                        u"非荣誉席·信条速报形态首用）"
                        % (HOT_TITLE, react_refs, CREED))
meta["source_pointer"] = (u"data/intel/daily/2026-09-29.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json "
                          u"台词池 weekend 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/C-00021.md "
                          u"万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）+anchors/C-00029.md 像素灵锚（城志互证·"
                          u"物种/城区/关系三断言）")
meta["attribution_rule"] = (u"署名=轴级/池级/职业级（求新轴/秩序轴/像素灵池/像素小学学生·charter v1.2 署名律禁虚构居民名·"
                            u"人设权红线照守）；热点=平台热榜转述（B站热门 2026-09-29 第 3 条·B站源线第 2 用·"
                            u"转述面合规=逐条来源链+不标题党）")
meta["triple_label"] = (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自B站热门·反应与信条皆取自虚构城市档案」——"
                        u"热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落）+AIGC 角标＝常驻每帧 "
                        u"[AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = (u"速报体裁+轴位映射=编辑选材面（weekend 桶候选→3 轴位对位判断：求新=桶内唯一游戏直配位"
                           u"〔「周末了，手头正好，给新游戏添个皮肤」=哈基米游戏上线热度×城里玩家给新游戏买皮肤=热度同构位·"
                           u"非典型主语句〕／秩序=陪玩日境位〔「今日没事，正好陪孩子玩会儿」=萌宠游戏老少咸宜×城里秩序派家长"
                           u"周末陪玩=家庭休闲面·日境陈述结构 vs v4 秩序建议句=结构异质〕／像素灵=猫族观战位〔「喵呜喵，星光下的梦」"
                           u"=哈基米猫梗×城市自有像素灵猫族淡定围观=IP 专属同类观察位·桶内仅存猫行〕）+GAME 城小学生信条收束"
                           u"（肉鸽游戏死循环挑战×「放学别走，先把今天的谜想完」=谜题纪律对仗金句级收束+语录↔图鉴↔速报跨形态"
                           u"信条复用链〔C-00021 信条速报形态首用·GAME 城锚=话题同域居民档案·CENSUS-v12 F-032 同源字段跨形态"
                           u"复用〕）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」平行连载识别结构·编辑价值防低创作度"
                           u" 7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=映射对位优先于纯热度第五证（B站 #3 猫×游戏"
                           u"双轴直配入选·未选理由全量注记：zhihu #1/#6/#9 亚运竞技×3=竞技面无映射桶〔R309/R313/R455/R575 注记维持〕"
                           u"／#2 常德老人养老金=真实人物隐私面回避〔涉具名当事人不幸遭遇·R455 寻亲同型〕+社会保障政策批评面敏感／"
                           u"#3 中美降税=政治敏感面回避律／#4 新大头儿子=文娱吐槽面无映射桶／#5 双汇火腿肠销量下滑=market 族+"
                           u"食物类双重复〔v2 牛肉涨价同主题族=R455 早餐月卡同型规避〕／#7 乾隆的字=文化审美面无映射桶／#8 预制菜 C端="
                           u"食物类跨桶弱对位+食品安全邻位敏感〔R313 注记维持〕／#10 超长蛋挞=食物类跨桶弱对位〔R313 注记维持〕／"
                           u"bilibili #1 三幻魔=动画内容面无城市反应映射位／#2 原神六周年=游戏 IP 官方周年宣传面·单轴〔游戏〕弱于 "
                           u"#3 双轴直配〔猫+游戏〕／#4 终极恶女=剧情剪辑面无映射位／#5 唐笑调上=音乐才艺面无桶／#6 CN零杠八="
                           u"音乐面无桶／#7 发量下降一万倍=脑洞搞笑抽象面无情境锚／#8 飞行滑板=科技 DIY 面·池 12 桶无科技桶"
                           u"〔R455 小米防窥屏同型注记维持〕／#9 鸣潮 PV=游戏 PV 宣传面〔同 #2 单轴注记〕／#10 国创导视="
                           u"行业宣传面无映射位）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔一猫哈气万狗哭=猫强势×狗破防 meme 喜剧×硅基城市"
                        u"像素灵猫族淡定星梦=外来猫梗×自有猫灵同类观察反差+GAME 城最小信使小学生「放学别走，先把今天的"
                        u"谜想完」谜题纪律×肉鸽死循环挑战=对仗金句级收束+求新派给新游戏添皮肤=玩家热度同构位·B站热门当日="
                        u"具体稀缺性〕/情 1 萌宠吃瓜温和共鸣非强极点〔G5 吃瓜未来党+G3 科技硬核极客/游戏人群副群对位〕"
                        u"/时 2 当日热点=速报时效本体〔B站热门在飞〕/台 2 公众号方图承载=MC-001~053 S3 实证复用·速报="
                        u"热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                        u"production open）")
meta["red_line"] = (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=平台视频标题 verbatim 转述"
                    u"零改写零加感叹〕／无来源不发布〔热点=B站热门+日期图内行·反应=台词池指针·信条=户籍卡 C-00021 指针"
                    u"README 双落〕／脱敏（UP 主名/平台排名等元数据不入卡面=README 记账·零仓位/密钥/token 量/未公开财务面）；"
                    u"政治敏感面回避律照守（当日榜中美降税条不选）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布")
meta["line"] = u"L-卡 图文轻内容线（REACT 形态第五件·charter v1.2 §4 形态码·#59 按日热点随轮领）"

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
io.open(os.path.join(TMP, "em-check-r643.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V5, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V5, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
