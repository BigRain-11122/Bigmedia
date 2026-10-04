# -*- coding: utf-8 -*-
# r1258 fresh probe run (five-checks + three probes un-skipped; declared-idle window 5/6 same chain as R1254-R1257; ledger baseline 43 post-R1247; dnums baseline 137 post-R1229)
# Adds: R1124 DAILY exhaustion adjudication excerpt + weekend-bucket supply facts (10-04 = Sunday = true weekend calendar match for DAILY lane date-context rule)
import json, os, re, subprocess, glob, io, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
w('weekday=%s' % datetime.datetime.now().strftime('%A'))

st = subprocess.run(['git','status','--short'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('GIT_STATUS_START'); w(st if st else '(clean)'); w('GIT_STATUS_END')
w('index.lock exists: %s' % os.path.exists(os.path.join(ROOT,'.git','index.lock')))
lg = subprocess.run(['git','log','-1','--format=%h %ad %s','--date=format:%m-%d %H:%M'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('LAST_COMMIT: '+lg)

orders = glob.glob(os.path.join(ROOT,'orders','*.md'))
latest = max(orders, key=os.path.getmtime)
w('ORDERS_TOP: %s (mtime %s)' % (os.path.basename(latest), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(latest)))))

ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
cnt = 0
last_hit = ''
txt = io.open(ledger, encoding='utf-8', errors='replace').read()
for line in txt.splitlines():
    if pat.search(line):
        cnt += 1
        last_hit = line[:160]
w('LEDGER @LINES: %d (baseline 43 post-R1247; mtime %s)' % (cnt, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(ledger)))))
w('LEDGER_LAST_HIT: %s' % last_hit)

dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dtxt = io.open(dec, encoding='utf-8', errors='replace').read()
dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', dtxt))
w('DECISIONS mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(dec))))
state = json.load(io.open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark',{}).get('dnums',[]))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))
bs_rows = sum(1 for l in dtxt.splitlines() if 'BigStream' in l)
w('DECISIONS_BS_ROWS: %d (baseline 46 post-R1229)' % bs_rows)
w('STATE tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('PRODUCTION: %s' % state.get('production'))

w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-04.md')) else 'MISSING'))
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-05.md')) else 'MISSING'))
w('CENSUS_ANCHOR_C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
w('GB_LAST_REFRESH: %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(os.path.join(ROOT,'docs','global-benchmarks.md')))))

# --- R1124 DAILY exhaustion adjudication excerpt (first 1500 chars of the log entry) ---
for entry in state.get('log', []):
    if 'R1124' in entry[:30]:
        w('=== R1124 LOG ENTRY (excerpt) ===')
        w(entry[:1500])
        break

# --- DAILY card lane: recent files ---
cards_dir = os.path.join(ROOT,'data','storylines','cards')
dfiles = sorted(glob.glob(os.path.join(cards_dir,'*DAILY*')), key=os.path.getmtime)
w('=== DAILY CARDS (last 8 by mtime) ===')
for f in dfiles[-8:]:
    w('%s  (%s)' % (os.path.basename(f), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(f)))))
w('DAILY_CARD_TOTAL: %d' % len(dfiles))

# --- weekend bucket supply facts: consumed weekend lines across DAILY/REACT fleet ---
POOLS = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
pd = json.load(io.open(POOLS, encoding='utf-8'))
axes = pd.get('axes', pd)
def get_bucket(axis, bucket):
    try:
        return axes[axis][bucket]
    except Exception:
        return None
wk = None
for axis in (axes if isinstance(axes, dict) else []):
    b = get_bucket(axis, 'weekend')
    if isinstance(b, list):
        wk = b
        break
w('POOLS weekend bucket found: %s len=%s' % (wk is not None, len(wk) if wk is not None else 'NA'))
if wk:
    w('WEEKEND_LINES_START'); [w('[%d] %s' % (i, s)) for i, s in enumerate(wk)]; w('WEEKEND_LINES_END')

# which weekend lines already consumed by fleet (cards dir scan)
wk_consumed = []
for f in dfiles:
    try:
        c = io.open(f, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    if wk:
        for i, s in enumerate(wk):
            if s in c:
                wk_consumed.append((os.path.basename(f), i, s[:40]))
react_files = sorted(glob.glob(os.path.join(cards_dir,'*REACT*')), key=os.path.getmtime)
for f in react_files:
    try:
        c = io.open(f, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    if wk:
        for i, s in enumerate(wk):
            if s in c:
                wk_consumed.append((os.path.basename(f), i, s[:40]))
w('WEEKEND_CONSUMED: %d' % len(wk_consumed))
for x in wk_consumed:
    w('  consumed: %s line%d %s' % x)

hq = os.path.join(ROOT,'HQ-FEEDBACK.md')
hq_txt = io.open(hq, encoding='utf-8', errors='replace').read() if os.path.exists(hq) else ''
w('HQ_ACK_F-20261004-01: %s' % ('EXISTS' if 'F-20261004-01' in hq_txt else 'MISSING'))

se = os.path.join(ROOT,'docs','status-export.json')
d = json.load(open(se, encoding='utf-8'))
w('export_ts=%s' % d.get('export_ts'))

def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or "") + (p.stderr or "")
    w('=== %s (rc=%d) ===' % (label, p.returncode))
    w(out.strip()[-1500:])

run('BOARD', ['python','src/board_check.py'])
run('READINESS', ['python','src/readiness.py'])
run('LOOP_HEALTH', ['python','src/os/loop_health.py'])

io.open(os.path.join(ROOT,'.c3-tmp','r1258_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
