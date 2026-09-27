# -*- coding: utf-8 -*-
# R536 close pre-check: json round-trip fidelity test (state.json + status-export.json)
import json, io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
for p in [ROOT + r'\src\os\state.json', ROOT + r'\docs\status-export.json']:
    raw = io.open(p, encoding='utf-8').read()
    data = json.loads(raw)
    dumped = json.dumps(data, ensure_ascii=False, indent=1)
    stripped = raw.rstrip('\n')
    print(p.split('\\')[-1], 'roundtrip_equal=%s' % (dumped == stripped), 'raw_len=%d dumped_len=%d' % (len(stripped), len(dumped)), 'raw_ends_nl=%s' % raw.endswith('\n'))
    if dumped != stripped:
        # find first divergence
        n = min(len(dumped), len(stripped))
        i = next((k for k in range(n) if dumped[k] != stripped[k]), n)
        print('  first_diff_at=%d' % i)
        print('  raw  :', repr(stripped[max(0,i-40):i+40]))
        print('  dump :', repr(dumped[max(0,i-40):i+40]))
