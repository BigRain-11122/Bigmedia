# -*- coding: utf-8 -*-
# R681 close verify (R655 lesson: verify after close, 13-point)
import io, json, collections
ST = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
SE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json'
ok = []
st = json.load(io.open(ST, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ok.append(('tick', st['tick'] == 681))
ok.append(('logN', len(st['log']) == 705))
ok.append(('log_tail_R681', 'R681' in st['log'][-1]))
ok.append(('task_len60', len(st['task']) == 60))
ok.append(('task_prefix', st['task'].startswith(u'R681:')))
ok.append(('ts_ascii', st['ts'] == st['ts'].encode('ascii', 'ignore').decode('ascii')))
ok.append(('focus_R682', st['focus'].startswith(u'R682:')))
ok.append(('production_open', st['production'] == 'open'))
se = json.load(io.open(SE, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
import re
ok.append(('export_ts_fresh', bool(re.match(r'2026-09-29T12:1', se['export_ts']))))
ok.append(('results_tail_681', se['results'][-1][0] == '681'))
osrow = se['outs'][0]
tickline = [el for el in osrow if isinstance(el, str) and el.startswith('tick ')]
ok.append(('os_row_tick681', bool(tickline and 'tick 681' in tickline[0])))
ok.append(('os_row_len2', len(osrow) == 2))
for name, passed in ok:
    print('%s %s' % ('PASS' if passed else 'FAIL', name))
print('ALL_PASS' if all(p for _, p in ok) else 'HAS_FAIL')
