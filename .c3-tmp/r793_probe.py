# -*- coding: utf-8 -*-
import io, json
s = io.open('src/os/state.json', 'r', encoding='utf-8-sig', newline='').read()
j = json.loads(s)
print('log entries:', len(j['log']))
print('last entry starts:', repr(j['log'][-1][:40]))
print('FILE-END-160:', repr(s[-160:]))
