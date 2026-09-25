# R226 probes: three probes with UTF-8 capture (R221/R225 pattern).
import io, os, subprocess

OUT = '.bs005-tmp'

def run(name, cmd):
    env = dict(os.environ)
    env['PYTHONUTF8'] = '1'
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.stdout.decode('utf-8', errors='replace')
    io.open(os.path.join(OUT, 'probe-r226-%s.txt' % name), 'w', encoding='utf-8').write(out)
    print(name, 'exit', p.returncode)

run('board', ['python', 'src/board_check.py'])
run('readiness', ['python', 'src/readiness.py'])
run('loop', ['python', 'src/os/loop_health.py'])
