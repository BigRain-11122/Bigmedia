# -*- coding: utf-8 -*-
# R520 three probes: board_check / readiness / loop_health - subprocess run, UTF-8 save, key-line ASCII summary
import os, re, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
KEY = re.compile(r'FAIL|ERROR|WARN|block|BLOCK|SUMMARY|PASS|distance|tick|account|heartbeat|GATE|renders|draft', re.I)
probes = [
    ('r520_board', [os.path.join(ROOT, 'src', 'board_check.py')]),
    ('r520_ready', [os.path.join(ROOT, 'src', 'readiness.py')]),
    ('r520_loop', [os.path.join(ROOT, 'src', 'os', 'loop_health.py')]),
]
for name, cmd in probes:
    p = subprocess.run(['python', '-u'] + cmd, cwd=ROOT, capture_output=True)
    raw = p.stdout + b'\n' + p.stderr
    txt = None
    for enc in ('utf-8', 'gbk'):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    if txt is None:
        txt = raw.decode('utf-8', errors='replace')
    with open(os.path.join(ROOT, '.c3-tmp', name + '.txt'), 'w', encoding='utf-8') as fh:
        fh.write('exit=%d\n' % p.returncode)
        fh.write(txt)
    lines = [l for l in txt.splitlines() if l.strip()]
    key = [l for l in lines if KEY.search(l)]
    print('===== %s exit=%d lines=%d keylines=%d =====' % (name, p.returncode, len(lines), len(key)))
    for l in key[:22]:
        print('  ' + l[:160].encode('ascii', errors='replace').decode('ascii'))
    print('  --- tail 4 ---')
    for l in lines[-4:]:
        print('  ' + l[:160].encode('ascii', errors='replace').decode('ascii'))
print('DONE')
