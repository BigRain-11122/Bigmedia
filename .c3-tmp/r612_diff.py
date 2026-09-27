# r612_diff.py -- manual ledger row-diff vs r611 baseline + fix r612_all.py baseline ref (ASCII source)
import io, re

G = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
PATS = ['@BigStream', '@\u4e03\u7ebf\u5168\u53f8', '@\u5168\u53f8', '@\u516d\u53f8', '@\u516b\u7ebf\u5168\u91cf']
cur = []
for raw in io.open(G, encoding='utf-8', errors='replace'):
    if any(p in raw for p in PATS):
        cur.append(raw.rstrip('\r\n'))
base = [re.sub(r'^L\d+\t', '', l.rstrip('\n')) for l in io.open(r'.c3-tmp/r611_lednew5.txt', encoding='utf-8') if l.strip()]
new = [l for l in cur if l not in base]
gone = [l for l in base if l not in cur]
print('BASE=%d CUR=%d NEW=%d GONE=%d' % (len(base), len(cur), len(new), len(gone)))
for l in new[:5]:
    print('NEWLINE ' + l[:150].encode('ascii', 'replace').decode())

p = r'.c3-tmp/r612_all.py'
t = io.open(p, encoding='utf-8').read()
t = t.replace("os.path.join(TMP, 'r612_lednew5.txt')", "os.path.join(TMP, 'r611_lednew5.txt')", 1)
io.open(p, 'w', encoding='utf-8').write(t)
print('fixed baseline ref in r612_all.py')
