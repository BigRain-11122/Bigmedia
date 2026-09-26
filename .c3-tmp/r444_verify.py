# -*- coding: utf-8 -*-
# R444 verify: JSON integrity + heartbeat fields + export fields
import json, io

s = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json', encoding='utf-8'))
e = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json', encoding='utf-8'))
print('state_ok tick=%s ts=%s' % (s['tick'], s['ts']))
print('task=%s' % s['task'])
print('log_tail=%s' % s['log'][-1][:60])
print('export_ok ts=%s results0=%s' % (e['export_ts'], e['results'][0]))
print('eng_dept=%s' % [d['t'][:80] for d in e['depts'] if d['n'] == u'工程技术部'])
