# -*- coding: utf-8 -*-
import io, json
d = json.load(io.open(r'src/os/state.json', encoding='utf-8'))
out = io.open(r'.c3-tmp/r812_verify.txt', 'w', encoding='utf-8', newline='\n')
out.write('tick=%d\n' % d['tick'])
out.write('ts=%s\n' % d['ts'])
out.write('task=%s\n' % d['task'])
out.write('focus_head=%s\n' % d['focus'][:100])
out.write('last_log_head=%s\n' % d['log'][-1][:150])
out.write('log_len=%d\n' % len(d['log']))
out.close()
print('VERIFY-WRITE-OK')
