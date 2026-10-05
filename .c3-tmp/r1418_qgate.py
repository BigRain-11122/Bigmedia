# -*- coding: utf-8 -*-
import io, re, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
q = open(ROOT + r'\docs\self-improvement-queue.md', encoding='utf-8').read()
o = io.open(ROOT + r'\.c3-tmp\r1418_qgate.txt', 'w', encoding='utf-8')
lines = q.splitlines()

# section headers
o.write('--- HEADERS ---\n')
for i, l in enumerate(lines):
    if re.match(r'^#{1,3}\s', l.strip()):
        o.write('H%d %s\n' % (i, l.strip()[:100]))

# lines mentioning 10-06/10-07/10-08 gates
o.write('--- GATE LINES (10-06/10-07/10-08/pending/standby 注册) ---\n')
for l in lines:
    s = l.strip()
    if re.search(r'10-0[678]', s) and re.search(r'(闸|gate|解锁|standby|注册|窗)', s):
        o.write('G| ' + s[:220] + '\n')

# recent dated entries 10-04/10-05 across all sections
o.write('--- RECENT DATED ENTRIES (10-04/10-05) ---\n')
for l in lines:
    s = l.strip()
    if re.match(r'^[-*]?\s*2026-10-0[45]:', s):
        o.write('D| ' + s[:200] + '\n')
o.close()
print('ok')
