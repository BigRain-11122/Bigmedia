# R458 quick-path check: group ledger five-mode scan + decisions non-empty count
import io, re

P1 = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
P2 = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'

pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = []
for l in io.open(P1, encoding='utf-8', errors='replace'):
    if pat.search(l):
        hits.append(l.rstrip('\n'))
print('ledger_matches', len(hits))
if hits:
    print('ledger_last_prefix', hits[-1][:40].encode('ascii', 'replace').decode('ascii'))
    from collections import Counter
    c = Counter()
    for l in hits:
        for m in pat.findall(l):
            c[m] += 1
    print('ledger_modes', dict(c))

d = [l for l in io.open(P2, encoding='utf-8') if l.strip()]
print('decisions_nonempty', len(d))
