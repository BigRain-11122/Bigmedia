# -*- coding: utf-8 -*-
# R441: dump all five-mode @ lines from group evolution-ledger (utf-8 file, then read_file per encoding law)
import io

G = r'C:\Users\sjs20\Desktop\FluxGroup'
pat = ('@BigStream', '@八线全量', '@七线全司', '@全司', '@六司')
hits = []
with io.open(G + r'\cph4\evolution-ledger.md', encoding='utf-8-sig') as f:
    for i, line in enumerate(f, 1):
        if any(p in line for p in pat):
            hits.append((i, line.rstrip()))
out = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r441_ledger.txt', 'w', encoding='utf-8', newline='\n')
for i, line in hits:
    out.write(u'L%d: %s\n' % (i, line))
out.close()
print('hits=%d' % len(hits))
