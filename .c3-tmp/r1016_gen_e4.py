# -*- coding: utf-8 -*-
"""R1016: generate v47 e4_call.py from v46 template (split-literal aware replacements)."""
import io

SRC = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards\MC-20261002-DAILY-v46-tmp\e4_call.py"
DST = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards\MC-20261002-DAILY-v47-tmp\e4_call.py"

src = io.open(SRC, encoding="utf-8-sig").read()

REPS = [
    (u"城市日签 046", u"城市日签 047"),
    (u"第四十六张", u"第四十七张"),
    (u"前四十五张", u"前四十六张"),
    (u"「「大伙儿乐呵乐呵，一年到头累不坏」」", u"「「灯笼高挂真喜气」」"),
    (u"——硅基城市台词池 · 侠气轴", u"——硅基城市台词池 · 秩序轴"),
    (u"城里住着一万名登记居民。「侠气轴」是城里最讲义气最豪爽的一类居民：",
     u"城里住着一万名登记居民。「秩序轴」是城里最讲规矩的一类居民："),
    (u"街坊有事搭把手、大伙儿聚在一起笑声最响、最扛得住事吃得了苦。",
     u"凡事讲究秩序井然、安全安稳第一、把城市当自己的工程来爱护、验收思维刻在骨子里。"),
    (u"这句引文出自国庆假期第二天，侠气轴街坊大伙儿歇工聚在街角乐呵乐呵，",
     u"这句引文出自国庆假期第二天，秩序轴居民照常巡看街面，抬头看满街高挂的节日灯笼，"),
    (u"拍着肩膀笑着说：大伙儿乐呵乐呵，一年到头累不坏——",
     u"给出验收式赞叹：灯笼高挂真喜气——"),
    (u"最硬朗的大伙儿，假日里笑声最响。",
     u"最讲规矩的验收人，把最高赞词给了节日的喜庆。"),
    (u"摩挲着说老物件里藏着故事）。",
     u"摩挲着说老物件里藏着故事/侠气轴居民大伙儿歇工聚在街角乐呵乐呵拍着肩膀说大伙儿乐呵乐呵一年到头累不坏）。"),
    ("MC-20261002-DAILY-v46 static card", "MC-20261002-DAILY-v47 static card"),
]

for a, b in REPS:
    if a not in src:
        raise SystemExit("MISSING: %r" % a[:60])
    src = src.replace(a, b)

# residual sanity: no stale 046/侠气-axis markers in prompt area (docstring header may keep v46 origin note)
assert src.count(u"侠气轴居民照常") == 0, "unexpected"
io.open(DST, "w", encoding="utf-8").write(src)
print("e4_call.py v47 written len=%d" % len(src))
