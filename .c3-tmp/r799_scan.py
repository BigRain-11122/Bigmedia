# -*- coding: utf-8 -*-
# r799 five-check content-addressed scan (r795 lineage rerun)
import io, json, os, re, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'r799_scan.txt')
L = []
def w(x): L.append(x)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# 1. orders anchor
omds = sorted(glob.glob(os.path.join(ROOT, 'orders', 'O-*.md')))
top_order = os.path.basename(omds[-1]) if omds else 'NONE'
w('orders=%d O-*.md +README=%d anchor, top=%s' % (len(omds), len(omds) + 1, top_order))

# 2. ledger six-mode rows (strict @-prefix patterns, row count)
ledger = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', 'r', encoding='utf-8', errors='replace').read()
six = [ln for ln in ledger.splitlines() if re.search(r'@BigStream|@七线全司|@全司|@六司', ln)]
p30 = [ln for ln in six if 'P-20260930' in ln]
p01n = sorted({int(m) for ln in six for m in re.findall(r'P-20261001-(\d{2})', ln)})
lastp = None
for ln in six:
    ms = re.findall(r'P-2026(09\d\d|100\d)-\d{2}', ln)
    if ms:
        lastp = ms[-1]
w('ledger_six_mode_hits=%d last_p=%s p20260930_rows=%d p20261001_max=%d (R798 baseline=40 hits, watch-band)' % (len(six), lastp, len(p30), (p01n[-1] if p01n else -1)))

# 3. decisions dnum set-diff vs watermark (D-20260930-19 law)
dec = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', 'r', encoding='utf-8', errors='replace').read()
dnums = set()
for m in re.finditer(r'\b([DC])-(\d{8})-(\d{2})(?!\d)', dec):
    dnums.add('%s-%s-%s' % (m.group(1), m.group(2), m.group(3)))
st = json.loads(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), 'r', encoding='utf-8-sig').read())
wm = set(st['decisions_watermark']['dnums'])
new = sorted(dnums - wm)
w('decisions_dnum_total=%d baseline=%d new_rows=%s (D-20260930-19 watermark diff, D-13 SLA %s)' % (len(dnums), len(wm), (','.join(new) if new else 'NONE'), ('TRIGGERED' if new else 'not triggered')))

# 4. production + lock + codex/CODELY mtimes (#86 c+d yield criterion)
w('production=%s tick=%d (pre-close read) / index.lock=%s' % (st['production'], st['tick'], os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))))
for rel, label in ((u'data/storylines/codex/README.md', 'codex README'), (u'data/storylines/codex/city-humanities.md', 'codex city-humanities'), (u'CODELY.md', 'CODELY.md')):
    p = os.path.join(ROOT, rel)
    w('%s mtime=%s' % (label, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S')))

# 5. GB 7-day gate
gb = io.open(os.path.join(ROOT, 'docs', 'global-benchmarks.md'), 'r', encoding='utf-8', errors='replace').read()
m = re.search(r'2026-\d{2}-\d{2}', gb)
w('gb_head_date_probe=%s (7-day gate due 10-08 per R798; today %s)' % (m.group(0) if m else 'NONE', now))

# 6. daily brief
b101 = 'PRESENT' if os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-01.md')) else 'ABSENT'
w('daily brief: 2026-10-01.md %s (R795 produced, REACT 10-01 window consumed F-077 R796)' % b101)

# 7. CENSUS supply gate: C-00030+ anchors (cross-repo read-only, anchors/ canonical position only)
anchors_dir = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors'
if os.path.isdir(anchors_dir):
    ids = sorted({m.group(1) for f in os.listdir(anchors_dir) for m in [re.match(r'(C-\d{5})\.md', f)] if m})
    w('census_anchors_top=%s (C-00030 present: %s) -> CENSUS-v21 supply gate %s' % (
        ids[-1] if ids else 'NONE', 'C-00030' in ids, 'OPEN' if 'C-00030' in ids else 'CLOSED'))
else:
    w('census_anchors_dir=ABSENT')

# 8. BigHouse receipt probe for D-20261001-06c consumption (preview topics framework)
q = {}
for path, label in ((r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\research\R-20261001-bigstream-01-city-growth-preview-topics.md', 'ours'),
                   (r'C:\Users\sjs20\Desktop\FluxGroup\HQ-FEEDBACK.md', 'hq')):
    pass
hq = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\HQ-FEEDBACK.md', 'r', encoding='utf-8', errors='replace').read() if os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\HQ-FEEDBACK.md') else ''
w('HQ-FEEDBACK mentions D-20261001-06 receipt-from-BigHouse: %s' % ('YES' if re.search(r'D-20261001-06[^0-9]', hq) else 'no-scan'))

io.open(OUT, 'w', encoding='utf-8').write((u'r799 five-check scan (content-addressed %s):\n' % now) + u'\n'.join(L) + u'\n')
print('SCAN-OK lines=%d out=%s' % (len(L), OUT))
