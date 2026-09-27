# -*- coding: utf-8 -*-
# R518 quick-path five checks + window-item probes (write-file UTF-8 + direct read, zero PS round-trip)
import io, os, time, json

BASE = r'C:\Users\sjs20\Desktop\FluxGroup'
REPO = os.path.join(BASE, 'media', 'BigStream')
out = []

# 1) orders top files (new-order check)
odir = os.path.join(REPO, 'orders')
mds = [(f, os.path.getmtime(os.path.join(odir, f))) for f in os.listdir(odir) if f.endswith('.md')]
mds.sort(key=lambda x: -x[1])
out.append('orders md count=%d' % len(mds))
for f, m in mds[:3]:
    out.append('  top: %s mtime=%s' % (f, time.strftime('%m-%d %H:%M:%S', time.localtime(m))))

# 2) ledger five-pattern case-sensitive line count (anchor=31 per R511-R517)
ledger = os.path.join(BASE, 'cph4', 'evolution-ledger.md')
pats = [u'@BigStream', u'@七线全司', u'@全司', u'@六司', u'@八线全量']
cnt, hits = 0, []
with io.open(ledger, 'r', encoding='utf-8', errors='replace') as fh:
    for i, line in enumerate(fh, 1):
        if any(p in line for p in pats):
            cnt += 1
            hits.append((i, line.strip()[:70]))
out.append('ledger five-pattern lines=%d (anchor=31)' % cnt)
for i, l in hits[-2:]:
    out.append('  L%d: %s' % (i, l))

# 3) decisions non-empty UTF-8 lines (anchor=56 per R513-R517)
dec = os.path.join(BASE, 'docs', 'decisions.md')
n = 0
with io.open(dec, 'r', encoding='utf-8', errors='replace') as fh:
    for line in fh:
        if line.strip():
            n += 1
out.append('decisions non-empty lines=%d (anchor=56)' % n)

# 4) index.lock
out.append('index.lock=%s' % os.path.exists(os.path.join(REPO, '.git', 'index.lock')))

# 5) production state field
try:
    st = json.load(io.open(os.path.join(REPO, 'src', 'os', 'state.json'), 'r', encoding='utf-8'))
    out.append('state production=%s tick=%s' % (st.get('production'), st.get('tick')))
except Exception as e:
    out.append('state read ERR %s' % e)

# window probes
# CENSUS supply gate: anchors dir top card
adir = os.path.join(BASE, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(adir):
    ids = sorted(f for f in os.listdir(adir) if f.endswith('.md'))
    out.append('census anchors top=%s C-00030=%s C-00031=%s' % (
        ids[-1] if ids else 'none',
        os.path.exists(os.path.join(adir, 'C-00030.md')),
        os.path.exists(os.path.join(adir, 'C-00031.md'))))
else:
    out.append('census anchors dir MISSING %s' % adir)

# FluxVerse footage tail (#78 probe)
fdir = os.path.join(REPO, 'data', 'sources', 'footage')
if os.path.isdir(fdir):
    ff = [(f, os.path.getmtime(os.path.join(fdir, f))) for f in os.listdir(fdir)]
    ff.sort(key=lambda x: -x[1])
    for f, m in ff[:3]:
        out.append('  footage: %s mtime=%s' % (f, time.strftime('%m-%d %H:%M', time.localtime(m))))

# E4 v7 result presence
v7 = os.path.join(REPO, 'data', 'storylines', 'cards', 'MC-20260927-DIGEST-v7-tmp')
out.append('v7-tmp files=%s' % sorted(os.listdir(v7)))
out.append('e4-result v7=%s' % os.path.exists(os.path.join(v7, 'e4-result.json')))

print('\n'.join(out))
