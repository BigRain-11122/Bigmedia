# r1985: find the two 13:2x rows (casting law + execution mechanism)
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md", encoding='utf-8').read()
lines = t.splitlines()
# all 10-11 rows regardless of BigStream mention
hits = [(i, l) for i, l in enumerate(lines) if re.match(r'^\|\s*10-11\s', l)]
print('ALL-10-11-ROWS:', len(hits))
for i, l in hits:
    print('---L%d---' % (i + 1))
    print(l[:420])
