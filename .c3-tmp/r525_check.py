# -*- coding: utf-8 -*-
# R525 quick-path five checks + window-item probes (write-file UTF-8, zero PS round-trip)
# Copy of r524_check.py with OUTP -> r525 (R462 no-refall law + R466 preflight law)
import io, os, time, json

BASE = r'C:\Users\sjs20\Desktop\FluxGroup'
REPO = os.path.join(BASE, 'media', 'BigStream')
out = []
out.append('now=%s' % time.strftime('%Y-%m-%d %H:%M:%S'))

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

# 2) ledger five-pattern case-sensitive line count (anchor=31 per R511-R524)
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

# 3) decisions non-empty UTF-8 lines (anchor=56 per R513-R524)
dec = os.path.join(BASE, 'docs', 'decisions.md')
n = 0
with io.open(dec, 'r', encoding='utf-8', errors='replace') as fh:
    for line in fh:
        if line.strip():
            n += 1
out.append('decisions non-empty lines=%d (anchor=56)' % n)

# 4) index.lock
out.append('index.lock=%s' % os.path.exists(os.path.join(REPO, '.git', 'index.lock')))

# 5) production + tick
try:
    st = json.load(io.open(os.path.join(REPO, 'src', 'os', 'state.json'), 'r', encoding='utf-8'))
    out.append('state production=%s tick=%s ts=%s' % (st.get('production'), st.get('tick'), st.get('ts')))
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

# storylines subdomain freshness (bm-a write-sign probe)
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

# daily briefs 09-27 (in-case) + 09-28 (REACT window day) + backlog + HQ-FEEDBACK mtimes
for rel in ('data/intel/daily/2026-09-27.md', 'data/intel/daily/2026-09-28.md', 'src/os/backlog.md', 'HQ-FEEDBACK.md'):
    p = os.path.join(REPO, *rel.split('/'))
    out.append('%s exists=%s mtime=%s' % (rel, os.path.exists(p), time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p))) if os.path.exists(p) else '-'))

# tmp batch state (SC-003 unclosed expected state)
for t in ('.sc003-tmp', '.sc003-v3-tmp'):
    tp = os.path.join(REPO, t)
    if os.path.isdir(tp):
        nm = max(os.path.getmtime(os.path.join(tp, f)) for f in os.listdir(tp))
        out.append('%s files=%d newest=%s' % (t, len(os.listdir(tp)), time.strftime('%m-%d %H:%M', time.localtime(nm))))

# W40 weekly audit file probe (opens 09-28; ISO week 40 = 2026-W40)
ap = os.path.join(REPO, 'docs', 'audits', '2026-W40-self-audit.md')
out.append('W40 self-audit exists=%s' % os.path.exists(ap))

with io.open(os.path.join(REPO, '.c3-tmp', 'r525_check.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print('CHECK_DONE lines=%d' % len(out))
