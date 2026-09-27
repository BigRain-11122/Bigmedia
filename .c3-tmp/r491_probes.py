# r491_probes.py - three probes run + capture (new file via write_file, OUTP new, utf-8, PYTHONIOENCODING)
import io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r491_probes.txt")
env = dict(os.environ, PYTHONIOENCODING="utf-8")
L = []
probes = [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop_health", ["python", "src/os/loop_health.py"]),
]
for name, cmd in probes:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    L.append("== %s exit=%d ==" % (name, p.returncode))
    out_lines = (p.stdout or "").splitlines()
    if name == "loop_health":
        keep = [ln for ln in out_lines if ("FAIL" in ln or "WARN" in ln)]
        tail = [ln for ln in out_lines if ln.strip()][-3:]
        L.extend(keep if keep else tail)
    elif name == "readiness":
        L.extend([ln for ln in out_lines if ln.strip()][-14:])
    else:
        L.extend([ln for ln in out_lines if ln.strip()][-8:])
    if p.stderr and p.stderr.strip():
        L.append("[stderr-tail] " + p.stderr.strip().splitlines()[-1][:200])
with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
