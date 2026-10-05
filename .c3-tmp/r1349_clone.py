# -*- coding: utf-8 -*-
# r1349 probe clone (write-side helper, not an evidence file)
import io
src = io.open(r'.c3-tmp/r1348_check.py', encoding='utf-8').read()
src = src.replace('r1348 fresh probe run (declared-idle window 2/6, same window as R1347)',
                  'r1349 fresh probe run (declared-idle window 3/6, same window as R1347/R1348)')
src = src.replace("'r1348_check.txt'", "'r1349_check.txt'")
io.open(r'.c3-tmp/r1349_check.py', 'w', encoding='utf-8').write(src)
print('cloned ok')
