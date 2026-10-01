# -*- coding: utf-8 -*-
"""R909 REACT-v8 build: cards.json + subs.srt + em-check (M2 front-fit law).
MC-20261002-REACT-v8 = #59 10-02 hot window piece (bilibili #8 cat-home-alone + pet sitter).
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VDIR = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261002-REACT-v8")
os.makedirs(VDIR, exist_ok=True)

# ---- verbatim sources (machine-asserted below) ----
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-02.md")
daily = io.open(DAILY, encoding="utf-8").read()
HOT_FULL = u"国庆放假百万网红猫留守家中！上门喂养师，能搞定我家猫咪的奇特怪癖吗？"
assert HOT_FULL in daily, "hot title not verbatim in daily brief"

POOLS = os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json")
pools = json.load(io.open(POOLS, encoding="utf-8"))
def line_of(axis, bucket, idx):
    return pools["axes"][axis][bucket][idx]
L1 = line_of(u"逍遥", u"festival", 17)   # 节日热闹，不如在家喝喝茶
L2 = line_of(u"烟火", u"festival", 12)    # 食堂师傅今天也得加班，做点好吃的
L3 = line_of(u"秩序", u"festival", 14)    # 这盏灯挂得正，夜里看家里才安心
assert L1 == u"节日热闹，不如在家喝喝茶", L1
assert L2 == u"食堂师傅今天也得加班，做点好吃的", L2
assert L3 == u"这盏灯挂得正，夜里看家里才安心", L3

ANCHOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00028.md")
anchor = io.open(ANCHOR, encoding="utf-8").read()
CREED = u"「灯不问来路，只管照路。」"
assert CREED in anchor and u"夜灯员" in anchor, "creed/occupation not verbatim in anchor"

HOT_R1 = u"国庆放假百万网红猫留守家中！"
HOT_R2 = u"上门喂养师，能搞定我家猫咪的奇特怪癖吗？"
assert (HOT_R1 + HOT_R2) == HOT_FULL, "hot rows must concatenate to verbatim substring"
assert HOT_FULL.startswith(HOT_R1), "row1 must be front substring start"

lines = [
    u"城市速报 008",
    u"今日热点 · B站热门 2026-10-02",
    HOT_R1,
    HOT_R2,
    u"逍遥轴：「%s」" % L1,
    u"烟火轴：「%s」" % L2,
    u"秩序轴：「%s」" % L3,
    u"夜灯员信条：「灯不问来路，只管照路。」",
]

meta = {
  "topic": "MC-20261002-REACT-v8",
  "line": u"L-卡 图文轻内容线（REACT 形态第八件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
  "form": u"REACT 热点城市反应版 008（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第七续件·R309 双律复用·B站源线第 2 用）——B站热门热点转述×硅基城市台词池 festival 情境桶反应×夜灯员信条收束",
  "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
  "source_facts": (u"热点转述律+反应抽取律 R309 双律复用：①热点行=B站热门 2026-10-02 第 8 条标题 verbatim "
    u"前段子串转述，设计排版跨两行（row1「国庆放假百万网红猫留守家中！」+row2「上门喂养师，能搞定我家猫咪的"
    u"奇特怪癖吗？」=v3/v4/v7 引文跨两行设计排版先例；全题前段=「国庆放假百万网红猫留守家中！上门喂养师，"
    u"能搞定我家猫咪的奇特怪癖吗？」〔原视频题尾「｜平平“无奇”的世界」=up主系列名注记不入卡面·up主名与排名"
    u"元数据不入卡面只入 README 记账=脱敏律〕·来源=data/intel/daily/2026-10-02.md bilibili-popular·"
    u"B站源线第 2 用〔v1 天气 zhihu/v2 行情价 zhihu/v3 财务自由 zhihu/v5 哈基米 bilibili/v6 香菜 zhihu/"
    u"v7 衬衫价格 zhihu 后 B 站源线第 2 用〕）"
    u"②反应行=BigLife 台词池 festival 情境桶 verbatim 三条轴位映射（逍遥轴 festival/17「节日热闹，不如在家"
    u"喝喝茶」／烟火轴 festival/12「食堂师傅今天也得加班，做点好吃的」／秩序轴 festival/14「这盏灯挂得正，"
    u"夜里看家里才安心」——**单桶纪律**=国庆节庆假期情境→festival 桶〔系列第 8 个不同桶=v1 rain/v2 market_open/"
    u"v3 market_close/v4-v5 weekend/v6 morning/v7 night 后 festival 首用·桶新鲜度=反套路化正面证据〕·三轴全"
    u" on-argument（留守面/喂养面/安心面）·编辑选材 3 轴位=轴位映射律+反套路化选句律 v2 常态（三句结构全异质="
    u"热闹对比句/加班叙事句/挂灯因果句·零人称口气句执行））"
    u"③收束行=万人卡 C-00028 十四号路灯信条 verbatim「灯不问来路，只管照路。」（夜灯员·职业级署名不指名="
    u"REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·照看/护送域=话题同域锚〔喂养师面对猫咪"
    u"奇特怪癖的题眼问句=「灯不问来路」的正面回答：不问怪癖，只管照看·信条↔热点题眼级直配〕·LC-006 F-060 "
    u"拆条件跨形态信条复用链续证）④城志互证锚注记=C-00029 咪喱（像素灵 radiocat·全巷公共宠物·罗大壮按月"
    u"画像《咪喱巷志》档案馆收副本=城内「网红猫」对应位·v5 哈基米件已用互证锚续用）+C-00026 高小满（穿城信使·"
    u"全城急件摆渡人=城内「上门服务者」对应位注记·非收束位不引信条）"),
  "source_pointer": (u"data/intel/daily/2026-10-02.md（热点源·当日一份为真相）"
    u"+life/BigLife/cognition/pools.json 台词池 festival 桶（跨仓只读·池句=情境口气零事实）"
    u"+life/BigLife/census/anchors/C-00028.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）"),
  "attribution_rule": (u"署名=轴级/职业级（逍遥轴/烟火轴/秩序轴/夜灯员·charter v1.2 署名律禁虚构居民名·"
    u"人设权红线照守）；热点=平台热榜转述（B站热门 2026-10-02 第 8 条·B站源线第 2 用·转述面合规="
    u"逐条来源链+不标题党+verbatim 子串零改字）"),
  "triple_label": (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自B站热门·反应与信条皆取自虚构城市档案」"
    u"——热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落）"
    u"+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）"),
  "editorial_value": (u"速报体裁+轴位映射=编辑选材面（festival 桶候选→3 轴位对位判断：逍遥=留守自在面直配位"
    u"〔「节日热闹，不如在家喝喝茶」=全城出门的节日里猫留守家中自得其乐=「留守」题眼正面同构位·热闹对比句结构〕"
    u"／烟火=假期出勤喂养面直配位〔「食堂师傅今天也得加班，做点好吃的」=节日里上门喂养师照常出勤开罐头=「喂养师」"
    u"职业题眼正面同构位·加班叙事句结构〕／秩序=照看安心面直配位〔「这盏灯挂得正，夜里看家里才安心」=喂养师上门"
    u"看过家里主人才能安心出远门=「能搞定吗」问句的安心面回答位·挂灯因果句结构〕）+夜灯员信条收束（百万网红猫的"
    u"奇特怪癖×「灯不问来路，只管照路。」=照看不追问金句级收束〔题眼：所谓搞定怪癖，就是先接住怪癖〕+语录↔图鉴↔"
    u"速报↔拆条跨形态信条复用链〔C-00028 信条速报形态首用·照看护送域=话题同域居民档案·LC-006 F-060 拆条件"
    u"直连〕+城志互证=C-00029 咪喱城内网红猫对应位〔《咪喱巷志》按月画像=网红猫档案直接对应·v5 互证锚续用〕）"
    u"+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」平行连载识别结构·编辑价值防低创作度 7.1-7.4"
    u"（charter §5 自动化合规上限）；热点择优判据留痕=映射对位优先于纯热度第八证（bilibili #8 festival 桶"
    u"三面位级直配〔留守面+喂养面+安心面=festival 桶三轴全直配·全题一问〔能搞定怪癖吗〕与三轴位+信条一一对应〕"
    u"入选·未选理由全量注记：bilibili #1 下一个是谁第七季=综艺内容面无映射位／#2 探秘日本最贵关东煮=食物族跨桶"
    u"弱对位〔R313 河虾/R643 双汇注记维持〕+价格族与 v2 行情价主题族重叠〔R455 同主题族规避〕+海外内容面／"
    u"#3 折断奥特钥匙大结局=影视内容面无映射位〔R643 剧集同型〕／#4 时光代理人第三季=影视内容面无映射位〔维持〕／"
    u"#5 大回忆时代=怀旧主题族与 v7 昨件同族·择优取事件性更强者〔v7 有高考满分作文具体事件锚+课本句文本锚="
    u"纪实转述面强；本条=音乐影像内容面无事件锚〕如实注记〔R643 zhihu #9 同型判〕／#6 章鱼哥快乐去哪了=影视梗"
    u"内容面无映射位／#7 iQOO 电竞宇宙=电竞产品发布面无桶〔科技/竞技双无位〕／#9 小米澎程N90 Max 打鸟=产品发布面"
    u"+户外摄影面无情境桶／#10 全网最爽职业=职业体验 vlog 面无事件锚〔市井百业=城内自有档案域·外采体验无映射位〕／"
    u"zhihu #1 华为赛力斯新五年合作=具名企业商务新闻面池无产业/商业桶+品牌具名面〔v6/v7 AMD·OpenAI 同型口径〕／"
    u"#2 车企 9 月销量数据=产业数据新闻面无情境桶〔同上口径〕／#3 土豆当主食瘦 25 斤=食物族跨桶弱对位〔R313/"
    u"R643 注记维持〕+健康宣称面合规回避〔不可证实的健康断言「脂肪肝没了血压血糖稳了」=医疗建议邻位红线·"
    u"不转述不背书〕／#4 地球自转 45 亿年=天文科普面无情境桶〔v7 #10 太阳系同型〕／#5 C 罗禁赛=竞技面无映射桶"
    u"〔R309/R313/R455/R575/R643 五连注记维持〕+具名当事人隐私回避／#6 大学生 AI 生成 PPT 代课=AI 工具面池无"
    u"科技/AI 桶〔v6/v7 同型〕+校园缺课争议批评面敏感／#7 中小学减负 5 天 8 小时=教育政策批评面敏感回避"
    u"〔R643 养老金同型〕／#8 华为 Mate 90 τ芯片=产品发布面无情境桶+具名品牌／#9 运营商叫停 0 元购机=产业监管"
    u"新闻面无情境桶／#10 月子中心=家庭消费争议+夫妻隐私面回避）"),
  "hit_chain_m0": (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔百万网红猫大排面 vs 国庆留守独守空房反差+"
    u"上门喂养师新职业稀缺性+「奇特怪癖」具体细节钩·B站热门当日=具体稀缺性〕/情 1 萌宠温和共鸣非强极点"
    u"〔G5 吃瓜未来党+G3 萌宠人群直配对位〕/时 2 当日热点=速报时效本体〔B站热门在飞+国庆假期当日双重时效〕/"
    u"台 2 公众号方图承载=MC-001~062 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·"
    u"按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）"),
  "aspect_note": u"1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
  "red_line": (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=B站热门标题 verbatim "
    u"前段子串转述零改写零加感叹·全题入 README〕／无来源不发布〔热点=B站热门+日期图内行·反应=台词池指针·"
    u"信条=户籍卡 C-00028 指针 README 双落〕／脱敏（up主名/系列名/排名元数据不入卡面=README 记账·零仓位/密钥/"
    u"token 量/未公开财务面·热点无具名当事人与具名猫=匿名化公开报道面·「网红猫」=粉丝量级描述非指名）；"
    u"政治敏感面回避律照守（华为/车企/C罗/政策批评条不选）；健康宣称面回避（土豆减肥条不转述不背书）；"
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

srt = u"1\n00:00:00,000 --> 00:00:02,600\n热点转述自B站热门·反应与信条皆取自虚构城市档案\n"
with io.open(os.path.join(VDIR, "subs.srt"), "w", encoding="utf-8") as f:
    f.write(srt)

# ---- em budget front-fit (M2 law) + vertical stack (R381 law) ----
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import render_card_video as R
budget_em = (1080 - 160) / 36.0   # 920px usable, ladder doc basis
rows = []
ok = True
for ln in lines[1:]:
    cost = R._line_cost(ln)
    rows.append((ln, cost))
    if cost > budget_em:
        ok = False
h1 = R._line_cost(lines[0])
subs_top = 1080 - 110 - 38
pitch = 1.35 * 36 + 12
h1_h = 1.35 * 84 + 36
stack_bottom = 1080 * 0.24 + h1_h + len(rows) * pitch
vert_gap = subs_top - stack_bottom
vert_ok = vert_gap >= 20
report = ["em-check-r909 (REACT-v8 M2 front-fit + VERT R381)"]
report.append("h2_size=36 budget=%.2fem  H1=%.2fem" % (budget_em, h1))
for ln, cost in rows:
    report.append(u"%s%.2fem margin %+.2f  %s" % ("OK " if cost <= budget_em else "FAIL", cost, budget_em - cost, ln))
report.append("VERT: est bottom=%.0fpx subs_top=%dpx gap=%.0fpx %s (assert >=20)" % (
    stack_bottom, subs_top, vert_gap, "OK" if vert_ok else "FAIL"))
report.append("ALL-HORIZ: %s  VERT: %s" % ("PASS" if ok else "FAIL", "PASS" if vert_ok else "FAIL"))
with io.open(os.path.join(VDIR, "em-check-r909.txt"), "w", encoding="utf-8") as f:
    f.write(u"\n".join(report) + u"\n")
print("\n".join(report).encode("utf-8", errors="replace").decode("ascii", errors="replace"))
assert ok and vert_ok, "em/vert budget FAIL - adjust ladder"
print("BUILD-OK", VDIR)
