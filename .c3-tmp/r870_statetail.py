# -*- coding: utf-8 -*-
import io
t = io.open('src/os/state.json', encoding='utf-8').read()
io.open('.c3-tmp/r870_statetail.txt', 'w', encoding='utf-8').write(repr(t[-320:]))
print('OK')
