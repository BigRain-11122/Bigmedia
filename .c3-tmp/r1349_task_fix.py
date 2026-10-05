# -*- coding: utf-8 -*-
# r1349 task-field fix: strip minute-approximation timestamp prefix ("2026-10-05 10:5x " style) per PT-20260925-02 law (task = log line minus ts prefix, first 60 chars)
import json, io, re

SP = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
st = json.load(io.open(SP, encoding='utf-8'))
line = st['log'][-1]
assert line.startswith('2026-10-05 10:5x R1349'), 'unexpected last log line'
fixed = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{1,2}x?\s*', '', line)
assert fixed.startswith('R1349:'), 'strip failed'
st['task'] = fixed[:60]
io.open(SP, 'w', encoding='utf-8', newline='\n').write(json.dumps(st, ensure_ascii=False, indent=2) + '\n')
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1349_task_fix.txt', 'w', encoding='utf-8').write('task=%s\nlen=%d\n' % (st['task'], len(st['task'])))
print('fixed')
