# -*- coding: utf-8 -*-
import io, json
j = json.load(io.open('src/os/state.json', 'r', encoding='utf-8'))
print('tick=', j['tick'])
print('ts=', j['ts'])
print('focus_head=', ascii(j['focus'][:20]))
print('log_last_head=', ascii(j['log'][-1][:70]))
print('log_last_tail=', ascii(j['log'][-1][-30:]))
print('task=', ascii(j['task']))
print('log_len=', len(j['log']))
