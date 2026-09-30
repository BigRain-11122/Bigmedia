# -*- coding: utf-8 -*-
# R718: LC-013 leg A - derive census-card-v11-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R710 build_leg_a.py adapted: C-00020 Su Zihan / F-030 CENSUS-v11)
import json, io, os, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v11', 'MC-20260925-CENSUS-v11.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v11-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc013-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc013', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 0: ffprobe final audio (ground truth duration) ---
prA = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                      '-of', 'default=nw=1', os.path.join(ROOT, '.lc013-tmp', 'audio.mp3')],
                     capture_output=True)
print('[audio]', prA.stdout.decode('utf-8', 'replace').strip())

# --- step 1: ffprobe LC-011 v15 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v11 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v11 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v11-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一给「夜班人员」留专属彩蛋的关卡建筑师」在帧（拆条形态=源卡即证据·F-030 成品卡 verbatim 行·hook 尾缀「找到了」=系列同型 LC-003~LC-012）",
    u"源卡编号名称行「C-00020 · 苏梓涵」+物种行「碳基市民 · 原生代 · 女 · 24 岁」在帧=居民档案面（拍文=锚 C-00020 卡题行+物种性别年龄行 verbatim 合并展开·数字 24→「二十四」口播形差分离·LC-002 b2 同型·同源多用注记）",
    u"源卡城区职务行「GAME 城 · 游戏楼街区 · 关卡建筑师」在帧（拍文=锚 C-00020 城区行 verbatim+职业行首词·职业行破折号展开「游戏世界的施工队长——每个转角都藏着心机与善意」=压缩分载由源卡承载·LC-009/LC-010 b3 同型·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00020 行为字段 verbatim「盖完就拆拆完再盖（『沙盒的楼是租来的快乐，正式关卡不行』）」展开·beat 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00020 经历转折字段 verbatim「转折：第一个署名关卡上线那晚，她蹲在城门口听了一夜玩家的议论，第二天把最狠的差评打印出来贴在工位」展开·punch 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00020 经历字段 verbatim「城生城长——出生档案在塔基，童年在测试关卡里过」展开·「出生档案在塔基」=压缩分载由卡锚列承载·turn 拍·同源多用注记）",
    u"源卡特质行「点子多 · 会折腾 · 记性好」在帧（拍文=锚 C-00020 性格字段首项 verbatim「点子多（脑子里永远有三十个方案在排队）」括号内展开·wink 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00020 经历现状字段 verbatim「现状：游戏楼 P05 楼的骨干，正带徒弟」+行为字段 verbatim「下班必去老城门给守门人带一杯热的」展开·「游戏楼 P05 楼的骨干带徒弟」=压缩分载由卡锚列承载·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00020 思想字段 verbatim「她说好关卡像好弄堂，走一遍就舍不得搬走」「新手道永远比规程多留半步余量」展开·「新手道永远比规程多留半步余量」=压缩分载由卡锚列承载·proof 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=**跨卡多向互证**：锚 C-00020 钩子字段 verbatim「守门人、巡夜员、灯塔守望都收到过，谁也没找到全部，他们管这叫『梓涵的深夜惊喜』」×三前件拆条卡同拍位对位〔LC-012 潘志明〔守门人〕×LC-007 邓建国〔巡夜值守〕×LC-006 十四号路灯〔灯塔守望〕=**拆条系列第六对人物链·多向互证网首件**·R717 选优定谳锚·跨卡互证拍·同源多用注记）",
    u"源卡信条行「信条：「每个转角都该藏一个惊喜。」」在帧（verbatim 直引·保护行零动）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00020）」在帧·载体位=M5 公众号图文页）",
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
j['meta']['storyboard'] = (u"LC-013 拆条形态=源卡即证据（LC-001~LC-012 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00020 字段，"
                          u"画面=被读档案本体（F-030 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-028/F-031/F-032/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·b9 三前件同拍位对位〔守门人=LC-012 潘志明×巡夜值守=LC-007 邓建国×灯塔守望=LC-006 十四号路灯〕=跨卡多向互证拍·"
                          u"拆条系列第六对人物链=多向互证网首件（前五对=单向/双向互证）·GAME 城拆条第三卡（王多多 LC-008→咪喱 LC-009→苏梓涵 LC-013）")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
