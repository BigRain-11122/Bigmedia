# -*- coding: utf-8 -*-
# R670 verify (per R618 number-expectation checklist law): state + export 12-point check, writes r670_verify.txt
import io, json

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = []
def chk(name, cond, detail=''):
    out.append('%s %s %s' % ('PASS' if cond else 'FAIL', name, detail))

st = json.load(io.open(ROOT + r'\src\os\state.json', encoding='utf-8'))
se = json.load(io.open(ROOT + r'\docs\status-export.json', encoding='utf-8'))

chk('tick670', st['tick'] == 670, str(st['tick']))
chk('production_open', st.get('production') == 'open', str(st.get('production')))
chk('ts_fresh_0935', st['ts'].startswith('2026-09-29 09:35'), st['ts'])
chk('task_R670_len60', st['task'].startswith('R670: ') and len(st['task']) == 60, 'len=%d head=%r' % (len(st['task']), st['task'][:12]))
chk('focus_R671', st['focus'].startswith('R671: '), st['focus'][:10])
chk('log_tail_R670', st['log'][-1].startswith('2026-09-29 09:35 R670: '), st['log'][-1][:24])
chk('log_prev_R669_addendum', st['log'][-2].startswith('2026-09-29 09:30 R669'), st['log'][-2][:24])
chk('log_count_693', len(st['log']) == 693, str(len(st['log'])))  # R669 verify read 691 pre-addendum; +1 addendum +1 R670 = 693

chk('export_ts_fresh', se['export_ts'].startswith('2026-09-29T09:35'), se['export_ts'])
chk('results_last_670', se['results'][-1][0] == '670', se['results'][-1][0])
chk('results_len_33', len(se['results']) == 33, str(len(se['results'])))
tick_el = None
for el in se['outs'][0]:
    if isinstance(el, str) and el.startswith('tick '):
        tick_el = el
        break
chk('os_row_tick670', tick_el is not None and tick_el.startswith('tick 670'), (tick_el or 'NONE')[:16])
chk('os_row_no_stale_extra', tick_el is None or len([e for e in se['outs'][0] if isinstance(e, str) and e.startswith('tick ')]) == 1, str(len(se['outs'][0])))

txt = io.open(ROOT + r'\src\os\state.json', encoding='utf-8').read()
chk('state_log_R670_line_in_json', 'R670: declared-idle' in txt, '')

io.open(ROOT + r'\.c3-tmp\r670_verify.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
fails = [l for l in out if l.startswith('FAIL')]
print('VERIFY_R670 %s (%d fail)' % ('ALL_PASS' if not fails else 'HAS_FAIL', len(fails)))
