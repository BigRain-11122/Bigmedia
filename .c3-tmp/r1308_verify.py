# -*- coding: utf-8 -*-
import io, json
st = json.load(io.open('src/os/state.json', encoding='utf-8'))
out = []
out.append('tick=%s' % st['tick'])
out.append('ts=%s' % st['ts'])
out.append('task_len=%d task_ok_prefix=%s' % (len(st['task']), st['task'][:20]))
out.append('log_tail_len=%d' % len(st['log'][-1]))
out.append('log_tail_head=' + st['log'][-1][:80])
out.append('log_tail_tail=' + st['log'][-1][-80:])
out.append('production=%s' % st['production'])
io.open('.c3-tmp/r1308_verify.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('verify written')
