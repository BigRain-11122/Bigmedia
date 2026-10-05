# -*- coding: utf-8 -*-
# r1350 task-field fix: strip minute-approximation timestamp prefix ("2026-10-05 11:0x " style) per PT-20260925-02 law (r1349_task_fix same pattern)
import json, io, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = ROOT + r'\src\os\state.json'
st = json.load(io.open(SP, encoding='utf-8'))
line = st['log'][-1]
assert line.startswith('2026-10-05 11:0x R1350'), 'unexpected last log line'
fixed = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{1,2}x?\s*', '', line)
assert fixed.startswith('R1350:'), 'strip failed'
st['task'] = fixed[:60]
io.open(SP, 'w', encoding='utf-8', newline='\n').write(json.dumps(st, ensure_ascii=False, indent=2) + '\n')
out = 'tick=%s\nts=%s\ntask=%s\ntask_len=%d\nlog_len=%d\n' % (st['tick'], st['ts'], st['task'], len(st['task']), len(st['log']))
io.open(ROOT + r'\.c3-tmp\r1350_task_fix.txt', 'w', encoding='utf-8').write(out)
print('fixed')
