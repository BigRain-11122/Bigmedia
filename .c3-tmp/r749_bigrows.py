# -*- coding: utf-8 -*-
# Find which dnums are > D-20260930-30 and dump their rows (BigStream relevance check)
import io, re
dtext = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
dnums = sorted(set(re.findall(r'[DC]-20\d{6}-\d{2}', dtext)))
big = [d for d in dnums if d > 'D-20260930-30']
out = ['dnums>30: %s' % big]
lines = dtext.splitlines()
for d in big:
    hits = [l for l in lines if d in l]
    for h in hits:
        out.append('%s -> %s' % (d, h[:400]))
io.open('.c3-tmp/r749_big_rows.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK')
