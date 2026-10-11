# -*- coding: utf-8 -*-
# SC-005-05 machine checks: format / verbatim anchors / beats-in-material inclusion / card cross-check
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
beats = open(BASE + r'\data\storylines\audio\SC-005-05-v1.beats.txt', encoding='utf-8').read()
mat = open(BASE + r'\data\storylines\audio\SC-005-05-v1-s1-material.md', encoding='utf-8').read()
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

# 2) verbatim anchor check (beats-side strings; punctuation-adapted card text marked below)
anchors = [
 '风控官——风控高地的瞭望员——全城最擅长说『不』的岗位，也是最受尊敬的',
 '红灯是为所有人亮的，包括我','过、不过、理由三条','限额、熔断、不碰红线',
 '从不说「应该没问题」——只有「实测没问题」','双栖通勤','白天现实上班，晚上回城把白天练的手艺镜像出来，挣的是两份踏实',
 '过不过就看这一眼，从不含糊','天塌下来先把手里这步做完','听见第一声异响',
 '拦下自己师父的一单，挨了骂','师父提着酒来道歉','规矩面前无师徒',
 '梦里都在拦单','没发生的事，就是她全部的功劳','红脉冲亮起来的时候，她心里反而最平静',
 '断电也不影响我上班','女儿画的红绿灯，她给做成了金属的','红灯亮起时永远第一个到岗',
 '绿灯常亮时反而睡不着','睡前必把当天的拦截日志复盘一遍',
 '全城唯一在拦截日志里给每单写「一句话理由」的风控官','被拦的人从没有不服的','像上了堂课',
 '家户 H-1006','丈夫是游戏城策划','每周带女儿去光桥看 commit 光点过江','「爸爸们下班了」','她家是妈妈们',
 '师父退休去了外环养线','每周通一封信','带徒弟了','徒弟是新人风控员','先学会说不过',
 '过，红灯还在闪烁，今天的工作日可不能松懈','不过，今天天气正好，风挺大，红灯还闪烁，得精神点',
 'H-1006','QUANT 城风控高地',
]
miss = [a for a in anchors if a not in beats]
print('verbatim_anchors=%d  MISS=%s' % (len(anchors), miss if miss else 'NONE'))

# 3) inclusion check (tech#96 dogfood: beats full text verbatim-embedded in s1 material)
lines = [l for l in beats.splitlines() if l.strip()]
inc_bad = [l[:30] for l in lines if l not in mat]
print('inclusion(beats in material)=%d/%d  bad=%s' % (len(lines)-len(inc_bad), len(lines), inc_bad if inc_bad else 'NONE'))

# 4) anchor card cross-check: beats-side adapted forms vs card verbatim forms
card = open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00015.md', encoding='utf-8').read()
card_forms = [
 ('风控官——风控高地的瞭望员——全城最擅长说『不』的岗位，也是最受尊敬的', None),
 ('红灯是为所有人亮的，包括我', None),
 ('过不过就看这一眼，从不含糊', None),
 ('天塌下来先把手里这步做完', None),
 ('听见第一声异响', None),
 ('梦里都在拦单', None),
 ('没发生的事，就是她全部的功劳', None),
 ('红脉冲亮起来的时候，她心里反而最平静', None),
 ('断电也不影响我上班', None),
 ('女儿画的红绿灯，她给做成了金属的', None),
 ('红灯亮起时永远第一个到岗', None),
 ('绿灯常亮时反而睡不着', None),
 ('睡前必把当天的拦截日志复盘一遍', None),
 ('每周带女儿去光桥看 commit 光点过江', None),
 ('她家是妈妈们', None),
 ('师父退休去了外环养线', None),
 ('每周通一封信', None),
 ('先学会说不过', None),
 ('被拦的人从没有不服的', None),
 ('像上了堂课', None),
 ('丈夫是游戏城策划', None),
 ('规矩面前无师徒', None),
 ('拦下自己师父的一单，挨了骂', None),
 ('第二天师父提着酒来道歉', None),
 ('带徒弟了', None),
 ('白天现实上班，晚上回城把白天练的手艺镜像出来，挣的是两份踏实', None),
 # punctuation/digit-adapted forms (beats -> card original)
 ('过、不过、理由三条', '「过」「不过」「理由三条」'),
 ('限额、熔断、不碰红线', '「限额」「熔断」「不碰红线」'),
 ('从不说「应该没问题」——只有「实测没问题」', '从不说「应该没问题」——只有「实测没问题」'),
 ('徒弟是新人风控员', '徒弟=新人风控员'),
 ('女儿八岁', '女儿 8 岁'),
 ('「爸爸们下班了」', None),
 ('「一句话理由」', None),
 ('全城唯一在拦截日志里给每单写「一句话理由」的风控官', None),
]
card_miss = []
for beats_form, card_form in card_forms:
    target = card_form if card_form else beats_form
    if target not in card:
        card_miss.append(target)
print('card_source_MISS=%s' % (card_miss if card_miss else 'NONE'))

# 5) composition guard: real-bank employer face excluded (F-025 desensitization precedent)
leak = [s for s in ('现实世界的银行','银行做风控') if s in beats]
print('bank_face_leak=%s' % (leak if leak else 'NONE (F-025 precedent honored)'))
