# -*- coding: utf-8 -*-
# SC-005-04 machine checks: format / verbatim anchors / beats-in-material inclusion
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
beats = open(BASE + r'\data\storylines\audio\SC-005-04-v1.beats.txt', encoding='utf-8').read()
mat = open(BASE + r'\data\storylines\audio\SC-005-04-v1-s1-material.md', encoding='utf-8').read()
PROFILES = {'hook','punch','body','wink','beat','turn','proof','close','cta'}

# 1) format check
rows = [l for l in beats.splitlines() if l.strip()]
bad = []
for i, l in enumerate(rows, 1):
    parts = l.split(' | ')
    if len(parts) != 3: bad.append(('cols', i)); continue
    if parts[0].strip() not in PROFILES: bad.append(('profile', i, parts[0]))
spoken = ''.join(p.split(' | ')[2] for p in rows)
nchars = len(re.sub(r'[\s，。：；、！？——…「」『』《》·（）]', '', spoken))
print('rows=%d  spoken_nchars=%d  format_bad=%s' % (len(rows), nchars, bad if bad else 'NONE'))

# 2) verbatim anchor check (anchor card + cross-card)
anchors = [
 '流量像潮水，我是灯塔不是渔船','涨的时候别飘，退的时候别慌','从湘中小城一路播进七段街区',
 '直播间不夸大、不卖惨、不恰烂钱','把这座城里「上夜班的人」一个个拍给全世界看',
 '主播——直播间的赛博后身——灯一开整个世界都要让路','新功能第一个上身的','从县城网吧练到七段街，一步没省',
 '评论区谁难受','数字迁移潮第一班车','从湖南迁入','光桥市集支了个小摊','代写文案，管饭就行',
 '第一次用方言全程做了一场直播','爷青回','真话最带货','霸得蛮','恰饭','了不得','家人们','上链接','上数据',
 '下播后瞬间静音','嗓子是吃饭的家伙','会随情绪变光的薄外套','降饱和品红','MEDIA 的门面子，我只敢借三分亮',
 '发间一支旧钢笔','第一次写通过稿时编辑送的','她给别成了发簪','开播前，她必摸一摸门口的温度计',
 '跟气象播报员学的仪式感','下播绕江走一圈','每条粉丝来信都亲笔回','交给隔壁回信人阿姨代笔','一字不改她的结尾',
 '家里给介绍了三回对象，全黄了','闺蜜是数据化妆师','合作最久的是字幕君缪一','俩人吵架只用剪辑术语',
 '和好只需要一句「发版了」','全城唯一把「真实时间」打进直播标题的主播','开播时间表跟交易所钟声对齐',
 '等她开播像等开盘','七段街有间小直播间','粉丝不多但黏','《夜班人》系列',
 '今儿这江风不小，直播间的氛围正好，得赶紧把流明调到最佳，灯塔不等人','H-1012',
]
miss = [a for a in anchors if a not in beats]
print('verbatim_anchors=%d  MISS=%s' % (len(anchors), miss if miss else 'NONE'))

# 3) inclusion check (tech#96 dogfood: beats full text verbatim-embedded in s1 material)
lines = [l for l in beats.splitlines() if l.strip()]
inc_bad = [l[:30] for l in lines if l not in mat]
print('inclusion(beats in material)=%d/%d  bad=%s' % (len(lines)-len(inc_bad), len(lines), inc_bad if inc_bad else 'NONE'))

# 4) anchor card cross-check: verbatim strings must also exist in the C-00022 anchor card itself
anchor_card = open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00022.md', encoding='utf-8').read()
card_anchors = [a for a in anchors if a not in ('和好只需要一句「发版了」',)]
card_miss = [a for a in card_anchors if a.replace('，她','').replace('她','') not in anchor_card and a not in anchor_card]
# heuristic above is weak for narrative adaptations; list misses for manual eye-check
print('card_source_MISS=%s' % (card_miss if card_miss else 'NONE'))
