# -*- coding: utf-8 -*-
# R674 close verification (post-close, pre-commit)
import io, json, datetime, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
st = json.load(io.open(ROOT + r'\src\os\state.json', encoding='utf-8'))
se = json.load(io.open(ROOT + r'\docs\status-export.json', encoding='utf-8'))

checks = collections.OrderedDict()
checks['tick=674'] = st.get('tick') == 674
checks['logN=698'] = len(st['log']) == 698
checks['ts_fresh'] = st.get('ts', '') >= '2026-09-29 10:14:00'
checks['task_len<=60'] = len(st.get('task', '')) <= 60
checks['log_tail_R674'] = st['log'][-1].find('R674: declared-idle') > 0
checks['log_prev_R673'] = st['log'][-2].find('R673: declared-idle') > 0
checks['focus_R675'] = st.get('focus', '').startswith(u'R675:')
checks['production=open'] = st.get('production') == 'open'
checks['se_export_ts_fresh'] = se.get('export_ts', '') >= '2026-09-29T10:14:00'
checks['se_results_last=674'] = se['results'][-1][0] == '674'
osrow = se['outs'][0]
checks['se_os_tick674'] = any(isinstance(e, str) and e.startswith(u'tick 674') for e in osrow)
checks['se_os_row_len=2'] = len(osrow) == 2

ok = all(checks.values())
for k, v in checks.items():
    print('%s: %s' % ('PASS' if v else 'FAIL', k))
print('ALL_PASS' if ok else 'HAS_FAIL')
