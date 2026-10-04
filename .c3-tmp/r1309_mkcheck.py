# -*- coding: utf-8 -*-
# r1309 probe script generator: python io channel copy of r1308_check.py (encoding law R1244/R1288)
import io
src = io.open('.c3-tmp/r1308_check.py', encoding='utf-8').read()
out = src.replace('r1308', 'r1309')
io.open('.c3-tmp/r1309_check.py', 'w', encoding='utf-8', newline='\n').write(out)
print('written r1309_check.py bytes=', len(out.encode('utf-8')))
