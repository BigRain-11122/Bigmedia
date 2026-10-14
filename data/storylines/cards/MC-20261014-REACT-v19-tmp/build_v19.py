# -*- coding: utf-8 -*-
"""MC-20261014-REACT-v19 build (R2256): M1 verbatim assertions + em-check + cards.json + subs.srt.
Pipeline: bigstream-lcard-pipeline (M0 hit-chain 7/8 A-档 judged in meta; machine asserts here).
Source faces:
  hot   = data/intel/daily/2026-10-14.md zhihu-hot #2 (verbatim)
  lines = life/BigLife/cognition/pools.json axes/{秩序,求新,侠气}/market_close (verbatim by index)
  close = life/BigLife/census/anchors/C-00023.md 信条 field (verbatim, non-honored seat)
  close rotation note: C-00015 风控官 line hit REACT-v6 face conflict (fleet catch) -> swap to C-00023 选题官
"""
import io, json, os, re, sys, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
LIFE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife'
CARD_DIR = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20261014-REACT-v19')
TMP_DIR = os.path.dirname(os.path.abspath(__file__))
R = 'R2256'

sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import _em_cost  # single truth glyph width

def read(p):
    return io.open(p, encoding='utf-8').read()

# ---------- 1. source faces ----------
brief = read(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-14.md'))
m = re.search(r'^2\.\s*(夫妻点一杯[^\n]+)$', brief, re.M)
assert m, 'zhihu #2 not found in daily brief'
HOT_FULL = m.group(1).strip()
HOT1, HOT2 = '夫妻点一杯58元咖啡只能一人落座，', '市监局称「一人一座一消费」合理与否不能一刀切判定，如何理解此事？'
assert HOT1 + HOT2 == HOT_FULL, 'hot split != full'

pools = json.load(io.open(os.path.join(LIFE, 'cognition', 'pools.json'), encoding='utf-8'))
L_ZHIXU  = pools['axes']['秩序']['market_close'][4]
L_QIUXIN = pools['axes']['求新']['market_close'][5]
L_XIAQI  = pools['axes']['侠气']['market_close'][5]
assert L_ZHIXU  == '别看这市场热闹，咱得守好规矩，才安稳'
assert L_QIUXIN == '街角的咖啡还香'
assert L_XIAQI  == '阿姨劝大家，别为这点事儿争吵'

anchor = read(os.path.join(LIFE, 'census', 'anchors', 'C-00023.md'))
mb = re.search(r'\*\*信条\*\* (.+)', anchor)
BELIEF = mb.group(1).strip()
assert BELIEF == '「毙稿不毙人，选题选良心。」', 'belief drift: ' + BELIEF
assert '荣誉' not in anchor[:400], 'honored-seat guard'

CLOSER = '选题官信条：' + BELIEF

# ---------- 2. card lines ----------
LINES = [
    '城市速报 019',
    '今日热点 · 知乎热榜 2026-10-14',
    HOT1, HOT2,
    '秩序轴：「%s」' % L_ZHIXU,
    '求新轴：「%s」' % L_QIUXIN,
    '侠气轴：「%s」' % L_XIAQI,
    CLOSER,
]
SUB = '热点转述自知乎热榜·反应与信条皆取自虚构城市档案'

# zero-conflict vs all prior card faces (fleet level: REACT + DAILY + all MC-* cards)
prev = []
for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-*', 'cards.json'))):
    if '-tmp' in os.path.dirname(f) or 'REACT-v19' in f:
        continue
    d = json.load(io.open(f, encoding='utf-8'))
    prev.extend(d.get('cards', [{}])[0].get('lines', []))
for ln in (LINES[4], LINES[5], LINES[6], CLOSER):
    assert ln not in prev, 'conflict with earlier card: ' + ln

# ---------- 3. em budget front-fit (ladder 50->46->44->40->36->32 excluded -> 28) ----------
def cost(t):
    return round(sum(_em_cost(ch) for ch in t), 2)

h1_cost = cost(LINES[0])
h1_budget = round(920 / 84, 2)
assert h1_cost <= h1_budget, 'H1 overflow'
h2_costs = [(ln, cost(ln)) for ln in LINES[1:]]
driver, driver_c = max(h2_costs, key=lambda x: x[1])
budget36 = round(920 / 36, 2)
budget32 = round(920 / 32, 2)
budget28 = round(920 / 28, 2)
assert driver_c > budget36, '36 tier unexpectedly admissible'
assert driver_c > budget32, '32 tier unexpectedly admissible'
for ln, c in h2_costs:
    assert c <= budget28, '28-tier overflow: %s %.2f' % (ln, c)
assert budget28 - driver_c >= 0.2, 'zero-margin exclusion'
sub_cost = cost(SUB)
sub_budget = round(920 / 38, 2)
assert sub_cost <= sub_budget, 'subs overflow'

# VERT est: h1 top at optical_center*H, block = h1 + gap + 7*h2 + 6*spacing
h1_top = 0.24 * 1080
block = 84 + 36 + 7 * 28 + 6 * 12
est_bottom = h1_top + block
subs_top = 1080 - 110 - 38
gap = subs_top - est_bottom
assert gap >= 20, 'VERT gap fail'

em_txt = ['em-check-%s (REACT-v19 M2 front-fit + VERT R381)' % R,
          'h2_size=28 budget=%.2fem (ladder: 36/32 excluded by driver line %.2fem>%.2f/%.2f -> 28 REACT 长热点标题档)' % (budget28, driver_c, budget36, budget32),
          'H1=%.2fem (h1 own face, h1_size=84, budget %.2fem margin +%.2f) OK' % (h1_cost, h1_budget, h1_budget - h1_cost)]
for ln, c in h2_costs:
    em_txt.append('OK    %.2fem margin +%.2f  %s' % (c, budget28 - c, ln))
em_txt.append('subs %.2fem < %.2fem budget OK' % (sub_cost, sub_budget))
em_txt.append('ALL-HORIZ: P')
em_txt.append('VERT: est bottom=%.0fpx subs_top=%dpx gap=%.0fpx (assert >=20) OK' % (est_bottom, subs_top, gap))

# ---------- 4. meta (M0 four-dim 7/8 judged, hit_chain in-data) ----------
meta = {
 "topic": "MC-20261014-REACT-v19",
 "line": "L-卡 图文轻内容线（REACT 形态第十九件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
 "form": "REACT 热点城市反应版 019（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第十八续件·R2256·bigstream-lcard-pipeline 技能产线第三十一用·R309 双律复用·热点择优判断第十九证=zhihu #2 258 万热度·民生消费题=城市买卖原生镜像面·映射对位优先于纯热度执法〔#4 168 万=v17 已消费·#5 116 万=v18 已消费·同窗零重复·#1/#3/#6/#7 敏感面全回避〕）——58 元咖啡一人一座之问×硅基城市市井买卖原生镜像×台词池 market_close 情境桶三轴位反应（v3 首采 2026-09-27 后回转=bucket 轮换律第二巡执行·三行全卡面零冲突机核）×风控官信条收束（换锚注：C-00015 风控官行 fleet 撞 REACT-v6 面=机核咬住当场换 C-00023 选题官）",
 "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
 "source_facts": "热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-14 第 2 条标题 verbatim 全题转述（零裁零改字·跨两行=逗号子句排版位〔v1-v18 长题设计位复用·拆行字符保全断言 HOT1+HOT2==HOT_FULL〕·热度 258 万元数据只入 README 记账不入卡面）·来源=data/intel/daily/2026-10-14.md zhihu-hot 第 2 条·知乎源线第 17 用；②反应行=BigLife 台词池 market_close 情境桶 verbatim 三轴位映射（秩序「别看这市场热闹，咱得守好规矩，才安稳」／求新「街角的咖啡还香」／侠气「阿姨劝大家，别为这点事儿争吵」——market_close 桶=REACT 卡面第二采〔v3 2026-09-27 首采后回转·12 桶全开巡后 bucket 轮换律第二巡执行〕·三行与全卡面零冲突机核（fleet 级 REACT+DAILY 全扫）·单桶纪律+三轴位纪律执行·编辑定谳=「店规三面镜像链」：规则面〔一人一座一消费=店规白纸黑字〕×秩序轴守规直配〔别看市场热闹·守好规矩才安稳=店家立场的本位陈述=店规正当性的市井答案〕／咖啡面〔58 元一杯=顾客要的不过一杯咖啡加一个座〕×求新轴直配〔街角的咖啡还香=消费纠纷里的不变日常·池行字面含「咖啡」=池-题字面直配系列首例〕／调解面〔市监局「不能一刀切判定」=个案裁量本位〕×侠气轴调解直配〔阿姨劝大家别为这点事儿争吵=城市调解位的原生镜像=监管裁量译成市民语=题眼级直配〕；③收束行=C-00023 选题官潘志明信条 verbatim「毙稿不毙人，选题选良心。」（碳基市民·原生代·MEDIA 城选题馆街区·选题官——职业级署名=REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·非荣誉席·题眼级直配=热点「一人一座合理与否之问」〔判定的两半：裁事不裁人+凭良心裁量〕×城市正身「毙稿不毙人，选题选良心」=店规判的是这单买卖合不合理·不是这对夫妻值不值得坐·「不能一刀切」=每单一单看的良心活·职业域对位=选题官=守门判定岗·「选题天平不斜」+每天毙稿三十留下三个=个案裁量的原生权威岗·C-00023 收束位=v1-v18 全未用=轮换律执行·换锚机核注=首选 C-00015 风控官信条行撞 REACT-v6 卡面〔fleet 级机核咬住=零直撞标准第三证〕·CENSUS-v14「信条：」前缀行与 REACT「选题官信条：」前缀行=行级异串合法并存〔C-00015 于 CENSUS-v6+REACT-v6 双前缀并存先例同型〕）",
 "source_pointer": "data/intel/daily/2026-10-14.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json 台词池 market_close 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/C-00023.md 选题官手写锚（跨仓只读·信条字段 verbatim·非荣誉席）",
 "attribution_rule": "署名=轴级/职业级（秩序轴/求新轴/侠气轴/选题官·charter v1.2 署名律禁虚构居民名·人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-10-14 第 2 条·热度 258 万元数据只入 README 记账不入卡面·转述面合规=逐条来源链+不标题党+verbatim 全题零改字·夫妻点咖啡=公开报道的消费纠纷事件转述=公开报道面·零具名自然人批判〔当事夫妻与店家均无姓名面〕·反应行零行业褒贬断言·规矩/咖啡/调解=城市买卖通用语义·卡面零自指零平台名）",
 "triple_label": "虚构级+来源级=图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）+AIGC 角标=常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）",
 "editorial_value": "速报体裁+轴位映射=编辑选材面（market_close 桶候选→3 轴位对位判断：秩序=店规正当性面直配〔「别看这市场热闹，咱得守好规矩，才安稳」=店规的本位辩护·热闹是生意·规矩是底色=对「合理与否」的店家立场镜像〕／求新=日常不变面直配〔「街角的咖啡还香」=吵完之后街角咖啡还在=消费纠纷的落点日常·池行字面含「咖啡」=池-题字面直配系列首例〕／侠气=调解裁量面直配〔「阿姨劝大家，别为这点事儿争吵」=城市调解位原生镜像=「不能一刀切」的市民语翻译〕·三句结构全异质〔立场式/落点式/调解式〕·映射对位=热点三面一一对应）——热点择优判断留痕=第十九证（#4 168 万=v17 已消费·#5 116 万=v18 已消费·同窗零重复执法·#2 258 万=入选〔民生消费题=城市买卖原生镜像面·硅基城市=市井买卖之城·店规/咖啡/调解=market 桶三轴位原生对位·求新轴池行字面含「咖啡」=字面直配系列首例·诚实注=v18 择优窗曾注「#2 映射弱」=彼窗科技题对比注非本题判·本题独立评估=三面全直配复证〕·#1 462 万=政治敏感面回避律〔执法未结案面全榜零涉〕·#3 190 万=暴力伤亡案件面回避·#6 109 万=具名当事人面回避·#7 106 万=具名艺人外貌评价面回避·#8=游戏动漫虚构面映射弱·#9/#10=具名 IP 讨论面映射弱·bilibili 10 条=具名 UP 主体裁面零直配行〔v14 判例复用〕）——城市视角独特性=活在建制系统里的城市看「一人一座一消费」=买卖本位的城市（人类问规则合不合理·硅基城市答规矩裁事不裁人、街角咖啡还香、有事好好说=把消费纠纷译成市井日常=系列 IP 独有视角）",
 "hit_chain_m0": "M0 选题四维分 7/8=A 档进 M1（钩 1 民生消费纠纷事实钩〔夫妻/58 元/一人落座=人物金额冲突三要素完整·好奇心中于消费纠纷族·弱于 v17 Karpathy 事件级故 1〕；情 2 全民消费场景强共鸣〔人人都当过顾客·人人都见过店规·规则与人情双立场=评论区站队势能·大众日常级〕；时 2 当日热榜在飞〔zhihu #2·258 万热度=榜内时效本体〕；台 2 民生消费题=城市原生镜像面最高适配〔硅基城市=市井买卖之城·店规/咖啡/调解=market 桶三轴位原生对位·求新轴池行字面含「咖啡」=字面直配系列首例·映射对位优先于纯热度执法〕）",
 "aspect_note": "1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
 "red_line": "aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律=不标题党〔热点行=知乎热榜标题 verbatim 全题转述零改写零加感叹〕/无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00015 指针·README 双落〕/脱敏（热度 258 万元数据不入卡面=README 记账·当事夫妻与店家均无姓名面=公开报道面转述零具名批判·零本司仓位/密钥/未公开财务面）/政治敏感面回避律照守（zhihu #1/#3/#6/#7 全回避·本卡零执法/政治/未结案面）/健康宣称面零涉及；成品只入库=M5 账号物理件未开+M4 全绿前零发布；F 登记位=F-187（F-186=v18 R2255 已登记·零顺延积压）",
 "h2_note": "em 预算前置适配律：驱动行=热点行第二段 %.2fem>32 档预算 28.75em=32 档被排除→降 28 档（%.2fem 预算·驱动行余量 +%.2fem·零余量排除律执法·28 档=REACT 长热点标题档）·文本 verbatim 零动只动版式档位" % (driver_c, budget28, budget28 - driver_c),
}
cards = {
 "meta": meta,
 "video": {"width": 1080, "height": 1080, "fps": 30, "bg": "black"},
 "font": {"file": "C:/Windows/Fonts/msyh.ttc", "cards_size": 50, "subs_size": 38, "subs_bottom": 110,
          "aigc_size": 30, "line_spacing": 12, "h1_font": "C:/Windows/Fonts/msyhbd.ttc",
          "h1_size": 84, "h1_color": "accent", "h2_size": 28, "h2_color": "white",
          "h1_gap": 36, "optical_center": 0.24},
 "aigc_notice": "[AIGC·AI 生成内容]",
 "tail": 0.8,
 "cards": [{"start": 0.0, "end": 2.6, "lines": LINES}],
}

os.makedirs(CARD_DIR, exist_ok=True)
io.open(os.path.join(CARD_DIR, 'cards.json'), 'w', encoding='utf-8').write(
    json.dumps(cards, ensure_ascii=False, indent=1))
io.open(os.path.join(CARD_DIR, 'subs.srt'), 'w', encoding='utf-8').write(
    "1\n00:00:00,000 --> 00:00:02,600\n%s\n" % SUB)
io.open(os.path.join(CARD_DIR, 'em-check-%s.txt' % R), 'w', encoding='utf-8').write('\n'.join(em_txt) + '\n')
io.open(os.path.join(CARD_DIR, 'm1-assert-%s.txt' % R), 'w', encoding='utf-8').write(
    "m1-assert-%s: HOT1+HOT2==HOT_FULL P (brief zhihu #2 verbatim); "
    "market_close lines verbatim-by-index P (pools.json zhixu[4]/qiuxin[5]/xiaqi[5]); "
    "belief verbatim P (C-00023 非荣誉席·换锚注=C-00015 撞 REACT-v6 面 fleet 咬住); zero-conflict vs all card faces (fleet scan) P; "
    "driver=%.2fem tier=28 margin=+%.2fem; ALL P\n" % (R, driver_c, budget28 - driver_c))
print('BUILD OK driver=%.2f est_bottom=%.0f gap=%.0f' % (driver_c, est_bottom, gap))
