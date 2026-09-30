# -*- coding: utf-8 -*-
# R747 context extraction (UTF-8 safe read; PS console GBK mojibake workaround)
import io, re

out = []

# (a) finished.md F-073 block (template for F-074)
fin = io.open('output/finished.md', encoding='utf-8').read().splitlines()
idx = [i for i, l in enumerate(fin) if l.startswith('## F-073')]
if idx:
    start = idx[0]
    nxt = [i for i, l in enumerate(fin) if i > start and l.startswith('## F-')]
    end = nxt[0] if nxt else min(start + 60, len(fin))
    out.append('=== FIN F-073 BLOCK (%d lines) ===' % (end - start))
    out.extend(fin[start:end])
else:
    out.append('=== FIN F-073 NOT FOUND; headers with F-07: ===')
    out.extend([l for l in fin if l.startswith('## F-07')][:6])
    # fallback: last 30 lines
    out.extend(fin[-30:])

# (b) renders README lc-018 row (upgraded chengpin format template)
rr = io.open('output/renders/README.md', encoding='utf-8').read().splitlines()
out.append('=== RENDERS lc-018 ROW ===')
for l in rr:
    if 'lc-018' in l:
        out.append(l)
out.append('=== RENDERS tail 3 lines ===')
out.extend([x[:400] for x in rr[-3:]])

# (c) release-schedule tail (v3.0 section)
rs = io.open('docs/release-schedule-v1.md', encoding='utf-8').read().splitlines()
out.append('=== RELEASE-SCHEDULE last 14 lines (of %d) ===' % len(rs))
out.extend([x[:500] for x in rs[-14:]])

# (d) queue E16/E20 tail + burn rows
q = io.open('docs/self-improvement-queue.md', encoding='utf-8').read().splitlines()
out.append('=== QUEUE tail 10 lines (of %d) ===' % len(q))
out.extend([x[:400] for x in q[-10:]])

# (e) station-reviews last row (format check)
sr = io.open('docs/reviews/station-reviews.md', encoding='utf-8').read().splitlines()
out.append('=== SR last 2 rows (of %d lines) ===' % len(sr))
out.extend([x[:300] for x in sr[-2:]])

io.open('.c3-tmp/r747_ctx.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK lines=%d' % len(out))
