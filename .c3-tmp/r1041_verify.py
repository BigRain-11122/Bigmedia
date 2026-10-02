# -*- coding: utf-8 -*-
import json, io

st = json.load(io.open(r'src/os/state.json', encoding='utf-8'))
out = []
out.append('tick=%s' % st['tick'])
out.append('ts=%s' % st['ts'])
out.append('task=%s' % st['task'])
out.append('loglen=%s' % len(st['log']))
out.append('loglast_head=%s' % st['log'][-1][:100])
out.append('loglast_tail=%s' % st['log'][-1][-100:])
io.open(r'.c3-tmp/r1041_verify.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('verify written')
