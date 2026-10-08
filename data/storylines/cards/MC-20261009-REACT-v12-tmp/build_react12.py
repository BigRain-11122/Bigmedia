# -*- coding: utf-8 -*-
"""build_react12.py - MC-20261009-REACT-v12 M1 build with machine assertions.

R1779 production round (day-boundary batch, daily brief 2026-10-09 first per
O-2304 iron rule). REACT hot-city-reaction card 012.
Sources (verbatim, zero-rewrite):
  hot      : zhihu-hot #1 2026-10-09 (870wan, top heat), full title across
             two rows (comma-clause typographic split, zero rewrite)
  reactions: BigLife pools.json ceo_order bucket, three distinct axes
             (REACT-series card-face first use of the bucket; fleet-level the
             bucket was first opened by DAILY-v70 R1738 axis=yanhuo/17 -
             different rows, R1010 exact zero collision)
  creed    : census anchor C-00011 (time-space calibrator) creed
Machine checks: pool/anchor/daily verbatim + split integrity, fleet dedup
(R1010 exact), em pre-fit ladder (largest feasible h2_size, zero-margin
exclusion, 38-step exclusion), VERT budget (R381).
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PIECE = HERE[:-4] if HERE.endswith("-tmp") else HERE
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(PIECE))))
POOL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00011.md"
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-09.md")

HOT_FULL = u"车子熄火距加油站仅 20 米，加油员拒绝打散装汽油，车主花 350 元拖车到加油站，到底是谁的问题？"
HOT1 = u"车子熄火距加油站仅 20 米，加油员拒绝打散装汽油，"   # row 1: comma-clause split
HOT2 = u"车主花 350 元拖车到加油站，到底是谁的问题？"        # row 2: remainder
R1 = u"守门人说，规矩不能松"          # zhixu/ceo_order
R2 = u"有难处，找我准没错"            # xiaqi/ceo_order
R3 = u"城主发令，咱悠着点"            # xiaoyao/ceo_order
CREED = u"差之毫秒，谬以全城。"
SERIES = u"城市速报 012"
SRCROW = u"今日热点 · 知乎热榜 2026-10-09"
SUBS = u"热点转述自知乎热榜·反应与信条皆取自虚构城市档案"

# --- 1) source verbatim assertions + split integrity
assert HOT1 + HOT2 == HOT_FULL, "hot split not character-preserving"
pools = json.load(io.open(POOL, encoding="utf-8"))
assert R1 in pools["axes"][u"秩序"]["ceo_order"], "R1 not verbatim in zhixu/ceo_order"
assert R2 in pools["axes"][u"侠气"]["ceo_order"], "R2 not verbatim in xiaqi/ceo_order"
assert R3 in pools["axes"][u"逍遥"]["ceo_order"], "R3 not verbatim in xiaoyao/ceo_order"
anchor = io.open(ANCHOR, encoding="utf-8").read()
assert CREED in anchor, "creed not verbatim in C-00011"
daily = io.open(DAILY, encoding="utf-8").read()
assert HOT_FULL in daily, "hot title not verbatim in daily brief"

# --- 2) fleet dedup (R1010 exact-line; self dir excluded)
cards_dir = os.path.join(ROOT, "data", "storylines", "cards")
collided = []
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
                if cand in ln:
                    collided.append((tag, d, ln))
assert not collided, "R1010 exact collisions: %s" % collided

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
H2_SIZE = 36               # selected ladder step (38 excluded by driver row)
SUBS_SIZE = 38
LINE_SPACING = 12
H1_GAP = 36
OPTICAL_CENTER = 0.24
SUBS_BOTTOM = 110

rows = [
    SRCROW,
    HOT1,
    HOT2,
    u"秩序轴：「%s」" % R1,
    u"侠气轴：「%s」" % R2,
    u"逍遥轴：「%s」" % R3,
    u"时空校准师信条：「%s」" % CREED,
]
h1_w = width(SERIES)
assert h1_w <= AVAIL / H1_SIZE, "H1 over budget"
budget38 = AVAIL / 38.0
driver_w = max(width(r) for r in rows)
assert driver_w == width(HOT1), "driver row is not HOT1 row"
assert width(HOT1) > budget38 - 0.2, "38-step not excluded: ladder selection broken (zero-margin rule)"
budget = AVAIL / H2_SIZE
lines_out = ["em-check-r1779 (REACT-v12 M2 front-fit + VERT R381)"]
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

# --- 4) R1010 probe evidence file
probe = []
probe.append("r1779_react_probe.txt - R1010 exact-line probe, REACT-v12 selected rows vs all fleet card faces")
probe.append("R1=%s" % R1)
probe.append("R2=%s" % R2)
probe.append("R3=%s" % R3)
probe.append("scan scope: data/storylines/cards/MC-*/cards.json (self excluded), exact substring")
probe.append("result: 0 collisions (build assertion passed)")
probe.append("bucket note: ceo_order REACT-series card-face FIRST USE; fleet-level first open = DAILY-v70 R1738 (yanhuo/17), rows disjoint, zero exact collision")

# --- 5) write piece files
meta = {
    "topic": "MC-20261009-REACT-v12",
    "line": u"L-卡 图文轻内容线（REACT 形态第十二件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
    "form": u"REACT 热点城市反应版 012（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第十一续件·R309 双律复用·热点择优判据第十二证=映射对位与纯热度同向的榜首直配首证——知乎源线第 10 用）——知乎热榜榜首热点转述×硅基城市台词池 ceo_order 令行情境桶反应（REACT 系列卡面首用）×时空校准师信条收束",
    "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
    "source_facts": (u"热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-09 第 1 条标题 verbatim 全题转述"
        u"（零裁零改字·跨两行=逗号子句排版位〔v1-v10 长题设计位复用·拆行字符保全断言〕·热度 870 万元数据只入 README 记账"
        u"不入卡面）·来源=data/intel/daily/2026-10-09.md zhihu-hot 第 1 条·知乎源线第 10 用"
        u"②反应行=BigLife 台词池 ceo_order 情境桶 verbatim 三轴位映射（秩序「守门人说，规矩不能松」"
        u"／侠气「有难处，找我准没错」／逍遥「城主发令，咱悠着点」——**ceo_order 桶=REACT 系列卡面首用**"
        u"〔fleet 面=DAILY-v70 R1738 已开桶族首行（烟火/17）·本件三行与已耗行全异行·R1010 exact 零冲突机核〕"
        u"·单桶纪律+三轴位纪律执行·编辑定谳=「城市的规矩本位」情境〔散装汽油是消防红线——加油员守的不是刁难是红线，"
        u"城市人懂这个理：规矩面前无例外〕·映射对位判据=三轴一一对应热点三面（规则坚守面/难处帮衬面/认规从容面——"
        u"「仅 20 米」的荒诞感由「差之毫秒」信条收束点破）·三轴全 on-argument·三句结构全异质（人物引语判断句/承诺句/"
        u"陈述态度句）·**三行全 CLEAN=R1010 卡面级 exact-line 探针零命中**〔build 断言·全 fleet cards.json 扫描〕）"
        u"③收束行=万人卡 C-00011 时空校准师信条 verbatim「差之毫秒，谬以全城。」（时空校准师·职业级署名=REACT 署名律"
        u"兼容·已登记字段 verbatim 零新增人格·人设权红线照守·**题眼级直配**：热点题眼「仅 20 米」×校准师「差之毫秒」="
        u"同构微小量词对仗——规矩的口子开在 20 米就不再是 20 米的口子，红线差一点就是全城的口子〔编辑定谳=城市规则观"
        u"金句级收束〕·**信条速报形态复用链第七续件**〔v6 C-00015/v7 C-00013/v8 C-00028/v9 C-00010/v10 C-00019/"
        u"v11 C-00016 后第七续·C-00011=REACT 收束位首用·CENSUS 互证位先例=C-00015 风控官「红灯是为所有人亮的，包括我」="
        u"规则域跨卡同域锚·非收束位不引信条〕）④城志互证锚注记=C-00015 风控官（「红灯是为所有人亮的，包括我」=规则"
        u"面前无例外域对应位·v6 收束位↔v12 互证位镜像·规矩域同族）"),
    "source_pointer": (u"data/intel/daily/2026-10-09.md（热点源·当日一份为真相）"
        u"+life/BigLife/cognition/pools.json 台词池 ceo_order 桶（跨仓只读·池句=情境口气零事实）"
        u"+life/BigLife/census/anchors/C-00011.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）"),
    "attribution_rule": (u"署名=轴级/职业级（秩序轴/侠气轴/逍遥轴/时空校准师·charter v1.2 署名律禁虚构居民名·人设权红线照守）；"
        u"热点=平台热榜转述（知乎热榜 2026-10-09 第 1 条·热度 870 万元数据只入 README 记账不入卡面·转述面合规="
        u"逐条来源链+不标题党+verbatim 全题零改字）"),
    "triple_label": (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——"
        u"热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）"
        u"+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）"),
    "editorial_value": (u"速报体裁+轴位映射=编辑选材面（ceo_order 桶候选→3 轴位对位判断：秩序=规则坚守位直配"
        u"〔「守门人说，规矩不能松」=加油员立场的城市正身——散装汽油是消防红线，守门人不松口不是刁难是守责·"
        u"「守门人」persona 与加油员=同一岗位位·人物引语判断句结构〕／侠气=难处帮衬位直配〔「有难处，找我准没错」="
        u"对车主 20 米困境的城市热心答案——规矩之内人情仍在，帮衬不越红线·承诺句结构〕／逍遥=认规从容位直配"
        u"〔「城主发令，咱悠着点」=350 元拖车后的城市心态——急事慢办，认了规则悠着点过·陈述态度句结构〕）"
        u"+时空校准师信条收束（规则之问×「差之毫秒，谬以全城。」=城市规则观金句级收束〔题眼：热点的荒诞感全在"
        u"「仅 20 米」——校准师一语点破：红线上的距离不分大小，差之毫秒谬以全城；加油员守的不是 20 米，是全城〕"
        u"+跨形态信条复用链第七续件〔C-00011 规则精度域=城市规则观同域居民档案〕+城志互证=C-00015 风控官"
        u"「红灯是为所有人亮的，包括我」规则域同族对应位）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」"
        u"「城市日签」平行连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕="
        u"映射对位与纯热度同向的榜首直配首证（第十二证）——zhihu #1 加油站散装汽油事件（870 万榜首）入选="
        u"城市规则日常事件本域直配〔ceo_order 桶 REACT 卡面首用+三轴位一一对应热点三面〕·榜首热度与映射对位同向"
        u"=择优律执行最顺形态；未选理由全量注记 19 条：**zhihu #2 祁连县征用宿舍官方回应=政务回应+具名地区+政策善后"
        u"评论面回避〔政治敏感面回避律〕／zhihu #3 国庆票房十三年新低=产业数据评论面无桶〔影视产业面〕／zhihu #4 "
        u"央行人民币汇率立场=金融政策+政治敏感面回避／zhihu #5 天台埋土坟维权=民事纠纷+维权敏感面回避〔阴宅忌讳面〕／"
        u"zhihu #6 字节Seed DeepSeek 性能漂移=具名企业商务新闻面回避〔R909/R1299 具名企业口径维持〕／zhihu #7 白酒"
        u"50-70后=食物酒族回避〔R313 注记维持〕+代际标签泛化面／zhihu #8 WTT 周启豪胜张本智和=具名当事人+体育赛果"
        u"评论面回避〔零具名当事人律·v11 孙颖莎同型〕／zhihu #9 德不配位 5A 景区=具名地区比较+批评面回避〔v10 "
        u"陕西铜川同型〕／zhihu #10 喊穷又疯狂旅游=消费观讨论面·逍遥 weekend festival 桶全已耗无诚实新鲜桶直配位"
        u"〔「穷」字面收入比较敏感度注记〕／bilibili #1 阴阳师咲耶CG=具名 IP 官方宣传面〔R909/R1030 IP 宣传面族〕／"
        u"bilibili #2 MrBeast 超市挑战=具名外国人+挑战内容面无城市事件锚／bilibili #3 妈妈是个超人=家庭情感内容面"
        u"无桶／bilibili #4 时光代理人 S3=具名 IP 影视宣传面／bilibili #5 我到底要怎么救你=剧情内容面／bilibili #6 "
        u"男巫 ZachKing 魔术=具名外国人内容面／bilibili #7 改造善良老人晚年=善意纪实 vlog 无城市事件锚〔v10 同型"
        u"维持〕／bilibili #8 好好吃饭=食物 vlog 面回避〔食物族〕／bilibili #9 带班主任体验黄毛=校园人物内容面无"
        u"事件锚／bilibili #10 长生契=影视剧情面**"),
    "hit_chain_m0": (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链〔「仅 20 米」的距离 vs 350 元的代价=微小量词"
        u"对仗反差具象在场+「到底是谁的问题」悬念追问=规则与人情的两难题面〕/情 1 日常共鸣非强极点〔G1 日常党+G5 "
        u"城市生活家+每位车主都可能遇到的规则课直配对位〕/时 2 当日热点=速报时效本体〔知乎热榜 2026-10-09 榜首在飞〕"
        u"/台 2 公众号方图承载=MC-001~166 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·"
        u"按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）"),
    "aspect_note": u"1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
    "red_line": (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim 全题转述零改写"
        u"零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00011 指针 README 双落〕／"
        u"脱敏（热度 870 万元数据不入卡面=README 记账·零具名当事人·车主加油员皆匿名主体·零仓位/密钥/token 量/未公开"
        u"财务面）；政治敏感面回避律照守（祁连县政务回应/央行汇率条不选）；健康宣称面回避零涉；成品只入库＝M5 账号"
        u"物理件未开+M4 全绿前零发布"),
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
                      u"秩序轴：「%s」" % R1,
                      u"侠气轴：「%s」" % R2,
                      u"逍遥轴：「%s」" % R3,
                      u"时空校准师信条：「%s」" % CREED],
        }
    ],
}

io.open(os.path.join(PIECE, "cards.json"), "w", encoding="utf-8").write(
    json.dumps(card, ensure_ascii=False, indent=1))
io.open(os.path.join(PIECE, "subs.srt"), "w", encoding="utf-8").write(
    u"1\n00:00:00,000 --> 00:00:02,600\n" + SUBS + u"\n")
io.open(os.path.join(PIECE, "em-check-r1779.txt"), "w", encoding="utf-8").write(
    "\n".join(lines_out) + "\n")
io.open(os.path.join(HERE, "r1779_react_probe.txt"), "w", encoding="utf-8").write(
    "\n".join(probe) + "\n")
print("BUILD OK: cards.json + subs.srt + em-check-r1779.txt + r1779_react_probe.txt")
print("\n".join(lines_out))
