# R515 probes runner - board / readiness / loop_health, UTF-8 file output only
import os, subprocess, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
env = dict(os.environ)
env["PYTHONUTF8"] = "1"
env["PYTHONIOENCODING"] = "utf-8"

PROBES = [
    ("board", ["board_check.py"]),
    ("readiness", ["readiness.py"]),
    ("loop_health", [os.path.join("os", "loop_health.py")]),
]

out = []
for name, rel in PROBES:
    path = os.path.join(ROOT, "src", *rel)
    try:
        p = subprocess.run([sys.executable, path], cwd=ROOT, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=300)
        body = p.stdout.decode("utf-8", errors="replace")
        out.append("===== %s (exit=%d) =====" % (name, p.returncode))
        out.append(body.strip()[-3000:])
        out.append("")
    except Exception as e:
        out.append("===== %s (RUN-FAIL %s) =====" % (name, e))

outp = os.path.join(ROOT, ".c3-tmp", "r515_probes_out.txt")
with open(outp, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK -> r515_probes_out.txt")
