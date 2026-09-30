# -*- coding: utf-8 -*-
# R745: LC-019 leg A - derive census-card-v5-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (12/12 source-card-as-evidence, field-level sourcing anchor C-00014)
#        (R741 build_leg_a.py adapted: C-00014 Zhou Haoyu / F-024 CENSUS-v5 / census 005)
#        + zero-bracket verification (col2 pure verbatim by design, R737/R741 strip-prevention)
#        + pre-audit geometry (R720 law, zero-char per-card size fix only on intrusion).
import json, io, os, subprocess, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v5', 'MC-20260925-CENSUS-v5.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v5-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc019-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc019', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG
assert os.path.getsize(PNG) == 224256, 'F-024 PNG size drift: %d' % os.path.getsize(PNG)

# --- step 1: ffprobe v15 reference ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v5 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v5 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v5-vertical.mp4'
REQS = [
    u"源画面=钩子位（锚 C-00014 钩子字段 verbatim「全城唯一给每个被毙策略写「讣告」的研究员——一行死因一行教训，攒了满满一本，同事借阅要排队」+钩子尾「找到了」=系列同型 LC-003~LC-018）。",
    u"源画面=居民档案位（卡题行 C-00014·周浩宇+物种行 verbatim「碳基市民 · 新市民派」·性别年龄行「男 · 28 岁」（28→二十八=口播数字读法全拼·「男」由字卡列承载=b2 卡口分工·LC-013/LC-014/LC-015/LC-016/LC-017/LC-018 b2 同型）。",
    u"源画面=城区职业位（城区行 verbatim「QUANT 城 · 扭塔算力街区」+职业行展开「量化策略研究员——扭塔里的研究员——真实行情是他的江水」=破折号展开压缩分载由源卡承载·LC-013~LC-018 b3 同型）。",
    u"源画面=盯盘规矩位（锚 C-00014 行为字段头 verbatim「盯盘时百毒不侵，收盘才想起泡面坨了」·beat 拍·年轮 2026-09-30 当日锚句「今儿个盯盘盯得有点晚…」=城市实况锚选材排除不进口播·M5 图文页语境候选·同源多拍注记）。",
    u"源画面=转折位（锚 C-00014 经历转折字段 verbatim「第一次策略上线被市场结结实实上了一课，从此把「敬畏」两个字纹在了工位上」·本件情绪峰=敬畏纹工位·punch 拍·同源多拍注记）。",
    u"源画面=川渝腔位（锚 C-00014 语言字段 verbatim「川渝腔：「要得」「巴适」「啥子」；行话：「因子」「回撤」「夏普」；汇报时秒变普通话，一紧张尾音就出卖他」·行话段「因子」「回撤」「夏普」不入口播由卡锚列承载〔夏普=黑话词表在列·因子/回撤=行话预防性分载·回撤=close 信条保护行单列直读〕·turn 拍·同源多拍注记）。",
    u"源画面=性格位（锚 C-00014 性格字段 verbatim「钻研（一个问题钻到底，饭都能忘）· 会折腾（日子要折腾出响儿才有味）· 守诺（说出口的字比章还硬）」·类别词钻研/会折腾/守诺由卡锚列承载·三词标签族 E4 弱位避让=口播取最生动两面·LC-018 b7 同型·wink 拍·同源多拍注记）。",
    u"源画面=全家福与平安消息位（锚 C-00014 服装字段头 verbatim「工牌挂绳上串着全家福小像（他娘非让挂的）」〔工牌→胸前的挂绳=口播 L18 卡口分工白话换位·卡锚列保留工牌原词〕+行为字段中段 verbatim「每晚给爹娘发一条消息，内容基本是「今天涨了」「今天没事」」+服装尾「袖口小屏只显示两样：行情、天气」=卡锚列承载位·双字段并拍=b8 fleet 同位·body 拍·同源多拍注记）。",
    u"源画面=一个道理验一万遍位（锚 C-00014 思想字段 verbatim「从川渝小城考出来那年，他爹说「钱的事最讲天理」。进了扭塔他才懂：策略不是赌运气，是把一个道理验一万遍」+思想门禁链句 verbatim「他最信门禁链——过不了的策略就是没道理，市场早晚教做人」=卡锚列承载位〔门禁=黑话词表在列·L18 卡口分工〕·本件主轴=验证纪律环=题材差异化角度位·proof 拍·同源多拍注记）。",
    u"源画面=互证位（锚 C-00014 关系字段 verbatim「食堂大厨徐根福总多给他打一勺（「长身体」——他都二十八了）」×关系字段 verbatim「风控官陈雅雯是他最怕又最服的人」=第十对人物链互证闭环后半件〔LC-018 b10 前件直连兑现·F-073 当日 10:44 收官·C-00014 关系字段被 LC-018 b10 引用后本件回引=双端闭合〕+C-00014 年轮 2026-09-30 相遇句×C-00015 年轮 2026-09-30 相遇句双端在册·BigMoney=虚构城市公司名选材排除+徐根福句=第十一对人物链前件埋点〔E20 LC-020 前件直连候选位〕·proof 拍·同源多拍注记）。",
    u"源画面=信条位（锚 C-00014 信条字段 verbatim「回撤教人做人，行情教人谦虚。」保护行零动·REACT-v4 F-051 信条收束行同句跨形态复用〔R575·收束位双源制第三态第二件：速报收束→拆条 close·F-067→LC-018 首件后本件第二件〕·close 拍·同源多拍注记）。",
    u"源画面=载体位（研究员全档案载体=M5 公众号图文页·语境层承接位·发布锁=M5 账号物理件·CTA 句式=LC-001~LC-018 先例·分享对象具明「转给相信敬畏市场的人」=punch 敬畏纹工位+信条行情教人谦虚受众侧对位设计·cta 拍）。",
]

