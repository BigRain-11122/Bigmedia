# -*- coding: utf-8 -*-
"""R1026: poll E4 result for v56 (max ~100s), dump verdict head to .c3-tmp/r1026_e4.txt."""
import io, json, os, time

P = r'data\storylines\cards\MC-20261002-DAILY-v56-tmp\e4-result.json'
for attempt in range(20):
    if os.path.exists(P):
        r = json.load(io.open(P, encoding='utf-8'))
        v = r.get('verdict', '')
        if v and v != 'TIMEOUT-1500s':
            with io.open(r'.c3-tmp\r1026_e4.txt', 'w', encoding='utf-8') as f:
                f.write(r.get('ts', '') + '\nMODEL: ' + r.get('model', '') + '\n\n' + v[:2400])
            print('LANDED at attempt', attempt, '| ts', r.get('ts', ''))
            break
        else:
            print('present but', v[:30]); break
    time.sleep(5)
else:
    print('STILL_WAITING after 100s')
