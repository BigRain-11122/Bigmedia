# -*- coding: utf-8 -*-
# R756: probe runner - run 4 probes, write UTF-8 outputs (PS 5.1 redirect mangles to UTF-16)
import subprocess, io

CMDS = [
    (['python', 'src/board_check.py'], '.c3-tmp/r756_board.txt'),
    (['python', 'src/readiness.py'], '.c3-tmp/r756_readiness.txt'),
    (['python', 'src/os/loop_health.py'], '.c3-tmp/r756_loop.txt'),
    (['python', '.c3-tmp/r750_scan.py'], '.c3-tmp/r756_scan.txt'),
]
for cmd, out in CMDS:
    p = subprocess.run(cmd, capture_output=True)
    with io.open(out, 'wb') as f:
        f.write(p.stdout)
        f.write(b'\n[stderr]\n')
        f.write(p.stderr)
    print(out, 'rc=%d' % p.returncode)
print('PROBE-RUN-DONE')
