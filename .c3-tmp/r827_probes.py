# -*- coding: utf-8 -*-
"""R827 probe driver: run board/readiness/loop_health, capture UTF-8 outputs."""
import subprocess, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'

JOBS = [
    (os.path.join(ROOT, 'src', 'board_check.py'), 'r827_board.txt'),
    (os.path.join(ROOT, 'src', 'readiness.py'), 'r827_readiness.txt'),
    (os.path.join(ROOT, 'src', 'os', 'loop_health.py'), 'r827_loop.txt'),
]
for script, out in JOBS:
    r = subprocess.run(['python', script], capture_output=True, env=env)
    io.open(os.path.join(HERE, out), 'wb').write(
        r.stdout + b'\n[stderr]\n' + r.stderr)
    print('%s -> %s rc=%d bytes=%d' % (os.path.basename(script), out, r.returncode, len(r.stdout)))
print('R827-PROBES-OK')
