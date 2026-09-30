# -*- coding: utf-8 -*-
# r795 probes runner (r683_probes lineage): run board/readiness/loop_health, write UTF-8 outputs
import subprocess, os, io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'

probes = [
    ('board', ['python', 'src/board_check.py'], 'r795_board.txt'),
    ('readiness', ['python', 'src/readiness.py'], 'r795_readiness.txt'),
    ('loop_health', ['python', 'src/os/loop_health.py'], 'r795_loop.txt'),
]

for name, cmd, out in probes:
    p = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    path = os.path.join(HERE, out)
    io.open(path, 'w', encoding='utf-8', newline='').write(p.stdout.decode('utf-8', errors='replace'))
    print('%s rc=%d out=%s bytes=%d' % (name, p.returncode, out, len(p.stdout)))
print('PROBES-DONE')
