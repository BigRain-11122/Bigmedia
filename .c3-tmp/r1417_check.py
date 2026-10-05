# -*- coding: utf-8 -*-
# R1416 fast-path five checks (fresh) + lane status probe
import json, re, os, glob, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HQ = os.path.abspath(os.path.join(ROOT, '..', '..', 'docs'))
out = []
def w(s): out.append(s)
def fmt(p): return time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))

# 1) orders latest file
orders_dir = os.path.join(ROOT, 'orders')
if os.path.isdir(orders_dir):
    files = [(os.path.getmtime(os.path.join(orders_dir, f)), f) for f in os.listdir(orders_dir) if f.endswith('.md')]
    files.sort()
    w('orders_top=%s mtime=%s count=%d' % (files[-1][1], fmt(os.path.join(orders_dir, files[-1][1])), len(files)))
else:
    w('orders_dir_missing')

# 2) decisions.md dnum regex set diff vs watermark (content-addressing)
state = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark', {}).get('dnums', []))
dec_path = os.path.join(HQ, 'decisions.md')
raw = open(dec_path, encoding='utf-8').read()
cur = set(re.findall(r'[DC]-\d{8}-\d{2}', raw))
w('decisions_mtime=%s' % fmt(dec_path))
w('decisions_cur=%d wm=%d NEW=%s GONE=%s' % (len(cur), len(wm), sorted(cur - wm), sorted(wm - cur)))

# 3) dispatch board top block scan (D-20260930-19)
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

# 4) evolution-ledger strict @BigStream scan
led_path = os.path.normpath(os.path.join(HQ, '..', 'cph4', 'evolution-ledger.md'))
if os.path.exists(led_path):
    lraw = open(led_path, encoding='utf-8').read()
    strict = [ln for ln in lraw.splitlines() if '@BigStream' in ln]
    w('ledger_mtime=%s' % fmt(led_path))
    w('ledger_bigstream_hits=%d' % len(strict))
    for s in strict[-3:]:
        w('  LED: ' + s.strip()[:150])
else:
    w('ledger_missing=%s' % led_path)

# 5) daily brief existence
for d in ('2026-10-04', '2026-10-05', '2026-10-06'):
    p = os.path.join(ROOT, 'data', 'intel', 'daily', d + '.md')
    w('daily_%s=%s' % (d, 'EXISTS' if os.path.exists(p) else 'MISSING'))

# 6) REACT 10-05 window evidence in state log
log = state.get('log', [])
react_1005 = [ln[:220] for ln in log if 'REACT' in ln and ('10-05' in ln[:14] or '2026-10-05' in ln[:20])]
w('react_1005_log_hits=%d' % len(react_1005))
for r in react_1005[-3:]:
    w('  RE: ' + r)

# 7) backlog top 3 numbered lines
bl = open(os.path.join(ROOT, 'src', 'os', 'backlog.md'), encoding='utf-8').read().splitlines()
tops = []
for ln in bl:
    s = ln.strip()
    if s and re.match(r'^\d+\.', s):
        tops.append(s[:200])
        if len(tops) >= 3:
            break
w('backlog_top3:')
for t in tops:
    w('  BL: ' + t)

# 8) self-improvement queue P- lines
q = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
if os.path.exists(q):
    qraw = open(q, encoding='utf-8').read()
    plines = [ln.strip()[:180] for ln in qraw.splitlines() if re.match(r'[-*]?\s*P-\d+', ln.strip())]
    w('queue_P_lines=%d last3:' % len(plines))
    for p in plines[-3:]:
        w('  QP: ' + p)
else:
    w('queue_missing')

# 9) W40/W41 weekly audit existence
for wk in ('W40', 'W41'):
    hits = glob.glob(os.path.join(ROOT, 'docs', 'audits', '*%s*' % wk))
    w('audit_%s=%s' % (wk, hits[-1] if hits else 'MISSING'))

sys.stdout.reconfigure(encoding='utf-8')
print('\n'.join(out))
