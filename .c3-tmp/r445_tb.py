# -*- coding: utf-8 -*-
import io, re
t = io.open('.c3-tmp/r445_t1.txt', encoding='utf-8', errors='replace').read()
for m in re.finditer(r'^(FAIL|ERROR): (\w+) \((\w+)\)', t, re.M):
    print(m.group(0))
segs = t.split('Traceback')
print('---tracebacks---')
for s in segs[1:]:
    lines = [l for l in s.splitlines() if 'AssertionError' in l or 'assert' in l.lower() or 'Error' in l][:3]
    print('/'.join(lines))
