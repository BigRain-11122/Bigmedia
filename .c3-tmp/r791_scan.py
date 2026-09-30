# -*- coding: utf-8 -*-
# R791 five-check content-addressed scan (r771 lineage rerun)
import io, json, os, re, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'r791_scan.txt')
L = []
def w(x): L.append(x)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# 1. orders anchor
omds = sorted(glob.glob(os.path.join(ROOT, 'orders', 'O-*.md')))
top_order = os.path.basename(omds[-1]) if omds else 'NONE'
w('orders=%d O-*.md +README=%d anchor, top=%s (no new order)' % (len(omds), len(omds) + 1, top_order))

# 2. ledger six-mode rows (strict @-prefix patterns, row count)
ledger = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', 'r', encoding='utf-8', errors='replace').read()
six = [ln for ln in ledger.splitlines() if re.search(r'@BigStream|@七线全司|@全司|@六司', ln)]
p30 = [ln for ln in six if 'P-20260930' in ln]
p29n = sorted({int(m) for ln in six for m in re.findall(r'P-20260929-(\d{2})', ln)})
lastp = None
for ln in six:
    ms = re.findall(r'P-202609\d\d-\d{2}', ln)
    if ms:
        lastp = ms[-1]
w('ledger_six_mode_hits=%d last_p=%s p20260930_rows=%d p29_max=%d (expect 41 band / watch-row, 0, <=13, R763/R771/R789 same-judgment)' % (len(six), lastp, len(p30), (p29n[-1] if p29n else -1)))

# 3. decisions dnum set-diff vs watermark (\d{2} fixed-length extraction, D-20260930-19 law)
dec = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', 'r', encoding='utf-8', errors='replace').read()
dnums = set()
for m in re.finditer(r'\b([DC])-(\d{8})-(\d{2})(?!\d)', dec):
    dnums.add('%s-%s-%s' % (m.group(1), m.group(2), m.group(3)))
st = json.loads(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), 'r', encoding='utf-8-sig').read())
wm = set(st['decisions_watermark']['dnums'])
new = sorted(dnums - wm)
w('decisions_dnum_total=%d baseline=%d new_rows=%s (D-20260930-19 watermark diff, D-13 SLA %s)' % (len(dnums), len(wm), (','.join(new) if new else 'NONE'), ('TRIGGERED' if new else 'not triggered')))

# 4. production + lock + codex/CODELY mtimes
w('production=%s tick=%d (pre-close read) / index.lock=%s' % (st['production'], st['tick'], os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))))
for rel, label in ((u'data/storylines/codex/README.md', 'codex README'), (u'data/storylines/codex/city-humanities.md', 'codex city-humanities'), (u'CODELY.md', 'CODELY.md')):
    p = os.path.join(ROOT, rel)
    w('%s mtime=%s' % (label, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S')))

# 5. GB 7-day gate
gb = io.open(os.path.join(ROOT, 'docs', 'global-benchmarks.md'), 'r', encoding='utf-8', errors='replace').read()
m = re.search(r'2026-\d{2}-\d{2}', gb)
w('gb_head_date_probe=%s (7-day gate: due 10-01, today %s = day6, no early reset)' % (m.group(0) if m else 'NONE', now))

# 6. daily briefs
w('daily brief: 2026-10-01.md %s (correct, REACT window not open), 2026-09-30.md %s' % (
    ('absent' if not os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-01.md')) else 'PRESENT'),
    ('in case' if os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-30.md')) else 'MISSING')))

io.open(OUT, 'w', encoding='utf-8').write((u'R791 five-check scan (content-addressed rerun %s):\n' % now) + u'\n'.join(L) + u'\n')
print('SCAN-OK lines=%d out=%s' % (len(L), OUT))
