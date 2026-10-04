# -*- coding: utf-8 -*-
# r1247: extract the 10-04 day-shift (15:07) patrol line, all BigStream mentions + the OSS name-call list segment
import io, re
txt = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
lines = txt.splitlines()
target = None
for l in lines:
    if '值守轮 2026-10-04（午班 15:07）' in l:
        target = l
        break
out = []
if target is None:
    out.append('LINE NOT FOUND')
else:
    out.append('LINE_LEN=%d' % len(target))
    # all BigStream mention contexts
    idxs = [m.start() for m in re.finditer('BigStream', target)]
    out.append('BIGSTREAM_MENTIONS=%d' % len(idxs))
    for i, ix in enumerate(idxs):
        out.append('--- mention %d (ctx %d-%d) ---' % (i + 1, max(0, ix - 120), min(len(target), ix + 220)))
        out.append(target[max(0, ix - 120):min(len(target), ix + 220)])
    # the dian-ming (name-call) segment: from ③点名 to end or 2000 chars
    m = re.search(r'③点名', target)
    if m:
        seg = target[m.start():m.start() + 2600]
        out.append('=== DIANMING SEGMENT (first 2600 chars) ===')
        out.append(seg)
    # waiting/decision segments
    for key in ['④', '⑤']:
        m2 = re.search(key + r'[^③①②]', target)
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1247_patrol_seg.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok len', len(target) if target else -1)
