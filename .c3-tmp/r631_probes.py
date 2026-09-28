# -*- coding: utf-8 -*-
# r631_probes.py -- three probes via python io.open UTF-8 capture (R585 law: never PS pipe redirect)
import io, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.dirname(os.path.abspath(__file__))

def run(cmd):
    p = subprocess.run(['python'] + cmd, cwd=ROOT, capture_output=True)
    return (p.stdout + p.stderr).decode('utf-8', errors='replace')

out = []
b = run(['src/board_check.py'])
r = run(['src/readiness.py'])
l = run(['src/os/loop_health.py'])
for name, txt in [('BOARD', b), ('READINESS', r), ('LOOP', l)]:
    out.append('==== %s (rc captured in text) ====' % name)
    out.append(txt)
res = '\n'.join(out)
io.open(os.path.join(TMP, 'r631_probes.txt'), 'w', encoding='utf-8').write(res)
# compact summary lines
summ = [ln for ln in res.splitlines() if ('FAIL' in ln or 'WARN' in ln or 'blocker' in ln.lower() or 'exit' in ln.lower())]
io.open(os.path.join(TMP, 'r631_probes_sum.txt'), 'w', encoding='utf-8').write('\n'.join(summ[:80]))
print('captured %d bytes; summary lines=%d' % (len(res), len(summ)))
