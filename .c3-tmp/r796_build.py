# -*- coding: utf-8 -*-
"""R796 REACT-v7 build: cards.json + subs.srt + em-check (M2 front-fit law)."""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VDIR = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261001-REACT-v7")
os.makedirs(VDIR, exist_ok=True)

# ---- verbatim sources (machine-asserted below) ----
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-01.md")
daily = io.open(DAILY, encoding="utf-8").read()
HOT_FULL = "如何看待江苏高考接近满分记叙文《衬衫的价格为 9 镑 15 便士》火了，为啥会引发大家的共鸣？"
assert HOT_FULL in daily, "hot title not verbatim in daily brief"

POOLS = os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json")
pools = json.load(io.open(POOLS, encoding="utf-8"))
def line_of(axis, bucket, idx):
    return pools["axes"][axis][bucket][idx]
L1 = line_of("怀旧", "night", 3)   # 老街的灯光，照亮了我半辈子的梦
L2 = line_of("逍遥", "night", 5)  # 梦里常回，那些年的灯与影
L3 = line_of("烟火", "night", 6)  # 夜深了，人散了，摊位上还留着烟火味
assert L1 == "老街的灯光，照亮了我半辈子的梦", L1
assert L2 == "梦里常回，那些年的灯与影", L2
assert L3 == "夜深了，人散了，摊位上还留着烟火味", L3

ANCHOR = os.path.join(ROOT, "..", "..", "life", "BigLife", "census", "anchors", "C-00013.md")
anchor = io.open(ANCHOR, encoding="utf-8").read()
CREED = "「城市不会忘记，除非我们偷懒。」"
assert CREED in anchor and "编年史馆员" in anchor, "creed/occupation not verbatim in anchor"

HOT_R1 = "如何看待江苏高考接近满分记叙文"
HOT_R2 = "《衬衫的价格为 9 镑 15 便士》火了"
assert (HOT_R1 + HOT_R2) in HOT_FULL, "hot rows must concatenate to verbatim substring"
assert HOT_FULL.startswith(HOT_R1), "row1 must be front substring start"

lines = [
    "城市速报 007",
    "今日热点 · 知乎热榜 2026-10-01",
    HOT_R1,
    HOT_R2,
    "怀旧轴：「%s」" % L1,
    "逍遥轴：「%s」" % L2,
    "烟火轴：「%s」" % L3,
    "编年史馆员信条：「城市不会忘记，除非我们偷懒。」",
]