with io.open(SRC_CARDS, encoding='utf-8') as fh:
    j = json.load(fh)
cards = j['cards']
assert len(cards) == 12, 'expect 12 beats, got %d' % len(cards)
durs = []
for i, c in enumerate(cards):
    durs.append((i, round(c['end'] - c['start'], 2)))
    c['visual'] = {'source': CARD_SRC, 'req': REQS[i]}
print('beat_durations', durs)
print('max_dur', max(d for _, d in durs))

# --- step 3a: zero-bracket verification (strip-prevention by design; R737/R741 precedent family) ---
for i, c in enumerate(cards):
    for ln in c['lines']:
        assert u'\u3014' not in ln and u'\u3015' not in ln, 'b%d col2 contains bracket annotation (design violation): %r' % (i, ln)
print('zero-bracket check: 12/12 col2 lines pure verbatim, no strip needed (R743 design)')

# --- step 3a-2: b8 fleet-longest col2 special fix (R720 law, R725 dot-split family, idempotent) ---
# 78-char subtitle = fleet-longest single col2 line (LC-017 max 61 chars). Size ladder 56..46 cannot
# reach the 787 fix floor (6 sub rows at 46 -> top 717.8, probe r745_wrap_probe.txt). Fix = newline-only
# semantic pre-split at 。/，boundaries (5 segments, zero-char verbatim per R293/R719/R725) +
# per-card size 36 (ladder extension below fleet floor 46, fleet-first case, em math in probe file)
# -> 6-line block, top 788.4, net 21.4px CLEAN (all-semantic row breaks; greedy-36 breaks mid-word
# "…天理」。进|了扭塔…" which pre-split prevents).
B8 = cards[8]
ORIG_B8 = (u"从川渝小城考出来那年，他爹说「钱的事最讲天理」。进了扭塔他才懂：策略不是赌运气，"
           u"是把一个道理验一万遍。他最信门禁链——过不了的策略就是没道理，市场早晚教做人")
b8_segs = [
    u"从川渝小城考出来那年，他爹说「钱的事最讲天理」。",
    u"进了扭塔他才懂：策略不是赌运气，",
    u"是把一个道理验一万遍。",
    u"他最信门禁链——过不了的策略就是没道理，",
    u"市场早晚教做人",
]
assert u''.join(b8_segs) == ORIG_B8, 'b8 segment join drift vs original col2'
assert u''.join(B8['lines'][1:]) == ORIG_B8, 'b8 col2 text drift (verbatim violation)'
if len(B8['lines']) == 2:
    B8['lines'] = [B8['lines'][0]] + b8_segs
    B8['size'] = 36
    print('b8 fix applied: 5-segment newline-only semantic pre-split + per-card size 36 '
          '(fleet-longest col2 78 chars; ladder extension below 46 floor; zero-char verified)')
