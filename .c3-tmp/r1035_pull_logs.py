# -*- coding: utf-8 -*-
import json, io, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
st = json.load(io.open(os.path.join(ROOT, 'src/os/state.json'), encoding='utf-8'))
logs = st.get('log', [])
out = io.open(os.path.join(ROOT, '.c3-tmp', 'r1035_r1034full.txt'), 'w', encoding='utf-8')
for ln in logs:
    if ln.startswith('2026-10-03 01:30 R1034') or ln.startswith('2026-10-03 00:52 R1032') or ln.startswith('2026-10-03 00:4x R1031'):
        out.write(ln + "\n\n====\n\n")
out.close()
print('ok')
