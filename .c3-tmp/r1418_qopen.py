# -*- coding: utf-8 -*-
import io
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
lines = open(ROOT + r'\docs\self-improvement-queue.md', encoding='utf-8').read().splitlines()
o = io.open(ROOT + r'\.c3-tmp\r1418_qopen.txt', 'w', encoding='utf-8')
# print lines 0..105 (standing sections A-E, before burn log)
for i, l in enumerate(lines[:110]):
    o.write('%03d| %s\n' % (i, l.rstrip()[:190]))
o.close()
print('ok')
