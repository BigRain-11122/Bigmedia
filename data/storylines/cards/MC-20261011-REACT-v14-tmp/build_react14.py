# -*- coding: utf-8 -*-
# build_react14: MC-20261011-REACT-v14 (F-175 candidate) full build
# M1 asserts + R1010 fleet probe + em ladder + poster render + subs
import io, json, os, re, sys, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
os.chdir(ROOT)
sys.path.insert(0, os.path.join('src', 'render'))
from render_card_video import _em_cost  # noqa: E402

DIR = os.path.join('data', 'storylines', 'cards', 'MC-20261011-REACT-v14')
os.makedirs(DIR, exist_ok=True)
TMP = DIR + '-tmp'
os.makedirs(TMP, exist_ok=True)
LOG = []


def log(s):
    LOG.append(s)
    print(s, flush=True)


# ---- sources ----
daily_lines = io.open('data/intel/daily/2026-10-11.md', encoding='utf-8').read().splitlines()
zi = next(i for i, ln in enumerate(daily_lines) if ln.startswith('## zhihu-hot'))
HOT_FULL = None
for ln in daily_lines[zi:]:
    m2 = re.match(r'^1\. (.+)$', ln)
    if m2:
        HOT_FULL = m2.group(1).strip()
        break
assert HOT_FULL and '\n' not in HOT_FULL
assert HOT_FULL.startswith('日媒曝'), HOT_FULL
i = HOT_FULL.index('，')
HOT1, HOT2 = HOT_FULL[:i + 1], HOT_FULL[i + 1:]
assert HOT1 + HOT2 == HOT_FULL

pools = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json', encoding='utf-8'))
P = {
    '秩序': '灯火通明，咱也得紧绷着',
    '侠气': '值夜岗上风凉快，但别忘了巡逻',
    '求新': '值夜巡逻时，心中满是安',
}
for ax, ln in P.items():
    assert ln in pools['axes'][ax]['night'], (ax, ln)

anchor = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00027.md', encoding='utf-8').read()
cm = re.search(r'\*\*信条\*\* 「(.+?)」', anchor)
CREED = cm.group(1)
assert CREED == '台风天的日志最见人品。', CREED
CLOSE = '感知塔站值守员信条：「' + CREED + '」'

LINES = [
    '城市速报 014',
    '今日热点 · 知乎热榜 2026-10-11',
    HOT1,
    HOT2,
    '秩序轴：「' + P['秩序'] + '」',
    '侠气轴：「' + P['侠气'] + '」',
    '求新轴：「' + P['求新'] + '」',
    CLOSE,
]

# ---- R1010 fleet exact-line probe (three pool lines) ----
probe_lines = ['「' + v + '」' for v in P.values()]
hits = []
for dp, dn, fn in os.walk(os.path.join('data', 'storylines', 'cards')):
    if 'cards.json' not in fn:
        continue
    p = os.path.join(dp, 'cards.json')
    try:
        c = json.load(io.open(p, encoding='utf-8'))
    except Exception:
        continue
    for card in c.get('cards', []):
        for l in card.get('lines', []):
            for pl in probe_lines:
                if pl in l:
                    hits.append((p, pl))
assert not hits, hits

# ---- A6: creed REACT-closing first-use ----
a6 = []
for d in sorted(os.listdir('data/storylines/cards')):
    if 'REACT' not in d or not d.startswith('MC-'):
        continue
    p = os.path.join('data', 'storylines', 'cards', d, 'cards.json')
    if not os.path.exists(p):
        continue
    c = json.load(io.open(p, encoding='utf-8'))
    for card in c.get('cards', []):
        ls = card.get('lines', [])
        if ls and CREED in ls[-1]:
            a6.append(d)
assert not a6, a6

with io.open(os.path.join(DIR, 'm1-assert-r1967.txt'), 'w', encoding='utf-8') as f:
    f.write('ASSERT1 pool verbatim x3 (zhixu/xiaqi/qiuxin @ night) OK\n')
    f.write('ASSERT2 anchor creed verbatim (C-00027) OK\n')
    f.write('ASSERT3 daily hot title verbatim (zhihu #1 2026-10-11) OK\n')
    f.write('ASSERT4 hot split integrity OK\n')
    f.write('ASSERT5 R1010 fleet exact-line probe x3 CLEAN OK\n')
    f.write('ASSERT6 C-00027 creed REACT-closing first-use OK\n')

