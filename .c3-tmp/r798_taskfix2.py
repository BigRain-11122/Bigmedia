# -*- coding: utf-8 -*-
import json, io, datetime

NOW = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
s = json.load(io.open(r'src/os/state.json', encoding='utf-8'))
LOG = s['log'][-1]
assert LOG.startswith('2026-10-01 '), LOG[:20]
s['task'] = LOG[11:][:60]
s['ts'] = NOW
json.dump(s, io.open(r'src/os/state.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
io.open(r'.c3-tmp\r798_verify2.txt', 'w', encoding='utf-8').write(
    'tick=%s\nts=%s\ntask=%s\nlogN=%d\n' % (s['tick'], s['ts'], s['task'], len(s['log'])))
print('ok')
