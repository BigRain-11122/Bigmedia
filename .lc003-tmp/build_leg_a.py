# -*- coding: utf-8 -*-
# R684: LC-003 leg A - derive census-card-v13-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v13', 'MC-20260925-CENSUS-v13.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v13-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc003-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc003', 'cards-v1-matched.json')

# --- step 1: ffprobe LC-002 v8 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v8-vertical.mp4')],
                    capture_output=True)
print('[v8 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v13 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v13 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v13-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一把「真实时间」打进直播标题的主播」在帧（拆条形态=源卡即证据·F-032 成品卡 verbatim 行）",
    u"源卡档案行 C-00022·何雨欣/碳基市民·新市民派·女·25 岁在帧=居民档案面",
    u"源卡在帧=被读档案（拍文=锚 C-00022 职业行「主播——直播间的赛博后身——灯一开整个世界都要让路」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 经历字段「数字迁移潮第一班车…摊牌上写「代写文案，管饭就行」」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 经历转折字段「第一次用方言全程做了一场直播，弹幕全在刷「爷青回」…真话最带货」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 思想字段「她给自己立的规矩是直播间不夸大、不卖惨、不恰烂钱」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 钩子字段「开播时间表跟交易所钟声对齐，粉丝说等她开播像等开盘」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 行为字段「开播前必摸一摸门口的温度计…下播绕江走一圈复盘…每条粉丝来信都亲笔回」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 服装字段「发间一支旧钢笔——她第一次写通过稿时编辑送的，她给别成了发簪」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00022 思想字段「最想做成的一期节目，是把这座城里「上夜班的人」一个个拍给全世界看」+经历尾「正在筹备《夜班人》系列」展开·同源多用注记）",
    u"源卡信条行「信条：「流量像潮水，我是灯塔不是渔船。」」在帧（verbatim 直引）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00022）」在帧）",
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
j['meta']['storyboard'] = (u"LC-003 拆条形态=源卡即证据（LC-001/002 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00022 字段，"
                          u"画面=被读档案本体（F-032 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 轮内修红先例）；"
                          u"对位 12/12·同源多用逐拍注记")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
