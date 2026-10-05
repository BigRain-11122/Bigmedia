import io, json, re, sys
root = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = io.StringIO()
def w(s): out.write(str(s) + "\n")

bt = io.open(root + r'\src\os\backlog.md', encoding='utf-8').read()
for pat in [r'^82\.', r'^94\.']:
    for m in re.finditer(pat, bt, re.M):
        seg = bt[m.start():m.start()+700]
        w('BLK_MATCH ' + pat + ': ' + seg.split('\n')[0][:400])
w('CLOUD_LINE in backlog count: %d' % bt.count('CLOUD_LINE'))
# find backlog lines containing CLOUD or 周报
for i, line in enumerate(bt.split('\n')):
    if 'CLOUD' in line or ('周报' in line and line.strip().startswith(('8','9'))):
        w('BLK_LINE %d: %s' % (i, line[:300]))

st = json.load(io.open(root + r'\src\os\state.json', encoding='utf-8'))
log = st['log']
for kw in ['CLOUD_LINE', 'W41 周轮', '周报', '#94']:
    hits = [(i, l) for i, l in enumerate(log) if kw in l]
    w('LOG kw=%s count=%d' % (kw, len(hits)))
    for i, l in hits[-4:]:
        w('  L%d: %s' % (i, l[:300]))
w('LAST_REAL_R1300s:')
for l in log:
    m = re.match(r'2026-10-0[45] (\d\d:\d\d) R1(3[0-3]\d):', l)
    if m:
        w('  R1%s: %s' % (l[16:20], l[16:230]))

io.open(root + r'\.c3-tmp\r1334_kw.txt', 'w', encoding='utf-8').write(out.getvalue())
print('OK lines', out.getvalue().count('\n'))
