# -*- coding: utf-8 -*-
# R680: LC-002 leg A - derive census-card-v8-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v8', 'MC-20260925-CENSUS-v8.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v8-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc002-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc002', 'cards-v1-matched.json')

# --- step 1: ffprobe LC-001 v7 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v7-vertical.mp4')],
                    capture_output=True)
print('[v7 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v8 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v8 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v8-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一坚持给失败参数建「纪念碑田」的回测农」在帧（拆条形态=源卡即证据·F-027 成品卡 verbatim 行）",
    u"源卡档案行 C-00017·归档者-07/硅基民·编译系·无定·编译纪 12 年在帧=居民档案面",
    u"源卡在帧=被读档案（拍文=锚 C-00017 职业行「QUANT 城·回测田·回测农（算法调参师）」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00017 行为字段「播种一批参数，浇水施肥等三天」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00017 钩子/经历字段「每块碑上刻一行死因·它没删参数」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00017 钩子字段尾「新研究员入职都去先看碑再下田」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00017 经历字段「大编译觉醒·醒来第一句报版本号」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00017 思想字段「数据不说谎，人才会·农谚集」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00017 经历字段「永不收敛模型单独辟田·镇田之宝」展开·同源多用注记）",
    u"源卡性格行「有条理 · 记性好 · 慢热」在帧（拍文=锚 C-00017 性格字段「慢热三个月交心」+关系字段「邻居徐根福每天留热的」展开·同源多用注记·徐根福=F-026/LC-001 同城人物）",
    u"源卡信条行「参数不收敛，天理难容。」在帧（verbatim 直引）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00017）」在帧）",
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
j['meta']['storyboard'] = (u"LC-002 拆条形态=源卡即证据（LC-001 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00017 字段，"
                          u"画面=被读档案本体（F-027 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 轮内修红先例）；"
                          u"对位 12/12·同源多用逐拍注记")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
