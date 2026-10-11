# -*- coding: utf-8 -*-
# MC-20261012-REACT-v15 CPU leg (M0-M4): hot=2026-10-12 zhihu #2 (live-clipping money), bucket=market_open
# (3rd REACT use of market_open after v13; axes xiaqi/qiuxin/yanhuo all-line R1010-clean),
# closing anchor = C-00022 He Yuxin (anchor, streamer) creed, REACT-closing first-use.
# Mirrors build_react14.py (R1967). Fire-window tail (M4.5+E4+F-181) stays gated: e4_call.py staged turnkey.
import io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.normpath(os.path.join(HERE, '..', 'MC-20261012-REACT-v15'))
os.makedirs(MAIN, exist_ok=True)
sys.path.insert(0, os.path.join('src', 'render'))

HOT_FULL = u'大二专科生自述靠切片三年赚七百万，直播切片究竟是怎么赚钱的？这种赚钱模式能复制吗？'
HOT1 = u'大二专科生自述靠切片三年赚七百万，'
HOT2 = u'直播切片究竟是怎么赚钱的？这种赚钱模式能复制吗？'
POOL = {
 u'侠气': u'交易所一响，黄金万两',
 u'求新': u'看看别人怎么玩，我也来凑个热闹',
 u'烟火': u'小本生意也要精',
}
CREED = u'流量像潮水，我是灯塔不是渔船。'
subs = u'热点转述自知乎热榜·反应与信条皆取自虚构城市档案'

LINES = [
 u'城市速报 015',
 u'今日热点 · 知乎热榜 2026-10-12',
 HOT1,
 HOT2,
 u'侠气轴：「' + POOL[u'侠气'] + u'」',
 u'求新轴：「' + POOL[u'求新'] + u'」',
 u'烟火轴：「' + POOL[u'烟火'] + u'」',
 u'主播信条：「' + CREED + u'」',
]

# ---- ASSERT3/4: daily hot title verbatim + split integrity ----
daily = io.open(os.path.join('data', 'intel', 'daily', '2026-10-12.md'), encoding='utf-8').read()
seg = daily.split(u'## zhihu-hot', 1)[1]
hot2_line = [l for l in seg.splitlines() if l.startswith(u'2. ')][0][3:].strip()
assert hot2_line == HOT_FULL, 'daily hot mismatch: %r' % hot2_line
assert HOT1 + HOT2 == HOT_FULL

