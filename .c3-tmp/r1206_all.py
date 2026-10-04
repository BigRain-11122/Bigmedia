# -*- coding: utf-8 -*-
# r1206 fresh check = five checks + three probes + queue pool dump (claimability decision).
# Window: R1204 batch-close reset, this round = declaration window 2/6 unless claimable work found.
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
last_hit = ''
if os.path.exists(ledger):
    txt = io.open(ledger, encoding='utf-8', errors='replace').read()
    for line in txt.splitlines():
        if pat.search(line):
            cnt += 1
            last_hit = line[:160]
    w('LEDGER @LINES: %d (mtime %s)' % (cnt, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(ledger)))))
    w('LEDGER_LAST_HIT: %s' % last_hit)
else:
    w('LEDGER: MISSING')

# 4) decisions.md D/C regex set diff vs state watermark (content-addressed, D-20260930-18)
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dnow = set()
txt = ''
if os.path.exists(dec):
    txt = io.open(dec, encoding='utf-8', errors='replace').read()
    dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', txt))
    w('DECISIONS mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(dec))))
state = json.load(io.open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark',{}).get('dnums',[]))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))
bs_rows = [l.strip() for l in txt.splitlines() if 'BigStream' in l]
w('DECISIONS_BS_ROWS: %d' % len(bs_rows))
board = txt[:txt.find('## ')] if '## ' in txt else txt
w('BOARD_HEAD_BS_ROWS: %d' % len([l for l in board.splitlines() if 'BigStream' in l or '七司' in l or '六司' in l]))

w('STATE tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('LOG_TAIL1>> '+state.get('log',[])[-1][:200])

# 5) waiting-object light facts (same-window ban on supply gates; R1124 no-rescan note holds)
db = os.path.join(ROOT,'data','intel','daily','2026-10-04.md')
w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(db) else 'MISSING'))
db5 = os.path.join(ROOT,'data','intel','daily','2026-10-05.md')
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(db5) else 'MISSING'))

# 5b) value-add core: bm-a source drop check + CENSUS supply anchor + backlog open items
nov = sorted(glob.glob(os.path.join(ROOT,'data','storylines','novel','SC-001-*-v*.md')))
w('NOVEL_LATEST: %s' % (os.path.basename(nov[-1]) if nov else 'none'))
w('CENSUS_ANCHOR_C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
bl = io.open(os.path.join(ROOT,'src','os','backlog.md'), encoding='utf-8', errors='replace').read()
open_items = []
for line in bl.splitlines():
    m = re.match(r'^(\d+)\.\s', line)
    if m and '[done' not in line and '[claimed' not in line:
        open_items.append(line[:120])
w('BACKLOG_OPEN_ITEMS: %d' % len(open_items))
for it in open_items[:8]:
    w('  OPEN>> '+it)

# 5c) self-improvement queue: pool/section status dump (claimability path ②)
q = os.path.join(ROOT,'docs','self-improvement-queue.md')
if os.path.exists(q):
    qt = io.open(q, encoding='utf-8', errors='replace').read()
    w('QUEUE_LEN: %d chars' % len(qt))
    heads = [l.strip()[:100] for l in qt.splitlines() if l.strip().startswith('#') or l.strip().startswith('## ')]
    w('QUEUE_HEADS: %s' % ' | '.join(heads[:12]))
    w('QUEUE_TAIL_START >>>')
    w('\n'.join([l[:200] for l in qt.splitlines()[-40:]]))
    w('<<< QUEUE_TAIL_END')
else:
    w('QUEUE: MISSING')

# 6) global-benchmarks 7-day refresh check (refreshed 10-01 R795, gate resets 10-08)
gb = os.path.join(ROOT,'docs','global-benchmarks.md')
if os.path.exists(gb):
    gtxt = io.open(gb, encoding='utf-8', errors='replace').read()
    sec4 = gtxt[gtxt.find('④'):] if '④' in gtxt else gtxt
    dm = re.search(r'202[56]-\d{2}-\d{2}', sec4)
    w('GLOBAL_BENCH first-date-in-sec4: %s' % (dm.group(0) if dm else 'NO_DATE'))
else:
    w('GLOBAL_BENCH: MISSING')

# export freshness
se = os.path.join(ROOT,'docs','status-export.json')
if os.path.exists(se):
    d = json.load(open(se, encoding='utf-8'))
    w('export_ts=%s' % d.get('export_ts'))

# three probes (照跑不省)
def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or "") + (p.stderr or "")
    w('=== %s (rc=%d) ===' % (label, p.returncode))
    w(out.strip()[-1200:])

run('BOARD', ['python','src/board_check.py'])
run('READINESS', ['python','src/readiness.py'])
run('LOOP_HEALTH', ['python','src/os/loop_health.py'])

io.open(os.path.join(ROOT,'.c3-tmp','r1206_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
