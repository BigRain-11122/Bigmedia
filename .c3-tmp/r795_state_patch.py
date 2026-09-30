# -*- coding: utf-8 -*-
# R795 state.json tail patch: append log line, refresh ts/task (newline-agnostic)
import io, re, json, datetime

P = 'src/os/state.json'
t = io.open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
logline = io.open('.c3-tmp/r795_logline.txt', encoding='utf-8').read().strip()

tsi = t.rindex('"ts":')
close = t.rindex(']', 0, tsi)          # ']' of the log-array '],'
ls = t.rindex(nl, 0, close) + len(nl)  # start of the '],' line
prev = t[:ls].rstrip()
assert prev.endswith('"'), 'last log entry quote not found: %r' % prev[-30:]

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
task = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x R795: ', '', logline)[:60]

t2 = prev + ',' + nl + '    "' + logline + '"' + nl + t[ls:]
tail_old = t2[t2.rindex('"ts":'):]
t2 = t2[:t2.rindex('"ts":')] + '"ts": "%s",%s  "task": %s%s}' % (
    now, nl, json.dumps(task, ensure_ascii=False), nl)

json.loads(t2)  # validate
io.open(P, 'w', encoding='utf-8', newline='').write(t2)
print('PATCH-OK ts=%s task=%s' % (now, task))
