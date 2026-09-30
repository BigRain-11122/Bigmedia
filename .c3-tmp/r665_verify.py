# -*- coding: utf-8 -*-
# R665 closeout verification: enumerated checks (R618 checklist law - all items explicit)
import io, json, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
st = json.load(io.open(ROOT + r'\src\os\state.json', encoding='utf-8'))
se = json.load(io.open(ROOT + r'\docs\status-export.json', encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

checks = []
def ck(name, cond, detail=''):
    checks.append((name, bool(cond), detail))

tail = st['log'][-1]
ck('TICK_EQ_665', st.get('tick') == 665, str(st.get('tick')))
ck('LOG_TAIL_R665', tail.startswith('2026-09-29 07:') and 'R665: declared-idle' in tail, tail[:60])
ck('LOG_R665_COUNT_EQ_1', sum(1 for l in st['log'] if l[:30].find('R665:') >= 0) == 1, 'exactly one R665 entry (idempotency)')
ck('TASK_R665_PREFIX', st.get('task', '').startswith('R665: declared-idle'), st.get('task', '')[:40])
ck('TASK_LEN_60', len(st.get('task', '')) == 60, str(len(st.get('task', ''))))
ck('TS_REFRESHED_0746', st.get('ts', '').startswith('2026-09-29 07:4'), st.get('ts', ''))
ck('FOCUS_R666', st.get('focus', '').startswith('R666:'), st.get('focus', '')[:24])
ck('SE_EXPORT_TS_REFRESHED', se.get('export_ts', '').startswith('2026-09-29T07:') and se.get('export_ts', '') > '2026-09-29T07:33:48', se.get('export_ts', ''))
ck('SE_RESULTS_665_APPENDED', se['results'][-1][0] == '665', se['results'][-1][0])
ck('SE_RESULTS_LEN', len(se['results']) == 28, str(len(se['results'])))
ck('SE_OS_ROW_TICK665', se['outs'][0][1].startswith('tick 665'), se['outs'][0][1][:30])
ck('SE_OS_ROW_R665_TEXT', 'R665 declared-idle' in se['outs'][0][1], '')
ck('PRODUCTION_OPEN', st.get('production') == 'open', st.get('production', ''))

fails = [c for c in checks if not c[1]]
with io.open(ROOT + r'\.c3-tmp\r665_verify.txt', 'w', encoding='utf-8') as f:
    for name, ok, detail in checks:
        f.write('%s: %s %s\n' % ('PASS' if ok else 'FAIL', name, detail))
    f.write('SUMMARY: %d/%d PASS\n' % (len(checks) - len(fails), len(checks)))
print('SUMMARY: %d/%d PASS' % (len(checks) - len(fails), len(checks)))
