import os, re, datetime
led = open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
lines = led.splitlines()
out = []
pats = ['@BigStream', '@七线全司', '@全司', '@六司', '@八线全量']
hits = []
for i, l in enumerate(lines):
    if any(p in l for p in pats):
        hits.append((i, l))
out.append('total hits=%d' % len(hits))
for i, l in hits:
    out.append('L%d | %s' % (i+1, l[:260]))
open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1911_ledger_rows.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('hits=%d' % len(hits))
