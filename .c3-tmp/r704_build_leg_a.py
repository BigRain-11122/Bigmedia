# -*- coding: utf-8 -*-
# R704: LC-009 leg A - derive census-card-v20-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R700 build_leg_a.py adapted: C-00029 Mile cat / F-040 CENSUS-v20)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260926-CENSUS-v20', 'MC-20260926-CENSUS-v20.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v20-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc009-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc009', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: derive v20 vertical (R511 law) ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v20 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v20-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一拥有「巷志」的猫」在帧（拆条形态=源卡即证据·F-040 成品卡 verbatim 行）",
    u"源卡编号名称行「C-00029·咪喱」+物种行「像素灵·radiocat·无定·第 19 数据季」在帧=居民档案面",
    u"源卡城区职业行「GAME 城·像素匠人巷·伴居灵」在帧（拍文=锚 C-00029 职业字段 verbatim「伴居灵——弄堂与三城屋顶的伴居者——尾巴天线永远对准最热闹的方向」展开·破折号展开项=压缩分载由源卡承载〔R302 在案律〕·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 经历字段「雨季的第一场雨里诞生——出生那晚它蹲在罗大壮的画室外窗台上，画匠把它画进了那天的门脸像里，从此它在编年史里有了第一笔」展开·「从此它在编年史里有了第一笔」=压缩分载由源卡承载·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 经历字段转折「尾巴天线在台风『梅花』那夜立了大功——全巷的通讯中断，是它一趟一趟把口信叼到位的，第二天的早饭它吃了七家的」展开·台风梅花=LC-006/LC-007 同夜三视角互补第三证=跨卡共时拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 思想字段「收编自己的人类有：粥铺阿凤（管布头）、回测田那位（管晒太阳的田埂）、画匠家（管毛线）」展开·括号注→逗号=停顿位文字零改·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 服装字段「左耳有个缺口——为救一只卡在管线里的小消息雀留下的，它不许任何人说那是『英勇』，『就是耳朵痒』」展开·不许任何人说→不许说是=L18 白话换位卡锚承载原词·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 经历现状字段「现状：匠人巷编外巷长（自封），办公室是罗家的窗台」展开·罗家的窗台→罗家窗台=停顿位压缩·字卡列保留「罗家窗台」原词·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 语言字段「喵语（音调有七八种，巷子里人人听得懂个大概）」展开·「生气时会把自己的耳朵拍得啪啪响，全巷的小孩都会学」=压缩分载由字卡副题承载·卡口分工·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00029 关系字段「最投缘=王多多（那孩子的口哨能召来消息雀，它服气）」展开·王多多互证拍=跨卡双向位：LC-008 hook「全城唯一能口哨唤来三只以上消息雀的孩子」同一本事两端在案=拆条系列第二对人物链双向互证·同源多用注记）",
    u"源卡信条行「信条：「蹭饭是门艺术，报恩是门手艺。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00029）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-009 拆条形态=源卡即证据（LC-001~LC-008 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00029 字段，"
                          u"画面=被读档案本体（F-040 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-031/F-032 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b9 王多多互证拍〔LC-008 同本事双向闭合=拆条系列第二对人物链双向互证〕"
                          u"+b4 台风梅花〔LC-006/LC-007 同夜三视角互补第三证〕=跨卡共时拍·系列首件像素灵物种+动物居民拆条位")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
