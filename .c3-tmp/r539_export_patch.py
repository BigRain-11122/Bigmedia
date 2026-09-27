# -*- coding: utf-8 -*-
# R539 export patch: eng dept s reflects all three op reds (F3 derived-from-reality law)
import json, io, time

SE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json'
old = 'one in-case PS && ParserError at round start = R524/R536/R537/R538 known type, switched to ; with zero disk side-effect'
new = ('three in-case op reds all closed in-round (1: PS && ParserError switched to ; zero side-effect; '
       '2: PS > redirect on close-verify output = R532/R536 known type, zero data impact; '
       '3: tmp-verify pattern literal mismatch printed false-negative, ground truth independently verified find_pos=17 + disk read, '
       'R533 ascii-escape pattern law now applied)')

se = json.load(io.open(SE, encoding='utf-8'))
hit = False
for d in se['depts']:
    s = d.get('s')
    if isinstance(s, str) and 'R539' in s:
        assert old in s, 'old substring not found'
        d['s'] = s.replace(old, new)
        hit = True
        break
assert hit, 'eng dept R539 s not found'
se['export_ts'] = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
io.open(SE, 'w', encoding='utf-8').write(json.dumps(se, ensure_ascii=False, indent=1) + '\n')

se2 = json.load(io.open(SE, encoding='utf-8'))
ok = any(isinstance(d.get('s'), str) and 'three in-case op reds' in d['s'] for d in se2['depts'])
print('EXPORT_PATCH_OK patched=%s export_ts=%s' % (ok, se2['export_ts']))
