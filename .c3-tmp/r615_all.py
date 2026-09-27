# r615_all.py -- fast-path five-check probe for round R614 (ASCII source only)
import os, io, json, re, subprocess, datetime
from collections import Counter

SCRIPT = os.path.abspath(__file__)
TMP = os.path.dirname(SCRIPT)
ROOT = os.path.dirname(TMP)
GROUP = os.path.dirname(os.path.dirname(ROOT))

PATS = ['@BigStream', '@\u4e03\u7ebf\u5168\u53f8', '@\u5168\u53f8', '@\u516d\u53f8', '@\u516b\u7ebf\u5168\u91cf']

lines = []
def ap(s):
    lines.append(s)

def fmt(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M:%S')
    except OSError:
        return 'MISSING'

# 1) orders dir
od = os.path.join(ROOT, 'orders')
entries = []
for f in os.listdir(od):
    p = os.path.join(od, f)
    if os.path.isfile(p):
        entries.append((os.path.getmtime(p), f))
entries.sort()
ofiles = [e for e in entries if e[1].upper().startswith('O-')]
ap('ORDERS_TOTAL=%d O_FILES=%d' % (len(entries), len(ofiles)))
for m, f in entries[-3:]:
    ap('ORDERS_TAIL %s | %s' % (datetime.datetime.fromtimestamp(m).strftime('%m-%d %H:%M:%S'), f))
cut = datetime.datetime(2026, 9, 28, 0, 0).timestamp()
recent = [(datetime.datetime.fromtimestamp(m).strftime('%m-%d %H:%M:%S'), f) for m, f in entries if m > cut]
ap('ORDERS_RECENT_0928=' + (';'.join('%s %s' % r for r in recent) if recent else 'NONE'))

# 2) ledger five-mode lines
ledger = os.path.join(GROUP, 'cph4', 'evolution-ledger.md')
matched = []
ledger_lnums = []
if os.path.exists(ledger):
    with io.open(ledger, encoding='utf-8', errors='replace') as fh:
        for ln, raw in enumerate(fh, 1):
            if any(p in raw for p in PATS):
                matched.append(raw.rstrip('\r\n'))
                ledger_lnums.append(ln)
ap('LEDGER_MTIME=%s' % fmt(ledger))
ap('LEDGER_FIVE_COUNT=%d' % len(matched))
base = os.path.join(TMP, 'r614_lednew5.txt')
if os.path.exists(base):
    with io.open(base, encoding='utf-8') as fh:
        prev = [re.sub(r'^L\d+\t', '', l.rstrip('\n')) for l in fh if l.strip()]
    new = [l for l in matched if l not in prev]
    gone = [l for l in prev if l not in matched]
    ap('LEDGER_NEW=%d GONE=%d' % (len(new), len(gone)))
    for l in new[:5]:
        ap('LEDGER_NEW_LINE %s' % l[:200])
else:
    ap('LEDGER_BASELINE_MISSING')
with io.open(os.path.join(TMP, 'r615_lednew5.txt'), 'w', encoding='utf-8') as fh:
    for idx, l in enumerate(matched):
        fh.write('L%d\t%s\n' % (ledger_lnums[idx], l))

# 3) decisions
dec = os.path.join(GROUP, 'docs', 'decisions.md')
if os.path.exists(dec):
    with io.open(dec, encoding='utf-8', errors='replace') as fh:
        content = fh.read().splitlines()
    ne = [l for l in content if l.strip()]
    ap('DECISIONS_NONEMPTY=%d MTIME=%s' % (len(ne), fmt(dec)))
else:
    ap('DECISIONS=MISSING')

# 4) state fields
with io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8') as fh:
    st = json.load(fh)
ap('STATE_PRODUCTION=%s TICK=%d TS=%s' % (st.get('production'), st.get('tick'), st.get('ts')))

# 5) git status
g = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
mods = [l for l in g if l[:1] == 'M' or (len(l) > 1 and l[1] == 'M')]
untr = [l for l in g if l.startswith('??')]
ap('GIT_MODIFIED=%d UNTRACKED=%d INDEX_LOCK=%s' % (len(mods), len(untr), os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))))
ap('GIT_MOD_LIST=' + ';'.join((l[3:].strip().strip('"') if len(l) > 3 else l) for l in mods))
fam = Counter()
for l in untr:
    p = l[3:].strip().strip('"').replace('/', os.sep)
    top = p.split(os.sep)[0] if os.sep in p else p
    fam[top] += 1
ap('UNTRACKED_FAM=' + ','.join('%s=%d' % (k, v) for k, v in sorted(fam.items())))
head = subprocess.run(['git', 'log', '-1', '--format=%h %s'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.strip()
ap('GIT_HEAD=%s' % head[:120])

# 6) census anchors supply gate
anch = os.path.join(GROUP, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(anch):
    ids = sorted(f[:-3] for f in os.listdir(anch) if f.endswith('.md'))
    ap('ANCHORS_COUNT=%d TAIL=%s C30=%s C31=%s' % (len(ids), ids[-1] if ids else 'none',
        os.path.exists(os.path.join(anch, 'C-00030.md')), os.path.exists(os.path.join(anch, 'C-00031.md'))))
else:
    ap('ANCHORS_DIR=MISSING')

# 7) daily brief
ap('DAILY_0928=%s DAILY_0929=%s' % (os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-28.md')),
                                     os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-29.md'))))

# 8) footprints
for k, rel in [('backlog', 'src/os/backlog.md'), ('hq', 'HQ-FEEDBACK.md'),
               ('station', 'docs/reviews/station-reviews.md'), ('finished', 'output/finished.md'),
               ('cards', 'data/storylines/cards/README.md'), ('export', 'docs/status-export.json'),
               ('renders', 'output/renders/README.md'), ('video', 'data/storylines/video/README.md'),
               ('novel_dir', 'data/storylines/novel'), ('plan', 'PLAN.md'), ('audio', 'data/storylines/audio')]:
    ap('FP %s %s' % (k, fmt(os.path.join(ROOT, rel.replace('/', os.sep)))))

# 9) verdicts 0928 (E4 backfill check)
ev = os.path.join(ROOT, 'docs', 'reviews', 'expert-verdicts')
if os.path.isdir(ev):
    v = sorted(f for f in os.listdir(ev) if f.startswith('20260928'))
    ap('VERDICTS_0928_COUNT=%d' % len(v))
    for f in v:
        ap('VERDICT %s' % f)

# 10) c3-tmp inventory (untracked family delta check)
c3 = sorted(os.listdir(TMP))
ap('C3TMP_COUNT=%d' % len(c3))
ap('C3TMP_LIST=' + ','.join(c3))

out = '\n'.join(lines)
with io.open(os.path.join(TMP, 'r615_all.txt'), 'w', encoding='utf-8') as fh:
    fh.write(out + '\n')
safe = '\n'.join(l for l in lines if all(ord(c) < 128 for c in l))
print(safe)
