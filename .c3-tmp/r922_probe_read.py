# -*- coding: utf-8 -*-
import io
for name in ('r922_loop.txt', 'r922_board.txt'):
    t = io.open(r'.c3-tmp' + '\\' + name, encoding='utf-16').read()
    lines = [l for l in t.splitlines() if l.strip()]
    print('== %s : %d lines ==' % (name, len(lines)))
    tail = 14 if 'loop' in name else 8
    print('\n'.join(lines[-tail:]).encode('ascii', 'replace').decode('ascii'))
