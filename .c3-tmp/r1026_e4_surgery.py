# -*- coding: utf-8 -*-
"""R1026: create MC-20261002-DAILY-v56(-tmp) dirs + e4_call.py via string surgery from v55."""
import io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
V55TMP = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20261002-DAILY-v55-tmp')
V56 = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20261002-DAILY-v56')
V56TMP = V56 + '-tmp'
os.makedirs(V56, exist_ok=True)
os.makedirs(V56TMP, exist_ok=True)

t = io.open(os.path.join(V55TMP, 'e4_call.py'), encoding='utf-8').read()

# 1) series number (appears twice: card title mention + top-title line)
t = t.replace(u'城市日签 055', u'城市日签 056')
# 2) quote (inner quote mention in layout description)
t = t.replace(u'老陈头又背着手溜达去了旧书摊', u'夕阳西下鱼也归巢了')
# 3) attribution line
t = t.replace(u'——硅基城市台词池 · 怀旧轴', u'——硅基城市台词池 · 逍遥轴')
# 4) background sentence (piece-specific, spans two source lines -> two surgical replaces)
t = t.replace(u'这句引文出自国庆假期第二天的傍晚：假期里交易所休市，怀旧轴的居民老陈头背着手，',
              u'这句引文出自国庆假期第二天的黄昏：逍遥轴的钓鱼人在江边收起钓竿，看夕阳落进江面，连鱼也归巢了。')
t = t.replace(u'慢悠悠地又溜达到了旧书摊。全城都在看节日灯会，最念旧的人，去了城里最旧的地方。',
              u'全城都在赶节日灯会的热闹，最闲适的人，在黄昏的水边收工回家。')
# 5) series ordinal + first-time context
t = t.replace(u'这是「城市日签」系列第五十五张，是这个系列第一次以「休市后的傍晚」作为当天的情境',
              u'这是「城市日签」系列第五十六张，是这个系列第一次以「黄昏归巢」作为当天的情境')
t = t.replace(u'（前五十四张：', u'（前五十五张：')
# 6) recap list: append v55 piece before the closing paren of the recap
t = t.replace(u'说闪闪灯辉照长廊）。',
              u'说闪闪灯辉照长廊/休市后的傍晚，交易所收了市，怀旧轴的老陈头背着手，又慢悠悠地溜达去了旧书摊）。')
# 7) material tag
t = t.replace(u'MC-20261002-DAILY-v55 static card', u'MC-20261002-DAILY-v56 static card')

# verify surgery completeness
for must in [u'城市日签 056', u'夕阳西下鱼也归巢了', u'逍遥轴', u'前五十五张', u'溜达去了旧书摊', u'第五十六张']:
    assert must in t, u'surgery incomplete: missing %s' % must
for gone in [u'城市日签 055', u'第五十五张', u'前五十四张', u'老陈头又背着手溜达去了旧书摊」」']:
    assert gone not in t, u'surgery residue: %s still present' % gone

io.open(os.path.join(V56TMP, 'e4_call.py'), 'w', encoding='utf-8', newline='\n').write(t)
print('e4_call.py written to v56-tmp, len', len(t))
