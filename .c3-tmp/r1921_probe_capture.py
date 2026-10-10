import subprocess, sys, io, datetime
root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
probes = [
    ("board_check", [sys.executable, "src/board_check.py"]),
    ("readiness", [sys.executable, "src/readiness.py", "--summary"]),
    ("loop_health", [sys.executable, "src/os/loop_health.py", "--loop"]),
]
lines = ["# probe-capture %s mode=compact" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
for name, cmd in probes:
    lines.append("=== %s ===" % name)
    p = subprocess.run(cmd, cwd=root, capture_output=True)
    txt = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    lines.append(txt.rstrip())
    lines.append("rc=%d" % p.returncode)
    lines.append("")
out = "\r\n".join(lines)
with io.open(root + r"\.c3-tmp\r1921_probes.txt", "w", encoding="utf-8", newline="") as f:
    f.write(out)
print(out)
