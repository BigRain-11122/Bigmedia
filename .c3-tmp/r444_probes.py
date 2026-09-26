# -*- coding: utf-8 -*-
# R444 probe runner (read-only): board/readiness/loop_health (r441 pattern)
import subprocess, io, os

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo)
env = dict(os.environ, PYTHONUTF8="1")
out_path = os.path.join(repo, ".c3-tmp", "r444_probe.txt")
out = io.open(out_path, "w", encoding="utf-8")
for name, cmd in [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop_health", ["python", "src/os/loop_health.py"]),
]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out.write(u"=== %s exit=%d ===\n" % (name, r.returncode))
    out.write(r.stdout or u"")
    if r.stderr:
        out.write(u"[stderr]\n" + r.stderr)
    out.write(u"\n")
    print("%s_exit=%d" % (name, r.returncode))
out.close()
print("probe_file=%s" % out_path)