else:
    assert len(B8['lines']) == 6 and int(B8.get('size', 0)) == 36, 'b8 rerun state unexpected'
    print('b8 fix already applied (idempotent rerun): 6 entries size 36')

# --- step 3b: pre-audit geometry (R720 law standing face; fix only on intrusion) ---
sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import wrap_for_width
fw = int(j['video']['width'])
base_size = int(j['font']['cards_size'])
budget_em = (fw - 160.0) / base_size
print('budget_em=%.2f' % budget_em)
problems = []
for i, c in enumerate(cards):
    size = int(c.get('size', base_size))
    n = 0
    for x in c['lines']:
        n += len(wrap_for_width(str(x), size, fw).split('\n'))
    pitch = size * 1.2 + 14
    text_h = n * pitch
    top = (1920 - text_h) / 2.0
    verdict = 'INTRUDES' if top < 767 else ('thin' if top < 787 else 'clean')
    if top < 767:
        problems.append(i)
    print('card%02d b%-2d size=%d lines=%d block_top=%.0f net=%.0fpx -> %s'
          % (i, i, size, n, top, top - 767, verdict))
if problems:
    # R720 law: per-card size downgrade (smallest intervention) - verbatim zero-char
    for i in problems:
        c = cards[i]
        for size_try in (56, 54, 52, 50, 48, 46):
            nn = 0
            for x in c['lines']:
                nn += len(wrap_for_width(str(x), size_try, fw).split('\n'))
            pitch = size_try * 1.2 + 14
            t2 = (1920 - nn * pitch) / 2.0
            if t2 >= 787:
                c['size'] = size_try
                print('FIX b%d: per-card size=%d -> %d lines top=%.0f net=%.0f (zero-char)' % (i, size_try, nn, t2, t2 - 767))
                break
        else:
            raise SystemExit('b%d cannot fix by size alone - needs dot-split' % i)
else:
    print('pre-audit: NO intrusion - no fix needed (R720 pre-emptive law not triggered)')

# --- final audit re-run (must be problems=NONE) ---
final_problems = []
for i, c in enumerate(cards):
    size = int(c.get('size', base_size))
    n = 0
    for x in c['lines']:
        n += len(wrap_for_width(str(x), size, fw).split('\n'))
    top = (1920 - n * (size * 1.2 + 14)) / 2.0
    if top < 767:
        final_problems.append((i, n, top))
print('FINAL_AUDIT problems=%s' % (final_problems if final_problems else 'NONE'))
assert not final_problems, 'post-fix audit still has intrusions'

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-019 视觉动态=源卡即证据（LC-001~LC-018 同型）：12 拍共用源卡（CENSUS-v5 周浩宇锚 C-00014 字段）；"
                          u"画面=静态图纵向派生（F-024 成品卡 660px 居中 y=160+zoompan ≤1.04 微动·AIGC 避让法=R511 前置（标签位=卡面左上=F-020/F-021/F-023/F-025/F-027/F-028/F-029/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12 逐拍字段级溯源对表（s1-review-material-v1.md 事实溯源对表）；"
                          u"**验证纪律环=题材差异化角度位**（思想字段「把一个道理验一万遍」主轴+经历转折「敬畏纹工位」——失败纪念面（钩子讣告）=钩子字段卡锚列承载非主轴·LC-002 纪念碑田/LC-012 毙稿档案近域避位=R723 注记差异化设计·量化近域三零断言承继 LC-018 先例〔零策略推荐/零收益承诺/零投资建议·M5 简介层合规位预留〕）；"
                          u"**第十对人物链互证闭环后半件**（C-00014×C-00015 双端在册·LC-018 F-073 当日 10:44 收官前件直连·C-00014 关系字段被 LC-018 b10 引用后本件回引=双端闭合）+第十一对人物链前件埋点（b10 徐根福句=E20 LC-020 前件直连候选位）；"
                          u"b10 互证拍=年轮相遇句双端在册位注记。")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
