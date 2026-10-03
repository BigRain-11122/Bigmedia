# -*- coding: utf-8 -*-
import io, re
out = []
def clean(s):
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\ufffd]', '?', s)
b = clean(io.open(r'.c3-tmp/r1138_board.txt', encoding='utf-8', errors='replace').read())
r = clean(io.open(r'.c3-tmp/r1138_rd.txt', encoding='utf-8', errors='replace').read())
l = clean(io.open(r'.c3-tmp/r1138_loop.txt', encoding='utf-8', errors='replace').read())
out.append('BOARD_FAIL_count=%d' % b.count('FAIL'))
out.append('BOARD_tail:')
out.extend(b.splitlines()[-6:])
out.append('RD_BLOCKER_count=%d RD_FINDING_count=%d' % (r.count('BLOCKER'), r.count('FINDING')))
out.append('RD_tail:')
out.extend(r.splitlines()[-8:])
lf = [x for x in l.splitlines() if 'FAIL' in x]
lw = [x for x in l.splitlines() if 'WARN' in x]
out.append('LOOP_FAIL_lines=%d LOOP_WARN_lines=%d' % (len(lf), len(lw)))
out.append('LOOP_fail_rows:')
for x in lf[:6]:
    out.append('  ' + x[:180])
out.append('LOOP_tail:')
out.extend(l.splitlines()[-5:])
io.open(r'.c3-tmp/r1138_probes_summary.txt', 'w', encoding='ascii', errors='backslashreplace').write('\n'.join(out))
print('WROTE %d lines' % len(out))
