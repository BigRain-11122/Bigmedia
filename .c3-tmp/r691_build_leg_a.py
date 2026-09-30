# -*- coding: utf-8 -*-
# R691: LC-005 leg A - derive census-card-v17-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R687 build_leg_a.py adapted: C-00026 Gao Xiaoman / F-036 CENSUS-v17)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260926-CENSUS-v17', 'MC-20260926-CENSUS-v17.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v17-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc005-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc005', 'cards-v1-matched.json')

# --- step 1: ffprobe LC-004 v16 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v16-vertical.mp4')],
                    capture_output=True)
print('[v16 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v17 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v17 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v17-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一给每单写「一句话交货注脚」的信使」在帧（拆条形态=源卡即证据·F-036 成品卡 verbatim 行）",
    u"源卡档案行 C-00026·高小满+物种行「碳基市民·新市民派·女·22 岁」在帧=居民档案面",
    u"源卡职业行「江面与光桥·光桥市集·穿城信使」在帧（拍文=锚 C-00026 职业字段「穿城信使——全城急件的摆渡人——光桥和渡轮是她家走廊」verbatim 展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 经历字段「跟着光桥修通进城的——桥那头是老家，桥这头是生计」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 经历字段转折「头一单加急件是给一位老人送药，跑丢了两次路，送到时天全黑，老人拉她吃了碗面」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 经历字段「从此她给自己立规矩：单可以少接，接了必须稳到」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 语言字段「全城口哨打得最响的姑娘，桥上的守夜灯灵都认得她那两声」展开·跨卡互证拍=C-00028 守夜灯灵同场互指·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 服装字段「包底永远有一把伞——不是给自己的，『桥上常有人淋着』」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 钩子字段「『今夜风大，交到本人手里』这样的字条，档案馆的年轻人专门收藏了一沓」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00026 关系字段「忘年交=渡轮船长陆海峰（她跨江从不用渡轮，他每回都说『你迟早得学会慢』）」展开·跨卡互证拍=C-00025 双向对位·连载链直接续证·同源多用注记）",
    u"源卡信条行「信条：「急件不急，稳到才算到。」」在帧（verbatim 直引）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00026）」在帧）",
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
j['meta']['storyboard'] = (u"LC-005 拆条形态=源卡即证据（LC-001/002/003/004 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00026 字段，"
                          u"画面=被读档案本体（F-036 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-035 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b6 守夜灯灵/b9 陆海峰=跨卡互证拍〔C-00028/C-00025〕")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