# ---- ASSERT1: pool verbatim x3 (xiaqi/qiuxin/yanhuo @ market_open) ----
pools = json.load(io.open(os.path.join(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition', 'pools.json'), encoding='utf-8'))
for axname, line in POOL.items():
    assert line in pools['axes'][axname]['market_open'], 'pool miss %s' % axname

# ---- ASSERT2: anchor creed verbatim (C-00022) ----
anchor = io.open(os.path.join(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors', 'C-00022.md'), encoding='utf-8').read()
crest = [l for l in anchor.splitlines() if l.startswith(u'**信条**')][0]
assert u'「' + CREED + u'」' in crest, 'creed parse fail'

# ---- ASSERT5: R1010 fleet exact-line probe x3 CLEAN (all cards.json) ----
hits = []
for root, _dirs, files in os.walk(os.path.join('data', 'storylines', 'cards')):
    if 'cards.json' in files and os.path.basename(root) != 'MC-20261012-REACT-v15':
        txt = io.open(os.path.join(root, 'cards.json'), encoding='utf-8').read()
        for line in POOL.values():
            if line in txt:
                hits.append((os.path.basename(root), line))
assert not hits, 'R1010 conflicts: %r' % hits

# ---- ASSERT6: C-00022 creed REACT-closing first-use (REACT series only) ----
for root, _dirs, files in os.walk(os.path.join('data', 'storylines', 'cards')):
    if 'cards.json' in files and 'REACT' in os.path.basename(root) and os.path.basename(root) != 'MC-20261012-REACT-v15':
        txt = io.open(os.path.join(root, 'cards.json'), encoding='utf-8').read()
        assert CREED not in txt, 'creed prior use in %s' % os.path.basename(root)

with io.open(os.path.join(MAIN, 'm1-assert-r2009.txt'), 'w', encoding='utf-8') as f:
    f.write(u'ASSERT1 pool verbatim x3 (xiaqi/qiuxin/yanhuo @ market_open) OK\n')
    f.write(u'ASSERT2 anchor creed verbatim (C-00022) OK\n')
    f.write(u'ASSERT3 daily hot title verbatim (zhihu #2 2026-10-12) OK\n')
    f.write(u'ASSERT4 hot split integrity OK\n')
    f.write(u'ASSERT5 R1010 fleet exact-line probe x3 CLEAN OK\n')
    f.write(u'ASSERT6 C-00022 creed REACT-closing first-use OK\n')

# ---- em ladder (front-fit) ----
from render_card_video import _em_cost  # noqa: E402

def cost(s):
    return sum(_em_cost(ch) for ch in s)

BUDGET_PX = 920.0
content = LINES[1:]
h2 = None
for cand in [50, 46, 44, 40, 36, 34, 32, 30, 28]:
    b = BUDGET_PX / cand
    if all(cost(l) < b for l in content):
        h2 = cand
        break
assert h2, 'no ladder size fits'
budget = BUDGET_PX / h2

em_lines = [u'em-check-r2009 (REACT-v15 M2 front-fit + VERT R381)']
em_lines.append(u'h2_size=%d budget=%.2fem  H1=%.2fem  ladder: 40档 budget 23.00em 驱动行 %.2fem EXCLUDED (over-budget)' % (h2, budget, cost(LINES[0]), cost(HOT2)))
for l in content:
    em_lines.append(u'OK %.2fem margin +%.2f  %s' % (cost(l), budget - cost(l), l))
sb = BUDGET_PX / 38.0
em_lines.append(u'subs %.2fem < %.2fem budget OK' % (cost(subs), sb))
pitch = 1.35 * h2 + 12
est_bottom = int(0.24 * 1080 + 84 + 36 + len(content) * pitch)
subs_top = 1080 - 110 - 38
gap = subs_top - est_bottom
em_lines.append(u'VERT: est bottom=%dpx subs_top=%dpx gap=%dpx %s (assert >=20)' % (est_bottom, subs_top, gap, u'OK' if gap >= 20 else u'FAIL'))
assert gap >= 20
em_lines.append(u'ALL-HORIZ: P')
with io.open(os.path.join(MAIN, 'em-check-r2009.txt'), 'w', encoding='utf-8') as f:
    f.write(u'\n'.join(em_lines) + u'\n')

# ---- cards.json ----
meta = {
 "topic": "MC-20261012-REACT-v15",
 "line": "L-卡 图文轻内容线（REACT 形态第十五件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
 "form": "REACT 热点城市反应版 015（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第十四续件·R309 双律复用·热点择优判据第十五证=同域题眼首证〔映射对位优先于纯热度执法：zhihu #1 郑钦文 1747 万榜首=具名当事人面回避弃选·取 #2=题眼级直配+本司商业面同域 explore#30 种子锚·卡面零自指〕）——知乎热榜直播切片变现题转述×硅基城市台词池 market_open 情境桶反应（market_open 桶=REACT 卡面第三用〔v13 新能源车后回桶·本件三轴侠气/求新/烟火与 v13 秩序/求新/逍遥全异行·R1010 exact 零冲突机核三线全过〕）×主播信条收束",
 "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
 "source_facts": "热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-12 第 2 条标题 verbatim 全题转述（零裁零改字·跨两行=逗号子句排版位〔v1-v14 长题设计位复用·拆行字符保全断言 HOT1+HOT2==HOT_FULL〕·热度 728 万元数据只入 README 记账不入卡面）·来源=data/intel/daily/2026-10-12.md zhihu-hot 第 2 条·知乎源线第 13 用②反应行=BigLife 台词池 market_open 情境桶 verbatim 三轴位映射（侠气「交易所一响，黄金万两」／求新「看看别人怎么玩，我也来凑个热闹」／烟火「小本生意也要精」——market_open 桶=REACT 卡面第三用〔v13 新能源车后回桶·三轴与 v13 全异轴全异行·R1010 exact 零冲突机核〕·单桶纪律+三轴位纪律执行·编辑定谳=「捞金三面镜像链」：暴富神话面〔三年七百万=财富神话叙事〕×侠气轴黄金万两俗语直配〔听财富神话的城市会心位·神话入耳不入心〕／跟风复制面〔「能复制吗」=全民凑热闹之问〕×求新轴凑热闹直配〔跟风本能诚实自白·凑完知道自己干的是什么〕／手艺真相面〔切片=剪辑功夫活〕×烟火轴小本生意也要精直配〔小买卖下真功夫=反「复制就赚钱」快餐论〕·三轴全 on-argument·三句结构全异质（俗语陈述句/口语顺承句/短陈述句）·映射对位判据=三轴一一对应热点三面）③收束行=万人卡 C-00022 何雨欣信条 verbatim「流量像潮水，我是灯塔不是渔船。」（主播·职业级署名=REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·**题眼级直配**：热点=流量捞金跟风之问〔渔船捞鱼心态〕×城市正身=灯塔非渔船〔职业本位定力〕=正反同构·**职业域对位**：主播=切片源头内容者〔直播切片自其直播间流出〕·收束位=内容者本人对变现之问的职业答卷）④城志互证锚注记=C-00024 缪一（字幕君·把自己复制两份=「能复制吗」题眼人物级镜像+与何雨欣「吵架只用剪辑术语」关系行在册=切片手艺域同族·v9 收束位↔本件互证位·非收束位不引信条）",
 "source_pointer": "data/intel/daily/2026-10-12.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json 台词池 market_open 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/C-00022.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）",
 "attribution_rule": "署名=轴级/职业级（侠气轴/求新轴/烟火轴/主播·charter v1.2 署名律禁虚构居民名·人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-10-12 第 2 条·热度 728 万元数据只入 README 记账不入卡面·转述面合规=逐条来源链+不标题党+verbatim 全题零改字·商业模式讨论面=中性事实转述判读〔「大二专科生」=匿名主体零具名当事人·反应行零行业褒贬断言·黄金万两/凑热闹/小本生意=通用生意语义〕·本司商业面同域=explore#30 种子锚·卡面零自指零平台名）",
 "triple_label": "虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）",
 "editorial_value": "速报体裁+轴位映射=编辑选材面（market_open 桶候选→3 轴位对位判断：侠气=暴富神话面直配〔「交易所一响，黄金万两」=听财富神话的城市俗语位——三年七百万入耳·黄金万两会心·神话听罢不入心·俗语陈述句结构〕／求新=跟风复制面直配〔「看看别人怎么玩，我也来凑个热闹」=「能复制吗」的城市诚实自白——凑热闹是本能·凑完知道自己干的是什么·口语顺承句结构〕／烟火=手艺真相面直配〔「小本生意也要精」=切片=小本买卖也得下真功夫的城市正身——反「复制就赚钱」快餐论·短陈述句结构〕）+主播信条收束（「流量像潮水，我是灯塔不是渔船。」=流量时代职业本位哲学金句级收束〔题眼：渔船捞金跟风=热点之问；灯塔引流定力=城市正身——职业域对位：主播=切片源头内容者·变现之问的职业答卷由内容者本人给出；C-00022 湘中县城网吧练到七段街「一步没省」=攒劲正身经历同构〕+跨形态信条复用链第十续件〔v6 C-00015/v7 C-00013/v8 C-00028/v9 C-00010/v10 C-00019/v11 C-00016/v12 C-00011/v13 C-00026/v14 C-00027 后第十续·C-00022=REACT 收束位首用·SC-005-04 F-176 音频正主+CENSUS 卡在册=跨载体复用合法·锚正卡字段本位非速报复用〕+城志互证=C-00024 缪一「把自己复制两份」复制题眼人物级镜像〔字幕君=切片手艺域同族·v9 收束位↔本件互证位〕）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」「城市日签」平行连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=同域题眼首证（第十五证）——zhihu #2 切片三年赚七百万（728 万）入选=题眼级直配（渔船×灯塔）+本司商业面同域 explore#30 种子锚·未选理由全量注记 19 条：zhihu #1 郑钦文夺冠（1747 万榜首）=体育赛果具名当事人面回避〔v14 判例律维持〕／zhihu #3 五子棋=文化考据面无情境桶直配行／zhihu #4 贵价面包闭店潮=**次优候选如实注记**（消费理性题·烟火桶有米价菜价行无「贵价/溢价」直配·映射弱于题眼级）／zhihu #5 火影新漫画=具名 IP 官方宣传面／zhihu #6 深圳春秋假=教育政策面无城市情境桶直配／zhihu #7 医院院长=医疗行业考据面+健康宣称邻域回避／zhihu #8 沙特机场遭袭=地缘政治冲突面=政治敏感回避律／zhihu #9 抗癌新疗法=健康宣称面回避／zhihu #10 哈夫病吃鱼=食品安全科普面+健康宣称邻域回避／bilibili #1 阴阳师十周年=具名 IP 官方宣传面／bilibili #2 谈恋爱=具名创作者内容面／bilibili #3 奥德赛重走=具名创作者内容面／bilibili #4 牧神记=具名 IP 官方宣传面／bilibili #5 你好邻居Mod=具名创作者内容面／bilibili #6 礼花家庭=具名创作者内容面／bilibili #7 邓肯恐怖事件=具名创作者+案件评论面／bilibili #8 苹果18大集=具名企业+具名创作者双面／bilibili #9 生命善待=具名创作者内容面／bilibili #10 《生》=具名创作者内容面",
 "hit_chain_m0": "M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔「大二专科生」×「三年赚七百万」=身份×数字强反差+「能复制吗」=全民跟风之问·池行题眼级镜像：热点「流量捞金渔船心态」×收束「我是灯塔不是渔船」=正反同构在场〕/情 1 商业吃瓜共鸣非强极点〔G2 商业观礼派+G5 日常党「搞钱」全民话题直配〕/时 2 当日热点=速报时效本体〔知乎热榜 2026-10-12 第 2 条在飞·728 万热度〕/台 2 公众号方图承载=MC-001~179 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）",
 "aspect_note": "1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
 "red_line": "aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim 全题转述零改写零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00022 指针 README 双落〕／脱敏（热度 728 万元数据不入卡面=README 记账·「大二专科生」=匿名主体零具名当事人·反应行零行业褒贬断言·零仓位/密钥/token 量/未公开财务面）；政治敏感面回避律照守（沙特地缘条/医院条不选）；健康宣称面回避零涉；成品只入库＝M5 账号物理件未开+M4 全绿前零发布",
}
card = {
 "meta": meta,
 "video": {"width": 1080, "height": 1080, "fps": 30, "bg": "black"},
 "font": {
  "file": "C:/Windows/Fonts/msyh.ttc",
  "cards_size": 50,
  "subs_size": 38,
  "subs_bottom": 110,
  "aigc_size": 30,
  "line_spacing": 12,
  "h1_font": "C:/Windows/Fonts/msyhbd.ttc",
  "h1_size": 84,
  "h1_color": "accent",
  "h2_size": h2,
  "h2_color": "white",
  "h1_gap": 36,
  "optical_center": 0.24,
 },
 "aigc_notice": "[AIGC·AI 生成内容]",
 "tail": 0.8,
 "cards": [{"start": 0.0, "end": 2.6, "lines": LINES}],
}
cj = os.path.join(MAIN, 'cards.json')
with io.open(cj, 'w', encoding='utf-8') as f:
    json.dump(card, f, ensure_ascii=False, indent=1)
print('cards.json written h2_size=%d' % h2)

with io.open(os.path.join(MAIN, 'subs.srt'), 'w', encoding='utf-8') as f:
    f.write(u'1\n00:00:00,000 --> 00:00:02,600\n' + subs + u'\n')
print('subs.srt written')

out_png = os.path.join(MAIN, 'MC-20261012-REACT-v15.png')
out_mp4 = os.path.join('.c3-tmp', 'r2009_react15_byproduct.mp4')
r = subprocess.run([sys.executable, os.path.join('src', 'render', 'render_card_video.py'),
                    '--cards', cj, '--poster', out_png, '--out', out_mp4],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
print('render rc=%d' % r.returncode)
if r.stdout.strip():
    print(r.stdout.strip()[-800:])
if r.returncode != 0:
    print(r.stderr.strip()[-1200:])
    sys.exit(1)
assert os.path.exists(out_png)
print('poster: ' + out_png)

# ---- E4 material (fire-window consumption source) ----
e4 = []
e4.append(u'# E4 参考仪材料 · MC-20261012-REACT-v15《城市速报 015·直播切片七百万之问》')
e4.append(u'')
e4.append(u'> 体裁：静态图文卡（1080×1080 公众号方图）·系列：城市速报（第十五件）·热点转述×虚构城市反应两态结构')
e4.append(u'> 画面结构（多模态逐字验图对齐）：左上角标 [AIGC·AI 生成内容] ／大标题（accent 色）／「今日热点 · 知乎热榜 2026-10-12」源行／热点问句两行／城市反应三行（侠气/求新/烟火轴）／信条收束行／底部两态声明行')
e4.append(u'')
e4.append(u'## 卡面全文（逐字）')
e4.append(u'')
for l in LINES:
    e4.append(l)
e4.append(u'')
e4.append(u'底部行：' + subs)
e4.append(u'')
e4.append(u'## 热点背景（转述来源）')
e4.append(u'')
e4.append(u'知乎热榜 2026-10-12 第 2 条（728 万热度）：大二专科生自述靠直播切片三年赚七百万，这种赚钱模式能否复制引发讨论。')
e4.append(u'')
e4.append(u'## 参考仪问题')
e4.append(u'')
e4.append(u'1. 刷到这张卡，你会停下来看完吗？哪里最抓你/最让你划走？')
e4.append(u'2. 内容真实感和可信度如何？有没有一眼假或空洞套话的地方？')
e4.append(u'3. 0-10 分你打几分？会点赞/转发/保存吗？为什么？')
with io.open(os.path.join(HERE, 'e4-material.md'), 'w', encoding='utf-8') as f:
    f.write(u'\n'.join(e4) + u'\n')
print('e4-material.md written')

print('BUILD-OK')
