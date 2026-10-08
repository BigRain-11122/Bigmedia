import subprocess, os, sys

GIT = r'C:\Program Files\Git\cmd\git.exe'

def run(args):
    r = subprocess.run([GIT] + args, capture_output=True)
    print('$ git', ' '.join(args), '-> rc', r.returncode)
    if r.returncode != 0:
        print((r.stdout + r.stderr).decode('utf-8', errors='replace'))
    return r.returncode

rc = run(['add', 'src/os/state.json', 'docs/status-export.json'])
if rc: sys.exit(1)
rc = run(['commit', '-m', ('R1788 addendum [via bm-a]: SDXL pull landed DONE-OK within round '
           '(byte-exact 6938078334, seated in ComfyUI checkpoints, no completion-check debt for R1789), '
           'export live row updated')])
if rc: sys.exit(1)
run(['push'])
os.remove(r'.c3-tmp\r1788_addendum.py')
run(['status', '--short'])
