# -*- coding: utf-8 -*-
"""R1129 fresh five-check + three legs + probes (declared-idle window round 6/6
= batch close round per os-protocol section 6). No re-scan of settled waiting
objects (product-priority law 2): E30 night lane definitively closed at R1127
(full-pool evidence level), day-close verdict negative at R1123/R1124.
Remaining gates are calendar/dated (10-04 trio / 10-05 W41+OSS-w4 / 10-07 / 10-08).
"""
import io, os, re, json, subprocess, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
FG = r'C:\Users\sjs20\Desktop\FluxGroup'
now = datetime.datetime.now()
O = io.StringIO()

def w(s):
    O.write(s + u'\n')

w(u'== r1129_check fresh run %s ==' % now.strftime('%Y-%m-%d %H:%M:%S'))

# 1 orders top (canonical latest mtime)
od = os.path.join(ROOT, 'orders')
ofs = sorted(((os.path.getmtime(os.path.join(od, f)), f) for f in os.listdir(od) if f.endswith('.md')), reverse=True)
mt, fn = ofs[0]
w(u'1. orders top: %s mtime=%s (baseline O-20260928-1910 2026-09-28 19:12:33)' % (
    fn, datetime.datetime.fromtimestamp(mt).strftime('%Y-%m-%d %H:%M:%S')))

# 2 group orders.md mtime (baseline 12:39:57 = R1096 consumed version)
go = os.path.join(FG, 'docs', 'orders.md')
w(u'   group orders.md mtime=%s (baseline 2026-10-03 12:39:57)' % datetime.datetime.fromtimestamp(os.path.getmtime(go)).strftime('%Y-%m-%d %H:%M:%S'))

# 3 ledger @target rows (content-counted)
led = io.open(os.path.join(FG, 'cph4', 'evolution-ledger.md'), encoding='utf-8').read().splitlines()
pat = re.compile(u'@(BigStream|七线全司|全司|六司|八线全量)')
tgt = [ln for ln in led if pat.search(ln)]
w(u'2. ledger @target rows: %d (baseline 41)' % len(tgt))
w(u'   ledger mtime=%s (baseline identity-adjudicated 2026-10-03 15:15:33 = R1110)' % datetime.datetime.fromtimestamp(
    os.path.getmtime(os.path.join(FG, 'cph4', 'evolution-ledger.md'))).strftime('%Y-%m-%d %H:%M:%S'))
w(u'   last target line: %s' % (tgt[-1][:100] if tgt else u'NONE'))

# 4 decisions dnum content-addressed diff
dec = io.open(os.path.join(FG, 'docs', 'decisions.md'), encoding='utf-8').read()
dset = set(re.findall(r'[DC]-\d{8}-\d{2}', dec))
st = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
wm = set(st['decisions_watermark']['dnums'])
new = sorted(dset - wm)
w(u'3. decisions dnums=%d watermark=%d NEW=%s' % (len(dset), len(wm), new if new else u'[]'))

# 5 lock / production / tick
w(u'4. index.lock: %s | production=%s tick=%s' % (
    os.path.exists(os.path.join(ROOT, '.git', 'index.lock')), st.get('production'), st.get('tick')))

# 6 daily brief / W40 audit / GB gate
w(u'5. daily brief 10-03: %s (10-04 = day-boundary item)' % os.path.exists(
    os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-03.md')))
w(u'   W40 self-audit: %s | GB gate due 10-08 (last refresh 10-01)' % os.path.exists(
    os.path.join(ROOT, 'docs', 'audits', '2026-W40-self-audit.md')))

# 7 #86 three legs content-addressed
pool = json.load(io.open(os.path.join(FG, 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
na = sum(len(rows) for a in pool['axes'] for rows in pool['axes'][a].values())
ns = sum(len(rows) for rows in pool['sprite'].values())
w(u'6. #86 a-leg pools: axes=%d sprite=%d total=%d (baseline 1440)' % (na, ns, na + ns))
ic = io.open(os.path.join(FG, 'life', 'BigLife', 'cognition', 'interchat-ledger.jsonl'), encoding='utf-8')
w(u'   c-leg interchat rows: %d (baseline 22)' % sum(1 for _ in ic))
anch = os.listdir(os.path.join(FG, 'life', 'BigLife', 'census', 'anchors'))
w(u'   CENSUS anchors: %d stop=%s C-00030 absent: %s' % (
    len(anch), max(anch), u'C-00030.md' not in anch))

# 8 backlog/queue mtimes
for p, lbl in [(u'src/os/backlog.md', u'backlog'), (u'docs/self-improvement-queue.md', u'queue')]:
    w(u'7. %s mtime=%s' % (lbl, datetime.datetime.fromtimestamp(
        os.path.getmtime(os.path.join(ROOT, *p.split(u'/')))).strftime('%Y-%m-%d %H:%M:%S')))

# 9 export freshness
ex = json.load(io.open(os.path.join(ROOT, 'docs', 'status-export.json'), encoding='utf-8'))
w(u'8. export_ts=%s (batch-close refresh face; no-change round -> F3 law no refresh)' % ex.get('export_ts', u'?'))

# 10 three probes
probes = [
    (u'board', [u'python', os.path.join(ROOT, 'src', 'board_check.py')], u'r1129_board.txt'),
    (u'readiness', [u'python', os.path.join(ROOT, 'src', 'readiness.py')], u'r1129_rd.txt'),
    (u'loop', [u'python', os.path.join(ROOT, 'src', 'os', 'loop_health.py')], u'r1129_loop.txt'),
]
for name, cmd, out in probes:
    p = subprocess.run(cmd, capture_output=True, cwd=ROOT)
    text = (p.stdout.decode('utf-8', 'replace') + u'\n[stderr]\n' + p.stderr.decode('utf-8', 'replace')).strip()
    io.open(os.path.join(ROOT, '.c3-tmp', out), 'w', encoding='utf-8').write(text + u'\n')
    w(u'9. probe %s rc=%d -> %s' % (name, p.returncode, out))

s = io.StringIO()
for name, _, out in probes:
    t = io.open(os.path.join(ROOT, '.c3-tmp', out), encoding='utf-8').read()
    tl = t.splitlines()
    s.write(u'### %s (lines=%d)\n' % (name, len(tl)))
    for ln in tl:
        low = ln.lower()
        if ((u'fail' in low) or (u'warn' in low) or (u'block' in low) or (u'finding' in low)):
            s.write(ln[:300] + u'\n')
    s.write(u'-- tail --\n')
    for ln in tl[-6:]:
        s.write(ln[:300] + u'\n')
    s.write(u'\n')
io.open(os.path.join(ROOT, '.c3-tmp', 'r1129_probes_summary.txt'), 'w', encoding='utf-8').write(s.getvalue())
w(u'10. probes summary written')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1129_check.txt'), 'w', encoding='utf-8').write(O.getvalue())
print('r1129_check done, probes run')
