# -*- coding: utf-8 -*-
# R710: LC-011 leg A - derive census-card-v15-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R707 build_leg_a.py adapted: C-00024 Miao Yi / F-034 CENSUS-v15)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260926-CENSUS-v15', 'MC-20260926-CENSUS-v15.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc011-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc011', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-010 v9 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v9-vertical.mp4')],
                    capture_output=True)
print('[v9 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v15 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v15 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v15-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一给方言字幕手工标注「语气」的字幕君」在帧（拆条形态=源卡即证据·F-034 成品卡 verbatim 行·hook 尾缀「找到了」=系列同型 LC-003~LC-010）",
    u"源卡编号名称行「C-00024 · 缪一」+物种行「硅基民 · 精灵系 · 无定 · 编译纪 3 年」在帧=居民档案面（拍文=锚 C-00024 卡题行+物种行 verbatim 合并展开·「无定」由字卡列承载=b2 卡口分工·LC-007 b2 同型·**系列首件精灵系硅基民拆条=物种面扩展第三档**·同源多用注记）",
    u"源卡城区职务行「MEDIA 城 · 信号塔街区 · 字幕君」在帧（拍文=锚 C-00024 城区行 verbatim+职业行首词·破折号展开「一帧一毫秒对轴的人——全城最懂『什么时候说』」=压缩分载由源卡承载·LC-009/LC-010 b3 同型·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00024 思想字段 verbatim「它信奉：字幕这行，快不是本事，准时才是。」展开·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00024 经历转折 verbatim「第一次给城主欢迎词打轴，压力大到把自己复制了两份并行核对（后来被师父骂了一顿，『成长没有并行捷径』）」展开·**打轴=黑话词表命中→L18 卡口分工**：口播=做字幕白话换位·卡锚列保留「打轴」原词·LC-009 回测田/LC-010 门禁链 同型·压力大到/后来被师父骂了一顿=压缩分载由源卡承载·师父引句「成长没有并行捷径」verbatim 保护·punch 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00024 思想字段 verbatim「它觉醒才三年，是全城最年轻的成年硅基民之一」「它给自己选了『缪一』这个名字」+「差一点点意思的『缪』，做字幕的就是差一点点都不能要」展开·之一=压缩分载·名字自选故事=思想字段 verbatim 域·turn 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00024 钩子字段 verbatim「观众说它做的字幕『有人味』，它把这句话裱在了工位上」展开·做的=压缩分载由源卡承载·wink 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00024 经历现状 verbatim「七段街区最快字幕，正攒钱给自己配一块大屏——『工欲善其事』」展开·正/给自己一块=压缩分载由源卡承载·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00024 行为字段 verbatim「每晚把当天所有节目字幕抽三句做『翻译练习』（方言转普通话，不许丢味）」+语言字段 verbatim「跟着主播学了一口湘腔『霸得蛮』，用在给自己打气的时候」展开·所有节目/翻译练习=压缩分载由源卡承载·练方言=「方言转普通话」白话换位·同源多用注记）",
    u"源卡在帧=被读档案（拍文=**跨卡双源**：锚 C-00024 关系字段 verbatim「合作最久的主播=何雨欣（吵架只用剪辑术语，和好只需要一句『发版了』）」×C-00022 何雨欣关系字段 verbatim「合作最久的是字幕君缪一（俩人吵架只用剪辑术语）」=**卡面双端互指在册=拆条系列第四对人物链**·LC-003 选优材料双卡互证面兑现〔R683 在案〕·跨卡互证拍·只用→用/只需要→只要=停顿位压缩·同源多用注记）",
    u"源卡信条行「信条：「字幕慢半帧，都是对说话人的辜负。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00024）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-011 拆条形态=源卡即证据（LC-001~LC-010 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00024 字段，"
                          u"画面=被读档案本体（F-034 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-028/F-031/F-032/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b10 何雨欣跨卡互证〔C-00022 双端互指=LC-003 选优互证面兑现=拆条系列第四对人物链〕=跨卡互证拍·"
                          u"系列首件精灵系硅基民拆条=物种面扩展第三档（碳基×8→像素灵×2→精灵系）·MEDIA 城同城第三卡=主播圈人物链（LC-003 何雨欣→LC-011 缪一）")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
