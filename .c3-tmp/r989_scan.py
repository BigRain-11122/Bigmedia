# -*- coding: utf-8 -*-
import json, io, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup'
pool = json.load(io.open(os.path.join(ROOT, 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
consumed = {u'求新': [4, 7, 12, 3, 11, 14], u'怀旧': [0, 3, 1, 6, 8, 15, 13],
            u'侠气': [5, 13, 2, 0, 6, 8], u'烟火': [4, 13, 3, 12, 0, 6, 14],
            u'秩序': [4, 12, 16, 14], u'逍遥': [3, 15, 1, 17, 0, 6, 8, 14]}
out = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r989_pool_scan.txt', 'w', encoding='utf-8')
for axis in [u'求新', u'怀旧', u'侠气', u'烟火', u'秩序', u'逍遥']:
    fest = pool['axes'][axis]['festival']
    avail = [i for i in range(len(fest)) if i not in consumed[axis]]
    out.write(u'=== %s festival %d lines, avail %d\n' % (axis, len(fest), len(avail)))
    for i, l in enumerate(fest):
        mark = u'USED' if i in consumed[axis] else u'    '
        out.write(u' %2d %s %s\n' % (i, mark, l))
out.close()
print('written')
