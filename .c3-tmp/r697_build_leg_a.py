# -*- coding: utf-8 -*-
# R697: LC-007 leg A - derive census-card-v18-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R694 build_leg_a.py adapted: C-00027 Deng Jianguo / F-037 CENSUS-v18)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260926-CENSUS-v18', 'MC-20260926-CENSUS-v18.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v18-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc007-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc007', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-006 v19 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v19-vertical.mp4')],
                    capture_output=True)
print('[v19 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v18 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v18 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v18-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一给每场大风起名字的值守员」在帧（拆条形态=源卡即证据·F-037 成品卡 verbatim 行）",
    u"源卡编号名称行「C-00027 · 邓建国」+种类行「碳基市民 · 通勤族」+性别年龄行「男 · 50 岁」在帧=居民档案面",
    u"源卡归属职务行「外环感知网 · 感知塔站」+职业行「感知塔站值守员——外环神经末梢的哨兵」在帧（拍文=锚 C-00027 职业字段首词与破折号前段 verbatim 展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00027 经历字段「半只脚进城——现实里退役后做了十年气象设备维护，进城那年塔站正好招熟手」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00027 经历字段转折「台风『梅花』过境那夜他守了一宿，第二天全城灯带如常亮起」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00027 行为字段「值守日志写满天气脾气（台风有台风的名字，他起的）」+钩子字段「『梅花』『烟嗓』『过云雨一号』」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00027 行为字段「休息日去光桥看人钓鱼，自己从不钓——『我钓了一辈子风』」展开·跨卡互证拍=REACT-v4 城志互证锚〔R575 在案〕·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00027 行为字段「每天真实天气一变就给江边那些夜宵摊发提醒」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00027 关系字段「搭档=信号中继员（俩人交接班时只说三句话，句句有用）」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 十四号路灯关系字段「塔站的值守员说它比仪器可靠」反向点名展开·跨卡互证拍=LC-006 锚卡 C-00028 对位呼应〔第三人物链第四卡〕·同源多用注记）",
    u"源卡信条行「信条：「台风天的日志最见人品。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00027）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-007 拆条形态=源卡即证据（LC-001~LC-006 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00027 字段，"
                          u"画面=被读档案本体（F-037 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-035/F-036/F-038 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b6 光桥钓鱼〔REACT-v4 城志互证锚 R575〕/b9 十四号路灯比仪器可靠〔C-00028 关系字段反向点名=LC-006 锚卡对位·第三人物链第四卡〕=跨卡互证拍")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
