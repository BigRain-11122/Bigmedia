import subprocess, os, io

OUT = os.path.join('.c3-tmp', 'r510_probes.txt')
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
cmds = [
    ('board', ['python', 'src' + os.sep + 'board_check.py']),
    ('readiness', ['python', 'src' + os.sep + 'readiness.py']),
    ('loop_health', ['python', 'src' + os.sep + 'os' + os.sep + 'loop_health.py']),
]
with io.open(OUT, 'w', encoding='utf-8') as out:
    for name, cmd in cmds:
        p = subprocess.run(cmd, capture_output=True, env=env)
        out.write('=== %s exit=%d ===\n' % (name, p.returncode))
        out.write(p.stdout.decode('utf-8', 'replace'))
        err = p.stderr.decode('utf-8', 'replace').strip()
        if err:
            out.write('[stderr] ' + err[:800] + '\n')
        out.write('\n')
print('probes done ->', OUT)
