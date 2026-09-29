# -*- coding: utf-8 -*-
# R714: lc012 README gate block update via slice (immune to invisible char drift)
import io
p = 'data/sources/lc012/README.md'
t = io.open(p, encoding='utf-8').read()
start = t.find(u'余腿=渲染腿')
assert start >= 0, 'start anchor missing'
end_anchor = u'随轮领。'
end = t.find(end_anchor, start)
assert end >= 0, 'end anchor missing'
end += len(end_anchor)
new_block = (u'S2=三门全绿（R714：ai_feel 0F0W+层 1.8 六面+spec 双 PASS）·帧验三律全过（R714）。\n'
             u'- 余腿=收官腿（E8+ASR+E4+M4→F-066 登记→冗余池第九件落位→release-schedule v2.4→E12 出池）R715 随轮领。')
t = t[:start] + new_block + t[end:]
io.open(p, 'w', encoding='utf-8').write(t)
print('gate block updated via slice')
