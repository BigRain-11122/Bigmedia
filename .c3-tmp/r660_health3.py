# -*- coding: utf-8 -*-
import subprocess, os, io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
r = subprocess.run(['python', '-X', 'utf8', 'src/os/loop_health.py'], cwd=ROOT, capture_output=True, env=env)
txt = r.stdout.decode('utf-8', errors='replace')
d = io.open(os.path.join(ROOT, '.c3-tmp', 'r660_health3.txt'), 'w', encoding='utf-8')
for l in txt.splitlines():
    if 'account-lag' in l or 'loop health:' in l or 'heartbeat-outage' in l:
        d.write(l[:160] + '\n')
d.close()
print('done')
