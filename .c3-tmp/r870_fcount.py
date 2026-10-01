# -*- coding: utf-8 -*-
import io, re
t = io.open('output/finished.md', encoding='utf-8').read()
# registration append lines: "- 2026-09-26: F-042 登记（R380）：..." and block headers "## F-0XX ... （2026-09-25 R290 登记"
rows = []
for m in re.finditer(r'(?:^## F-(\d{3})[^\n]*?（(2026-\d{2}-\d{2})[ ）]|^- (2026-\d{2}-\d{2}): F-(\d{3}) 登记)', t, re.M):
    if m.group(1):
        rows.append((m.group(2), m.group(1)))
    else:
        rows.append((m.group(3), m.group(4)))
rows.sort()
n = len(rows)
out = ['registered total=%d, last=%s' % (n, rows[-1] if rows else '?')]
since = [(d, f) for d, f in rows if d >= '2026-09-29']
out.append('on/after 2026-09-29: %d' % len(since))
after13 = [(d, f) for d, f in rows if d >= '2026-09-29']
for d, f in after13:
    out.append('%s F-%s' % (d, f))
# also count 10-01 rows separately
r1001 = [x for x in rows if x[0] == '2026-10-01']
out.append('on 2026-10-01: %d' % len(r1001))
io.open('.c3-tmp/r870_fcount.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('total=%d since0929=%d on1001=%d' % (n, len(since), len(r1001)))
