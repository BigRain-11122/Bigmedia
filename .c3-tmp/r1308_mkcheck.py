# -*- coding: utf-8 -*-
import io
src = io.open(r'.c3-tmp\r1306_check.py', encoding='utf-8').read()
src = src.replace(
    "r1297 fresh probe run (window 2/6 same-window continuation; ledger baseline 43 post-R1247; dnums baseline 137 post-R1229)",
    "r1308 fresh probe run (dnums baseline 142 post-R1300; BS rows baseline 47 post-R1300; ledger baseline 43 post-R1247)")
old_out = "'r1306_check.txt'"
new_out = "'r1308_check.txt'"
assert old_out in src, 'output filename anchor missing'
src = src.replace(old_out, new_out)
io.open(r'.c3-tmp\r1308_check.py', 'w', encoding='utf-8').write(src)
print('r1308_check.py written')
