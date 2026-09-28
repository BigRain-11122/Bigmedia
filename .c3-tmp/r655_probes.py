# -*- coding: utf-8 -*-
"""R655 three-probe runner: capture stdout as UTF-8 files (R631 law: no PS > redirection)."""
import subprocess, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
probes = [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop", ["python", "src/os/loop_health.py"]),
]
summary = []
for name, cmd in probes:
    r = subprocess.run(cmd, capture_output=True, cwd=ROOT)
    out = (r.stdout or b"") + (r.stderr or b"")
    try:
        text = out.decode("utf-8")
    except UnicodeDecodeError:
        text = out.decode("utf-8", "replace")
    with io.open(ROOT + r"\.c3-tmp\r655_probe_" + name + ".txt", "w", encoding="utf-8") as fh:
        fh.write("RC=" + str(r.returncode) + "\n" + text)
    summary.append(name + "_rc=" + str(r.returncode))
print(" ".join(summary))
