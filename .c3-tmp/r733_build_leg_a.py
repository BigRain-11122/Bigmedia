# -*- coding: utf-8 -*-
# R733: LC-016 leg A - derive census-card-v1-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R729 build_leg_a.py adapted: C-00010 Gu Afeng / F-020 CENSUS-v1)
#        + pre-audit geometry: auto-detect intrusion (block_top<767); fix only if needed (R720 law, zero-char).
import json, io, os, subprocess, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v1', 'MC-20260925-CENSUS-v1.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v1-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc016-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc016', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG
assert os.path.getsize(PNG) == 221360, 'F-020 PNG size drift: %d' % os.path.getsize(PNG)

# --- step 1: ffprobe v15 reference ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v1 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v1 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v1-vertical.mp4'
REQS = [
    u"源画面=钩子位（锚 C-00010 钩子字段 verbatim「全城唯一记得每个早班信使口味的人」+钩子尾「谁的粢饭加不加辣、豆浆放不放糖，她心里有整本账」=卡锚列承载位·hook 尾缀「找到了」=系列同型 LC-003~LC-015）。",
    u"源画面=居民档案位（卡题行 C-00010·顾阿凤+物种行 verbatim「碳基市民·弄堂派」+性别年龄行「女 · 68 岁」·「女」由字卡列承载=b2 卡口分工·LC-013/LC-014/LC-015 同型）。",
    u"源画面=城区职业位（城区行 verbatim「北外滩·治理岸·脑环广场街区」+职业行首词「数据粥铺摊主」verbatim+破折号展开「早点摊的赛博后身——蒸笼里升腾的是暖光不是白汽，四大金刚一样不少」=压缩分载由源卡承载·LC-008/012/013/014/015 b3 同型）。",
    u"源画面=行为位（锚 C-00010 行为字段 verbatim「每天真实北京时间 04:30 开档，卖完最后一屉才收摊」+行为尾「给广场的电波猫群留碎布头（它们衔回去筑巢）」=卡锚列承载）。",
    u"源画面=转折位（锚 C-00010 经历转折字段 verbatim「进城第三年台风掀了棚子，是全街坊凑料帮着重搭的，从此这条街就是家」·punch 拍·同源多拍注记）。",
    u"源画面=出身位（锚 C-00010 经历头 verbatim「旧影像转生——从一张 1992 年董家渡早点摊的老照片里被城收留，照片里那口蒸笼现在还摆在铺头」·1992 数字形=口播全拼分载·LC-015 b6 一九七五同型·turn 拍·同源多拍注记）。",
    u"源画面=性格位（锚 C-00010 性格字段 verbatim「起早（天没亮就醒，说早上的城最真）· 嘴甜（夸人不重样，但句句都真心）」·类别词起早/嘴甜由卡锚列承载·LC-015 b7 同型·wink 拍·同源多拍注记）。",
    u"源画面=现状位（锚 C-00010 经历现状 verbatim「摊位在脑环广场西角」+「儿子在现实世界，每年来住半个月」+关系头「家户 H-1001 独居」=卡锚列承载·同源多拍注记）。",
    u"源画面=头一锅位（锚 C-00010 思想字段 verbatim「坚信一座城醒来的第一口热乎气比什么口号都金贵」+思想尾「每天头一锅暖光粢饭出笼时，她觉得全城都是她的熟客」=字卡呈现位·与钩子「全城熟客」语义回扣·proof 拍·同源多拍注记）。",
    u"源画面=互证位（锚 C-00010 关系字段 verbatim「棋友=时空校准师朱鸿奎（每周三杀一盘）」=第八对人物链卡面双端互证拍：C-00010×C-00011 双端在册·LC-015 b9/b10 前件点名兑现位·SC-001-02 有声线 ch.2 章尾冲突钩「周三棋局·彩头一座钟」=跨载体正典连接位=拆条系列首个「章尾钩兑现位」·proof 拍·同源多拍注记）。",
    u"源画面=信条位（锚 C-00010 信条字段 verbatim「灶上留一壶，路过的都是客。」保护行零动·close 拍·同源多拍注记）。",
    u"源画面=载体位（全档案载体=M5 公众号图文页·语境层承接位·发布锁=M5 账号物理件·CTA 句式=LC-001~LC-015 先例·非锚内事实=载体与转发位设计·cta 拍）。",
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

# --- step 3b: pre-audit geometry (R720 law standing face; fix only on intrusion) ---
sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import wrap_for_width
fw = int(j['video']['width'])
base_size = int(j['font']['cards_size'])
budget_em = (fw - 160.0) / base_size
print('budget_em=%.2f' % budget_em)
problems = []
audit_lines = []
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
        problems.append((i, n, top))
    audit_lines.append('card%02d b%-2d size=%d lines=%d block_top=%.0f net=%.0fpx -> %s'
                       % (i, i, size, n, top, top - 767, verdict))
    print(audit_lines[-1])
if problems:
    # R720 law: per-card size downgrade (smallest intervention) - verbatim zero-char
    for i, n, top in problems:
        c = cards[i]
        # find size so that n_lines*size pitch keeps top >= 787 (floor 20px net)
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

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-016 视觉动态=源卡即证据（LC-001~LC-015 同型）：12 拍共用源卡（CENSUS-v1 顾阿凤锚 C-00010 字段）；"
                          u"画面=静态图纵向派生（F-020 成品卡 660px 居中 y=160+zoompan ≤1.04 微动·AIGC 避让法=R511 前置（标签位=卡面左上=F-027/F-028/F-029/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12 逐拍字段级溯源对表（s1-review-material-v1.md 事实溯源对表）；"
                          u"**烟火早点摊主题系列首件位**（时间校准 LC-015 后烟火轴首件）；"
                          u"**第八对人物链卡面双端互证**（C-00010×C-00011 双端在册·LC-015 b9/b10 前件点名兑现位·SC-001-02 ch.2 章尾冲突钩=拆条系列首个「章尾钩兑现位」）；"
                          u"**跨载体复用最厚位**（网文 SC-001-01 主角+有声 F-009 ch.1 主角+图鉴 CENSUS-v1 F-020=三载体已验后视频线第四载体·R227 登记）；"
                          u"b9 互证拍=章尾钩兑现位注记。")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
