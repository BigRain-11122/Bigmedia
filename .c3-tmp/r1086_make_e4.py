# -*- coding: utf-8 -*-
"""R1086: derive e4_call.py for DAILY-v63 from DAILY-v62's wrapper (programmatic, zero-drift on the 61-entry history)."""
import io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SRC = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20261003-DAILY-v62-tmp', 'e4_call.py')
DST = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20261003-DAILY-v63-tmp', 'e4_call.py')
os.makedirs(os.path.dirname(DST), exist_ok=True)
src = io.open(SRC, encoding='utf-8').read()

REPL = [
    (u'《城市日签 062》', u'《城市日签 063》'),
    (u'顶部标题「城市日签 062」', u'顶部标题「城市日签 063」'),
    (u'中间引文一行「「鱼竿一甩，梦醒时分」」；署名行「——硅基城市台词池 · 逍遥轴」；',
     u'中间引文一行「「嗡嗡嗡，晨风中的舞」」；署名行「——硅基城市台词池 · 城市生灵」；'),
    (u'城里住着一万名登记居民。台词池按六种「轴」收录居民的话。',
     u'城里住着一万名登记居民，还登记着一批城市生灵（动物宠物小灵们）。台词池按六种「轴」收录居民的话，生灵们的话收在城市生灵声部。'),
    (u'这句引文出自国庆假期第三天的清晨（此刻正是早晨七点来钟）：假期里全城还泡在睡梦里，',
     u'这句引文出自国庆假期第三天的上午（此刻正是上午十一点来钟）：假期里城市醒得慢，人潮还没涌上街，'),
    (u'逍遥轴的钓鱼人已经到了江边，手腕一抖把鱼竿甩出去——鱼竿一甩，梦醒时分。',
     u'晨风一起，城里的生灵们先开了嗓——嗡嗡嗡，晨风中的舞。'),
    (u'最短的一瞬（从睡到醒的切换）对上最长的慢工艺（晨间垂钓的起手），',
     u'最小的身体（一只小生灵的嗡鸣，全城最细的声音）对上最大的舞台（整个城市的晨风），'),
    (u'假期最大的睡和最早的醒在这一竿里碰头。',
     u'无形的风（看不见）对上有形的舞（看得见的姿态）——最小舞者在最大舞台上开演。'),
    (u'这是「城市日签」系列第六十二张，出自逍遥轴（这个轴的居民最松弛、闲适至上）。',
     u'这是「城市日签」系列第六十三张，出自城市生灵声部（第四次登场）。'),
    (u'前六十一张：', u'前六十二张：'),
    (u'猫鸟小灵们在夜里轻轻发着微光，说灵光闪烁夜未央）。',
     u'猫鸟小灵们在夜里轻轻发着微光，说灵光闪烁夜未央/'
     u'国庆假期第三天的清晨（周六），逍遥轴的钓鱼人一早到江边，手腕一抖把鱼竿甩出去，说鱼竿一甩，梦醒时分）。'),
    (u"'material': 'MC-20260925-DAILY-v62 static card (cards.json + render output)'",
     u"'material': 'MC-20260925-DAILY-v63 static card (cards.json + render output)'"),
    (u"'material': 'MC-20261003-DAILY-v62 static card (cards.json + render output)'",
     u"'material': 'MC-20261003-DAILY-v63 static card (cards.json + render output)'"),
]
for old, new in REPL:
    if old in src:
        src = src.replace(old, new, 1)
    else:
        print('MISS: %s' % old[:50])

io.open(DST, 'w', encoding='utf-8').write(src)
# verify no residual v62-only strings
for bad in [u'城市日签 062', u'鱼竿一甩，梦醒时分」」', u'前六十一张', u'第六十二张，出自逍遥轴']:
    assert bad not in src, 'residual: %s' % bad
print('E4 wrapper derived OK -> %s' % DST)
