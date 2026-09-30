# -*- coding: utf-8 -*-
import json, io, datetime

NOW = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
s = json.load(io.open(r'src/os/state.json', encoding='utf-8'))
LOG = s['log'][-1]
# house format: strip date prefix only, keep "HH:MM R798: ..." then cut 60 chars
s['task'] = LOG[len('2026-10-01 ')][:60]
s['ts'] = NOW
json.dump(s, io.open(r'src/os/state.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('task ->', s['task'].encode('unicode_escape')[:90])
