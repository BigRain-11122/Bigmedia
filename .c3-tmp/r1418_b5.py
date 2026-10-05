# -*- coding: utf-8 -*-
import json, io, re
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
st = json.load(open(ROOT + r'\src\os\state.json', encoding='utf-8'))
log = st.get('log', [])
o = io.open(ROOT + r'\.c3-tmp\r1418_b5.txt', 'w', encoding='utf-8')
for rn in ['R1357', 'R1358', 'R1362', 'R1363', 'R1389']:
    hits = [l for l in log if re.search(r'\b' + rn + r': ', l)]
    for h in hits[-1:]:
        o.write('==== ' + rn + ' ====\n' + h + '\n\n')
o.close()
print('ok')
