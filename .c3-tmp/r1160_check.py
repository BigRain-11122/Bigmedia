# -*- coding: utf-8 -*-
import json, os, re, subprocess, glob, io, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(s)

# 1) git status + index.lock
try:
    st = subprocess.run(['git','status','--short'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
except Exception as e:
    st = 'ERR '+str(e)
w('GIT_STATUS_START'); w(st if st else '(clean)'); w('GIT_STATUS_END')
w('index.lock exists: %s' % os.path.exists(os.path.join(ROOT,'.git','index.lock')))

# 2) last commit
lg = subprocess.run(['git','log','-1','--format=%h %ad %s','--date=format:%m-%d %H:%M'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('LAST_COMMIT: '+lg)

# 3) orders/ latest
orders = glob.glob(os.path.join(ROOT,'orders','*.md'))
if orders:
    latest = max(orders, key=os.path.getmtime)
    w('ORDERS_TOP: %s (mtime %s)' % (os.path.basename(latest), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(latest)))))
else:
    w('ORDERS_TOP: none')

# 4) ledger strict @ lines count
ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
cnt = 0
if os.path.exists(ledger):
    txt = io.open(ledger, encoding='utf-8', errors='replace').read()
    for line in txt.splitlines():
        if pat.search(line): cnt += 1
    w('LEDGER @LINES: %d' % cnt)
else:
    w('LEDGER: MISSING')

# 5) decisions.md D/C regex set diff vs state watermark
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dnow = set()
if os.path.exists(dec):
    txt = io.open(dec, encoding='utf-8', errors='replace').read()
    dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', txt))
state = json.load(io.open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark',{}).get('dnums',[]))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))

# 6) full last 2 log lines of state
log = state.get('log',[])
w('LOG_R1159_FULL>> '+log[-1])
w('LOG_R1158_FULL>> '+log[-2])

# 7) backlog: first unfinished items
bl = io.open(os.path.join(ROOT,'src','os','backlog.md'), encoding='utf-8').read().splitlines()
unfinished = []
for ln in bl:
    m = re.match(r'^(\d+)\.\s', ln)
    if m and '[done' not in ln:
        unfinished.append((int(m.group(1)), ln[:170]))
    if len(unfinished) >= 14: break
w('BACKLOG_TOP_UNFINISHED:')
for n,t in unfinished: w('  #%d %s' % (n,t))

# 8) self-improvement queue head + last date
q = os.path.join(ROOT,'docs','self-improvement-queue.md')
if os.path.exists(q):
    qt = io.open(q, encoding='utf-8').read()
    lines = [l for l in qt.splitlines() if l.strip()]
    w('QUEUE_HEAD:')
    for l in lines[:12]: w('  Q| '+l[:150])
    dates = re.findall(r'2026-\d{2}-\d{2}', qt)
    w('QUEUE_LAST_DATE: %s' % (dates[-1] if dates else 'none'))
else:
    w('QUEUE: MISSING')

# 9) audits
for wk in ['2026-W39','2026-W40','2026-W41']:
    p = os.path.join(ROOT,'docs','audits','%s-self-audit.md'%wk)
    w('AUDIT %s: %s' % (wk, 'EXISTS' if os.path.exists(p) else 'MISSING'))

# 10) global-benchmarks dates
gb = os.path.join(ROOT,'docs','global-benchmarks.md')
if os.path.exists(gb):
    gt = io.open(gb, encoding='utf-8').read()
    all_dates = re.findall(r'2026-\d{2}-\d{2}', gt)
    w('GB_ALL_LAST_DATES: %s' % all_dates[-5:])
else:
    w('GB: MISSING')

# 11) daily briefs
for d in ['2026-10-02','2026-10-03','2026-10-04']:
    p = os.path.join(ROOT,'data','intel','daily','%s.md'%d)
    w('DAILY %s: %s' % (d, 'EXISTS' if os.path.exists(p) else 'MISSING'))

# 12) HQ-FEEDBACK today lines
hq = os.path.join(ROOT,'HQ-FEEDBACK.md')
if os.path.exists(hq):
    ht = io.open(hq, encoding='utf-8').read()
    tod = [l for l in ht.splitlines() if '2026-10-03' in l]
    w('HQ_1003_LINES: %d' % len(tod))
    for l in tod[-3:]: w('  HQ| '+l[:170])
else:
    w('HQ: MISSING')

io.open(os.path.join(ROOT,'.c3-tmp','r1160_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
