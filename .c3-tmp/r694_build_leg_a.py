# -*- coding: utf-8 -*-
# R694: LC-006 leg A - derive census-card-v19-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R691 build_leg_a.py adapted: C-00028 Lamp No.14 / F-038 CENSUS-v19)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260926-CENSUS-v19', 'MC-20260926-CENSUS-v19.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v19-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc006-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc006', 'cards-v1-matched.json')

# --- step 1: ffprobe LC-005 v17 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v17-vertical.mp4')],
                    capture_output=True)
print('[v17 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v19 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v19 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v19-vertical.mp4'
REQS = [
    u"源卡特征行「全城唯一在台风夜把自己亮度开满格的灯灵」在帧（拆条形态=源卡即证据·F-038 成品卡 verbatim 行）",
    u"源卡编号名称行「C-00028 · 十四号路灯」+种类行「像素灵 · nightlamp · 无定 · 第 41 数据季」在帧=居民档案面",
    u"源卡归属职务行「外环感知网 · 边缘街区 · 夜灯员」在帧（拍文=锚 C-00028 职业字段「夜灯员——夜城照明与独行客的护送者——执灯照径，天亮交晨」verbatim 展开·夜城照明=选材排除·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 思想字段「感知网调试夜——全城对频那一秒，它在塔尖亮了起来」+经历字段「全城对频的那一秒出生，编号十四」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 经历字段转折「有一年它照着一个在桥上哭的年轻人坐到天亮，天亮时那人冲它鞠了一躬」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 钩子字段「那晚它把外环一段路照成了白昼，检修日志写：超载运行，无损耗，原因不明。它自己说：知道原因，不能说。」展开·钩子字段头「台风夜」回指归位·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 服装字段「头顶灯罩有块补丁，是台风『梅花』留下的，它不许修——『疤是资历』」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 思想字段「每个深夜经过的人，它都用『多亮一档』打过招呼」+行为字段「路过夜宵摊会多亮半档」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 语言字段「学会了雾天跟渡轮船长的铜哨对暗号——两长一短，意思是『这段有我』」+关系字段「老友=渡轮船长陆海峰（铜哨暗号对传三十年）」展开·跨卡互证拍=C-00025 陆海峰 LC-004 wink「守夜灯灵十四号路灯必到」对位呼应·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00028 关系字段「它照过的路里，最惦记高小满——『那丫头跑夜单，伞永远在包里却永远不撑』」展开·跨卡互证拍=C-00026 高小满 LC-005 b8/wink 双向对位·连载链直接续证·同源多用注记）",
    u"源卡信条行「信条：「灯不问来路，只管照路。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00028）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-006 拆条形态=源卡即证据（LC-001~LC-005 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00028 字段，"
                          u"画面=被读档案本体（F-038 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-035/F-036 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b8 铜哨陆海峰〔C-00025 互证·LC-004 wink 对位〕/b9 高小满〔C-00026 互证·LC-005 b8/wink 双向对位〕=跨卡互证拍")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
