# r467 probe runner: board / readiness / loop_health via subprocess UTF-8 capture (zero-token routine)
import subprocess, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r467_probe.txt")
out = io.open(OUTP, "w", encoding="utf-8")

probes = [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop_health", ["python", "src/os/loop_health.py"]),
]

for name, cmd in probes:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    txt = p.stdout.decode("utf-8", errors="replace")
    out.write("=== %s exit=%d ===\n" % (name, p.returncode))
    out.write(txt)
    out.write("\n")
    if p.stderr:
        out.write("[stderr] " + p.stderr.decode("utf-8", errors="replace")[:500] + "\n")

out.close()
print("OK")
