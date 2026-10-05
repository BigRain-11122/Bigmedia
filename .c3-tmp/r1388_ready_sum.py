# -*- coding: utf-8 -*-
import io
t = io.open('.c3-tmp/r1388_probes.txt', encoding='utf-8').read()
i = t.find('== readiness')
j = t.find('== loop_health')
seg = t[i:j] if i >= 0 and j > i else t[i:]
lines = seg.split('\n')
tail = [l for l in lines if ('blocking' in l or 'findings' in l or 'FAIL' in l or 'blocker' in l.lower() or 'summary' in l.lower() or 'checks' in l)]
io.open('.c3-tmp/r1388_ready_sum.txt', 'w', encoding='utf-8').write('\n'.join(tail[:30]) + '\n===TAIL===\n' + seg[-1200:])
print('ok')
