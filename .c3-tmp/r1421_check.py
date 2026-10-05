# -*- coding: utf-8 -*-
# r1421 fast-path five checks (fresh) + lane/queue/W41 status
import json, re, os, glob, sys, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HQ = os.path.abspath(os.path.join(ROOT, '..', '..', 'docs'))
out = []
def w(s): out.append(s)
def fmt(p): return time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))

w('NOW=%s' % time.strftime('%Y-%m-%d %H:%M:%S'))

# 0) git status + lock
p = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
gs = p.stdout.strip().splitlines()
w('git_status_lines=%d' % len(gs))
for ln in gs[:40]:
    w('  GS: ' + ln[:120])
w('index_lock=%s' % os.path.exists(os.path.join(ROOT, '.git', 'index.lock')))

# 1) orders latest file
orders_dir = os.path.join(ROOT, 'orders')
files = [(os.path.getmtime(os.path.join(orders_dir, f)), f) for f in os.listdir(orders_dir) if f.endswith('.md')]
files.sort()
w('orders_top=%s mtime=%s count=%d' % (files[-1][1], fmt(os.path.join(orders_dir, files[-1][1])), len(files)))

# 2) decisions.md dnum regex set diff vs watermark (content-addressing)
state = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark', {}).get('dnums', []))
dec_path = os.path.join(HQ, 'decisions.md')
raw = open(dec_path, encoding='utf-8').read()
cur = set(re.findall(r'[DC]-\d{8}-\d{2}', raw))
w('decisions_mtime=%s' % fmt(dec_path))
w('decisions_cur=%d wm=%d NEW=%s GONE=%s' % (len(cur), len(wm), sorted(cur - wm), sorted(wm - cur)))

# 3) dispatch board top block scan
dec_lines = raw.splitlines()
board_start = None
for i, ln in enumerate(dec_lines):
    if '派工通告板' in ln:
        board_start = i
        break
if board_start is not None:
    seg = dec_lines[board_start:board_start + 40]
    hits = [ln.strip()[:160] for ln in seg if ('BigStream' in ln or '七司' in ln or '全司' in ln) and ln.strip()]
    w('dispatch_board_hits=%d' % len(hits))
    for h in hits[:6]:
        w('  DB: ' + h)
else:
    w('dispatch_board_not_found')

# 4) evolution-ledger scan (all five patterns) + strict @BigStream
led_path = os.path.normpath(os.path.join(HQ, '..', 'cph4', 'evolution-ledger.md'))
lraw = open(led_path, encoding='utf-8').read()
pats = ['@BigStream', '@七线全司', '@全司', '@六司', '@八线全量']
allhits = [ln for ln in lraw.splitlines() if any(pp in ln for pp in pats)]
strict = [ln for ln in lraw.splitlines() if '@BigStream' in ln]
w('ledger_mtime=%s' % fmt(led_path))
w('ledger_allpat_hits=%d strict_BS=%d' % (len(allhits), len(strict)))
for s in strict[-3:]:
    w('  LED: ' + s.strip()[:150])

# 5) daily brief existence
for d in ('2026-10-06', '2026-10-07'):
    pp = os.path.join(ROOT, 'data', 'intel', 'daily', d + '.md')
    w('daily_%s=%s' % (d, 'EXISTS ' + fmt(pp) if os.path.exists(pp) else 'MISSING'))

# 6) R1420 artifact verification: finished tail / cards README tail / station-reviews tail
fin = os.path.join(ROOT, 'output', 'finished.md')
finlines = [l for l in open(fin, encoding='utf-8').read().splitlines() if l.strip()]
w('finished_tail=%s' % finlines[-1][:150] if finlines else 'finished_empty')
cr = os.path.join(ROOT, 'docs', 'reviews', 'cards', 'README.md')
if os.path.exists(cr):
    crlines = [l for l in open(cr, encoding='utf-8').read().splitlines() if l.strip()]
    w('cards_readme_tail=%s' % crlines[-1][:150] if crlines else 'cards_readme_empty')
sr = os.path.join(ROOT, 'docs', 'reviews', 'station-reviews.md')
srlines = [l for l in open(sr, encoding='utf-8').read().splitlines() if l.strip()]
w('station_reviews_tail=%s' % srlines[-1][:150] if srlines else 'sr_empty')
evd = glob.glob(os.path.join(ROOT, 'docs', 'reviews', 'expert-verdicts', '20261006-*'))
w('e4_verdicts_1006=%d' % len(evd))

# 7) queue open-item scan: sections B/D/E non-done lines
q = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
qraw = open(q, encoding='utf-8').read()
open_lines = [ln.strip()[:170] for ln in qraw.splitlines()
              if ln.strip().startswith(('-', '*')) and '[done' not in ln and 'done]' not in ln
              and re.search(r'^[-*]\s*(P-\d|B\d|C\d|A\d|E\d)', ln.strip())]
w('queue_open_lines=%d' % len(open_lines))
for ol in open_lines[:10]:
    w('  QO: ' + ol)

# 8) backlog open-item probe: #57 / #59 / #63 / #66 / #67 / #70 heads
bl = open(os.path.join(ROOT, 'src', 'os', 'backlog.md'), encoding='utf-8').read().splitlines()
for num in ('57.', '59.', '63.', '66.', '67.', '70.', '86.', '98.'):
    for ln in bl:
        s = ln.strip()
        if s.startswith(num):
            w('  BL%s %s' % (num, s[:170]))
            break

# 9) W41 weekly artifacts
for pat in ('*W41*', '*2026-W41*'):
    hits = glob.glob(os.path.join(ROOT, 'docs', 'audits', pat))
    if hits:
        for h in hits: w('audit_file=%s %s' % (os.path.basename(h), fmt(h)))
        break
else:
    w('audit_W41=MISSING')
hf = os.path.join(ROOT, 'HQ-FEEDBACK.md')
hflines = open(hf, encoding='utf-8').read().splitlines()
nonempty = [l for l in hflines if l.strip()]
w('hq_feedback_tail=%s' % (nonempty[-1][:180] if nonempty else 'EMPTY'))

# 10) GB refresh date
gb = os.path.join(ROOT, 'docs', 'global-benchmarks.md')
if os.path.exists(gb):
    graw = open(gb, encoding='utf-8').read()
    mm = re.search(r'2026-\d{2}-\d{2}', graw[:3000])
    w('gb_mtime=%s first_date=%s' % (fmt(gb), mm.group(0) if mm else '?'))

# 11) CEO visualization check (global memory: 可视化= gaming/MiniGame/硅基生命元宇宙.html)
for cand in (r'C:\Users\sjs20\Desktop\FluxGroup\gaming\MiniGame',):
    html = os.path.join(cand, '硅基生命元宇宙.html')
    if os.path.exists(html):
        w('viz_html mtime=%s' % fmt(html))
        datajs = os.path.join(cand, '硅基生命元宇宙-data.js')
        if os.path.exists(datajs):
            w('viz_datajs mtime=%s' % fmt(datajs))
        break
else:
    w('viz_html=NOT_FOUND')

# 12) export freshness
exp = os.path.join(ROOT, 'docs', 'status-export.json')
if os.path.exists(exp):
    w('export_mtime=%s' % fmt(exp))

# 13) window state
w('tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('production=%s mode=%s' % (state.get('production'), state.get('mode')))

sys.stdout.reconfigure(encoding='utf-8')
open(os.path.join(ROOT, '.c3-tmp', 'r1421_check.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('written %d lines' % len(out))
