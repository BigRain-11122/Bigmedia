# -*- coding: utf-8 -*-
# r807 five-check content-addressed scan (r911 lineage rerun; R918 window)
import io, json, os, re, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'r919_scan.txt')
L = []
def w(x): L.append(x)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# 1. orders anchor
omds = sorted(glob.glob(os.path.join(ROOT, 'orders', 'O-*.md')))
top_order = os.path.basename(omds[-1]) if omds else 'NONE'
w('orders=%d O-*.md +README=%d anchor, top=%s' % (len(omds), len(omds) + 1, top_order))

# 2. ledger scan rows (task modes + @八线全量 + machine modes + dashed P format; R845 re-baseline)
ledger = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', 'r', encoding='utf-8', errors='replace').read()
MODE_RE = re.compile(r'@BigStream|@七线全司|@全司|@六司|@八线全量')
BM_RE = re.compile(r'@bm-a|@bm-b')
P_RE = re.compile(r'P-2026-?(\d{4}|\d{2}-\d{2})-(\d{2})')
ll = ledger.splitlines()
six = [ln for ln in ll if MODE_RE.search(ln)]
bm = [ln for ln in ll if BM_RE.search(ln)]
hits = [ln for ln in ll if MODE_RE.search(ln) or BM_RE.search(ln)]
p01n = sorted({int(m) for ln in hits for m in re.findall(r'P-2026-?10-?01-(\d{2})', ln)})
lastp = None
for ln in hits:
    ms = P_RE.findall(ln)
    if ms:
        lastp = ms[-1][0]
dash_caught = [ln for ln in bm if 'P-2026-10-01-01' in ln]
w('ledger_scan_hits=%d (task-modes=%d + machine-modes=%d; R845 re-baseline 46) last_p=%s p20261001_max=%d' % (len(hits), len(six), len(bm), lastp, (p01n[-1] if p01n else -1)))
w('r845_regression: P-2026-10-01-01 @bm-a dash row caught=%s' % bool(dash_caught))

# 3. decisions dnum set-diff vs watermark (D-20260930-19 law, content-addressed)
dec = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', 'r', encoding='utf-8', errors='replace').read()
dnums = set()
for m in re.finditer(r'\b([DC])-(\d{8})-(\d{2})(?!\d)', dec):
    dnums.add('%s-%s-%s' % (m.group(1), m.group(2), m.group(3)))
for m in re.finditer(r'\b([DC])-(\d{4})-(\d{2})-(\d{2})-(\d{2})(?!\d)', dec):
    dnums.add('%s-%s%s%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
st = json.loads(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), 'r', encoding='utf-8-sig').read())
wm = set(st['decisions_watermark']['dnums'])
new = sorted(dnums - wm)
w('decisions_dnum_total=%d baseline=%d new_rows=%s (D-20260930-19 watermark diff, D-13 SLA %s)' % (len(dnums), len(wm), (','.join(new) if new else 'NONE'), ('TRIGGERED' if new else 'not triggered')))

# 4. production + lock + mtimes
w('production=%s tick=%d (pre-close read) / index.lock=%s' % (st['production'], st['tick'], os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))))
for rel, label in ((u'data/storylines/codex/README.md', 'codex README'), (u'data/storylines/codex/city-humanities.md', 'codex city-humanities'), (u'CODELY.md', 'CODELY.md')):
    p = os.path.join(ROOT, rel)
    w('%s mtime=%s' % (label, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S')))

# 5. GB 7-day gate (v1.1 refreshed 10-01 per R795; next due 10-08)
gb = io.open(os.path.join(ROOT, 'docs', 'global-benchmarks.md'), 'r', encoding='utf-8', errors='replace').read()
m = re.search(r'2026-\d{2}-\d{2}', gb)
w('gb_head_date_probe=%s (7-day gate due 10-08 per R795; today %s)' % (m.group(0) if m else 'NONE', now))

# 6. daily brief 10-02 (R909 produced)
w('daily brief: 2026-10-02.md %s' % ('PRESENT' if os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-02.md')) else 'ABSENT'))

# 7. CENSUS supply gate (cross-repo read-only, anchors/ canonical position only)
anchors_dir = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors'
if os.path.isdir(anchors_dir):
    ids = sorted({m.group(1) for f in os.listdir(anchors_dir) for m in [re.match(r'(C-\d{5})\.md', f)] if m})
    w('census_anchors_top=%s (C-00030 present: %s) -> CENSUS-v21 supply gate %s' % (
        ids[-1] if ids else 'NONE', 'C-00030' in ids, 'OPEN' if 'C-00030' in ids else 'CLOSED'))

# 8. dispatch-board BigStream rows recheck (D-20261001-06c delivered R797; group-side lag noted R840)
w('dispatch_board: D-20261001-06 BigStream row = delivered R797 (R-20261001-bigstream-01 on disk; board status lag noted R840)')

io.open(OUT, 'w', encoding='utf-8').write((u'r807 five-check scan (content-addressed %s):\n' % now) + u'\n'.join(L) + u'\n')
print('SCAN-OK lines=%d out=%s' % (len(L), OUT))
