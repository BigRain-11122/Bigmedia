# -*- coding: utf-8 -*-
# R463 patch: fix task field to match established convention (strip "date time R463: " prefix, first 60 chars)
import json, io

SP = 'src/os/state.json'
with io.open(SP, encoding='utf-8') as f:
    st = json.load(f)
assert st['tick'] == 463, st['tick']
line = st['log'][-1]
assert ' R463: ' in line, line[:40]
body = line.split(' R463: ', 1)[1]
st['task'] = body[:60]
with io.open(SP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write('\n')
with io.open(SP, encoding='utf-8') as f:
    st2 = json.load(f)
out = io.open('.c3-tmp/r463_verify.txt', 'w', encoding='utf-8')
out.write('tick=%d\n' % st2['tick'])
out.write('ts=%s\n' % st2['ts'])
out.write('task=%s\n' % st2['task'])
out.write('task_len=%d\n' % len(st2['task']))
out.write('focus_head=%s\n' % st2['focus'][:80])
out.write('focus_tail=%s\n' % st2['focus'][-60:])
out.write('log_len=%d\n' % len(st2['log']))
out.write('last_log_head=%s\n' % st2['log'][-1][:100])
out.write('prev_log_head=%s\n' % st2['log'][-2][:60])
out.write('production=%s\n' % st2['production'])
out.close()
print('task=' + st2['task'])
print('OK')
