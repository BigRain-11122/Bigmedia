# -*- coding: utf-8 -*-
# r1353 probe suite: three probes fresh run (independent OUT per R1311)
import os, subprocess, io, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or "") + (p.stderr or "")
    w('=== %s (rc=%d) ===' % (label, p.returncode))
    w(out.strip()[-1600:])

run('BOARD', ['python', 'src/board_check.py'])
run('READINESS', ['python', 'src/readiness.py'])
run('LOOP_HEALTH', ['python', 'src/os/loop_health.py'])

io.open(os.path.join(ROOT, '.c3-tmp', 'r1353_probe.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
