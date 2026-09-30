# -*- coding: utf-8 -*-
# r678 five-check probe: ledger rowdiff + decisions + orders + supply gates + three probes + LC-002 supply
import subprocess, io, os, re, datetime, json, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GROUP = r'C:\Users\sjs20\Desktop\FluxGroup'
T = os.path.join(ROOT, '.c3-tmp')
LEDGER = os.path.join(GROUP, 'cph4', 'evolution-ledger.md')
DECISIONS = os.path.join(GROUP, 'docs', 'decisions.md')
BASELINE = os.path.join(T, 'r644_lednew5.txt')
OUT = os.path.join(T, 'r678_led.txt')

PATS = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8", "@media\u5168\u7ebf", "@\u516b\u7ebf\u5168\u91cf"]

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
res = collections.OrderedDict()
res['now'] = now.strftime('%Y-%m-%d %H:%M:%S')
res['ledger_six'] = len(six)
res['ledger_new'] = len(new)
res['ledger_gone'] = len(gone)
res['ledger_mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(LEDGER)).strftime('%Y-%m-%d %H:%M:%S')
res['decisions_nonempty'] = dcount
res['decisions_mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(DECISIONS)).strftime('%Y-%m-%d %H:%M:%S')
res['orders_count'] = len(orders)
res['orders_top'] = orders[0] if orders else 'NONE'
res['state_tick'] = st.get('tick')
res['state_ts'] = st.get('ts')
res['state_logN'] = len(st.get('log') or [])
res['production'] = st.get('production')
res['index_lock'] = os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))
res['se_export_ts'] = se.get('export_ts')
res['se_results_len'] = len(se.get('results') or [])

rl = os.path.join(ROOT, 'logs', 'iteration-loop', 'round.lock')
res['round_lock'] = io.open(rl, encoding='utf-8').read()[:80].replace('\n', ' | ') if os.path.exists(rl) else 'ABSENT'

# supply gates
ADIR = os.path.join(GROUP, 'life', 'BigLife', 'census', 'anchors')
anchors = sorted([f for f in os.listdir(ADIR) if f.endswith('.md')]) if os.path.isdir(ADIR) else []
res['anchors_count'] = len(anchors)
res['anchor_c00017'] = os.path.exists(os.path.join(ADIR, 'C-00017.md'))
res['anchor_c00030'] = os.path.exists(os.path.join(ADIR, 'C-00030.md'))

# LC-002 supply: F-027 card PNG + lc001/lc002 dirs
CARD8 = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v8')
res['card8_dir'] = os.path.isdir(CARD8)
if res['card8_dir']:
    files = sorted(os.listdir(CARD8))
    res['card8_files'] = ' | '.join(files)
res['lc001_dir'] = os.path.isdir(os.path.join(ROOT, 'data', 'sources', 'lc001'))
res['lc002_dir_exists'] = os.path.isdir(os.path.join(ROOT, 'data', 'sources', 'lc002'))
res['footage_census_v8'] = os.path.exists(os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v8-vertical.mp4'))
res['footage_census_v7'] = os.path.exists(os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v7-vertical.mp4'))

# codex batch (bm-a yield check)
def wtdiff(path):
    r = subprocess.run(['git', 'diff', '--stat', '--', path], cwd=ROOT, capture_output=True)
    return r.stdout.decode('utf-8', errors='replace').strip()
res['codex_readme_wtdiff'] = wtdiff('data/storylines/codex/README.md') or 'CLEAN'
res['codex_humanities_wtdiff'] = wtdiff('data/storylines/codex/city-humanities.md') or 'CLEAN'

r = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True)
res['head'] = r.stdout.decode('utf-8', errors='replace').strip()

# S1/E4/ASR in-flight check (python processes with s1/e4/asr wrappers)
ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                     "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],
                    capture_output=True)
try:
    plist = json.loads(ps.stdout.decode('utf-8', errors='replace')) if ps.stdout.strip() else []
    if isinstance(plist, dict): plist = [plist]
    infl = ['%s::%s' % (p.get('ProcessId'), (p.get('CommandLine') or '')[:110]) for p in plist]
    res['python_procs'] = len(plist)
    res['inflight_task'] = ' | '.join([x for x in infl if any(k in x for k in ('s1_call', 'e4_call', 'asr', 's1v15'))]) or 'NONE'
except Exception as e:
    res['python_procs'] = 'ERR:%s' % e

res['daily_0929'] = os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-29.md'))
res['audit_w40'] = os.path.exists(os.path.join(ROOT, 'docs', 'audits', '2026-W40-self-audit.md'))

def run(args, outfile):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    r = subprocess.run(['python', '-X', 'utf8'] + args, cwd=ROOT, capture_output=True, env=env)
    txt = r.stdout.decode('utf-8', errors='replace')
    io.open(outfile, 'w', encoding='utf-8').write(txt + '\n[rc]=' + str(r.returncode) + '\n[stderr]' + r.stderr.decode('utf-8', errors='replace')[:800] + '\n')
    return txt, r.returncode

board, rc1 = run(['src/board_check.py'], os.path.join(T, 'r678_board.txt'))
ready, rc2 = run(['src/readiness.py'], os.path.join(T, 'r678_readiness.txt'))
health, rc3 = run(['src/os/loop_health.py'], os.path.join(T, 'r678_health.txt'))
res['rc'] = 'board=%d readiness=%d health=%d' % (rc1, rc2, rc3)

dig = io.open(os.path.join(T, 'r678_digest.txt'), 'w', encoding='utf-8')
for k, v in res.items():
    dig.write('%s: %s\n' % (k, v))
for name, txt in [('BOARD', board), ('READINESS', ready), ('HEALTH', health)]:
    dig.write('\n===== %s FAIL/WARN lines:\n' % name)
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
