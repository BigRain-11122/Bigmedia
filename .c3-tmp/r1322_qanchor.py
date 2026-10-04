# -*- coding: utf-8 -*-
import io
q = io.open(r'docs\self-improvement-queue.md', encoding='utf-8').read()
lines = q.splitlines()
# find lines containing R1321
hits = [i for i, l in enumerate(lines) if 'R1321' in l]
out = []
for i in hits:
    out.append('LINE %d (len=%d):' % (i, len(lines[i])))
    out.append(lines[i])
    if i + 1 < len(lines):
        out.append('NEXT %d: %s' % (i + 1, lines[i + 1][:120]))
io.open(r'.c3-tmp\r1322_qanchor.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('hits', hits)
