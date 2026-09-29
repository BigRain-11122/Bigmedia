# -*- coding: utf-8 -*-
# R729: LC-015 leg A - derive census-card-v2-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R725 build_leg_a.py adapted: C-00011 Zhu Hongkui / F-021 CENSUS-v2)
#        + R720-law pre-emptive geometry auto-fix: any card with block top < 787 (net < 20px vs source-line band
#          y745-767) gets candidate ladder [size x {no-split, dot-split}] - verbatim zero-char (newline insertion
#          only, asserted), largest size first. Floor = block top >= 787, net >= 20px (R720 fix statement).
import json, io, os, re, subprocess, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v2', 'MC-20260925-CENSUS-v2.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v2-vertical.mp4')
REF_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v10-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc015-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc015', 'cards-v1-matched.json')

sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import wrap_for_width

LOG = io.open(os.path.join(ROOT, '.c3-tmp', 'r729_build.txt'), 'w', encoding='utf-8')
def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    LOG.write(s + '\n')

assert os.path.exists(PNG), 'PNG missing: ' + PNG

# --- step 1: ffprobe LC-014 v10 vertical (recipe reference) ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', REF_MP4], capture_output=True)
say('[v10 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v2 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
say('[v2 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: geometry helpers (audit math == r729_card_audit.py / R725 validated math) ---
def card_lines(card, size, fw):
    n = 0
    for x in card['lines']:
        n += len(wrap_for_width(str(x), size, fw).split('\n'))
    return n

def block_top(card, size, fw):
    n = card_lines(card, size, fw)
    pitch = size * 1.2 + 14
    return (1920.0 - n * pitch) / 2.0, n

def dot_split(s):
    # zero-char: insert '\n' after each CJK mid-dot separator; keep any space before the newline
    # 'A · B' -> 'A · \nB' ; 'A·B' -> 'A·\nB'  (chars preserved, newline-only insertion)
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        out.append(ch)
        if ch == u'\u00b7':  # ·
            if i + 1 < len(s) and s[i + 1] == ' ':
                out.append(' ')
                i += 1
            out.append('\n')
        i += 1
    fixed = ''.join(out)
    assert fixed.replace('\n', '') == s.replace('\n', ''), 'dot_split must be zero-char'
    return fixed

# --- step 4: build matched cards + R720-law pre-emptive geometry fix ---
CARD_SRC = 'data/sources/footage/census-card-v2-vertical.mp4'
REQS = [
    u"源卡钩子行「全城唯一坚持用机械钟声对时的人」在帧（拆条形态=源卡即证据·F-021 成品卡 verbatim 行·hook 尾缀「找到了」=系列同型 LC-003~LC-014·「档案馆的人说那是城的心跳备份」=钩子字段同源展开注记）",
    u"源卡编号名称行「C-00011 · 朱鸿奎」+物种行「碳基市民 · 弄堂派 · 男 · 74 岁」在帧=居民档案面（拍文=锚 C-00011 卡题行+物种行 verbatim 合并展开·同源多用注记）",
    u"源卡城区职务行「北外滩 · 治理岸 · 时空校准师」在帧（拍文=锚 C-00011 城区行 verbatim+职业行展开「时空校准师——修表匠的赛博后身——校准的是全城的钟，也是人心里的时区」=压缩分载由源卡承载·LC-009/LC-010/LC-014 b3 同型·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 行为字段 verbatim「铺里永远只开一盏暖灯（说强光看不清游丝）」·「强光看不清游丝」verbatim 保护·beat 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 经历转折 verbatim「第一次给交易所时钟做全城对时 · 误差压进微秒那晚 · 在工位上坐到天亮」→「·」段化展开·punch 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 经历出身 verbatim「旧影像转生——从一张 1975 年钟表柜台前的合影里进城 · 怀里还揣着没修完的最后一块表」展开·turn 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 性格字段 verbatim「老派（再新的城也要按老礼数过日）· 较真（一个数据对不上，觉都睡不好）」·wink 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 经历现状 verbatim「铺子下午才开 · 收了两个徒弟 · 一个碳基一个硅基」·body 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 行为字段 verbatim「端三十年汤一滴没洒过 · 镊子起落比秒针还准」→「·」段化展开·proof 拍·同源多用注记）",
    u"源卡在帧=被读档案（拍文=锚 C-00011 关系字段 verbatim「硅基徒弟=归档者-07（他说这徒弟比碳基的还像老派人）」·**第七对人物链双端互证拍**〔C-00011×C-00017 同一师门评语双卡在册·R727 在案〕·棋友=顾阿凤〔C-00010 F-009 有声线 ch.1 主角〕侧链注记·proof 拍·同源多用注记）",
    u"源卡信条行「信条：「差之毫秒，谬以全城。」」在帧（verbatim 直引·保护行零动·F-021 卡面信条行同源）",
    u"源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00011）」在帧·载体位=M5 公众号图文页）",
]

with io.open(SRC_CARDS, encoding='utf-8') as fh:
    j = json.load(fh)
cards = j['cards']
assert len(cards) == 12, 'expect 12 beats, got %d' % len(cards)
fw = int(j['video']['width'])
base_size = int(j['font']['cards_size'])
durs = []
for i, c in enumerate(cards):
    durs.append((i, round(c['end'] - c['start'], 2)))
    c['visual'] = {'source': CARD_SRC, 'req': REQS[i]}
say('beat_durations', durs)
say('max_dur', max(d for _, d in durs), '(src 13.0s, wrap-crossing check)')

# pre-emptive geometry fix ladder (R720 law): sizes desc, within size no-split preferred over dot-split
LADDER = [(60, False), (60, True), (54, False), (54, True), (50, False), (50, True),
          (46, False), (46, True), (42, False), (42, True)]
fixes = []
for i, c in enumerate(cards):
    top0, n0 = block_top(c, base_size, fw)
    if top0 >= 787:
        say('card%02d b%-2d [%s] size=60 as-is top=%.0f net=%.0f -> clean' % (i, i, c['lines'][0][:10], top0, top0 - 767))
        continue
    say('card%02d b%-2d baseline top=%.0f net=%.0f -> FIX (R720 law)' % (i, i, top0, top0 - 767))
    for size, do_split in LADDER:
        trial = dict(c)
        trial['lines'] = list(c['lines'])
        if do_split:
            trial['lines'][1] = dot_split(c['lines'][1])
        top, n = block_top(trial, size, fw)
        if top >= 787:
            c['lines'] = trial['lines']
            if size != base_size:
                c['size'] = size
            fixes.append((i, size, do_split, n, top))
            say('   -> fixed: size=%d dot_split=%s lines=%d top=%.0f net=%.0f' % (size, do_split, n, top, top - 767))
            for l in wrap_for_width(str(c['lines'][1]), size, fw).split('\n'):
                say('      L: [%s]' % l)
            break
    else:
        raise SystemExit('card %d: no passing config in ladder' % i)

say('geometry_fixes:', fixes if fixes else 'NONE')

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-015 拆条形态=源卡即证据（LC-001~LC-014 同型）：12 拍拍稿逐拍引源卡/锚卡 C-00011 字段，"
                          u"画面=被读档案本体（F-021 成品卡 660px 上区 y=160+zoompan ≤1.04 微动·AIGC 标签避让=R511 先例·标签位=卡面左上=F-027/F-028/F-029/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12·同源多用逐拍注记·**时间校准主题系列首件位**（R723/R727 选优定谳）·"
                          u"**第七对人物链双端互证拍=b9**（C-00011 关系字段「硅基徒弟=归档者-07（他说这徒弟比碳基的还像老派人）」×C-00017 关系字段「师承=朱鸿奎」=同一师门评语双卡在册）·"
                          u"棋友=顾阿凤侧链（C-00010 F-009 有声线 ch.1 主角）·F-010 有声线同源人格面（SC-001-03 ch.3 主角=朱鸿奎·跨载体复用第二件 R227 登记）·"
                          u"超长副题几何修=R720 律前置（dot-split verbatim 零字符+per-card size·块顶 ≥787 净距 ≥20px·R711 五行块前科防）")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
say('written ->', DST)
LOG.close()
print('BUILD_DONE')