meta = {
  "topic": "MC-20261001-REACT-v7",
  "line": "L-卡 图文轻内容线（REACT 形态第七件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
  "form": "REACT 热点城市反应版 007（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第六续件·R309 双律复用·知乎源线第 4 用）——知乎热榜热点转述×硅基城市台词池 night 情境桶反应×编年史馆员信条收束",
  "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
  "source_facts": ("热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-01 第 5 条标题 verbatim "
    "前段子串转述，设计排版跨两行（row1「如何看待江苏高考接近满分记叙文」+row2「《衬衫的价格为 9 镑 15 便士》火了」"
    "=v3/v4 引文跨两行设计排版先例；全题=「如何看待江苏高考接近满分记叙文《衬衫的价格为 9 镑 15 便士》火了，"
    "为啥会引发大家的共鸣？」·来源=data/intel/daily/2026-10-01.md zhihu-hot·排名与 185 万热度元数据不入卡面"
    "只入 README 记账=脱敏律·知乎源线第 4 用〔v1 天气/v2 行情价/v3 财务自由/v6 香菜后第 4 用〕）"
    "②反应行=BigLife 台词池 night 情境桶 verbatim 三条轴位映射（怀旧轴 night/3「老街的灯光，照亮了我半辈子的梦」"
    "／逍遥轴 night/5「梦里常回，那些年的灯与影」／烟火轴 night/6「夜深了，人散了，摊位上还留着烟火味」——"
    "**单桶纪律**=夜深回望记忆情境→night 桶〔系列第 7 个不同桶=v1 rain/v2 market_open/v3 market_close/"
    "v4-v5 weekend/v6 morning 后 night 首用·桶新鲜度=反套路化正面证据〕·sprite 位沿 v6 自觉弃用维持（观战位"
    "离记忆论题·三轴全 on-argument）·编辑选材 3 轴位=轴位映射律+反套路化选句律 v2 常态（三句结构全异质="
    "灯照长梦抒情句/梦里常回短句回环/人散留味场景叙事句·怀旧/逍遥双轴=v6 烟火/侠气/秩序后两轴首归））"
    "③收束行=万人卡 C-00013 林之恒信条 verbatim「城市不会忘记，除非我们偷懒。」（编年史馆员·职业级署名不指名="
    "REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·档案/记忆域=话题同域锚〔一句旧课本价格句"
    "二十年不散=城市不会忘记的满分证词·信条↔热点题眼级直配〕·CENSUS-v4/LC-017 跨形态信条复用链续证）"),
  "source_pointer": ("data/intel/daily/2026-10-01.md（热点源·当日一份为真相）"
    "+life/BigLife/cognition/pools.json 台词池 night 桶（跨仓只读·池句=情境口气零事实）"
    "+life/BigLife/census/anchors/C-00013.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）"),
  "attribution_rule": ("署名=轴级/职业级（怀旧轴/逍遥轴/烟火轴/编年史馆员·charter v1.2 署名律禁虚构居民名·"
    "人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-10-01 第 5 条·知乎源线第 4 用·转述面合规="
    "逐条来源链+不标题党+verbatim 子串零改字）"),
  "triple_label": ("虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」"
    "——热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落）"
    "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）"),
  "editorial_value": ("速报体裁+轴位映射=编辑选材面（night 桶候选→3 轴位对位判断：怀旧=集体记忆直配位"
    "〔「老街的灯光，照亮了我半辈子的梦」=半辈子的梦×一代人共同听过的课本句=共鸣题眼「为啥引发大家的共鸣」"
    "正面同构位·抒情长句结构〕／逍遥=记忆回返直配位〔「梦里常回，那些年的灯与影」=一句旧台词把人带回那些年"
    "=转述面「火了」机制同构位·短句回环结构〕／烟火=留存面直配位〔「夜深了，人散了，摊位上还留着烟火味」="
    "学生时代散场后句子还留着=旧句穿越二十年仍满分的存证位·场景叙事句结构〕）+编年史馆员信条收束"
    "（满分作文=一句 9 镑 15 便士被一代人记住×「城市不会忘记，除非我们偷懒。」=记忆档案对仗金句级收束"
    "〔题眼：所谓共鸣，就是城市没有偷懒〕+语录↔图鉴↔速报↔拆条跨形态信条复用链〔C-00013 信条速报形态首用·"
    "档案记忆域=话题同域居民档案·LC-017 F-072 前日收官件直连〕）+系列「城市速报」与「城市语录」「城市图鉴」"
    "「城市盘点」平行连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；"
    "热点择优判据留痕=映射对位优先于纯热度第七证（zhihu #5 三面位级直配〔共鸣面+回返面+留存面=night 桶三轴全直配·"
    "全题两问〔为什么火了/为啥引发共鸣〕与三轴位+信条一一对应〕入选·未选理由全量注记：zhihu #1 迪拜航空俄裔机长"
    "乌克兰裔副驾争吵=俄乌具名民族敏感面+空难隐患悲剧面=政治敏感/隐私双回避〔R455 寻亲同型〕／#2 25 岁博主胃癌"
    "去世=真实当事人死亡悲剧+隐私回避〔R455 同型〕／#3 GPT-6 我的世界种土豆=池 12 桶无游戏/数字世界情境桶"
    "〔v6 AMD 收购同型 ai_hit=0 口径〕+逍遥垂钓句=跨桶隐喻弱对位不算直配／#4 亚运男足中韩半决赛=竞技面无映射桶"
    "〔R309/R313/R455/R575/R643 五连注记维持〕／#6 王楚钦林诗栋退赛=竞技面无映射桶〔维持〕／#7 最好吃的淡水鱼="
    "食物族跨桶弱对位〔R313 河虾注记维持〕+烟火食物价格族与 v2 牛肉涨价主题族重叠〔R455 早餐月卡/R643 双汇同型规避〕"
    "／#8 虫子为啥不可爱=泛趣味科普面无情境桶／#9 OpenAI 个人助理 Dot=AI 产业新闻面池无科技/AI 桶〔v6 AMD 同型〕"
    "／#10 太阳系扁平向上飞=天文科普面无情境桶／bilibili #1 起名TV 爆笑小朋友=搞笑综艺面无映射位／#2 内蒙古野生卤虫="
    "自然科普面无桶／#3 李佳琦美妆新品秀=直播带货消费面无桶／#4 给阿嬷的情书=影视内容面无映射位〔R643 剧集同型〕"
    "／#5 三角洲行动二洲年庆典=游戏内容面池无游戏桶〔同 zhihu #3 口径〕／#6 身高 1 米管 2000 人=人物纪实面+具名当事人"
    "隐私回避／#7 艾希十周年续作众筹=游戏 IP 新闻面无桶／#8 哀牢山采菌子=户外安全警示面+食品安全邻域敏感"
    "〔R643 银鳕鱼同型〕菌子主题食物族跨桶弱对位／#9 90后00后童年含金量=怀旧主题族与入选件同族·择优取事件性更强者"
    "〔#5 有满分作文具体事件锚+课本句具体文本锚=纪实转述面强；本条=梗题无具体事件锚〕如实注记／"
    "#10 长生契剧情=剧集内容面无映射位〔维持〕）"),
  "hit_chain_m0": ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔一句课本里背过的旧价格句 vs 二十年后考场上写出"
    "接近满分=最小日常句×最高分值反差·9 镑 15 便士具体数字稀缺性+「课本台词活了」反差·知乎热榜当日=具体稀缺性〕"
    "/情 1 集体怀旧温和共鸣非强极点〔G5 吃瓜未来党+G4 集体记忆共鸣党对位〕/时 2 当日热点=速报时效本体〔知乎热榜在飞〕"
    "/台 2 公众号方图承载=MC-001~054 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·"
    "按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）"),
  "aspect_note": "1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
  "red_line": ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim "
    "前段子串转述零改写零加感叹·全题入 README〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·"
    "信条=户籍卡 C-00013 指针 README 双落〕／脱敏（排名/热度元数据不入卡面=README 记账·零仓位/密钥/token 量/"
    "未公开财务面·热点无具名当事人·高考作文=匿名化公开报道面）；政治敏感面回避律照守（迪拜航空俄乌民族条/博主去世条不选）；"
    "成品只入库＝M5 账号物理件未开+M4 全绿前零发布"),
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

