# -*- coding: utf-8 -*-
# R519 quick-path five checks + window-item probes (write-file UTF-8, zero PS round-trip)
import io, os, time, json

BASE = r'C:\Users\sjs20\Desktop\FluxGroup'
REPO = os.path.join(BASE, 'media', 'BigStream')
out = []

# 1) orders: count + top + edited-since-anchor (anchor: O-1050 mtime 13:53:11 = R515 append footprint)
odir = os.path.join(REPO, 'orders')
mds = [(f, os.path.getmtime(os.path.join(odir, f))) for f in os.listdir(odir) if f.endswith('.md')]
mds.sort(key=lambda x: -x[1])
o_files = [f for f, _ in mds if f.startswith('O-')]
out.append('orders md total=%d O-prefix=%d (anchor total 36 / O- 35)' % (len(mds), len(o_files)))
for f, m in mds[:3]:
    out.append('  top: %s mtime=%s' % (f, time.strftime('%m-%d %H:%M:%S', time.localtime(m))))
edited = [(f, time.strftime('%H:%M:%S', time.localtime(m))) for f, m in mds if m > time.mktime(time.strptime('2026-09-27 13:53:12', '%Y-%m-%d %H:%M:%S'))]
out.append('orders_edited_since_anchor=%s' % (edited if edited else 'NONE'))

# 2) ledger five-pattern case-sensitive line count (anchor=31 per R511-R518)
ledger = os.path.join(BASE, 'cph4', 'evolution-ledger.md')
pats = [u'@BigStream', u'@七线全司', u'@全司', u'@六司', u'@八线全量']
cnt, hits = 0, []
with io.open(ledger, 'r', encoding='utf-8', errors='replace') as fh:
    for i, line in enumerate(fh, 1):
        if any(p in line for p in pats):
            cnt += 1
            hits.append((i, line.strip()[:60]))
out.append('ledger five-pattern lines=%d (anchor=31)' % cnt)
for i, l in hits[-2:]:
    out.append('  L%d: %s' % (i, l))

# 3) decisions non-empty UTF-8 lines (anchor=56 per R513-R518)
dec = os.path.join(BASE, 'docs', 'decisions.md')
n = 0
with io.open(dec, 'r', encoding='utf-8', errors='replace') as fh:
    for line in fh:
        if line.strip():
            n += 1
out.append('decisions non-empty lines=%d (anchor=56)' % n)

# 4) index.lock + git state markers
out.append('index.lock=%s' % os.path.exists(os.path.join(REPO, '.git', 'index.lock')))

# 5) production + tick
try:
    st = json.load(io.open(os.path.join(REPO, 'src', 'os', 'state.json'), 'r', encoding='utf-8'))
    out.append('state production=%s tick=%s ts=%s' % (st.get('production'), st.get('tick'), st.get('ts')))
    out.append('state focus head=%s' % st.get('focus', '')[:40])
except Exception as e:
    out.append('state read ERR %s' % e)

# window probes
adir = os.path.join(BASE, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(adir):
    ids = sorted(f for f in os.listdir(adir) if f.endswith('.md'))
    out.append('census anchors top=%s C-00030=%s C-00031=%s' % (
        ids[-1] if ids else 'none',
        os.path.exists(os.path.join(adir, 'C-00030.md')),
        os.path.exists(os.path.join(adir, 'C-00031.md'))))
else:
    out.append('census anchors dir MISSING %s' % adir)

# #78 footage tail probe (FluxVerse live-capture arrival check)
fdir = os.path.join(REPO, 'data', 'sources', 'footage')
if os.path.isdir(fdir):
    ff = [(f, os.path.getmtime(os.path.join(fdir, f))) for f in os.listdir(fdir)]
    ff.sort(key=lambda x: -x[1])
    for f, m in ff[:3]:
        out.append('  footage: %s mtime=%s' % (f, time.strftime('%m-%d %H:%M', time.localtime(m))))
else:
    out.append('  footage dir MISSING')

# storylines three-subdomain freshness (bm-a write-sign probe)
for sub in ('video', 'novel', 'audio', 'comic'):
    d = os.path.join(REPO, 'data', 'storylines', sub)
    if os.path.isdir(d):
        newest = 0.0
        for root, _, files in os.walk(d):
            for f in files:
                m = os.path.getmtime(os.path.join(root, f))
                if m > newest:
                    newest = m
        out.append('storylines/%s newest=%s' % (sub, time.strftime('%m-%d %H:%M', time.localtime(newest)) if newest else 'none'))
    else:
        out.append('storylines/%s MISSING' % sub)

# daily brief + backlog + HQ-FEEDBACK mtimes
for rel in ('data/intel/daily/2026-09-27.md', 'src/os/backlog.md', 'HQ-FEEDBACK.md'):
    p = os.path.join(REPO, *rel.split('/'))
    out.append('%s exists=%s mtime=%s' % (rel, os.path.exists(p), time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p))) if os.path.exists(p) else '-'))

# tmp batch state (SC-003 unclosed expected state)
t1 = os.path.join(REPO, '.sc003-tmp')
t2 = os.path.join(REPO, '.sc003-v3-tmp')
if os.path.isdir(t1):
    n1 = max(os.path.getmtime(os.path.join(t1, f)) for f in os.listdir(t1))
    out.append('.sc003-tmp files=%d newest=%s' % (len(os.listdir(t1)), time.strftime('%m-%d %H:%M', time.localtime(n1))))
if os.path.isdir(t2):
    n2 = max(os.path.getmtime(os.path.join(t2, f)) for f in os.listdir(t2))
    out.append('.sc003-v3-tmp files=%d newest=%s' % (len(os.listdir(t2)), time.strftime('%m-%d %H:%M', time.localtime(n2))))

print('\n'.join(out))
