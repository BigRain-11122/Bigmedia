# -*- coding: utf-8 -*-
# R674 five-check probe: window R669-R674 6/6 close candidate. ledger rowdiff + decisions + orders + supply gates + three probes
import subprocess, io, os, re, datetime, json, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GROUP = r'C:\Users\sjs20\Desktop\FluxGroup'
T = os.path.join(ROOT, '.c3-tmp')
LEDGER = os.path.join(GROUP, 'cph4', 'evolution-ledger.md')
DECISIONS = os.path.join(GROUP, 'docs', 'decisions.md')
BASELINE = os.path.join(T, 'r644_lednew5.txt')
OUT = os.path.join(T, 'r674_led.txt')

PATS = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8", "@media\u5168\u53f8", "@\u516b\u7ebf\u5168\u91cf"]

lines = io.open(LEDGER, encoding='utf-8').read().splitlines()
six = []
for i, line in enumerate(lines):
    hit5 = [p for p in PATS[:5] if p in line]
    if hit5 or PATS[5] in line:
        six.append('L%d\t%s' % (i + 1, line.strip()))
io.open(OUT, 'w', encoding='utf-8').write('\n'.join(six) + ('\n' if six else ''))

base = io.open(BASELINE, encoding='utf-8').read().splitlines() if os.path.exists(BASELINE) else []
cur, bset = set(six), set(base)
new, gone = sorted(cur - bset), sorted(bset - cur)

dcount = sum(1 for l in io.open(DECISIONS, encoding='utf-8').read().splitlines() if l.strip())

st = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
se = json.load(io.open(os.path.join(ROOT, 'docs', 'status-export.json'), encoding='utf-8'))

odir = os.path.join(ROOT, 'orders')
orders = sorted([f for f in os.listdir(odir) if f.endswith('.md')],
                key=lambda n: os.path.getmtime(os.path.join(odir, n)), reverse=True)

now = datetime.datetime.now()
oss_open = (now.hour, now.minute) >= (21, 40)
cross_day = now.strftime('%Y-%m-%d') > '2026-09-29'

se_results = se.get('results') or []
res = collections.OrderedDict()
res['now'] = now.strftime('%Y-%m-%d %H:%M:%S')
res['ledger_six'] = len(six)
res['baseline_lines'] = len(base)
res['ledger_new'] = len(new)
res['ledger_gone'] = len(gone)
res['decisions_nonempty'] = dcount
res['orders_count'] = len(orders)
res['orders_top'] = orders[0] if orders else 'NONE'
res['orders_top_mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(odir, orders[0]))).strftime('%Y-%m-%d %H:%M:%S') if orders else 'NONE'
res['oss_window2_open(2140)'] = oss_open
res['cross_day(0930)'] = cross_day
res['state_tick'] = st.get('tick')
res['state_ts'] = st.get('ts')
res['state_logN'] = len(st.get('log') or [])
res['production'] = st.get('production')
res['index_lock'] = os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))
res['se_export_ts'] = se.get('export_ts')
res['se_results_len'] = len(se_results)

# round.lock read-only (launcher-managed)
rl = os.path.join(ROOT, 'logs', 'iteration-loop', 'round.lock')
res['round_lock'] = io.open(rl, encoding='utf-8').read()[:80].replace('\n', ' | ') if os.path.exists(rl) else 'ABSENT'

# supply-gate anchor check: census/anchors C-00030 existence (canonical position, cross-registry read-only)
ADIR = os.path.join(GROUP, 'life', 'BigLife', 'census', 'anchors')
anchors = sorted([f for f in os.listdir(ADIR) if f.endswith('.md')]) if os.path.isdir(ADIR) else []
res['anchors_count'] = len(anchors)
res['anchors_tail'] = anchors[-1] if anchors else 'NONE'
res['anchor_c00030'] = os.path.exists(os.path.join(ADIR, 'C-00030.md'))

