# -*- coding: utf-8 -*-
import io, re
t = io.open('src/os/state.json', encoding='utf-8').read()
m = re.search(r'R1329: declared-idle[^\"]{0,80}', t)
out = m.group(0) if m else 'NOT FOUND'
io.open('.c3-tmp/r1329_verify.txt', 'w', encoding='utf-8').write(out)
print('OK len=%d' % len(out))
