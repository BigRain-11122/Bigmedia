# -*- coding: utf-8 -*-
# r1198 board verify: dispatch-board rows involving BigStream in group decisions.md -> UTF-8 file (GBK console trap avoided)
import io
t = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8', errors='replace').read()
i = t.find('派工通告板')
seg = t[i:i+6000] if i >= 0 else ''
rows = [l for l in seg.splitlines() if ('BigStream' in l or '七司' in l or '六司' in l) and l.strip()]
out = ['BOARD_SEG_FOUND=%s' % (i >= 0), 'BOARD_BS_ROWS=%d' % len(rows)]
for r in rows:
    out.append('  ' + r.strip()[:220])
# mtime evidence
import os, time
out.append('DECISIONS_MTIME=%s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'))))
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1198_board.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written', len(out), 'lines')
