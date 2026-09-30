# -*- coding: utf-8 -*-
# R673 close verify: authoritative re-read of state.json + status-export.json
import io, json, re, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
ST = ROOT + r'\src\os\state.json'
SE = ROOT + r'\docs\status-export.json'

st = json.load(io.open(ST, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
se = json.load(io.open(SE, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

checks = []
def ck(name, cond, detail=''):
    checks.append((name, bool(cond), detail))

ck('tick==673', st['tick'] == 673, 'tick=%s' % st['tick'])
ck('production==open', st.get('production') == 'open', st.get('production'))
ck('log_count==697', len(st['log']) == 697, 'logN=%d' % len(st['log']))
last = st['log'][-1]
ck('log[-1] is R673', ('R673:' in last) and last.startswith('2026-09-29 '), last[:30])
ck('log[-2] is R672', 'R672:' in st['log'][-2], st['log'][-2][:20])
ck('ts ascii seconds', bool(re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', st['ts'])), st['ts'])
ck('task_len==60', len(st['task']) == 60, 'len=%d' % len(st['task']))
ck('task_head R673', st['task'].startswith('R673:'), st['task'][:12])
ck('focus_head R674', st['focus'].startswith('R674:'), st['focus'][:12])
ck('focus batch-commit note', ('6/6' in st['focus']) and ('batch commit R669-R674' in st['focus']), '')
ck('export_ts fresh', str(se.get('export_ts', '')).startswith('2026-09-29T10:'), se.get('export_ts'))
ck('results[-1]==673', se['results'][-1][0] == '673', se['results'][-1][0])
osrow = se['outs'][0]
tickrow = [el for el in osrow if isinstance(el, str) and el.startswith('tick ')]
ck('os_row tick 673', len(tickrow) == 1 and tickrow[0].startswith('tick 673'), tickrow[0][:12] if tickrow else 'NONE')

fails = [c for c in checks if not c[1]]
for name, ok, detail in checks:
    print(('PASS ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))
print('SUMMARY: %d/%d PASS' % (len(checks) - len(fails), len(checks)))
raise SystemExit(1 if fails else 0)