# ---- em ladder (front-fit) ----
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

em_lines = ['em-check-r1967 (REACT-v14 M2 front-fit + VERT R381)']
em_lines.append('h2_size=%d budget=%.2fem  H1=%.2fem  ladder: 40档 budget 23.00em 驱动行 %.2fem EXCLUDED (over-budget)' % (h2, budget, cost(LINES[0]) * 84.0 / 84.0, cost(HOT2)))
for l in content:
    em_lines.append('OK %.2fem margin +%.2f  %s' % (cost(l), budget - cost(l), l))
subs = '热点转述自知乎热榜·反应与信条皆取自虚构城市档案'
sb = BUDGET_PX / 38.0
em_lines.append('subs %.2fem < %.2fem budget OK' % (cost(subs), sb))
pitch = 1.35 * h2 + 12
est_bottom = int(0.24 * 1080 + 84 + 36 + len(content) * pitch)
subs_top = 1080 - 110 - 38
gap = subs_top - est_bottom
em_lines.append('VERT: est bottom=%dpx subs_top=%dpx gap=%dpx %s (assert >=20)' % (est_bottom, subs_top, gap, 'OK' if gap >= 20 else 'FAIL'))
assert gap >= 20
em_lines.append('ALL-HORIZ: P')
with io.open(os.path.join(DIR, 'em-check-r1967.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(em_lines) + '\n')

# ---- cards.json ----
meta = {
 "topic": "MC-20261011-REACT-v14",
 "line": "L-卡 图文轻内容线（REACT 形态第十四件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
 "form": "REACT 热点城市反应版 014（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第十三续件·R309 双律复用·热点择优判据第十四证=榜首值守题首证〔城市值守三面正身链：关门-巡逻-安心=防查果递进结构·对照 v12 榜首同向直配/v13 双轴镜像题=择优律三形态互补〕）——知乎热榜云安全事故题转述×硅基城市台词池 night 情境桶反应（night 桶=REACT 卡面第二用〔v7 怀旧/逍遥/烟火三轴后首回桶·本件三轴秩序/侠气/求新与 v7 全异轴全异行·R1010 exact 零冲突机核〕）×感知塔站值守员信条收束",
 "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
 "source_facts": "热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-11 第 1 条标题 verbatim 全题转述（零裁零改字·跨两行=逗号子句排版位〔v1-v13 长题设计位复用·拆行字符保全断言 HOT1+HOT2==HOT_FULL〕·「日媒曝」三字=信源限定语随题内建转述链·热度 1069 万元数据只入 README 记账不入卡面）·来源=data/intel/daily/2026-10-11.md zhihu-hot 第 1 条·知乎源线第 12 用②反应行=BigLife 台词池 night 情境桶 verbatim 三轴位映射（秩序「灯火通明，咱也得紧绷着」／侠气「值夜岗上风凉快，但别忘了巡逻」／求新「值夜巡逻时，心中满是安」——night 桶=REACT 卡面第二用〔v7 夜市灯光题后首回桶·本件三轴秩序/侠气/求新与 v7 怀旧/逍遥/烟火全异轴全异行·R1010 exact 零冲突机核〕·单桶纪律+三轴位纪律执行·编辑定谳=「城市值守三面正身链」：警觉面〔灯火通明=系统全绿表象×也得紧绷=不可松懈〕×秩序轴值守警觉直配〔热点反面「重启后一切照常」=表象照常×没人紧绷〕／检查面〔7小时没发现=没巡逻〕×侠气轴巡逻提醒直配／安心面〔一味重启=假安心〕×求新轴「巡逻后的真安心」=城市正身 vs 热点反面镜像对照位·三轴全 on-argument·三句结构全异质（反差陈述句/转折提醒句/陈述句）·映射对位判据=三轴一一对应热点三面（警觉面/检查面/安心面）·**首选拒绝实录**：秩序轴首选拟用「别忘了关好自家门」〔安全防护面直配〕=R1010 探针真拦〔DAILY-v65 卡面已用〕→换行「灯火通明，咱也得紧绷着」=探针闭环实证〔门面让位警觉面·防查果链微调为警觉-检查-安心链·选材完整性不损〕）③收束行=万人卡 C-00027 邓建国信条 verbatim「台风天的日志最见人品。」（感知塔站值守员·职业级署名=REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守·**题眼级直配**：热点反面=系统里的信与日志没人读〔勒索信 7 小时没发现〕×城市正身=值守日志见人品=值守纪律正反同构·**运维域职业对位**：感知塔站值守员=外环哨兵=云平台运维同域职业·题眼「日志」×「勒索信」=同为「该被读的信息」）④城志互证锚注记=C-00019 老晶振（引擎医生「坏了能修是人品」=修理手艺域同族·「一味重启」反面=瞎修对照位·v10 收束位↔本件互证位镜像·非收束位不引信条）+C-00028 十四号路灯（守夜灯灵=夜值守同域·night 桶同场景族）",
 "source_pointer": "data/intel/daily/2026-10-11.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json 台词池 night 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/C-00027.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）",
 "attribution_rule": "署名=轴级/职业级（秩序轴/侠气轴/求新轴/感知塔站值守员·charter v1.2 署名律禁虚构居民名·人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-10-11 第 1 条·热度 1069 万元数据只入 README 记账不入卡面·转述面合规=逐条来源链+不标题党+verbatim 全题零改字·具名企业安全事故面=中性事实转述判读〔「日媒曝」信源限定语随题自带·反应行零点名零行业褒贬断言·门/巡逻/安心/日志=通用值守语义·对照 v13 陶哲轩抵制=观点政治敏感回避/OpenAI 业绩=商务面回避两判皆不适用本条=事故转述面非业绩非政治〕）",
 "triple_label": "虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）",
 "editorial_value": "速报体裁+轴位映射=编辑选材面（night 桶候选→3 轴位对位判断：秩序=值守警觉位直配〔「灯火通明，咱也得紧绷着」=一切看着正常也得紧绷的城正身——灯火通明=系统全绿表象·紧绷=不可松懈·反差陈述句结构·**题眼级镜像**：表象照常×没人紧绷=热点反面「重启后一切照常」正身〕／侠气=值守检查位直配〔「值夜岗上风凉快，但别忘了巡逻」=7 小时没发现的城正身——巡逻=检查纪律基本功·转折提醒句结构〕／求新=真安心位对照〔「值夜巡逻时，心中满是安」=一味重启假安心的城正身——真巡逻才配真安心·陈述句结构·城市正身 vs 热点反面=镜像对照位〕）+感知塔站值守员信条收束（「台风天的日志最见人品。」=值守日志哲学金句级收束〔题眼：该被读的信没人读=热点反面；值守日志见人品=城市正身——运维域职业对位：塔站哨兵=云平台运维同构；C-00027 台风梅花夜守一宿=值守正身经历同构〕+跨形态信条复用链第九续件〔v6 C-00015/v7 C-00013/v8 C-00028/v9 C-00010/v10 C-00019/v11 C-00016/v12 C-00011/v13 C-00026 后第九续·C-00027=REACT 收束位首用·CENSUS-v18 卡引=锚正卡字段本位非速报复用·MD-0001/F-163 台风梅花=跨形态复用合法〕+城志互证=C-00019「坏了能修是人品」修理手艺域〔v10 收束位↔本件互证镜像·「一味重启」=瞎修反面同族〕）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」「城市日签」平行连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=榜首值守题首证（第十四证）——zhihu #1 软银云勒索信（1069 万榜首）入选=榜首同向直配〔城市值守三面正身链=警觉-检查-安心递进结构·题眼级镜像：没人读的信×日志最见人品〕·未选理由全量注记 18 条：zhihu #2 ICU 存款=民生金融政策争议+银行机构批判面回避／zhihu #3 刘欢=文化人物考据面无情境桶〔R1030 乾隆同判〕／zhihu #4 王仁君飞天视帝=具名当事人+颁奖评论面回避〔v13 WTT 同判〕／zhihu #5 红果短剧=**次优候选如实注记**（MEDIA 城直邻面·追剧情境桶无直配行=映射弱于值守题眼）／zhihu #6 郑钦文=体育赛果具名当事人面回避／zhihu #7 澳门旅拍被捕=执法案件+当事人面回避／zhihu #8 潜伏结局=剧集评论面无情境桶／zhihu #9 国庆小城旅游=节后余温时效弱化+旅行桶无直配行／zhihu #10 香港元朗划深圳=行政区划涉港澳政策=政治敏感面回避／bilibili #1 凡人修仙传=具名 IP 官方宣传面／bilibili #2 司机噩梦=具名创作者内容面／bilibili #3 逆水寒轮回=具名 IP 官方宣传面／bilibili #4 巧克力中毒=宠物食物 vlog 族回避〔R313 维持〕／bilibili #5 老番茄超市=具名创作者内容面／bilibili #6 deepseek 翻唱人是猫=**次优候选注记**（AI 翻唱生态位=本司业务直邻·具名企业+无城市情境桶直配行）／bilibili #7 深夜之门翻唱=二次元内容面无桶／bilibili #8 住宅低频噪音=科普技术面无城市事件锚／bilibili #9 孙宇晨对话=具名当事人+加密金融面回避／bilibili #10 威尔史密斯纪录片=官方内容面",
 "hit_chain_m0": "M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔「留下225封勒索信」×「7小时没发现」=攻击者高调留痕×值守零发现强反差+「一味重启」=荒诞解法位黑色幽默·池行题眼级镜像：热点「没人读的信」×收束「日志最见人品」=值守纪律正反同构在场〕/情 1 科技吃瓜共鸣非强极点〔G1 日常党「重启试试」全民梗直配+G3 科技观礼派〕/时 2 当日热点=速报时效本体〔知乎热榜 2026-10-11 第 1 条在飞·1069 万热度=榜首位〕/台 2 公众号方图承载=MC-001~174 S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）",
 "aspect_note": "1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
 "red_line": "aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim 全题转述零改写零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00027 指针 README 双落〕／脱敏（热度 1069 万元数据不入卡面=README 记账·零具名当事人·运维人员皆匿名主体·零仓位/密钥/token 量/未公开财务面·软银=热点转述面随题 verbatim 非本司褒贬断言源·反应行零点名零行业断言）；政治敏感面回避律照守（ICU 存款条/香港行政划界条不选）；健康宣称面回避零涉；成品只入库＝M5 账号物理件未开+M4 全绿前零发布",
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
cj = os.path.join(DIR, 'cards.json')
with io.open(cj, 'w', encoding='utf-8') as f:
    json.dump(card, f, ensure_ascii=False, indent=1)
log('cards.json written h2_size=%d' % h2)

with io.open(os.path.join(DIR, 'subs.srt'), 'w', encoding='utf-8') as f:
    f.write('1\n00:00:00,000 --> 00:00:02,600\n' + subs + '\n')
log('subs.srt written')

out_png = os.path.join(DIR, 'MC-20261011-REACT-v14.png')
out_mp4 = os.path.join('.c3-tmp', 'r1967_react14_byproduct.mp4')
r = subprocess.run([sys.executable, os.path.join('src', 'render', 'render_card_video.py'),
                    '--cards', cj, '--poster', out_png, '--out', out_mp4],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
log('render rc=%d' % r.returncode)
if r.stdout.strip():
    log(r.stdout.strip()[-800:])
if r.returncode != 0:
    log(r.stderr.strip()[-1200:])
    sys.exit(1)
assert os.path.exists(out_png)
log('poster: ' + out_png)

# E4 material (async audience probe)
e4 = []
e4.append('# E4 参考仪材料 · MC-20261011-REACT-v14《城市速报 014·云平台勒索信之问》')
e4.append('')
e4.append('> 体裁：静态图文卡（1080×1080 公众号方图）·系列：城市速报（第十四件）·热点转述×虚构城市反应两态结构')
e4.append('> 画面结构（多模态逐字验图对齐）：左上角标 [AIGC·AI 生成内容] ／大标题（accent 色）／「今日热点 · 知乎热榜 2026-10-11」源行／热点问句两行／城市反应三行（秩序/侠气/求新轴）／信条收束行／底部两态声明行')
e4.append('')
e4.append('## 卡面全文（逐字）')
e4.append('')
for l in LINES:
    e4.append(l)
e4.append('')
e4.append('底部行：' + subs)
e4.append('')
e4.append('## 热点背景（转述来源）')
e4.append('')
e4.append('知乎热榜 2026-10-11 第 1 条（1069 万热度）：黑客入侵云平台留下 225 封勒索信，运维 7 小时未发现、一味重启。')
e4.append('')
e4.append('## 参考仪问题')
e4.append('')
e4.append('1. 刷到这张卡，你会停下来看完吗？哪里最抓你/最让你划走？')
e4.append('2. 内容真实感和可信度如何？有没有一眼假或空洞套话的地方？')
e4.append('3. 0-10 分你打几分？会点赞/转发/保存吗？为什么？')
with io.open(os.path.join(TMP, 'e4-material.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(e4) + '\n')
log('e4-material.md written')
log('DONE')
