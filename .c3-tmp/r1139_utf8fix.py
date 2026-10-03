# -*- coding: utf-8 -*-
import io
for name in ('r1139_board', 'r1139_rd', 'r1139_loop'):
    src = r'.c3-tmp\%s.txt' % name
    raw = io.open(src, 'rb').read()
    for enc in ('utf-16', 'utf-8-sig', 'utf-8'):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeError:
            txt = None
    if txt is None:
        txt = raw.decode('utf-8', errors='replace')
    io.open(src, 'w', encoding='utf-8', newline='').write(txt)
    print('%s -> utf-8, %d chars' % (name, len(txt)))
