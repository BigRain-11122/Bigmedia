# r617_probes.py -- three probe run for R617 (board / readiness / loop_health), UTF-8 evidence files
import os, io, subprocess, sys

SCRIPT = os.path.abspath(__file__)
TMP = os.path.dirname(SCRIPT)
ROOT = os.path.dirname(TMP)

def run(label, cmd, outfile):
    r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True)
    out = (r.stdout or b'').decode('utf-8', errors='replace')
    err = (r.stderr or b'').decode('utf-8', errors='replace')
    body = 'RC=%d\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n' % (r.returncode, out, err)
    with io.open(os.path.join(TMP, outfile), 'w', encoding='utf-8') as fh:
        fh.write(body)
    print('%s_RC=%d' % (label, r.returncode))
    for l in out.splitlines():
        if ('FAIL' in l or 'WARN' in l or 'blocker' in l or 'PASS' in l) and all(ord(c) < 128 for c in l):
            print(l[:160])

run('BOARD', ['src/board_check.py'], 'r617_board.txt')
run('READINESS', ['src/readiness.py'], 'r617_readiness.txt')
run('LOOP', ['src/os/loop_health.py'], 'r617_loop.txt')
print('PROBES_DONE')
