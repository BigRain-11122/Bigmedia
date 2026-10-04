# -*- coding: utf-8 -*-
# r1247: extract last matching ledger @lines to UTF-8 file (console GBK unsafe)
import io, re
txt = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
lines = txt.splitlines()
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = [l for l in lines if pat.search(l)]
out = ['total hits: %d' % len(hits)]
for l in hits[-3:]:
    out.append('=' * 40)
    out.append(l)
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1247_ledger_tail2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok', len(hits))
