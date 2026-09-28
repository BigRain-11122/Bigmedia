# -*- coding: utf-8 -*-
import io
p = r'data\storylines\audio\README.md'
with io.open(p, encoding='utf-8-sig') as f:
    t = f.read()
tail = t.splitlines()[-1]
with io.open(r'.c3-tmp\r637_readme_tail.txt', 'w', encoding='utf-8') as f:
    f.write('chars=%d\n' % len(t))
    f.write('has_bom=%s\n' % (t.startswith('\ufeff')))
    f.write('tail=%s\n' % tail[:80])
    f.write('v4_rows=%d\n' % t.count('SC-001-01-v4'))
print('OK chars=%d v4=%d bom=%s' % (len(t), t.count('SC-001-01-v4'), t.startswith('\ufeff')))
