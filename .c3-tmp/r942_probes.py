import subprocess, os

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

probes = [
    ("board", ["python", os.path.join(BS, "src", "board_check.py")], "r942_board.txt"),
    ("readiness", ["python", os.path.join(BS, "src", "readiness.py")], "r942_rd.txt"),
    ("loop", ["python", os.path.join(BS, "src", "os", "loop_health.py")], "r942_loop.txt"),
]

for name, cmd, out in probes:
    p = subprocess.run(cmd, capture_output=True, cwd=BS)
    text = (p.stdout.decode("utf-8", "replace") + "\n[stderr]\n" + p.stderr.decode("utf-8", "replace")).strip()
    open(os.path.join(BS, ".c3-tmp", out), "w", encoding="utf-8").write(text + "\n")
    tail = "\n".join(text.splitlines()[-6:])
    print("== %s rc=%d ==" % (name, p.returncode))
    print(tail)
