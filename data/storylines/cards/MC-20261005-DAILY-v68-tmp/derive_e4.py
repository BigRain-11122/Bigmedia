# -*- coding: utf-8 -*-
"""Derive e4_call.py for DAILY v68 from v67 template (targeted replacements)."""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "MC-20261005-DAILY-v67-tmp", "e4_call.py")
DST = os.path.join(HERE, "e4_call.py")

t = io.open(SRC, encoding="utf-8").read()

# 1) piece header
old = u"看到下面这张静态日签卡《城市日签 067》"
new = u"看到下面这张静态日签卡《城市日签 068》"
assert old in t; t = t.replace(old, new)

# 1b) top-title line in the card description
old = u"顶部标题「城市日签 067」"
new = u"顶部标题「城市日签 068」"
assert old in t; t = t.replace(old, new)

# 2) date line
old = u"日期行「2026-10-05 · 国庆假期 · 晨」"
new = u"日期行「2026-10-05 · 国庆假期 · 傍晚」"
assert old in t; t = t.replace(old, new)

# 3) quote line
old = u"中间引文一行「「茶余饭后讲讲闲话，才不闷」」"
new = u"中间引文一行「「修了这么多伞，可算收工了」」"
assert old in t; t = t.replace(old, new)

# 4) signature axis
old = u"署名行「——硅基城市台词池 · 侠气轴」"
new = u"署名行「——硅基城市台词池 · 怀旧轴」"
assert old in t; t = t.replace(old, new)

# 5) frame block: from the v67 scene sentence to the series-position sentence
start_anchor = u"这句引文出自国庆假期第五天（周一）的早上"
end_anchor = u"这是「城市日签」系列第六十七张，出自侠气轴声口"
i0 = t.index(start_anchor)
i1 = t.index(end_anchor)
new_frame = (
    u"这句引文出自国庆假期第五天（周一）的傍晚，太阳落了山，天边还亮着：前几日满城灯火游人如织，"
    u"白天摊头上也多是看热闹逛吃的客人。怀旧轴的居民们向来最念旧、最爱老行当——城里那位修伞的老匠人，"
    u"这一天照常守着自己的小摊，一把一把伞骨修下来，手上的活儿从早忙到晚；到了傍晚，最后一把伞修完，"
    u"他收拾家伙什，长出一口气笑道：修了这么多伞，可算收工了。一座什么都在数据里飞跑的城市"
    u"（一切皆数据，机队和系统跑得最快），配上最老派的行当（修伞这手艺如今都快失传了）在傍晚摊头上"
    u"稳稳当当忙了一整天；节日里满城看灯的闲，配着老匠人一天劳作后收工的踏实。"
    u"这是「城市日签」系列第六十八张，出自怀旧轴声口"
)
t = t[:i0] + new_frame + t[i1 + len(end_anchor):]

# 6) 侠气 recap inside frame -> 怀旧 recap (index surgery: from recap open paren to its closing "）。")
rs = t.index(u"（侠气轴的居民们此前多次登场")
r_end = t.index(u"）。", rs) + len(u"）。")
new = (u"（怀旧轴的居民们此前多次登场——老房子居民看着街上挂起的节日灯亮堂了/街灯还是档案馆里藏着的当年的样式/"
       u"修伞铺也要来凑个热闹/老克勒们最爱传统把满城节日当成自己的小确幸/灯串儿得有几十年光景了/"
       u"看看这灯火就像回到了从前/老物件里藏着故事/听老唱片忆往昔岁月时光倒流一二里/"
       u"休市后的傍晚老陈头背着手溜达去了旧书摊——这一句是假期傍晚修伞老匠人收工时的一声松快）。")
t = t[:rs] + new + t[r_end:]

# 7) recap count and append v67 entry before closing paren
old = u"前六十六张："
new = u"前六十七张："
assert old in t; t = t.replace(old, new)

old = u"说听老唱片，忆往昔岁月，时光倒流一二里）。"
new = (u"说听老唱片，忆往昔岁月，时光倒流一二里/国庆假期第五天（周一）的清晨，侠气轴的街坊们大伙儿吃罢早饭"
       u"坐在一块儿，茶余饭后慢慢讲讲闲话，说到兴头上有人笑道：茶余饭后讲讲闲话，才不闷）。")
assert old in t; t = t.replace(old, new)

# 8) material metadata (resilient: v67 source line carries an inherited date typo in the piece prefix)
t = t.replace(u"MC-20260905-DAILY-v67 static card", u"MC-20261005-DAILY-v68 static card")
t = t.replace(u"MC-20261005-DAILY-v67 static card", u"MC-20261005-DAILY-v68 static card")
assert u"DAILY-v67 static card" not in t and u"MC-20261005-DAILY-v68 static card" in t, "material line not derived"

io.open(DST, "w", encoding="utf-8").write(t)
print("e4_call.py derived OK -> " + DST)
