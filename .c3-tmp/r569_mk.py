# -*- coding: utf-8 -*-
# mk: r568_all.py -> r569_all.py (rename law; ASCII only)
import io
src = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r568_all.py'
dst = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r569_all.py'
s = io.open(src, encoding='utf-8').read()
s = s.replace('R568', 'R569').replace('r568', 'r569')
io.open(dst, 'w', encoding='utf-8').write(s)
print('r569_all.py written')
