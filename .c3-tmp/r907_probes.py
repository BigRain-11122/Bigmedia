# -*- coding: utf-8 -*-
import subprocess, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
env = dict(os.environ, PYTHONIOENCODING="utf-8")
for name, script in [("board", "src/board_check.py"), ("rd", "src/readiness.py"), ("loop", "src/os/loop_health.py")]:
    p = subprocess.run([os.sys.executable, script], cwd=ROOT, capture_output=True, env=env)
    with open(os.path.join(ROOT, ".c3-tmp", "r907_%s.txt" % name), "wb") as f:
        f.write(p.stdout)
        f.write(b"\n[stderr]\n" + p.stderr)
    print(name, "rc=", p.returncode, "bytes=", len(p.stdout))
