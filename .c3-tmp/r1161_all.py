# -*- coding: utf-8 -*-
# R1161 fresh check = five checks + three probes. Output: r1161_check.txt
import json, os, re, subprocess, glob, io, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 1) git status + index.lock
st = subprocess.run(['git','status','--short'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('GIT_STATUS_START'); w(st if st else '(clean)'); w('GIT_STATUS_END')
w('index.lock exists: %s' % os.path.exists(os.path.join(ROOT,'.git','index.lock')))
lg = subprocess.run(['git','log','-1','--format=%h %ad %s','--date=format:%m-%d %H:%M'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('LAST_COMMIT: '+lg)

# 2) orders/ latest
orders = glob.glob(os.path.join(ROOT,'orders','*.md'))
if orders:
    latest = max(orders, key=os.path.getmtime)
    w('ORDERS_TOP: %s (mtime %s)' % (os.path.basename(latest), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(latest)))))
else:
    w('ORDERS_TOP: none')

# 3) ledger strict @ lines count + mtime
ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
cnt = 0
if os.path.exists(ledger):
    txt = io.open(ledger, encoding='utf-8', errors='replace').read()
    for line in txt.splitlines():
        if pat.search(line): cnt += 1
    w('LEDGER @LINES: %d (mtime %s)' % (cnt, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(ledger)))))
else:
    w('LEDGER: MISSING')

# 4) decisions.md D/C regex set diff vs state watermark
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dnow = set()
if os.path.exists(dec):
    txt = io.open(dec, encoding='utf-8', errors='replace').read()
    dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', txt))
    w('DECISIONS mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(dec))))
state = json.load(io.open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark',{}).get('dnums',[]))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))
# board rows mentioning BigStream in the dispatch board section
bs_rows = [l.strip() for l in txt.splitlines() if 'BigStream' in l]
w('DECISIONS_BS_ROWS: %d' % len(bs_rows))
for l in bs_rows[-3:]: w('  D| '+l[:180])

w('STATE tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('LOG_TAIL1>> '+state.get('log',[])[-1][:200])

# 5) supply gates fresh evidence
pools = os.path.join(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife','census')
# pools count via known ledger path (line-count proxy from state baseline) -> use file existence checks only
anchor = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'
w('CENSUS C-00030 anchor: %s' % ('present' if os.path.exists(anchor) else 'absent'))
db = os.path.join(ROOT,'data','intel','daily','2026-10-04.md')
w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(db) else 'MISSING'))
db5 = os.path.join(ROOT,'data','intel','daily','2026-10-05.md')
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(db5) else 'MISSING'))
for wk in ['2026-W40','2026-W41']:
    p = os.path.join(ROOT,'docs','audits','%s-self-audit.md'%wk)
    w('AUDIT %s: %s' % (wk, 'EXISTS' if os.path.exists(p) else 'MISSING'))

# export freshness
se = os.path.join(ROOT,'docs','status-export.json')
if os.path.exists(se):
    d = json.load(open(se, encoding='utf-8'))
    w('export_ts=%s' % d.get('export_ts'))

# three probes
def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or "") + (p.stderr or "")
    w('=== %s (rc=%d) ===' % (label, p.returncode))
    w(out.strip()[-1500:])

run('BOARD', ['python','src/board_check.py'])
run('READINESS', ['python','src/readiness.py'])
run('LOOP_HEALTH', ['python','src/os/loop_health.py'])

io.open(os.path.join(ROOT,'.c3-tmp','r1161_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
