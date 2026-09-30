# -*- coding: utf-8 -*-
# R675 post-close verify (ASCII-only output)
import io, json, os, re, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = []

st = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
se = json.load(io.open(os.path.join(ROOT, 'docs', 'status-export.json'), encoding='utf-8'))

def chk(name, cond, detail=''):
    out.append('%s %s%s' % ('PASS' if cond else 'FAIL', name, (' | ' + detail) if detail else ''))

chk('tick==675', st['tick'] == 675, str(st['tick']))
chk('logN==699', len(st['log']) == 699, str(len(st['log'])))
chk('ts fresh close format', bool(re.match(r'^2026-09-29 10:\d\d:\d\d$', st['ts'])), st['ts'])
chk('task len==60 R675 head', len(st['task']) == 60 and st['task'].startswith('R675'), 'len=%d' % len(st['task']))
chk('log[-1] R675 line', st['log'][-1].startswith('2026-09-29 10:') and 'R675' in st['log'][-1][:40], st['log'][-1][:24])
chk('log[-2] R674 line', 'R674' in st['log'][-2][:40], st['log'][-2][:24])
chk('focus R676 head', st.get('focus', '').startswith('R676'), st.get('focus', '')[:12])
chk('production open', st.get('production') == 'open')
chk('ts != stale', st['ts'] != '2026-09-29 10:14:26')

chk('export_ts fresh', se.get('export_ts', '').startswith('2026-09-29T10:'), se.get('export_ts', ''))
res = se.get('results') or []
chk('results_len==38', len(res) == 38, str(len(res)))
chk('results last==675', res[-1][0] == '675', res[-1][0] if res else 'EMPTY')
osrow = se['outs'][0]
tickrow = [el for el in osrow if isinstance(el, str) and el.startswith('tick ')]
chk('os row tick 675', bool(tickrow) and tickrow[0].startswith('tick 675'), tickrow[0][:12] if tickrow else 'NONE')

# loop_health post-close: account-lag must be resolved (done675==tick675), outages remain in-case
env = dict(os.environ); env['PYTHONIOENCODING'] = 'utf-8'
r = subprocess.run(['python', '-X', 'utf8', 'src/os/loop_health.py'], cwd=ROOT, capture_output=True, env=env)
txt = r.stdout.decode('utf-8', errors='replace')
io.open(os.path.join(ROOT, '.c3-tmp', 'r675_verify_health.txt'), 'w', encoding='utf-8').write(txt)
lag = [l for l in txt.splitlines() if 'account-lag' in l]
outages = [l for l in txt.splitlines() if 'heartbeat-outage' in l]
summary = [l for l in txt.splitlines() if 'loop health:' in l]
chk('account-lag resolved', len(lag) == 0, lag[0][:90] if lag else 'none')
chk('outage FAILs in-case x2', len(outages) == 2)
out.append('health summary: ' + (summary[-1][:80] if summary else 'NONE'))

io.open(os.path.join(ROOT, '.c3-tmp', 'r675_verify.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