# supply-gate: ch3+ v4 source draft (bm-a line, novel SC-001-03/04/05)
NDIR = os.path.join(ROOT, 'data', 'storylines', 'novel')
ch3 = []
if os.path.isdir(NDIR):
    for f in sorted(os.listdir(NDIR)):
        if 'SC-001-03' in f or 'SC-001-04' in f or 'SC-001-05' in f:
            p = os.path.join(NDIR, f)
            ch3.append('%s mtime=%s' % (f, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S')))
res['novel_ch345_files'] = ' | '.join(ch3) if ch3 else 'NONE'

# bm-a codex batch state: worktree diff vs HEAD for the two shared files
def wtdiff(path):
    r = subprocess.run(['git', 'diff', '--stat', '--', path], cwd=ROOT, capture_output=True)
    return r.stdout.decode('utf-8', errors='replace').strip()
res['codex_readme_wtdiff'] = wtdiff('data/storylines/codex/README.md') or 'CLEAN'
res['codex_humanities_wtdiff'] = wtdiff('data/storylines/codex/city-humanities.md') or 'CLEAN'
for p in ['data/storylines/codex/README.md', 'data/storylines/codex/city-humanities.md']:
    full = os.path.join(ROOT, *p.split('/'))
    res['mtime_' + os.path.basename(p)] = datetime.datetime.fromtimestamp(os.path.getmtime(full)).strftime('%m-%d %H:%M:%S')

# HEAD commit id
r = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True)
res['head'] = r.stdout.decode('utf-8', errors='replace').strip()

# routine-file presence
res['daily_0929'] = os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-29.md'))
res['audit_w40'] = os.path.exists(os.path.join(ROOT, 'docs', 'audits', '2026-W40-self-audit.md'))
res['monthly_note'] = os.path.exists(os.path.join(ROOT, 'docs', 'research', 'R-20260928-03-monthly-stats-note.md'))

# queue top re-derive (R666 lesson: re-derive claimable set from source files)
QF = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
qhead = []
if os.path.exists(QF):
    qlines = [l for l in io.open(QF, encoding='utf-8').read().splitlines() if l.strip()]
    for l in qlines[:18]:
        qhead.append(l[:120])
io.open(os.path.join(T, 'r674_queue.txt'), 'w', encoding='utf-8').write('\n'.join(qhead))

def run(args, outfile):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    r = subprocess.run(['python', '-X', 'utf8'] + args, cwd=ROOT, capture_output=True, env=env)
    txt = r.stdout.decode('utf-8', errors='replace')
    io.open(outfile, 'w', encoding='utf-8').write(txt + '\n[rc]=' + str(r.returncode) + '\n[stderr]' + r.stderr.decode('utf-8', errors='replace')[:800] + '\n')
    return txt, r.returncode

board, rc1 = run(['src/board_check.py'], os.path.join(T, 'r674_board.txt'))
ready, rc2 = run(['src/readiness.py'], os.path.join(T, 'r674_readiness.txt'))
health, rc3 = run(['src/os/loop_health.py'], os.path.join(T, 'r674_health.txt'))
res['rc'] = 'board=%d readiness=%d health=%d' % (rc1, rc2, rc3)

dig = io.open(os.path.join(T, 'r674_digest.txt'), 'w', encoding='utf-8')
for k, v in res.items():
    dig.write('%s: %s\n' % (k, v))
for name, txt in [('BOARD', board), ('READINESS', ready), ('HEALTH', health)]:
    dig.write('\n===== %s lines FAIL/WARN/block/ERROR:\n' % name)
    for l in txt.splitlines():
        if re.search(r'FAIL|WARN|\u963b\u585e|block|ERROR|Error', l):
            dig.write('  ' + l[:170] + '\n')
    dig.write('  [tail 3]\n')
    for l in txt.splitlines()[-3:]:
        dig.write('  | ' + l[:170] + '\n')
for l in new:
    dig.write('NEW_LINE: ' + l[:160] + '\n')
for l in gone:
    dig.write('GONE_LINE: ' + l[:160] + '\n')
dig.close()
print('done')
