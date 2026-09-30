# -*- coding: utf-8 -*-
# R700: LC-008 leg A - derive census-card-v12-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R697 build_leg_a.py adapted: C-00021 Wang Duoduo / F-031 CENSUS-v12)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v12', 'MC-20260925-CENSUS-v12.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v12-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc008-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc008', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-007 v18 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v18-vertical.mp4')],
                    capture_output=True)
print('[v18 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v12 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v12 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v12-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一能口哨唤来三只以上消息雀的孩子」在帧（拆条形态=源卡即证据·F-031 成品卡 verbatim 行）",
    u"源卡编号名称行「C-00021·王多多」+物种行「碳基市民·原生代·男·11 岁」在帧=居民档案面",
    u"源卡归属职务行「GAME 城·X026 城门区·像素小学学生」在帧（拍文=锚 C-00021 职业字段 verbatim「像素小学学生（信使小跟班）——放学就往驿站跑的编外学徒」展开·括号注=源卡承载〔R302 在案律〕·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 经历字段「城生城长——爹妈都在游戏楼上班」「家里人说他是『跟版本一起长的娃』」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 经历字段转折「第一次独立送完一封跨城急件……被驿站正式收为『小跟班』，那天他失眠了，激动的」展开·收为→收他当=L18 白话换位卡锚承载原词·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 关系字段「师父=穿城信使高小满（『等长到她那么高就能转正』）」展开·师徒对双向闭合拍=LC-005 高小满侧行为字段「等他长到我这么高就转正」同一转正之约两端=拆条系列首对人物链双向互证·跨卡互证拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 行为字段「养了一只没名字的纸飞机（他坚持它有灵魂）」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 经历现状字段「现状：四年级，数学一般，方向感全班第一」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 行为字段「放学绕路只为看一眼 commit 光点过江」展开·事实性赛博意象拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00021 服装字段「格子衫配帆布鞋（鞋带是自己改装的电致发光款——妈妈不知道）」展开·电致发光→发光=L18 白话换位卡锚承载原词·同源多用注记）",
    u"源卡信条行「信条：「放学别走，先把今天的谜想完。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00021）」在帧·载体位=M5 公众号图文页）",
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

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-008 拆条形态=源卡即证据（LC-001~LC-007 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00021 字段，"
                          u"画面=被读档案本体（F-031 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-035/F-036/F-038 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b6 师父高小满转正之约〔LC-005 高小满侧行为字段双向闭合=拆条系列首对人物链双向互证〕=跨卡互证拍·系列首件儿童居民拆条位")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
