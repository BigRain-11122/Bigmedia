# -*- coding: utf-8 -*-
"""R1420 REACT-v9 build: cards.json + subs.srt + em-check (M2 front-fit law).
MC-20261006-REACT-v9 = #59 10-06 hot window piece (zhihu #9 thirst-physiology +
heatwave bucket reactions + C-00010 porridge-stall creed closing).
F-156 pre-designated slot (R1419 waiting-state pointer, R978 precedent).
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VDIR = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261006-REACT-v9")
os.makedirs(VDIR, exist_ok=True)

# ---- verbatim sources (machine-asserted below) ----
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-06.md")
daily = io.open(DAILY, encoding="utf-8").read()
HOT_FULL = u"水刚咽下去，口渴怎么就缓解了？身体从哪里知道我喝水了？"
assert HOT_FULL in daily, "hot title not verbatim in daily brief"

POOLS = os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json")
pools = json.load(io.open(POOLS, encoding="utf-8"))
def line_of(axis, bucket, idx):
    return pools["axes"][axis][bucket][idx]
L1 = line_of(u"烟火", u"heatwave", 3)    # 卖西瓜嘞，又甜又解渴，来一斤？
L2 = line_of(u"侠气", u"heatwave", 6)    # 热天里喝杯凉茶最解渴
L3 = line_of(u"逍遥", u"heatwave", 6)    # 树荫下喝口凉茶真爽
assert L1 == u"卖西瓜嘞，又甜又解渴，来一斤？", L1
assert L2 == u"热天里喝杯凉茶最解渴", L2
assert L3 == u"树荫下喝口凉茶真爽", L3

ANCHOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00010.md")
anchor = io.open(ANCHOR, encoding="utf-8").read()
CREED = u"「灶上留一壶，路过的都是客。」"
assert CREED in anchor and u"数据粥铺摊主" in anchor, "creed/occupation not verbatim in anchor"

HOT_R1 = u"水刚咽下去，口渴怎么就缓解了？"
HOT_R2 = u"身体从哪里知道我喝水了？"
assert (HOT_R1 + HOT_R2) == HOT_FULL, "hot rows must concatenate to verbatim title"
assert HOT_FULL.startswith(HOT_R1), "row1 must be front substring start"

lines = [
    u"城市速报 009",
    u"今日热点 · 知乎热榜 2026-10-06",
    HOT_R1,
    HOT_R2,
    u"烟火轴：「%s」" % L1,
    u"侠气轴：「%s」" % L2,
    u"逍遥轴：「%s」" % L3,
    u"数据粥铺摊主信条：「灶上留一壶，路过的都是客。」",
]

meta = {
  "topic": "MC-20261006-REACT-v9",
  "line": u"L-卡 图文轻内容线（REACT 形态第九件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
  "form": u"REACT 热点城市反应版 009（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第八续件·R309 双律复用·R1030/R1160 两连判负窗后首件复窗·知乎源线第 7 用）——知乎热榜热点转述×硅基城市台词池 heatwave 情境桶反应×数据粥铺摊主信条收束",
  "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
  "source_facts": (u"热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-06 第 9 条标题 verbatim "
    u"全题转述（零裁零改字·双问句完整），设计排版跨两行（row1「水刚咽下去，口渴怎么就缓解了？」+"
    u"row2「身体从哪里知道我喝水了？」=v3/v4/v7/v8 引文跨两行设计排版先例·row1/row2 逐字拼接=全题）·"
    u"来源=data/intel/daily/2026-10-06.md zhihu-hot·知乎源线第 7 用〔v1 天气/v2 行情价/v3 财务自由/"
    u"v6 香菜/v7 衬衫价格 zhihu+v5/v8 bilibili 后 zhihu 第 7 用〕②反应行=BigLife 台词池 heatwave 情境桶 "
    u"verbatim 三条轴位映射（烟火轴 heatwave/3「卖西瓜嘞，又甜又解渴，来一斤？」／侠轴 heatwave/6"
    u"「热天里喝杯凉茶最解渴」／逍遥轴 heatwave/6「树荫下喝口凉茶真爽」——**单桶纪律**=口渴/解渴情境→"
    u"heatwave 桶〔解渴句驻桶·系列第 9 个不同桶=v1 rain/v2 market_open/v3 market_close/v4-v5 weekend/"
    u"v6 morning/v7 night/v8 festival 后 heatwave 首用·桶新鲜度=反套路化正面证据〕·三轴全 on-argument"
    u"（叫卖解渴面/喝茶解渴面/乘凉享受面=全题「口渴→缓解」的三个市民答案位）·三句结构全异质（叫卖招呼句式/"
    u"陈述直配句式/感叹句式·零人称口气句执行）·**三行全 CLEAN=卡面级 shingle 碰撞律 R1010 探针零命中**"
    u"〔r1420_react_probe.txt 机核·池扫描→fleet 全卡面 2-5 字 shingle 对撞→三行全零〕）"
    u"③收束行=万人卡 C-00010 顾阿凤信条 verbatim「灶上留一壶，路过的都是客。」（数据粥铺摊主·职业级署名"
    u"不指名=REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·给水待客域=话题同域锚"
    u"〔「身体从哪里知道我喝水了」的题眼=城市早有答案：灶上永远留一壶，路过的都能喝上·信条↔热点题眼级直配〕"
    u"·信条速报形态首用·语录/图鉴/速报跨形态信条复用链续证）④城志互证锚注记=C-00016 徐根福（QUANT 食堂"
    u"大厨·绿盘日免费例汤=城内「给喝的」对应位注记·非收束位不引信条）"),
  "source_pointer": (u"data/intel/daily/2026-10-06.md（热点源·当日一份为真相）"
    u"+life/BigLife/cognition/pools.json 台词池 heatwave 桶（跨仓只读·池句=情境口气零事实）"
    u"+life/BigLife/census/anchors/C-00010.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）"),
  "attribution_rule": (u"署名=轴级/职业级（烟火轴/侠气轴/逍遥轴/数据粥铺摊主·charter v1.2 署名律禁虚构居民名·"
    u"人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-10-06 第 9 条·热度 105 万=元数据只入 README 记账"
    u"不入卡面·转述面合规=逐条来源链+不标题党+verbatim 全题零改字）"),
  "triple_label": (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」"
    u"——热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）"
    u"+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）"),
  "editorial_value": (u"速报体裁+轴位映射=编辑选材面（heatwave 桶候选→3 轴位对位判断：烟火=叫卖解渴面直配位"
    u"〔「卖西瓜嘞，又甜又解渴，来一斤？」=摊贩对渴的街头答案·「解渴」题眼词直配位·叫卖招呼句结构〕／"
    u"侠气=喝茶解渴面直配位〔「热天里喝杯凉茶最解渴」=口渴缓解的市民第一答案·「解渴」题眼词直配位·"
    u"陈述直配句结构〕／逍遥=乘凉享受面直配位〔「树荫下喝口凉茶真爽」=喝水之外的城市式舒适解法·题眼问句的"
    u"生活方式回答位·感叹句结构〕）+数据粥铺摊主信条收束（身体怎么知道喝水×「灶上留一壶，路过的都是客。」"
    u"=待客给水金句级收束〔题眼：城市对「渴」的回答早就写在一壶热水里〕+跨形态信条复用链〔C-00010 信条"
    u"速报形态首用·给水待客域=话题同域居民档案〕+城志互证=C-00016 徐根福绿盘日免费例汤「给喝的」对应位）"
    u"+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」「城市日签」平行连载识别结构·编辑价值防低创作度"
    u" 7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=映射对位优先于纯热度第九证（zhihu #9 105 万"
    u"heatwave 桶三面位级直配〔叫卖解渴面+喝茶解渴面+乘凉享受面=heatwave 桶三轴全直配·全题双问句与三轴位+"
    u"信条一一对应〕入选·未选理由全量注记：bilibili #1 诡异的她剧集纯享=影视综艺内容面无映射位〔R909 影视"
    u"五连注记维持〕／#2 大学生爆改宿舍=校园家居改造面池无宿舍/改造桶〔探针 D 组零命中·R575 科普面无桶同型〕／"
    u"#3 我上哪给你整假的=影视内容面无映射位／#4 惊惊惊惊惊惊惊惊了=脑洞抽象面无桶〔R455 发量同型〕／"
    u"#5 看这个视频我不烧心=健康暗示面回避〔R1030 健康纹身同型〕／#6 AIZO 司凤版=音乐内容面+具名 IP 宣传面"
    u"〔R1030 音乐面注记维持〕／#7 夏果新片山鸟=影视宣传内容面／#8 Windows XP 开机音乐=科技怀旧科普面池无"
    u"开机/系统桶〔探针 C 组零开机/系统行·R455 可燃冰/小米防窥屏=科技面无桶同型〕／#9 印度军事=政治军事敏感面"
    u"回避／#10 斥巨资买衣服=消费购物面价格族三连同构〔v2 牛肉涨价+v7 衬衫价格已耗=R455 早餐月卡同型规避〕"
    u"+vlog 无事件锚／zhihu #1 华为高通专利协议=具名企业商务新闻面+华为族〔R909/R1299 具名企业口径维持〕+"
    u"专利许可面无情境桶／#2 巴西总统选举=外国政治敏感面回避／#3 国安部通报非法采血样=国家安全敏感面回避"
    u"〔不转述不评论〕／#4 日本窄轨铁路=交通制式科普面探针全撞〔A 组池内零轨交行·慢系/船系行全与既有卡面 "
    u"shingle 相撞=R1010 卡面碰撞律·无 CLEAN 直配行=不可诚实配对·判负留痕 P-2026-09-28-02〕／#5 耐克股价跌"
    u"50% 裁员重组=具名企业+股价市场族〔R455 价格族三连同构规避+v8 车企产业数据同型〕／#6 生化危机大银幕="
    u"影视观影体验面无映射位／#7 明军萨尔浒之战=历史战争科普面无情境桶〔R909 地球自转天文科普同型〕／"
    u"#8 医生辟谣 HPV 高铁座椅=健康辟谣面回避〔R1030 健康纹身同型·医疗建议邻位不转述〕／#10 蜗居小贝不借"
    u"6 万=影视剧评价面〔具名剧集内容面无映射位〕+借贷存款敏感理财面回避）"),
  "hit_chain_m0": (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔人人每天喝水的最平常事×「身体从哪里知道」"
    u"反直觉双问句好奇缺口=喝水越平常·问句越抓人·知乎热榜当日=具体稀缺性〕/情 1 生活小智慧温和共鸣非强极点"
    u"〔G1 日常党+G2 生活家直配对位〕/时 2 当日热点=速报时效本体〔知乎热榜在飞〕/台 2 公众号方图承载="
    u"MC-001~068 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 "
    u"hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）"),
  "aspect_note": u"1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
  "red_line": (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim "
    u"全题转述零改写零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 "
    u"C-00010 指针 README 双落〕／脱敏（热度 105 万元数据不入卡面=README 记账·零具名当事人·零仓位/密钥/"
    u"token 量/未公开财务面）；政治敏感面回避律照守（华为高通/巴西选举/国安部/印度军事条不选）；健康宣称面"
    u"回避（HPV 辟谣条不转述不背书·本件三池句=日常口语非医疗断言·「解渴」=直接生理描述非疗效宣称）；"
    u"成品只入库＝M5 账号物理件未开+M4 全绿前零发布"),
}

cards = {
  "meta": meta,
  "video": {"width": 1080, "height": 1080, "fps": 30, "bg": "black"},
  "font": {"file": "C:/Windows/Fonts/msyh.ttc", "cards_size": 50, "subs_size": 38,
           "subs_bottom": 110, "aigc_size": 30, "line_spacing": 12,
           "h1_font": "C:/Windows/Fonts/msyhbd.ttc", "h1_size": 84, "h1_color": "accent",
           "h2_size": 36, "h2_color": "white", "h1_gap": 36, "optical_center": 0.24},
  "aigc_notice": "[AIGC·AI 生成内容]",
  "tail": 0.8,
  "cards": [{"start": 0.0, "end": 2.6, "lines": lines}],
}

cj = os.path.join(VDIR, "cards.json")
with io.open(cj, "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)

srt = u"1\n00:00:00,000 --> 00:00:02,600\n热点转述自知乎热榜·反应与信条皆取自虚构城市档案\n"
with io.open(os.path.join(VDIR, "subs.srt"), "w", encoding="utf-8") as f:
    f.write(srt)

# ---- em budget front-fit (M2 law) + vertical stack (R381 law) ----
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import render_card_video as R
H2 = 36
budget_em = (1080 - 160) / float(H2)   # 920px usable, ladder doc basis
rows = []
ok = True
for ln in lines[1:]:
    cost = R._line_cost(ln)
    rows.append((ln, cost))
    if cost > budget_em:
        ok = False
h1 = R._line_cost(lines[0])
subs_top = 1080 - 110 - 38
pitch = 1.35 * H2 + 12
h1_h = 1.35 * 84 + 36
stack_bottom = 1080 * 0.24 + h1_h + len(rows) * pitch
vert_gap = subs_top - stack_bottom
vert_ok = vert_gap >= 20
report = ["em-check-r1420 (REACT-v9 M2 front-fit + VERT R381)"]
report.append("h2_size=%d budget=%.2fem  H1=%.2fem" % (H2, budget_em, h1))
for ln, cost in rows:
    report.append(u"%s%.2fem margin %+.2f  %s" % ("OK " if cost <= budget_em else "FAIL", cost, budget_em - cost, ln))
report.append("VERT: est bottom=%.0fpx subs_top=%dpx gap=%.0fpx %s (assert >=20)" % (
    stack_bottom, subs_top, vert_gap, "OK" if vert_ok else "FAIL"))
report.append("ALL-HORIZ: %s  VERT: %s" % ("PASS" if ok else "FAIL", "PASS" if vert_ok else "FAIL"))
with io.open(os.path.join(VDIR, "em-check-r1420.txt"), "w", encoding="utf-8") as f:
    f.write(u"\n".join(report) + u"\n")
assert ok and vert_ok, "em/vert budget FAIL - adjust ladder"
print("EM-OK budget=%.2f vertgap=%.0f" % (budget_em, vert_gap))
print("BUILD-OK", VDIR)
