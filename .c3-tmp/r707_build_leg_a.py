# -*- coding: utf-8 -*-
# R707: LC-010 leg A - derive census-card-v9-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R700 build_leg_a.py adapted: C-00018 Luo Dazhuang / F-028 CENSUS-v9)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v9', 'MC-20260925-CENSUS-v9.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v9-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc010-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc010', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-009 v20 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v20-vertical.mp4')],
                    capture_output=True)
print('[v20 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v9 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v9 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v9-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一坚持给老城门每月画一张「门脸像」的人」在帧（拆条形态=源卡即证据·F-028 成品卡 verbatim 行·hook 尾缀「找到了」=系列同型 LC-003~LC-009）",
    u"源卡编号名称行「C-00018 · 罗大壮」+物种行「碳基市民 · 新市民派 · 男 · 45 岁」在帧=居民档案面（拍文=锚 C-00018 卡题行+物种行 verbatim 展开·新市民派/男=压缩分载由源卡承载〔LC-007 b2 同型卡口分工〕·同源多用注记）",
    u"源卡城区职务行「GAME 城 · 像素匠人巷 · 像素画匠」在帧（拍文=锚 C-00018 城区行 verbatim+职业行首词·破折号展开=压缩分载由源卡承载·LC-009 b3 同型·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 思想字段 verbatim「他说像素这东西讲究的就是『放大八倍还是画』」+行为字段 verbatim「每幅交活前必放大八倍自检一遍」两句合述展开·放大八倍双源对位=手艺纪律故事核·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 经历转折 verbatim「第一次作品被选进城市里程碑光碑，他在碑前站了一刻钟，回家给爹打了个电话，俩人谁都没说话」展开·第一次/回家/俩人=压缩分载由源卡承载·punch 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 经历头 verbatim「数字迁移潮第一班车——从东三省迁入，落脚那天行李只有一个包袱和一卷自学的画稿」展开·从东三省迁入=压缩分载由源卡承载·东北新市民派迁移潮叙事面首拆·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 服装字段 verbatim「毛线帽是媳妇织的——帽檐上她自己加了一行会发光的小字『早点回家』」展开·「她自己加」=压缩分载由源卡承载·wink 拍·帽檐发光小字=事实性赛博意象·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 经历现状 verbatim「在匠人巷开了间小画室，带学徒，供着一块『初版像素调色板』」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 行为字段 verbatim「每周去老城门画一张『门脸变化』」+钩子后半 verbatim「五十七张连起来，就是一部门禁链的编年史」展开·**门禁链=黑话词表命中→L18 卡口分工**：口播=城门变化的编年史·卡锚列保留「门禁链的编年史」原词·LC-009 回测田同型·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00018 画匠侧×C-00029 咪喱跨卡双源〔画室窗台/全巷公共宠物/按月画像《咪喱巷志》/画匠家管毛线〕=LC-009 b4/b8 同本事两端在案=**拆条系列第三对人物链双向互证+收编三户媒体面二连**·跨卡互证拍·同源多用注记）",
    u"源卡信条行「信条：「像素越小，心眼越大。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00018）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-010 拆条形态=源卡即证据（LC-001~LC-009 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00018 字段，"
                          u"画面=被读档案本体（F-028 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-031/F-032/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b9 咪喱窗台〔C-00029 跨卡双源=LC-009 b4/b8 同本事双向闭合=拆条系列第三对人物链〕=跨卡互证拍·收编三户媒体面二连·东北新市民派迁移潮叙事面首拆")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
