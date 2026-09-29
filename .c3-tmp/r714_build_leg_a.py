# -*- coding: utf-8 -*-
# R714: LC-012 leg A - derive census-card-v14-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R710 build_leg_a.py adapted: C-00023 Pan Zhiming / F-033 CENSUS-v14)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v14', 'MC-20260925-CENSUS-v14.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v14-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc012-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc012', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-011 v15 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v14 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v14 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v14-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一保留『毙稿理由档案』的选题官」在帧（拆条形态=源卡即证据·F-033 成品卡 verbatim 行·hook 尾缀「找到了」=系列同型 LC-003~LC-011·「二十年每条毙稿一行理由/镇馆之宝」=压缩分载由源卡承载）",
    u"源卡编号名称行「C-00023 · 潘志明」+物种行「碳基市民 · 原生代 · 男 · 47 岁」在帧=居民档案面（拍文=锚 C-00023 卡题行+物种行 verbatim 合并展开·47→四十七=L18 数字白话·「男」「原生代」由字卡列承载=b2 卡口分工·LC-011 b2 同型·同源多用注记）",
    u"源卡城区职务行「MEDIA 城 · 选题馆街区 · 选题官」在帧（拍文=锚 C-00023 城区行 verbatim+职业行首词·破折号展开「选题馆的守门人——留言墙的真实来信都汇到他案头」=压缩分载由源卡承载·LC-009/LC-010/LC-011 b3 同型·**内容产线三工种图鉴拆条链闭环位**·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00023 行为字段 verbatim「每天毙稿三十留下三个」展开·毙稿三十→毙三十个选题=停顿位展开·留→只留=语气位·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00023 经历转折 verbatim「第一次迫于人情放过一篇查不实的稿，第二天凌晨自己把它撤了，从此馆里立规矩：选题官的笔不认人情」展开·馆里=压缩分载·punch 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00023 经历头 verbatim「城生城长——他爹是初代建城工人，编年史里查得到名字，所以他干活总觉得有双眼睛看着」展开·所以=压缩分载·锚语「爹」保留原词·turn 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00023 语言字段 verbatim「生气不骂人，只把红笔按得很重」·wink 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00023 经历现状 verbatim「带着五个年轻选题官，每周雷打不动去留言墙值班一天」+行为字段「每周去留言墙坐一下午，亲手拆信」=压缩分载由源卡承载·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00023 思想字段 verbatim「他常说选题馆这座楼是『城的心电图室』——哪条街在笑、哪条街在熬夜、哪条街在惦记现实里的谁，纸上都有波形」展开·常说→说/这座楼/惦记现实里的谁=压缩分载由源卡承载·同源多用注记）",
    u"源卡在帧=被读档案（拍文=**跨卡双源**：锚 C-00023 关系字段 verbatim「最服气的主播是何雨欣（『她那期方言直播，我抄了三页笔记』）」×C-00022 何雨欣卡在册=**卡面互指第五对人物链**〔CENSUS v13/v14/v15 同城三工种同构·R303/R305 在案〕·内容产线三工种图鉴拆条链闭环（主播 LC-003→字幕君 LC-011→选题官 LC-012）·跨卡互证拍·我→他=叙述位·同源多用注记）",
    u"源卡信条行「信条：「毙稿不毙人，选题选良心。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00023）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-012 拆条形态=源卡即证据（LC-001~LC-011 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00023 字段，"
                          u"画面=被读档案本体（F-033 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-028/F-031/F-032/F-033/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b9 何雨欣跨卡互证=拆条系列第五对人物链〔C-00022 相邻卡互引第二案 R303 兑现位〕=内容产线三工种图鉴拆条链闭环拍"
                          u"（主播 LC-003 何雨欣→字幕君 LC-011 缪一→选题官 LC-012 潘志明·MEDIA 城同城三工种同构）")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
