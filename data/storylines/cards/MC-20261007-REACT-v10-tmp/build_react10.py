# -*- coding: utf-8 -*-
"""build_react10.py - MC-20261007-REACT-v10 M1 build with machine assertions.

R1548 production round. REACT hot-city-reaction card 010.
Sources (verbatim, zero-rewrite):
  hot      : zhihu-hot #10 2026-10-07, split at clause comma across two rows
  reactions: BigLife pools.json morning bucket, three distinct axes
  creed    : census anchor C-00019 (engine doctor) 信条
Machine checks: pool/anchor/daily verbatim, split integrity, em pre-fit
(ladder: largest feasible h2_size, zero-margin exclusion), VERT budget,
fleet dedup (R1010 exact-line).
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PIECE = HERE[:-4] if HERE.endswith("-tmp") else HERE
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(PIECE))))
POOL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00019.md"
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-07.md")

HOT_FULL = u"媒体称破铜烂铁、废纸壳、废塑料可能正在创造巨量财富，这是真的吗？为啥「破烂」正在变成黄金赛道？"
HOT1 = u"媒体称破铜烂铁、废纸壳、废塑料可能正在创造巨量财富，"
HOT2 = u"这是真的吗？为啥「破烂」正在变成黄金赛道？"
R1 = u"捡破烂也是门技术活，得眼尖手快"          # 怀旧/morning
R2 = u"晨风一扫夜的凉，摊子开张早赚两分光"        # 侠气/morning
R3 = u"早市忙，人声鼎沸"                        # 逍遥/morning
CREED = u"机器不坏是本事，坏了能修是人品。"
SERIES = u"城市速报 010"
SRCROW = u"今日热点 · 知乎热榜 2026-10-07"
SUBS = u"热点转述自知乎热榜·反应与信条皆取自虚构城市档案"

# --- 1) source verbatim assertions
pools = json.load(io.open(POOL, encoding="utf-8"))
assert R1 in pools["axes"]["怀旧"]["morning"], "R1 not verbatim in 怀旧/morning"
assert R2 in pools["axes"]["侠气"]["morning"], "R2 not verbatim in 侠气/morning"
assert R3 in pools["axes"]["逍遥"]["morning"], "R3 not verbatim in 逍遥/morning"
anchor = io.open(ANCHOR, encoding="utf-8").read()
assert CREED in anchor, "creed not verbatim in C-00019"
daily = io.open(DAILY, encoding="utf-8").read()
assert HOT_FULL in daily, "hot title not verbatim in daily brief"
assert HOT1 + HOT2 == HOT_FULL, "hot split integrity broken"

# --- 2) fleet dedup (R1010 exact-line; self dir excluded)
cards_dir = os.path.join(ROOT, "data", "storylines", "cards")
for d in sorted(os.listdir(cards_dir)):
    if not d.startswith("MC-") or d.endswith("-tmp"):
        continue
    cj = os.path.join(cards_dir, d, "cards.json")
    if not os.path.exists(cj):
        continue
    c = json.load(io.open(cj, encoding="utf-8"))
    for card in c.get("cards", []):
        for ln in card.get("lines", []):
            for cand, tag in [(R1, "R1"), (R2, "R2"), (R3, "R3")]:
                assert cand not in ln, "R1010 exact collision %s vs %s: %s" % (tag, d, ln)

# --- 3) em pre-fit (ladder: largest feasible, zero-margin exclusion)
def em_cost(ch):
    o = ord(ch)
    if o >= 0x2E80:
        return 1.0
    if ch in (" ", "\t"):
        return 0.5
    return 0.55

def width(s):
    return sum(em_cost(ch) for ch in s)

CANVAS = 1080
MARGINS = 160
AVAIL = CANVAS - MARGINS  # 920px
H1_SIZE = 84
H2_SIZE = 32               # selected ladder step (36 excluded by driver row)
SUBS_SIZE = 38
LINE_SPACING = 12
H1_GAP = 36
OPTICAL_CENTER = 0.24
SUBS_BOTTOM = 110

rows = [
    SRCROW,
    HOT1,
    HOT2,
    u"怀旧轴：「%s」" % R1,
    u"侠气轴：「%s」" % R2,
    u"逍遥轴：「%s」" % R3,
    u"引擎医生信条：「%s」" % CREED,
]
h1_w = width(SERIES)
assert h1_w <= AVAIL / H1_SIZE, "H1 over budget"
budget36 = AVAIL / 36.0
driver_w = max(width(r) for r in rows)
assert driver_w == width(HOT1), "driver row is not HOT1"
assert width(HOT1) > budget36, "36-step not excluded: ladder selection broken"
budget = AVAIL / H2_SIZE
lines_out = ["em-check-r1548 (REACT-v10 M2 front-fit + VERT R381)"]
lines_out.append("h2_size=%g budget=%.2fem  H1=%.2fem" % (H2_SIZE, budget, h1_w))
for r in rows:
    w = width(r)
    assert w <= budget - 0.2, "zero-margin exclusion: %s (%.2fem)" % (r, w)
    lines_out.append("OK %.2fem margin +%.2f  %s" % (w, budget - w, r))
subs_w = width(SUBS)
subs_budget = AVAIL / float(SUBS_SIZE)
assert subs_w <= subs_budget, "subs row over budget"
lines_out.append("subs %.2fem < %.2fem budget OK" % (subs_w, subs_budget))
# VERT (R381): pitch = 1.35*size + spacing, stack bottom must clear subs top by >=20px
h1_block = 1.35 * H1_SIZE + H1_GAP
h2_pitch = 1.35 * H2_SIZE + LINE_SPACING
est_bottom = CANVAS * OPTICAL_CENTER + h1_block + len(rows) * h2_pitch
subs_top = CANVAS - SUBS_BOTTOM - SUBS_SIZE
gap = subs_top - est_bottom
assert gap >= 20, "VERT gap %d < 20px" % gap
lines_out.append("VERT: est bottom=%.0fpx subs_top=%dpx gap=%dpx OK (assert >=20)" % (est_bottom, subs_top, gap))
lines_out.append("ALL-HORIZ: PASS  VERT: PASS")

# --- 4) write piece files
meta = {
    "topic": "MC-20261007-REACT-v10",
    "line": u"L-卡 图文轻内容线（REACT 形态第十件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
    "form": u"REACT 热点城市反应版 010（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第九续件·R309 双律复用·**热点择优判据第十证=映射对位优先于纯热度的最大热度差首证**：zhihu #1 缅北电诈覆灭纪实〔1628 万热度榜一+双平台交叉=bilibili #4 同题第二集〕判负留痕×zhihu #10 破烂变黄金赛道〔197 万热度榜尾〕入选=榜首→榜尾映射对位反差首证——知乎源线第 8 用）——知乎热榜热点转述×硅基城市台词池 morning 情境桶反应×引擎医生信条收束",
    "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
    "source_facts": (u"热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-07 第 10 条标题 verbatim 全题转述"
        u"（零裁零改字·双问句完整），设计排版逗号子句跨两行（row1「媒体称破铜烂铁、废纸壳、废塑料可能正在创造巨量财富，」"
        u"+row2「这是真的吗？为啥「破烂」正在变成黄金赛道？」=v5/v12/v14/v15/v16 逗号子句跨两行先例·row1/row2 逐字拼接=全题）"
        u"·来源=data/intel/daily/2026-10-07.md zhihu-hot 第 10 条·知乎源线第 8 用〔v9 后 zhihu 第 8 用〕"
        u"②反应行=BigLife 台词池 morning 情境桶 verbatim 三条轴位映射（怀旧/3「捡破烂也是门技术活，得眼尖手快」"
        u"／侠气/9「晨风一扫夜的凉，摊子开张早赚两分光」／逍遥/0「早市忙，人声鼎沸」——单桶纪律=破烂变财富情境→morning 桶"
        u"〔**morning 桶复用=v6 后首复·系列 9 桶新鲜度中断如实注**：四新鲜桶 dusk/typhoon/coldsnap/ceo_order 对本题三轴直配"
        u"全不成立〔r1548_react_probe.txt C 段机核：ceo_order 仅怀旧「旧物摊寻宝去，古董新客两相迎」+侠气「城主一声令，"
        u"咱这买卖就能赚翻天」两直配行无第三轴；dusk 三轴近配〔烟火「收摊回家了，今儿的生意不错」+怀旧「街角那家修伞铺子，"
        u"生意不赖」+侠气「夜市开张，热闹才刚开始」〕=修复/夜市邻域·题眼词「破烂」缺席弱于 morning 本域；typhoon/coldsnap"
        u" 零三轴〕→映射对位优先级＞桶新鲜度·morning 桶「捡破烂」题眼 verbatim 行=全池唯一破烂本域行+两支撑位=诚实配对唯一解〕"
        u"·三轴全 on-argument（技术门槛位/生计赚钱位/市场热度位=全题双问句「真的吗+为啥」的三个市民答案位）"
        u"·三句结构全异质（判断句/场景叙事句/四六短句·零人称口气句执行）·**三行全 CLEAN=R1010 卡面级 shingle 探针"
        u"零内容核命中**〔r1548_react_probe.txt B 段机核·2-3 字命中全为功能词/标点/场景名词噪声（是门/，得/，摊/凉，/，人）"
        u"·「晨风」=场景名词词汇面重叠非内容核 shingle 定谳注记〕）③收束行=万人卡 C-00019 引擎医生信条 verbatim"
        u"「机器不坏是本事，坏了能修是人品。」（引擎医生·职业级署名=REACT 署名律兼容·已登记字段 verbatim 零新增人格"
        u"·人设权红线照守·修复域=回收价值链同域锚〔题眼：破烂的黄金不在料里，在「能修」里——价值不在新旧，在能不能修回来〕"
        u"·**信条速报形态复用链第五续件**〔v6 C-00015/v7 C-00013/v8 C-00028/v9 C-00010 后第五续·C-00019 信条 CENSUS-v10 已引"
        u"=语录↔图鉴↔速报跨形态信条复用链 by-design·R1010 探针适用面=三反应行·信条行=户籍档案字段跨形态复用非选句面〕）"
        u"④城志互证锚注记=C-00013 编年史馆员（旧物有史=城内「旧物价值」对应位注记·非收束位不引信条）"),
    "source_pointer": (u"data/intel/daily/2026-10-07.md（热点源·当日一份为真相）"
        u"+life/BigLife/cognition/pools.json 台词池 morning 桶（跨仓只读·池句=情境口气零事实）"
        u"+life/BigLife/census/anchors/C-00019.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）"),
    "attribution_rule": (u"署名=轴级/职业级（怀旧轴/侠气轴/逍遥轴/引擎医生·charter v1.2 署名律禁虚构居民名·人设权红线照守）；"
        u"热点=平台热榜转述（知乎热榜 2026-10-07 第 10 条·热度 197 万元数据只入 README 记账不入卡面·转述面合规="
        u"逐条来源链+不标题党+verbatim 全题零改字）"),
    "triple_label": (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——"
        u"热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）"
        u"+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）"),
    "editorial_value": (u"速报体裁+轴位映射=编辑选材面（morning 桶候选→3 轴位对位判断：怀旧=技术门槛位直配"
        u"〔「捡破烂也是门技术活，得眼尖手快」=「为啥变成黄金赛道」的技术门槛答案位·「捡破烂」题眼词全池唯一 verbatim 直配"
        u"·判断句结构〕／侠气=生计赚钱位直配〔「晨风一扫夜的凉，摊子开张早赚两分光」=「可能正在创造巨量财富」的街头生计"
        u"实证位·「开张/赚」财富题眼词直配·场景叙事句结构〕／逍遥=市场热度位直配〔「早市忙，人声鼎沸」=「这是真的吗」的"
        u"市场热度回答位·人声鼎沸=赛道热闹实感·四六短句结构〕）+引擎医生信条收束（破烂变黄金赛道×「机器不坏是本事，"
        u"坏了能修是人品。」=修复价值金句级收束〔题眼：破烂的黄金不在料里，在「能修」里——价值不在新旧，在能不能修回来〕"
        u"+跨形态信条复用链第五续件〔C-00019 修复域=回收价值链同域居民档案〕+城志互证=C-00013 编年史馆员「旧物有史」"
        u"对应位）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」「城市日签」平行连载识别结构·编辑价值防低创作度"
        u"7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=映射对位优先于纯热度第十证·**榜首→榜尾最大热度差首证**"
        u"（zhihu #10 197 万 morning 桶三面位级直配〔技术门槛位+生计赚钱位+市场热度位=全题双问句一一对应〕入选·"
        u"未选理由全量注记：**zhihu #1 纪录片《缅北电诈覆灭纪实》首播〔1628 万热度榜一〕+bilibili #4 同题第二集《犁庭扫穴》"
        u"〔双平台交叉热点=R1547 预指候选〕判负留痕=全池 1440 行+sprite 144 行扫描零「骗/诈/防骗/抓捕/覆灭/正义/审判」域句"
        u"〔唯一「贼」行=秩序/heatwave「门口那扇铁闸可要关紧，别让贼光顾」防贼语境≠电诈覆灭论点=语义错配 R1299 A 组"
        u"「安全第一」族同型〕+敏感子面回避〔伴生条 zhihu #4 遗骸/涉外摩擦不转述·纪录片本体跨境执法面〕**／"
        u"zhihu #2 教育部辅导员同吃同住=教育政策评论面回避／zhihu #3 睡眠 7 小时=健康宣称面回避〔R1030 健康纹身同型·"
        u"医疗建议邻位不转述〕／zhihu #4 缅方遗骸=涉外敏感面回避〔不转述〕／zhihu #5 王皓遭辱骂=具名当事人面回避"
        u"〔零具名当事人律〕／zhihu #6 东南亚真的很危险吗=涉外风险面+伴生电诈子面回避／zhihu #7 OPPO 银团贷款=具名企业"
        u"商务新闻面〔R909/R1299 具名企业口径维持〕／zhihu #8 Photoshop 过时=具名产品科技面无桶〔R455 小米同型〕／"
        u"zhihu #9 macOS vs Windows=科技科普面无桶〔R455/R909 同型·v9 注记维持〕／bilibili #1/#2/#3/#5/#7 明日方舟终末地×5"
        u"〔汤汤EP/特别映像塔卫二/丹青渡PV/前瞻节目/特别映像宏山〕=具名 IP 宣传面〔R909/R1030 影视/音乐/IP 宣传面族〕"
        u"+游戏版本内容面无映射桶／bilibili #6 泛式 7 月新番=影视综艺内容面无映射位〔R909 影视五连注记维持〕／"
        u"bilibili #8 VCTCN 冠军赛单曲=音乐内容面〔R1030 音乐面注记维持〕／bilibili #9 算命TV 反封建迷信=迷信域池零行"
        u"〔机核〕+喜剧内容面无映射位／bilibili #10 树屋像后室=vlog 无事件锚）"),
    "hit_chain_m0": (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔破铜烂铁/废纸壳/废塑料=最不起眼的破烂 vs 巨量财富/黄金赛道="
        u"最贵气意象反差具象在场+双问句「这是真的吗？为啥」好奇缺口=破烂越日常·问句越抓人〕/情 1 生活小智慧温和共鸣非强极点"
        u"〔G1 日常党+G2 生活家+省钱精打细算族直配对位〕/时 2 当日热点=速报时效本体〔知乎热榜 2026-10-07 在飞〕/台 2 公众号"
        u"方图承载=MC-001~168 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism "
        u"v1.0 §2/§9·D-BS-06 production open）"),
    "aspect_note": u"1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
    "red_line": (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim 全题转述零改写"
        u"零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00019 指针 README 双落〕／"
        u"脱敏（热度 197 万元数据不入卡面=README 记账·零具名当事人·零仓位/密钥/token 量/未公开财务面）；政治敏感面回避律照守"
        u"（缅北电诈条/教育部条/东南亚条不选）；健康宣称面回避（睡眠条不转述不背书）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布"),
}

card = {
    "meta": meta,
    "video": {"width": 1080, "height": 1080, "fps": 30, "bg": "black"},
    "font": {
        "file": "C:/Windows/Fonts/msyh.ttc",
        "cards_size": 50,
        "subs_size": SUBS_SIZE,
        "subs_bottom": SUBS_BOTTOM,
        "aigc_size": 30,
        "line_spacing": LINE_SPACING,
        "h1_font": "C:/Windows/Fonts/msyhbd.ttc",
        "h1_size": H1_SIZE,
        "h1_color": "accent",
        "h2_size": H2_SIZE,
        "h2_color": "white",
        "h1_gap": H1_GAP,
        "optical_center": OPTICAL_CENTER,
    },
    "aigc_notice": "[AIGC·AI 生成内容]",
    "tail": 0.8,
    "cards": [
        {
            "start": 0.0,
            "end": 2.6,
            "lines": [SERIES, SRCROW, HOT1, HOT2,
                      u"怀旧轴：「%s」" % R1,
                      u"侠气轴：「%s」" % R2,
                      u"逍遥轴：「%s」" % R3,
                      u"引擎医生信条：「%s」" % CREED],
        }
    ],
}

io.open(os.path.join(PIECE, "cards.json"), "w", encoding="utf-8").write(
    json.dumps(card, ensure_ascii=False, indent=1))
io.open(os.path.join(PIECE, "subs.srt"), "w", encoding="utf-8").write(
    u"1\n00:00:00,000 --> 00:00:02,600\n" + SUBS + u"\n")
io.open(os.path.join(PIECE, "em-check-r1548.txt"), "w", encoding="utf-8").write(
    "\n".join(lines_out) + "\n")
print("BUILD OK: cards.json + subs.srt + em-check-r1548.txt")
print("\n".join(lines_out))
