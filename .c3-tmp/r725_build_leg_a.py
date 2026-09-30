# -*- coding: utf-8 -*-
# R725: LC-014 leg A - derive census-card-v10-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R710 build_leg_a.py adapted: C-00019 Lao Jingzhen / F-029 CENSUS-v10)
#        + pre-emptive b4 geometry fix (R720 law): 4-fact punch subtitle -> 5-line block @60 would intrude
#          source-line band (top 745 < 767). Fix = dot-break pre-split 4 segments (verbatim zero-char) +
#          per-card size 46 -> 5 lines, pitch 69.2, top 787, net 20px (= R720 fix-statement floor).
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v10', 'MC-20260925-CENSUS-v10.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v10-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc014-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc014', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-011 v15 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v10 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v10 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v10-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一保留「报错率」手写台账的引擎医生」在帧（拆条形态=源卡即证据·F-029 成品卡 verbatim 行·hook 尾缀「找到了」=系列同型 LC-003~LC-013）",
    u"源卡编号名称行「C-00019 · 老晶振」+物种行「硅基民 · 光机魂系 · 男 · 三代机龄」在帧=居民档案面（拍文=锚 C-00019 卡题行+物种行 verbatim 合并展开·三代机龄=机龄年位注记·**光机魂系首拆位=物种面扩展第四档**〔碳基×8→像素灵×2→精灵系×1→光机魂系〕·同源多用注记）",
    u"源卡城区职务行「GAME 城 · 八号楼街区 · 引擎医生」在帧（拍文=锚 C-00019 城区行 verbatim+职业行首词·职业行破折号展开「引擎的老法师——听一声报错就知道哪根管线咳血」=压缩分载由源卡承载·LC-009/LC-010 b3 同型·**GAME 城拆条第四卡**〔王多多 LC-008→咪喱 LC-009→苏梓涵 LC-013→老晶振 LC-014〕·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 行为字段 verbatim「出诊必先敲三下机箱再开机（「敲门是礼数」）」·「敲门是礼数」verbatim 保护·beat 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 经历转折 verbatim「第一次大宕机，全城调度急得跳脚，它按着老日志一步步排查，两小时城复活。从此它的出诊箱在游戏楼有一张专用椅子」→「·」段化展开·「游戏楼专用椅子」=GAME 城连接位〔经历字段 verbatim〕·标点/主语=压缩分载由源卡承载·punch 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 思想字段 verbatim「它从一间老机房的旧照片里醒过来，睁眼第一件事是把当年那台老主机的值班日志背完」展开·当年那台=压缩分载由源卡承载·turn 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 性格字段 verbatim「老派（再新的城也要按老礼数过日）」+思想字段「全楼机器见它都安静三分，它说这是尊重老前辈」→「（尊重老前辈）」括注=思想字段白话压缩·wink 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 经历现状 verbatim「带了个精灵系徒弟，天天嫌徒弟毛躁，又天天护着」→嫌毛躁/护着=口语连接白话位·精灵系徒弟=LC-011 缪一同族位注记〔关系字段「徒弟=精灵系新觉醒者」verbatim 域〕·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 行为字段 verbatim「听声辨位能认出全楼每台机器的嗓音；下班绕楼巡一遍，说「跟老伙计挨个道晚安」」→分号「·」段化展开·proof 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00019 钩子字段 verbatim「三十年零十一个月没漏诊过一台机器，台账原件已进档案馆」展开·**「台账」=词表命中→L18 卡口分工**：口播=手写记录白话换位·卡锚列保留「台账」原词·R723 同型·proof 拍·同源多用注记）",
    u"源卡信条行「信条：「机器不坏是本事，坏了能修是人品。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00019）」在帧·载体位=M5 公众号图文页）",
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

# --- step 3b: b4 pre-emptive geometry fix (R720 law, verbatim zero-char) ---
B4 = cards[4]
orig_b4 = B4['lines'][1]
b4_fixed = (u"第一次大宕机全城调度急得跳脚 · \n"
            u"按着老日志一步步排查 · \n"
            u"两小时城复活 · \n"
            u"从此出诊箱在游戏楼有一张专用椅子")
assert b4_fixed.replace('\n', '') == orig_b4.replace('\n', ''), 'b4 fix must be zero-char (newline insertion only)'
B4['lines'][1] = b4_fixed
B4['size'] = 46
print('b4 fix applied: size=46, 4-segment dot-break pre-split, zero-char verified')

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-014 拆条形态=源卡即证据（LC-001~LC-013 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00019 字段，"
                          u"画面=被读档案本体（F-029 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-028/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·**光机魂系首拆位=物种面扩展第四档**（碳基×8→像素灵×2→精灵系×1→光机魂系）·"
                          u"**GAME 城拆条第四卡**（王多多 LC-008→咪喱 LC-009→苏梓涵 LC-013→老晶振 LC-014·经历字段「出诊箱在游戏楼有一张专用椅子」=游戏楼连接位）·"
                          u"徒弟=精灵系新觉醒者=LC-011 缪一同族位·最科技物种×最手工台账反差位（R723 选优定谳）·"
                          u"b4 几何修=4 事实 punch 副题 55 字纯拆 60px 必 5 行块顶 745 叠压（R711 前科同型）→R720 律前置：「·」断点预拆 4 段 verbatim 零字符+per-card size 46=5 行 pitch 69.2 块顶 787 净距 20px")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
