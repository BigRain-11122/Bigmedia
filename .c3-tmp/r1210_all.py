# -*- coding: utf-8 -*-
# r1210 fresh probe run (five-checks + three probes un-skipped; new declared-idle window position 1/6).
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
w('LEDGER @LINES: %d (mtime %s)' % (cnt, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(ledger)))))
w('LEDGER_LAST_HIT: %s' % last_hit)

dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dtxt = io.open(dec, encoding='utf-8', errors='replace').read()
dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', dtxt))
w('DECISIONS mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(dec))))
state = json.load(io.open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark',{}).get('dnums',[]))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))
w('DECISIONS_BS_ROWS: %d' % len([l for l in dtxt.splitlines() if 'BigStream' in l]))
w('STATE tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('PRODUCTION: %s' % state.get('production'))

# waiting-object light facts (no-rescan law holds for supply faces)
w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-04.md')) else 'MISSING'))
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-05.md')) else 'MISSING'))
nov = sorted(glob.glob(os.path.join(ROOT,'data','storylines','novel','SC-001-*-v*.md')))
w('NOVEL_LATEST: %s (mtime %s)' % (os.path.basename(nov[-1]) if nov else 'none', time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(nov[-1]))) if nov else '-'))
w('CENSUS_ANCHOR_C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
w('W40_AUDIT: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'docs','audits','2026-W40-self-audit.md')) else 'MISSING'))

bl = io.open(os.path.join(ROOT,'src','os','backlog.md'), encoding='utf-8', errors='replace').read()
open_items = [line[:100] for line in bl.splitlines() if re.match(r'^\d+\.\s', line) and '[done' not in line and '[claimed' not in line]
w('BACKLOG_OPEN_ITEMS: %d' % len(open_items))
for it in open_items:
    w('  OPEN: '+it)

gb = os.path.join(ROOT,'docs','global-benchmarks.md')
gtxt = io.open(gb, encoding='utf-8', errors='replace').read()
sec4 = gtxt[gtxt.find('④'):] if '④' in gtxt else gtxt
dm = re.search(r'202[56]-\d{2}-\d{2}', sec4)
w('GLOBAL_BENCH first-date-in-sec4: %s' % (dm.group(0) if dm else 'NO_DATE'))

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

io.open(os.path.join(ROOT,'.c3-tmp','r1210_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
