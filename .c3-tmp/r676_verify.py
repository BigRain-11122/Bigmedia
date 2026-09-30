# -*- coding: utf-8 -*-
# R676 closeout verify rig
import io, json, subprocess, datetime, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
T = os.path.join(ROOT, '.c3-tmp')
OUT = os.path.join(T, 'r676_verify.txt')

st = json.load(io.open(ROOT + r'\src\os\state.json', encoding='utf-8'))
se = json.load(io.open(ROOT + r'\docs\status-export.json', encoding='utf-8'))

lines = []
def chk(name, cond, detail=''):
    lines.append(('PASS ' if cond else 'FAIL ') + name + (' | ' + detail if detail else ''))

log = st['log']
tail = log[-1] if log else ''
logN = len(log)

chk('tick676', st.get('tick') == 676, str(st.get('tick')))
chk('logN700', logN == 700, str(logN))
chk('log_tail_R676', tail.startswith('2026-09-29 10:3') and 'R676: declared-idle' in tail, tail[:40])
chk('log_tail_newwindow2of6', u'新窗 2/6=R675-R680' in tail, '')
chk('ts_refresh', st.get('ts') == '2026-09-29 10:35:02', str(st.get('ts')))
task = st.get('task') or ''
chk('task_len60_prefix', len(task) == 60 and task.startswith('R676: declared-idle'), 'len=%d' % len(task))
focus = st.get('focus') or ''
chk('focus_R677', focus.startswith('R677:'), focus[:20])
chk('focus_newwindow3of6', u'新窗 3/6=R675-R680' in focus, '')
chk('production_open', st.get('production') == 'open', str(st.get('production')))

chk('se_export_ts', se.get('export_ts') == '2026-09-29T10:35:02+08:00', str(se.get('export_ts')))
res = se.get('results') or []
chk('se_results_last_676', res and res[-1][0] == '676', str(res[-1][0]) if res else 'EMPTY')
chk('se_results_len_39', len(res) == 39, str(len(res)))
osrow = (se.get('outs') or [[]])[0]
tick_el = [el for el in osrow if isinstance(el, str) and el.startswith('tick ')]
chk('se_os_tick676', bool(tick_el) and tick_el[0].startswith(u'tick 676'), (tick_el[0][:12] if tick_el else 'NONE'))
chk('se_os_row_len2', len(osrow) == 2, str(len(osrow)))

r = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True)
gs = r.stdout.decode('utf-8', errors='replace')
mod = [l for l in gs.splitlines() if l.startswith(' M ') or l.startswith('M ')]
chk('wt_modified_set', sorted(l[3:] for l in mod) == ['data/storylines/codex/README.md', 'data/storylines/codex/city-humanities.md', 'docs/status-export.json', 'src/os/state.json'], ' | '.join(sorted(l[3:] for l in mod)))
chk('no_index_lock', not os.path.exists(ROOT + r'\.git\index.lock'), '')

r2 = subprocess.run(['git', 'diff', '--stat', '--', 'src/os/state.json', 'docs/status-export.json'], cwd=ROOT, capture_output=True)
ds = r2.stdout.decode('utf-8', errors='replace').strip()
lines.append('--- self-file diff stat (expect 2 files, export add-only minimal):')
lines.append(ds)

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
nfail = sum(1 for l in lines if l.startswith('FAIL '))
print('verify: %d checks, FAIL=%d -> %s' % (sum(1 for l in lines if l.startswith(('PASS ', 'FAIL '))), nfail, 'ALL_PASS' if nfail == 0 else 'HAS_FAIL'))
