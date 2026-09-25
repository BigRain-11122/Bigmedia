# -*- coding: utf-8 -*-
"""R234 fragment grep: check whether R197 #14 DD wrapper (PID 58052) was ever read back, and #14 state."""
import json, io, re

d = json.load(io.open('src/os/state.json', encoding='utf-8'))
out = []
for i, e in enumerate(d['log']):
    s = e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)
    for kw in ('58052', 'wrapper', '#14'):
        hits = list(re.finditer(kw, s))
        if hits:
            out.append('--- log[%d] kw=%s hits=%d' % (i, kw, len(hits)))
            for m in hits[:2]:
                out.append('    ...%s...' % s[max(0, m.start() - 100):m.start() + 160].replace('\n', ' '))
io.open('.bs005-tmp/r234-frag-u8.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('fragments=%d' % len(out))
