# -*- coding: utf-8 -*-
# R910 probe runner: run three probes, capture UTF-8 outputs (r897 lineage)
import subprocess, sys, io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
OUT = ROOT + r'\.c3-tmp'

def run(cmd, outfile):
    p = subprocess.run([sys.executable] + cmd, capture_output=True)
    txt = (p.stdout.decode('utf-8', errors='replace')
           + '\n[stderr]\n' + p.stderr.decode('utf-8', errors='replace'))
    with io.open(OUT + '\\' + outfile, 'w', encoding='utf-8') as f:
        f.write('exit=%d\n%s' % (p.returncode, txt))
    print(outfile, 'exit=%d' % p.returncode)

run([ROOT + r'\src\board_check.py'], 'r910_board.txt')
run([ROOT + r'\src\readiness.py', '--out', OUT + r'\r910_rd.txt'], 'r910_rd.txt')
run([ROOT + r'\src\os\loop_health.py'], 'r910_loop.txt')
