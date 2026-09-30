# -*- coding: utf-8 -*-
# R666 five-check probe: reuse r665_probe.py logic + round value-add (ollama Phase1 常驻 API recheck / HEAD+codex mtimes / novel v4 glob)
import subprocess, io, os, re, datetime, json, collections, glob, urllib.request

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GROUP = r'C:\Users\sjs20\Desktop\FluxGroup'
T = os.path.join(ROOT, '.c3-tmp')
LEDGER = os.path.join(GROUP, 'cph4', 'evolution-ledger.md')
DECISIONS = os.path.join(GROUP, 'docs', 'decisions.md')
BASELINE = os.path.join(T, 'r644_lednew5.txt')
OUT = os.path.join(T, 'r666_led.txt')

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

se_results = se.get('results') or []
res = collections.OrderedDict()
res['now'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
res['ledger_six'] = len(six)
res['baseline_lines'] = len(base)
res['ledger_new'] = len(new)
res['ledger_gone'] = len(gone)
res['decisions_nonempty'] = dcount
res['orders_top'] = orders[0] if orders else 'NONE'
res['orders_top_mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(odir, orders[0]))).strftime('%Y-%m-%d %H:%M:%S') if orders else 'NONE'
res['state_tick'] = st.get('tick')
res['state_ts'] = st.get('ts')
res['production'] = st.get('production')
res['se_export_ts'] = se.get('export_ts')
res['se_results_len'] = len(se_results)

# round value-add 1: ollama Phase1 常驻 API recheck (P-20260925-07 obligation)
try:
    with urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=8) as r6:
        tags = json.loads(r6.read().decode('utf-8'))
    models = [m.get('name') for m in tags.get('models', [])]
    res['ollama_api'] = 'OK models=%d %s' % (len(models), ','.join(sorted(models)))
except Exception as ex:
    res['ollama_api'] = 'FAIL %s' % ex

# round value-add 2: HEAD + bm-a codex batch mtime freshness
g = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True)
res['head'] = g.stdout.strip()
for rel in ('data/storylines/codex/README.md', 'data/storylines/codex/city-humanities.md'):
    p = os.path.join(ROOT, rel.replace('/', os.sep))
    res['codex_mtime_' + os.path.basename(rel)] = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S') if os.path.exists(p) else 'MISSING'

# round value-add 3: novel v4 source glob (audio chain unlock probe)
v4 = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, 'data', 'storylines', 'novel', '*v4*'))]
res['novel_v4_files'] = v4 if v4 else 'NONE'

def run(args, outfile):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    r = subprocess.run(['python', '-X', 'utf8'] + args, cwd=ROOT, capture_output=True, env=env)
    txt = r.stdout.decode('utf-8', errors='replace')
    io.open(outfile, 'w', encoding='utf-8').write(txt + '\n[rc]=' + str(r.returncode) + '\n[stderr]' + r.stderr.decode('utf-8', errors='replace')[:800] + '\n')
    return txt, r.returncode

board, rc1 = run(['src/board_check.py'], os.path.join(T, 'r666_board.txt'))
ready, rc2 = run(['src/readiness.py'], os.path.join(T, 'r666_readiness.txt'))
health, rc3 = run(['src/os/loop_health.py'], os.path.join(T, 'r666_health.txt'))
res['rc'] = 'board=%d readiness=%d health=%d' % (rc1, rc2, rc3)

dig = io.open(os.path.join(T, 'r666_digest.txt'), 'w', encoding='utf-8')
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
