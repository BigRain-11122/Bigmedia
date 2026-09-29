# -*- coding: utf-8 -*-
# R687: LC-004 leg A - derive census-card-v16-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260926-CENSUS-v16', 'MC-20260926-CENSUS-v16.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v16-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc004-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc004', 'cards-v1-matched.json')

# --- step 1: ffprobe LC-003 v13 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v13-vertical.mp4')],
                    capture_output=True)
print('[v13 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v16 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v16 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v16-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一保留「慢班渡轮」的船长——不为生意，只为给想慢慢看江的人留一趟船」在帧（拆条形态=源卡即证据·F-035 成品卡 verbatim 行）",
    u"源卡档案行 C-00025·陆海峰/碳基市民·弄堂派/男·52 岁在帧=居民档案面",
    u"源卡在帧=被读档案（拍文=锚 C-00025 职业行「渡轮船长——江上摆渡人——三流数据道的活船老大」verbatim 展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 思想字段「他爹是现实里黄浦江上的轮渡船长，他打小在码头长大，江的脾气全在骨头里」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 思想字段「数据道再快，他这条渡轮永远留着慢班，「给想看江的人留的」」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 行为字段「开航前绕船三圈（一步不少）」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 服装字段「腰间挂着一只旧铜哨——他爹传的，现在用来在雾天跟守夜灯灵对暗号」+关系字段「老友=守夜灯灵十四号路灯（雾天铜哨一响，灯灵必到）」展开·跨卡互证拍=C-00028 同场互指·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 经历字段「转折：一次大雾夜全船人合唱等雾散，那首歌成了船上的保留节目，他嘴上嫌吵，每回都减速唱完才靠泊」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 钩子字段「船票恒价：一句「多谢」」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00025 经历字段「正教一个想学开船的年轻人——「手艺不传就沉江了」」+关系字段「徒弟=穿城信使高小满」展开·跨卡互证拍=C-00026 双向对位·同源多用注记）",
    u"源卡信条行「信条：「船稳，人心才稳。」」在帧（verbatim 直引）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00025）」在帧）",
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
j['meta']['storyboard'] = (u"LC-004 拆条形态=源卡即证据（LC-001/002/003 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00025 字段，"
                          u"画面=被读档案本体（F-035 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 轮内修红先例）；"
                          u"对位 12/12·同源多用逐拍注记·b7 铜哨/b10 高小满=跨卡互证拍〔C-00028/C-00026〕")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
