# -*- coding: utf-8 -*-
# R867 declaration-round accounting: tick+1, log append, ts/task refresh (r866 lineage; ASCII-only logic)
import io, json, datetime

line = io.open('.c3-tmp/r867_log_line.txt', encoding='utf-8').read().strip()
assert line.startswith('2026-10-01 16:') and ' R867: ' in line, 'log line header check'
assert '"' not in line and '\\' not in line, 'json-unsafe chars in log line'
assert 'waiting: ' in line, 'waiting marker missing'

p = 'src/os/state.json'
s = io.open(p, encoding='utf-8').read()
nl = '\r\n' if '\r\n' in s else '\n'

# 1) tick 866 -> 867
assert s.count('"tick": 866,') == 1, 'tick anchor not unique'
s = s.replace('"tick": 866,', '"tick": 867,', 1)

# 2) log append + ts refresh (structural anchor: log-array close + old ts line)
anchor = '"' + nl + ' ],' + nl + ' "ts": "2026-10-01 15:54:03",'
assert s.count(anchor) == 1, 'log close anchor count=%d' % s.count(anchor)
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
repl = '",' + nl + '  "' + line + '"' + nl + ' ],' + nl + ' "ts": "' + ts + '",'
s = s.replace(anchor, repl, 1)

# 3) task refresh (last field; value has no embedded double quotes)
task = line.split(' R867: ', 1)[1][:60]
k = s.rfind('"task": "')
assert k != -1, 'task field missing'
v0 = k + len('"task": "')
k2 = s.find('"', v0)
assert k2 != -1, 'task closing quote missing'
rest = s[k2 + 1:]
assert rest.strip() == '}', 'unexpected tail after task: %r' % rest[:30]
new_tail = '"' + nl + '}' + (nl if rest.endswith(nl) else '')
s = s[:v0] + task + new_tail

# 4) validate JSON integrity before write
d = json.loads(s)
assert d['tick'] == 867, 'tick validate'
assert d['ts'] == ts, 'ts validate'
assert d['task'] == task, 'task validate'
assert d['log'][-1].startswith('2026-10-01 16:') and ' R867: ' in d['log'][-1], 'log append validate'
assert len(d['log']) >= 2 and ' R866: ' in d['log'][-2], 'log order validate'
assert d['log'][-1].split(' R867: ', 1)[0] >= d['log'][-2].split(' R866: ', 1)[0], 'log ts order'

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ACCOUNT-OK tick=867 log_entries=%d ts=%s task_len=%d' % (len(d['log']), ts, len(task)))
