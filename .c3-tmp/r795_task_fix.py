# -*- coding: utf-8 -*-
# R795 task-field fix: strip timestamp prefix per machine-readout law
import io, re, json

P = 'src/os/state.json'
t = io.open(P, encoding='utf-8', newline='').read()
logline = io.open('.c3-tmp/r795_logline.txt', encoding='utf-8').read().strip()
task = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{1,2}x R795: ', '', logline)[:60]

i = t.rindex('"task": "')
j = t.index('"', i + len('"task": "'))
t2 = t[:i] + '"task": ' + json.dumps(task, ensure_ascii=False) + t[j + 1:]
json.loads(t2)
io.open(P, 'w', encoding='utf-8', newline='').write(t2)
print('TASK-FIX-OK len=%d' % len(task))
print(task.encode('unicode_escape')[:120])
