import subprocess, io, os, re, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
T = os.path.join(ROOT, '.c3-tmp')

def run(args, outfile):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    r = subprocess.run(['python', '-X', 'utf8'] + args, cwd=ROOT, capture_output=True, env=env)
    txt = r.stdout.decode('utf-8', errors='replace')
    io.open(outfile, 'w', encoding='utf-8').write(txt + '\n[rc]=' + str(r.returncode) + '\n[stderr]' + r.stderr.decode('utf-8', errors='replace')[:800] + '\n')
    return txt, r.returncode

board, rc1 = run(['src/board_check.py'], os.path.join(T, 'r660_board.txt'))
ready, rc2 = run(['src/readiness.py'], os.path.join(T, 'r660_readiness.txt'))
health, rc3 = run(['src/os/loop_health.py'], os.path.join(T, 'r660_health.txt'))

d = io.open(os.path.join(T, 'r660_digest.txt'), 'w', encoding='utf-8')
d.write(f"now={datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
d.write(f"rc board={rc1} readiness={rc2} health={rc3}\n\n")
for name, txt in [('BOARD', board), ('READINESS', ready), ('HEALTH', health)]:
    d.write(f"===== {name} lines_matching FAIL/WARN/block/阻塞/ERROR:\n")
    for l in txt.splitlines():
        if re.search(r'FAIL|WARN|阻塞|block|ERROR|Error', l):
            d.write("  " + l[:170] + "\n")
    d.write(f"  [tail 4]\n")
    for l in txt.splitlines()[-4:]:
        d.write("  | " + l[:170] + "\n")
d.close()
print('done')
