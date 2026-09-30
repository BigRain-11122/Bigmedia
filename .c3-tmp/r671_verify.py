# -*- coding: utf-8 -*-
# R671 close verify: parse-level authoritative recheck (R655/R670 verify pattern, must-read after run)
import io, json, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
ST = ROOT + r'\src\os\state.json'
SE = ROOT + r'\docs\status-export.json'
OUT = ROOT + r'\.c3-tmp\r671_verify.txt'

st = json.load(io.open(ST, encoding='utf-8'))
se = json.load(io.open(SE, encoding='utf-8'))
raw_st = io.open(ST, encoding='utf-8').read()
raw_se = io.open(SE, encoding='utf-8').read()

checks = []
def ck(name, cond, detail=''):
    checks.append('%s: %s' % ('PASS' if cond else 'FAIL', name + (' [' + detail + ']' if detail else '')))

ck('state_parse', isinstance(st, dict))
ck('tick=671', st.get('tick') == 671, str(st.get('tick')))
ck('log_count=695', len(st.get('log', [])) == 695, str(len(st.get('log', []))))
log_last = st['log'][-1] if st.get('log') else ''
log_prev = st['log'][-2] if len(st.get('log', [])) > 1 else ''
ck('log_tail=R671', 'R671' in log_last[:30], log_last[:24])
ck('log[-2]=R670_addendum', (u'R670 轮末补记' in log_prev), log_prev[:24])
ck('ts_fresh_ascii', bool(re_ts := st.get('ts')) and '2026-09-29 09:4' in st.get('ts', ''), str(st.get('ts')))
task = st.get('task', '')
ck('task_len=60_prefix_log', len(task) == 60 and log_last.endswith(task) is False and log_last[log_last.find(task[:24]):log_last.find(task[:24]) + 60] == task, 'len=%d' % len(task))
ck('focus=R672', st.get('focus', '').startswith('R672'), st.get('focus', '')[:10])
ck('production=open', st.get('production') == 'open')
ck('se_parse', isinstance(se, dict))
ck('se_export_ts_fresh', '2026-09-29T09:4' in se.get('export_ts', ''), str(se.get('export_ts')))
ck('se_results_len=34_tail671', len(se.get('results', [])) == 34 and se['results'][-1][0] == '671', 'len=%s tail=%s' % (len(se.get('results', [])), se['results'][-1][0] if se.get('results') else 'NONE'))
osrow = se['outs'][0] if se.get('outs') else []
ck('se_os_tick671', len(osrow) >= 2 and osrow[1].startswith('tick 671'), osrow[1][:12] if len(osrow) > 1 else 'NONE')
ck('se_indent1_format', raw_se.splitlines()[1].startswith(' "'), raw_se.splitlines()[1][:14])
ck('st_indent2_format', raw_st.splitlines()[1].startswith('  "'), raw_st.splitlines()[1][:14])

txt = '\n'.join(checks) + '\nALL_PASS=%s (%d/%d)' % (all(c.startswith('PASS') for c in checks), sum(c.startswith('PASS') for c in checks), len(checks))
io.open(OUT, 'w', encoding='utf-8').write(txt)
print(txt)