srt = "1\n00:00:00,000 --> 00:00:02,600\n热点转述自知乎热榜·反应与信条皆取自虚构城市档案\n"
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
# vertical stack estimate (R381: pitch=1.35*size+ls, stack bottom <= subs_top-20)
subs_top = 1080 - 110 - 38
pitch = 1.35 * 36 + 12
h1_h = 1.35 * 84 + 36
stack_bottom = 1080 * 0.24 + h1_h + len(rows) * pitch
vert_gap = subs_top - stack_bottom
vert_ok = vert_gap >= 20
report = ["em-check-r796 (REACT-v7 M2 front-fit + VERT R381)"]
report.append("h2_size=36 budget=%.2fem  H1=%.2fem" % (budget_em, h1))
for ln, cost in rows:
    report.append("%s%.2fem margin %+.2f  %s" % ("OK " if cost <= budget_em else "FAIL", cost, budget_em - cost, ln))
report.append("VERT: est bottom=%.0fpx subs_top=%dpx gap=%.0fpx %s (assert >=20)" % (
    stack_bottom, subs_top, vert_gap, "OK" if vert_ok else "FAIL"))
report.append("ALL-HORIZ: %s  VERT: %s" % ("PASS" if ok else "FAIL", "PASS" if vert_ok else "FAIL"))
with io.open(os.path.join(VDIR, "em-check-r796.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")
print("\n".join(report))
assert ok and vert_ok, "em/vert budget FAIL - adjust ladder"
print("BUILD-OK", VDIR)
