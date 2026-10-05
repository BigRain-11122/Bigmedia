# -*- coding: utf-8 -*-
# r1419 fast-path five checks (fresh) + lane/queue/W41 status + derive blind-spot resolve
import json, re, os, glob, sys, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HQ = os.path.abspath(os.path.join(ROOT, '..', '..', 'docs'))
out = []
def w(s): out.append(s)
def fmt(p): return time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))

w('NOW=%s' % time.strftime('%Y-%m-%d %H:%M:%S'))

# 0) git status + lock
p = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
w('git_status=[%s]' % p.stdout.strip()[:400])
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

# 4) evolution-ledger scan (all five patterns)
led_path = os.path.normpath(os.path.join(HQ, '..', 'cph4', 'evolution-ledger.md'))
lraw = open(led_path, encoding='utf-8').read()
pats = ['@BigStream', '@七线全司', '@全司', '@六司', '@八线全量']
strict = [ln for ln in lraw.splitlines() if any(p in ln for p in pats)]
w('ledger_mtime=%s' % fmt(led_path))
w('ledger_allpat_hits=%d' % len(strict))
for s in strict[-3:]:
    w('  LED: ' + s.strip()[:150])

# 5) daily brief existence
for d in ('2026-10-05', '2026-10-06'):
    pp = os.path.join(ROOT, 'data', 'intel', 'daily', d + '.md')
    w('daily_%s=%s' % (d, 'EXISTS ' + fmt(pp) if os.path.exists(pp) else 'MISSING'))

# 6) W41 weekly artifacts: audit + queue D-proposal + HQ-FEEDBACK
for pat in ('*W41*', '*2026-W41*'):
    hits = glob.glob(os.path.join(ROOT, 'docs', 'audits', pat))
    if hits:
        for h in hits: w('audit_file=%s %s' % (os.path.basename(h), fmt(h)))
        break
else:
    w('audit_W41=MISSING')
q = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
qraw = open(q, encoding='utf-8').read()
proposals = [ln.strip()[:200] for ln in qraw.splitlines() if re.match(r'[-*]?\s*P-\d+', ln.strip())]
w('queue_P_lines=%d' % len(proposals))
for pr in proposals[-4:]:
    w('  QP: ' + pr)
hf = os.path.join(ROOT, 'HQ-FEEDBACK.md')
hflines = open(hf, encoding='utf-8').read().splitlines()
nonempty = [l for l in hflines if l.strip()]
w('hq_feedback_tail=%s' % (nonempty[-1][:180] if nonempty else 'EMPTY'))

# 7) derive blind-spot resolve: R1295-R1310 log extracts
log = state.get('log', [])
for ln in log:
    m = re.match(r'^2026-10-0[45] \d{2}:\d+x R(129[5-9]|130[0-9]|131[0-1]): ', ln)
    if m:
        w('  RLOG %s: %s' % (m.group(1), ln[:260]))

# 8) backlog open-item probe: #14 / #57 / #63 / #66 / #67 heads
bl = open(os.path.join(ROOT, 'src', 'os', 'backlog.md'), encoding='utf-8').read().splitlines()
for num in ('14.', '57.', '63.', '66.', '67.', '98.'):
    for ln in bl:
        s = ln.strip()
        if s.startswith(num):
            w('  BL%s %s' % (num, s[:170]))
            break

# 9) global-benchmarks refresh date
gb = os.path.join(ROOT, 'docs', 'global-benchmarks.md')
if os.path.exists(gb):
    graw = open(gb, encoding='utf-8').read()
    m2 = re.search(r'§?④.*?更新记录.*', graw)
    mm = re.search(r'2026-\d{2}-\d{2}', graw[:3000])
    w('gb_mtime=%s first_date=%s' % (fmt(gb), mm.group(0) if mm else '?'))

# 10) CEO visualization check (global memory: 可视化= gaming/MiniGame/硅基生命元宇宙.html)
for cand in (r'C:\Users\sjs20\Desktop\FluxGroup\gaming\MiniGame', r'C:\Users\sjs20\Desktop\FluxGroup\media\gaming\MiniGame'):
    html = os.path.join(cand, '硅基生命元宇宙.html')
    if os.path.exists(html):
        w('viz_html=%s mtime=%s' % (html, fmt(html)))
        datajs = os.path.join(cand, '硅基生命元宇宙-data.js')
        if os.path.exists(datajs):
            w('viz_datajs mtime=%s' % fmt(datajs))
        break
else:
    w('viz_html=NOT_FOUND under FluxGroup/gaming/MiniGame')

# 11) window state
w('tick=%s ts=%s' % (state.get('tick'), state.get('ts')))

sys.stdout.reconfigure(encoding='utf-8')
open(os.path.join(ROOT, '.c3-tmp', 'r1420_check.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('written %d lines' % len(out))

