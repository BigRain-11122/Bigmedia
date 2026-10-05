# -*- coding: utf-8>
# r1340 copy helper (R1302 script-file channel per PS5.1 inline -c quoting pitfall)
import io
s = io.open(r'.c3-tmp/r1339_check.py', encoding='utf-8').read()
s = s.replace("'r1339_check.txt'", "'r1340_check.txt'").replace('r1339 fresh probe run', 'r1340 fresh probe run')
io.open(r'.c3-tmp/r1340_check.py', 'w', encoding='utf-8').write(s)
print('copied -> r1340_check.py')
