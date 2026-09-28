# -*- coding: utf-8 -*-
# r637 fast-path five-check probe (ASCII-only console output, UTF-8 detail file)
import io, os, re, subprocess, json

BS = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
FG = r'C:\Users\sjs20\Desktop\FluxGroup'
LEDGER = os.path.join(FG, 'cph4', 'evolution-ledger.md')
DEC = os.path.join(FG, 'docs', 'decisions.md')
OUT = os.path.join(BS, '.c3-tmp', 'r637_check.txt')

rep = []
def w(s):
    rep.append(s)

# 1) git status --short
g = subprocess.run(['git', '-C', BS, 'status', '--short'],
                    capture_output=True, text=True, encoding='utf-8', errors='replace')
lines = [l for l in g.stdout.splitlines() if l.strip()]
w('== GIT STATUS (%d lines) ==' % len(lines))
for l in lines:
    w(l)
w('GIT_MODIFIED=%d' % len([l for l in lines if l.strip() and not l.startswith('??')]))
w('GIT_INDEX_LOCK=%s' % os.path.exists(os.path.join(BS, '.git', 'index.lock')))

# 2) orders latest (anchor: top=O-20260928-1910 mtime 2026-09-28 19:12:33, count 35)
od = os.path.join(BS, 'orders')
files = [(f, os.path.getmtime(os.path.join(od, f))) for f in os.listdir(od) if os.path.isfile(os.path.join(od, f))]
files.sort(key=lambda x: -x[1])
w('== ORDERS (count=%d) ==' % len(files))
for f, m in files[:6]:
    import datetime
    w('%s  %s' % (datetime.datetime.fromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S'), f))
recent_new = [f for f, m in files if m > datetime.datetime(2026, 9, 28, 19, 12, 40).timestamp()]
w('ORDERS_NEW_SINCE_ANCHOR=%s' % (','.join(recent_new) if recent_new else 'NONE'))

# 3) daily brief 2026-09-29
w('DAILY_0929=%s' % os.path.exists(os.path.join(BS, 'data', 'intel', 'daily', '2026-09-29.md')))

# 4) ledger five-pattern recount (anchor 34) + new-row diff vs 2026-09-29
import datetime
with io.open(LEDGER, 'r', encoding='utf-8', errors='replace') as fh:
    led = fh.read().splitlines()
pat = re.compile(r'(@BigStream|@七线全司|@全司|@六司|@八线全量)')
five = [i for i, l in enumerate(led) if pat.search(l)]
w('== LEDGER ==')
w('LEDGER_MTIME=%s' % datetime.datetime.fromtimestamp(os.path.getmtime(LEDGER)).strftime('%Y-%m-%d %H:%M:%S'))
w('LEDGER5_COUNT=%d (anchor 34)' % len(five))
new29 = [(i + 1, led[i][:120]) for i in five if '2026-09-29' in led[i] or '20260929' in led[i]]
w('LEDGER5_NEW_0929=%d' % len(new29))
for n, t in new29:
    w('  L%d %s' % (n, t))

# 5) decisions non-empty line count (anchor 65, mtime 2026-09-28 21:07:21)
with io.open(DEC, 'r', encoding='utf-8', errors='replace') as fh:
    dec = [l for l in fh.read().splitlines() if l.strip()]
w('== DECISIONS ==')
w('DEC_MTIME=%s' % datetime.datetime.fromtimestamp(os.path.getmtime(DEC)).strftime('%Y-%m-%d %H:%M:%S'))
w('DEC_NONEMPTY=%d (anchor 65)' % len(dec))

# 6) state production + tick + ts
with io.open(os.path.join(BS, 'src', 'os', 'state.json'), 'r', encoding='utf-8') as fh:
    st = json.load(fh)
w('== STATE ==')
w('STATE_PRODUCTION=%s TICK=%s TS=%s' % (st.get('production'), st.get('tick'), st.get('ts')))

# 7) #85 source + anchors + W40 audit + global-benchmarks date
nov = os.path.join(BS, 'data', 'storylines', 'novel')
w('== SOURCES ==')
w('NOVEL_V4=%s' % os.path.exists(os.path.join(nov, 'SC-001-01-v4.md')))
if os.path.exists(os.path.join(nov, 'SC-001-01-v4.md')):
    with io.open(os.path.join(nov, 'SC-001-01-v4.md'), 'r', encoding='utf-8') as fh:
        v4 = fh.read()
    w('NOVEL_V4_CHARS=%d' % len(re.sub(r'\s', '', v4)))
anch = os.path.join(FG, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(anch):
    a = sorted(os.listdir(anch))
    w('ANCHORS_COUNT=%d TAIL=%s C30=%s C31=%s' % (len(a), a[-1] if a else '-',
        os.path.exists(os.path.join(anch, 'C-00030.md')), os.path.exists(os.path.join(anch, 'C-00031.md'))))
w('W40_AUDIT=%s' % os.path.exists(os.path.join(BS, 'docs', 'audits', '2026-W40-self-audit.md')))

# 8) recent backlog top + untracked family summary
untracked = [l[3:] for l in lines if l.startswith('??')]
fams = {}
for u in untracked:
    top = u.split('/')[0] if '/' in u else u
    fams[top] = fams.get(top, 0) + 1
w('== UNTRACKED FAMILIES ==')
for k in sorted(fams):
    w('%s=%d' % (k, fams[k]))

with io.open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(rep))
print('OK r637_check written=%d lines' % len(rep))
