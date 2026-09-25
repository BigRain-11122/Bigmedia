# -*- coding: utf-8 -*-
# R234 three-probe run (UTF-8 clean-file readings, R214/R227/R229 convention)
import io, subprocess, sys

BS = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
probes = [
    ('board', [sys.executable, 'src/board_check.py']),
    ('readiness', [sys.executable, 'src/readiness.py']),
    ('loop_health', [sys.executable, 'src/os/loop_health.py']),
]
out = []
for name, cmd in probes:
    p = subprocess.run(cmd, cwd=BS, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    txt = p.stdout.decode('utf-8', errors='replace')
    out.append('===== %s exit=%d =====' % (name, p.returncode))
    out.append(txt)
io.open(BS + r'\.bs005-tmp\probe-r234-all.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done probes')
