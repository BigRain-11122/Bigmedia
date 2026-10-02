# -*- coding: utf-8 -*-
import json, io
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup'
pool = json.load(io.open(ROOT + r'\life\BigLife\cognition\pools.json', encoding='utf-8'))
out = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1003_pool_read.txt', 'w', encoding='utf-8')
consumed = {u'侠气': [0, 1, 2, 5, 10, 13], u'秩序': [4, 12, 6, 9, 2, 16], u'逍遥': [3, 15, 1, 2, 4, 17]}
for ax in [u'侠气', u'秩序', u'逍遥']:
    lines = pool['axes'][ax]['festival']
    out.write(u'== %s festival (18) ==\n' % ax)
    for i, l in enumerate(lines):
        mark = u'USED' if i in consumed[ax] else u'FREE'
        out.write(u'%2d [%s] %s\n' % (i, mark, l))
out.write(u'== axes keys ==\n')
out.write(u', '.join(pool['axes'].keys()) + u'\n')
out.close()
print('OK')
