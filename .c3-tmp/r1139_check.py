# -*- coding: utf-8 -*-
"""R1139 declared-idle fresh five-check core (reused from R1131-R1138 chain).
ASCII script body per encoding law; evidence -> r1139_check.txt"""
import io, os, re, json, datetime

R = r'C:\Users\sjs20\Desktop\FluxGroup'
BS = os.path.join(R, 'media', 'BigStream')
GRP_DEC = os.path.join(R, 'docs', 'decisions.md')
GRP_ORD = os.path.join(R, 'docs', 'orders.md')
LEDGER = os.path.join(R, 'cph4', 'evolution-ledger.md')
ST = os.path.join(BS, 'src', 'os', 'state.json')
BLOG = os.path.join(R, 'media', 'BigStream', 'docs', 'status-export.json')
OUT = []

def w(s):
    OUT.append(s)

def mt(f):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m-%d %H:%M:%S')
    except OSError:
        return 'ABSENT'

# 1. decisions dnum content-addressed delta
st = json.load(io.open(ST, encoding='utf-8'))
wm = set(st.get('decisions_watermark', {}).get('dnums', []))
dec = io.open(GRP_DEC, encoding='utf-8').read()
dnums = set(re.findall(r'\b([DC]-\d{8}-\d{2})\b', dec))
new = sorted(dnums - wm)
w('decisions dnums: file=%d watermark=%d NEW=%s' % (len(dnums), len(wm), new if new else '[]'))

# 2. group file mtimes
for label, f in (('evolution-ledger', LEDGER), ('group decisions', GRP_DEC), ('group orders', GRP_ORD)):
    w('%s mtime: %s' % (label, mt(f)))

# local orders top
od = os.path.join(BS, 'orders')
try:
    latest = max(os.listdir(od), key=lambda n: os.path.getmtime(os.path.join(od, n)))
    w('orders top: %s mtime=%s' % (latest, mt(os.path.join(od, latest))))
except OSError:
    w('orders dir ABSENT')

# 3. index.lock
w('index.lock present: %s' % os.path.exists(os.path.join(BS, '.git', 'index.lock')))

# 4. production + tick
w('production=%s tick=%s' % (st.get('production'), st.get('tick')))

# 5. daily intel / W40 audit / GB gate
w('daily 2026-10-03 exists: %s' % os.path.exists(os.path.join(BS, 'data', 'intel', 'daily', '2026-10-03.md')))
w('daily 2026-10-04 exists (day-boundary item, expected absent): %s' % os.path.exists(os.path.join(BS, 'data', 'intel', 'daily', '2026-10-04.md')))
w('W40 self-audit exists: %s' % any('W40' in n for n in os.listdir(os.path.join(BS, 'docs', 'audits'))))

# 1b. ledger @target rows (frozen baseline 41) + dispatch board rows (baseline 8)
led = io.open(LEDGER, encoding='utf-8', errors='replace').read()
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线)')
hits = [ln for ln in led.splitlines() if pat.search(ln)]
w('ledger @target rows: %d (frozen baseline 41)' % len(hits))
for ln in hits[41:]:
    w('   NEW ROW: ' + ln.strip()[:200])
m = re.search(r'派工通告板(.*?)(?:\n#{1,3} |\Z)', dec, re.S)
board = m.group(1) if m else ''
brows = [ln.strip() for ln in board.splitlines() if re.search(r'BigStream|七司', ln)]
w('board BigStream/七司 rows: %d (baseline 8, collected set per R1031)' % len(brows))

# #86 three legs (BigLife cross-repo read-only; content-addressing per R1076)
LIFE = os.path.join(R, 'life', 'BigLife')
pj = os.path.join(LIFE, 'cognition', 'pools.json')
try:
    pjdata = json.load(io.open(pj, encoding='utf-8'))
    tot = 0
    for _ax, buckets in pjdata.get('axes', {}).items():
        if isinstance(buckets, dict):
            tot += sum(len(v) for v in buckets.values() if isinstance(v, list))
    for _bk, v in pjdata.get('sprite', {}).items():
        if isinstance(v, list):
            tot += len(v)
    w('#86 leg-a pools content count: %d (baseline 1440)' % tot)
except Exception as e:
    w('#86 leg-a pools read FAIL: %r' % e)
try:
    ti = io.open(os.path.join(LIFE, 'cognition', 'interchat-ledger.jsonl'), encoding='utf-8', errors='replace').read().strip()
    w('#86 leg-c interchat entries: %d (baseline 22)' % ((ti.count('\n') + 1) if ti else 0))
except Exception as e:
    w('#86 leg-c interchat read FAIL: %r' % e)
w('#86 CENSUS C-00030 present: %s (gate closed expected False)' % os.path.exists(os.path.join(LIFE, 'census', 'anchors', 'C-00030.md')))

# export age
try:
    ex = json.load(io.open(BLOG, encoding='utf-8'))
    ets = ex.get('export_ts', '')
    w('export_ts=%s' % ets)
except Exception as e:
    w('export read FAIL: %r' % e)

# backlog / queue mtimes
for label, f in (('backlog', os.path.join(BS, 'src', 'os', 'backlog.md')), ('queue', os.path.join(BS, 'docs', 'self-improvement-queue.md'))):
    w('%s mtime: %s' % (label, mt(f)))

w('check_ts=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
io.open(os.path.join(BS, '.c3-tmp', 'r1139_check.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
print('\n'.join(OUT))
