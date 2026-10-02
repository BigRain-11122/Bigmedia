# -*- coding: utf-8 -*-
import subprocess, io, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
def run(cmd, outfile):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    txt = p.stdout.decode('utf-8', errors='replace') + "\n[stderr]\n" + p.stderr.decode('utf-8', errors='replace')
    io.open(os.path.join(ROOT, '.c3-tmp', outfile), 'w', encoding='utf-8').write(txt[:6000])
    print(outfile, 'rc=%d bytes=%d' % (p.returncode, len(p.stdout)))
run(['python', '.c3-tmp/fast_check.py'], 'r1035_fc.txt')
run(['python', 'src/os/loop_health.py'], 'r1035_lh.txt')
