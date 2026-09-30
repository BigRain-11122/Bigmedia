# -*- coding: utf-8 -*-
import io
src = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read().splitlines()
hits = [l for l in src if ('C-20260929-01' in l) or ('20260929' in l)]
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r680_comt.txt', 'w', encoding='utf-8').write('\n'.join(hits))
print('rows=%d' % len(hits))
for h in hits:
    print(h[:1200])
    print('---8<---')
