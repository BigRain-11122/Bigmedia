# -*- coding: utf-8 -*-
# r1228 fresh probe run (five-checks + three probes un-skipped; declared-idle candidate, NEW window 1/6
# after R1227 batch close R1222-R1227). New-window legal fresh supply-gate content-addressing:
# #86 three-leg (pools.json leaf strings vs 1440, interchat rows vs 22, novel ch3+ v4 texts) +
# gate facts (CENSUS C-00030 anchor, DAILY 10-04/10-05, HQ ack, OSS w4 ledger). Prior-window
# adjudications (R1216 audio-lane, R1222 supply chain) not rescanned beyond this light content addressing.
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
w('DECISIONS_BS_ROWS: %d (baseline 44)' % bs_rows)
w('STATE tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('PRODUCTION: %s' % state.get('production'))

# waiting-object light gate facts (gate-open detection only)
w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-04.md')) else 'MISSING'))
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-05.md')) else 'MISSING'))
nov = sorted(glob.glob(os.path.join(ROOT,'data','storylines','novel','SC-001-*-v*.md')))
w('NOVEL_LATEST: %s (mtime %s)' % (os.path.basename(nov[-1]) if nov else 'none', time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(nov[-1]))) if nov else '-'))
w('CENSUS_ANCHOR_C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
w('W40_AUDIT: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'docs','audits','2026-W40-self-audit.md')) else 'MISSING'))
q = os.path.join(ROOT,'docs','self-improvement-queue.md')
w('QUEUE mtime %s' % (time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(q))) if os.path.exists(q) else 'MISSING'))
gb = os.path.join(ROOT,'docs','global-benchmarks.md')
w('GB mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(gb))))

# #86 three-leg supply-gate light content-addressing (new window legal fresh re-verify)
POOLS = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
pd = json.load(io.open(POOLS, encoding='utf-8'))
leaves = []
def walk(node):
    if isinstance(node, dict):
        for v in node.values(): walk(v)
    elif isinstance(node, list):
        for v in node: walk(v)
    elif isinstance(node, str):
        if node.strip(): leaves.append(node.strip())
    elif isinstance(node, (int, float)):
        leaves.append(str(node))
walk(pd)
w('POOLS_LEAF_STRINGS: %d (baseline 1440; mtime %s)' % (len(leaves), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(POOLS)))))
w('POOLS_GATE: %s' % ('FIRED (increment trigger per R893)' if len(leaves) != 1440 else 'QUIET 1440==1440 (no expansion)'))
inter = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\interchat-ledger.jsonl'
if os.path.exists(inter):
    n_inter = sum(1 for l in io.open(inter, encoding='utf-8', errors='replace') if l.strip())
    w('INTERCHAT_ROWS: %d (baseline 22; mtime %s)' % (n_inter, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(inter)))))
    w('INTERCHAT_GATE: %s' % ('FIRED (increment)' if n_inter != 22 else 'QUIET 22==22'))
else:
    w('INTERCHAT_ROWS: FILE MISSING')
ch3 = glob.glob(os.path.join(ROOT,'data','storylines','novel','SC-001-03-*-v4*.md')) + glob.glob(os.path.join(ROOT,'data','storylines','novel','SC-001-03-v4*.md'))
w('NOVEL_CH3_V4_TEXTS: %d (gate = ch3+ v4 texts absent -> supply-gated maintains)' % len(ch3))

hq = os.path.join(ROOT,'HQ-FEEDBACK.md')
hq_txt = io.open(hq, encoding='utf-8', errors='replace').read() if os.path.exists(hq) else ''
w('HQ_ACK_F-20261004-01: %s' % ('EXISTS' if 'F-20261004-01' in hq_txt else 'MISSING'))
oh = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20261002-bigstream.md'
w('OSS_W4_LEDGER_FILE: %s (window 4 opens 10-05 21:40)' % ('EXISTS' if os.path.exists(oh) else 'MISSING'))

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

io.open(os.path.join(ROOT,'.c3-tmp','r1228_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
