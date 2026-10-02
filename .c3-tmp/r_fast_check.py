import json, io, re, os, subprocess, glob, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
OUT = os.path.join(ROOT, '.c3-tmp', 'r_fast_check.txt')
out = []

# ---- state.json ----
d = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
out.append('=== STATE ===')
for k in sorted(d.keys()):
    if k == 'log':
        continue
    out.append('FIELD %s = %s' % (k, str(d[k])[:260]))
logs = d.get('log', [])
out.append('log_len=%d' % len(logs))
for line in logs[-4:]:
    out.append('--- LOG: %s' % line[:420])
    out.append('')

wm = d.get('decisions_watermark', {})
wm_dnums = set(wm.get('dnums', []) if isinstance(wm, dict) else [])

# ---- group ledger scan ----
LGR = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
try:
    llines = io.open(LGR, encoding='utf-8').read().splitlines()
    out.append('=== LEDGER ===')
    out.append('total_lines=%d' % len(llines))
    for pat in ('@BigStream', '@七线全司', '@全司', '@六司', '@八线'):
        hits = [l for l in llines if pat in l]
        out.append('pat=%s count=%d' % (pat, len(hits)))
        for h in hits[-3:]:
            out.append('  LG: %s' % h[:200])
except Exception as e:
    out.append('LEDGER ERR %s' % e)

# ---- decisions.md watermark diff ----
DEC = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
try:
    dtxt = io.open(DEC, encoding='utf-8').read()
    dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dtxt)))
    new_d = [x for x in dnums if x not in wm_dnums]
    out.append('=== DECISIONS ===')
    out.append('file_dnums=%d wm_dnums=%d new=%s' % (len(dnums), len(wm_dnums), new_d[:20]))
    # top of file (dispatch board)
    dlines = dtxt.splitlines()
    out.append('-- decisions.md head 25 --')
    for l in dlines[:25]:
        if l.strip():
            out.append('D: %s' % l[:200])
except Exception as e:
    out.append('DEC ERR %s' % e)

# ---- orders latest ----
out.append('=== ORDERS ===')
od = os.path.join(ROOT, 'orders')
files = sorted(glob.glob(od + os.sep + '*'), key=os.path.getmtime)
for f in files[-4:]:
    out.append('  %s  mtime=%s' % (os.path.basename(f), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(f)))))

# ---- git ----
out.append('=== GIT ===')
g = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
out.append('status:')
out.append(g.stdout[:1500] or '(clean)')
g2 = subprocess.run(['git', 'log', '--oneline', '-4'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
out.append('log:')
out.append(g2.stdout)
lock = os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))
out.append('index.lock=%s' % lock)

# ---- backlog top undone ----
out.append('=== BACKLOG TOP UNDONE ===')
b = io.open(os.path.join(ROOT, 'src', 'os', 'backlog.md'), encoding='utf-8').read().splitlines()
count = 0
for l in b:
    m = re.match(r'^(\d+)\.\s', l)
    if m and '[done' not in l:
        out.append('UNDONE #%s: %s' % (m.group(1), l[:300]))
        count += 1
        if count >= 4:
            break

# ---- routine checks ----
out.append('=== ROUTINE ===')
db = os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-03.md')
out.append('daily_1003_exists=%s' % os.path.exists(db))
aud = glob.glob(os.path.join(ROOT, 'docs', 'audits', '*W40*'))
out.append('audit_W40=%s' % [os.path.basename(x) for x in aud])
gb = os.path.join(ROOT, 'docs', 'global-benchmarks.md')
if os.path.exists(gb):
    t = io.open(gb, encoding='utf-8').read()
    dates = re.findall(r'2026-\d{2}-\d{2}', t)
    out.append('gb_first_dates=%s (today=2026-10-03)' % dates[:4])
se = os.path.join(ROOT, 'docs', 'status-export.json')
if os.path.exists(se):
    sd = json.load(open(se, encoding='utf-8'))
    out.append('export_ts=%s' % sd.get('export_ts'))

# ---- self-improvement queue top ----
q = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
if os.path.exists(q):
    qt = io.open(q, encoding='utf-8').read().splitlines()
    out.append('=== QUEUE (first 18 non-empty) ===')
    n = 0
    for l in qt:
        if l.strip():
            out.append('Q: %s' % l[:180])
            n += 1
            if n >= 18:
                break

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
print('OK lines=%d' % len(out))
