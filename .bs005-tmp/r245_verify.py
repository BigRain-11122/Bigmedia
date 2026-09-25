import subprocess, sys, os
REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
r = subprocess.run([sys.executable, 'src/os/loop_health.py'], capture_output=True, cwd=REPO)
out = (r.stdout + r.stderr).decode('utf-8', errors='replace')
lines = [l for l in out.splitlines() if l.strip()]
with open(os.path.join(REPO, '.bs005-tmp', 'r245-loop-verify.txt'), 'w', encoding='utf-8') as fh:
    fh.write("exit=%d\n" % r.returncode)
    fh.write("\n".join(lines[-3:]))
print("exit=%d" % r.returncode)
