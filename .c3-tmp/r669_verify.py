import json, io
s = json.load(io.open('src/os/state.json', encoding='utf-8'))
print('STATE_OK tick=%d logN=%d' % (s['tick'], len(s['log'])))
print('ts=%s' % s['ts'])
print('lastIsAddendum=%s' % s['log'][-1].startswith('2026-09-29 09:30 R669'))
print('r669MainInPlace=%s' % any(l.startswith('2026-09-29 09:27 R669: declared-idle') for l in s['log']))
print('taskLen=%d taskR669=%s' % (len(s['task']), s['task'].startswith('R669: ')))
e = json.load(io.open('docs/status-export.json', encoding='utf-8'))
print('EXPORT_OK last=%s osRow=%s' % (e['results'][-1][0], e['outs'][0][1][:8]))
