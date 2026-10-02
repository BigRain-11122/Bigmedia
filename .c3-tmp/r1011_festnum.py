# -*- coding: utf-8 -*-
import io, json, re, subprocess
out = subprocess.run(['git', 'show', 'HEAD:src/os/state.json'], stdout=subprocess.PIPE).stdout.decode('utf-8')
st = json.loads(out)
m = re.search(u'festival \u5c45\u6c11\u6876\u4f59 (\\d+) \u884c', st['focus'])
q = subprocess.run(['git', 'show', 'HEAD:docs/self-improvement-queue.md'], stdout=subprocess.PIPE).stdout.decode('utf-8')
rows = re.findall(u'E30 \u7eed\u4ef6\u4f4d\u7ef4\u6301 standby\uff08festival \u5c45\u6c11\u6876\u4f59 (\\d+) \u884c', q)
lines = q.strip().split('\n')
r1010 = [l for l in lines if 'R1010' in l and 'E30' in l]
io.open(r'.c3-tmp\r1011_festnum.txt', 'w', encoding='utf-8').write(
    'FOCUS-NUM: ' + (m.group(1) if m else 'NONE') + '\n' +
    'QUEUE-ROWS-NUMS: ' + repr(rows) + '\n' +
    'R1010-QUEUE-ROW-TAIL: ' + (r1010[-1][-400:] if r1010 else 'NONE') + '\n')
print('WROTE')
