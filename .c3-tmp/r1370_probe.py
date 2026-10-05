import subprocess, sys, io

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1370_probe.txt", "w", encoding="utf-8")
w = out.write
for name, cmd in [
    ("board", [sys.executable, r"src\board_check.py"]),
    ("readiness", [sys.executable, r"src\readiness.py"]),
    ("loop_health", [sys.executable, r"src\os\loop_health.py"]),
]:
    try:
        p = subprocess.run(cmd, cwd=repo, capture_output=True, timeout=300)
        w("== %s rc=%d ==\n" % (name, p.returncode))
        w((p.stdout or b"").decode("utf-8", "replace")[-3000:] + "\n")
        err = (p.stderr or b"").decode("utf-8", "replace").strip()
        if err:
            w("[stderr] " + err[-600:] + "\n")
    except Exception as e:
        w("== %s EXC: %s: %s ==\n" % (name, type(e).__name__, str(e)[:200]))
out.close()
print("ok")
