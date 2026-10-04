# r1212_check.py - R1212 fast-path five-check probe (read-only; writes UTF-8 report r1212_scan.txt)
# Covers: clock, state heartbeat/watermark, backlog top-level scan, group ledger/decisions/orders
# scan, local orders, intel daily, audits, research monthly note, census anchors gate,
# status export freshness, item blocks of interest, git state.
import json, re, io, os, subprocess, datetime

BASE = r'C:\Users\sjs20\Desktop\FluxGroup'
REP = 'r1212_scan.txt'
out = io.open(REP, 'w', encoding='utf-8')
def w(*a): print(*a, file=out)
def sec(t): w(''); w('=== %s ===' % t)

now = datetime.datetime.now()
sec('CLOCK')
w('now:', now.strftime('%Y-%m-%d %H:%M:%S'))
iso_y, iso_w, iso_d = now.isocalendar()
w('iso_week: %d-W%02d day%d' % (iso_y, iso_w, iso_d))

# ---- state.json ----
sj = json.load(io.open('src/os/state.json', encoding='utf-8'))
wm = sj.get('decisions_watermark', {}) or {}
wmd = set(wm.get('dnums', []))
sec('STATE')
w('ts:', sj.get('ts'))
w('task:', str(sj.get('task'))[:140])
w('tick:', sj.get('tick'), '| production:', sj.get('production'))
w('wm_count:', len(wmd), '| wm_last:', (sorted(wmd) or ['-'])[-1], '| wm_ts:', wm.get('ts'))
log = sj.get('log', [])
w('log_count:', len(log))
w('--- log tail 3 (truncated) ---')
for line in log[-3:]:
    w(line[:300]); w('   ...')

# ---- backlog overview ----
bl = io.open('src/os/backlog.md', encoding='utf-8').read().splitlines()
sec('BACKLOG TOP-LEVEL ITEMS')
for l in bl:
    if re.match(r'^\d+\.\s', l):
        st = 'DONE' if '[done ' in l else 'OPEN'
        w(st, '|', l[:130])

# ---- group decisions diff ----
dtxt = io.open(os.path.join(BASE, 'docs', 'decisions.md'), encoding='utf-8').read()
dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dtxt)))
new = [d for d in dnums if d not in wmd]
sec('GROUP DECISIONS')
w('total_dnums:', len(dnums), '| new_vs_wm:', new if new else 'NONE')
dl = dtxt.splitlines()
w('--- decisions.md head 26 lines ---')
for l in dl[:26]: w(l[:170])

# ---- group ledger scan ----
ll = io.open(os.path.join(BASE, 'cph4', 'evolution-ledger.md'), encoding='utf-8').read().splitlines()
pats = ['@BigStream', '@七线全司', '@全司', '@六司', '@八线']
hits = [(i + 1, l) for i, l in enumerate(ll) if any(p in l for p in pats)]
sec('GROUP LEDGER')
w('total_lines:', len(ll), '| pattern_hit_lines:', len(hits))
for ln, l in hits[-8:]:
    w('L%d: %s' % (ln, l[:230]))

# ---- group orders head ----
op = os.path.join(BASE, 'docs', 'orders.md')
if os.path.exists(op):
    ol = io.open(op, encoding='utf-8').read().splitlines()
    sec('GROUP ORDERS')
    w('total_lines:', len(ol))
    for l in ol[:14]: w(l[:160])

# ---- local orders ----
sec('LOCAL ORDERS (last 5 by mtime)')
try:
    fs = sorted(os.listdir('orders'), key=lambda f: os.path.getmtime(os.path.join('orders', f)))
    for f in fs[-5:]: w(f)
except Exception as e: w('ERR', e)

# ---- intel daily / audits / research ----
sec('INTEL DAILY (last 4)')
try:
    fs = sorted(os.listdir('data/intel/daily'))
    for f in fs[-4:]: w(f)
except Exception as e: w('ERR', e)
sec('AUDITS DIR (last 14)')
try:
    for f in sorted(os.listdir('docs/audits'))[-14:]: w(f)
except Exception as e: w('ERR', e)
sec('RESEARCH: monthly note + last 8 by mtime')
try:
    for f in sorted(os.listdir('docs/research')):
        if 'month' in f.lower() or '月度统计' in f: w('MONTHLY:', f)
    fs = sorted(os.listdir('docs/research'), key=lambda f: os.path.getmtime(os.path.join('docs/research', f)))
    for f in fs[-8:]: w(f)
except Exception as e: w('ERR', e)

# ---- census anchors gate ----
sec('CENSUS ANCHORS (BigLife)')
ap = os.path.join(BASE, 'life', 'BigLife', 'census', 'anchors')
try:
    fs = sorted(os.listdir(ap))
    w('anchor_count:', len(fs), '| last3:', fs[-3:])
    w('C-00030 exists:', os.path.exists(os.path.join(ap, 'C-00030.md')))
except Exception as e: w('ERR', e)

# ---- status export ----
sec('STATUS EXPORT')
try:
    se = json.load(io.open('docs/status-export.json', encoding='utf-8'))
    w('export_ts:', se.get('export_ts'))
except Exception as e: w('ERR', e)

# ---- item blocks of interest ----
for num in ('14', '94', '21'):
    sec('ITEM %s BLOCK (head lines)' % num)
    idx = [i for i, l in enumerate(bl) if re.match(r'^%s\.\s' % num, l)]
    if idx:
        j = idx[0]
        for l in bl[j:j + 14]: w(l[:200])
    else:
        w('not found')

# ---- git ----
sec('GIT')
w('index_lock_exists:', os.path.exists('.git/index.lock'))
r = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
w(r.stdout.strip()[:900] or 'CLEAN')
r2 = subprocess.run(['git', 'log', '-3', '--format=%h|%ci|%s'], capture_output=True, text=True)
for line in r2.stdout.strip().splitlines(): w(line[:150])

out.close()
print('REPORT WRITTEN:', REP)
