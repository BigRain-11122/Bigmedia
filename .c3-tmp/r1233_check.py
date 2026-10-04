# -*- coding: utf-8 -*-
# r1233 fresh probe run (five-checks + three probes un-skipped; declared-idle candidate, window 4/6
# same window as R1230/R1231/R1232 which inherited fresh supply chain from R1229 12:03). Per same-window no-rescan law,
# supply-gate facts inherited from R1229~R1232 fresh chain (~10 min gap, zero new facts expected).
# Canonical \d{2} decision-number regex (D-20260930-18 no-row-count law).
import json, os, re, subprocess, glob, io, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

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
w('LEDGER @LINES: %d (baseline 42; mtime %s)' % (cnt, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(ledger)))))
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

# waiting-object light gate facts (gate-open detection only, no heavy rescan)
w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-04.md')) else 'MISSING'))
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-05.md')) else 'MISSING'))
w('CENSUS_ANCHOR_C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
w('W40_AUDIT: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'docs','audits','2026-W40-self-audit.md')) else 'MISSING'))

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

io.open(os.path.join(ROOT,'.c3-tmp','r1233_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
