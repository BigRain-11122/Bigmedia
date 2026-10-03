import subprocess, os, io

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

probes = [
    ("board", ["python", os.path.join(BS, "src", "board_check.py")], "r1108_board.txt"),
    ("readiness", ["python", os.path.join(BS, "src", "readiness.py")], "r1108_rd.txt"),
    ("loop", ["python", os.path.join(BS, "src", "os", "loop_health.py")], "r1108_loop.txt"),
]

for name, cmd, out in probes:
    p = subprocess.run(cmd, capture_output=True, cwd=BS)
    text = (p.stdout.decode("utf-8", "replace") + "\n[stderr]\n" + p.stderr.decode("utf-8", "replace")).strip()
    open(os.path.join(BS, ".c3-tmp", out), "w", encoding="utf-8").write(text + "\n")
    print("== %s rc=%d -> %s ==" % (name, p.returncode, out))

s = io.StringIO()
for name, _, out in probes:
    t = io.open(os.path.join(BS, ".c3-tmp", out), encoding="utf-8").read()
    tl = t.splitlines()
    s.write(u"### %s (rc lines=%d)\n" % (name, len(tl)))
    for ln in tl:
        low = ln.lower()
        if (("fail" in low) or ("warn" in low) or ("block" in low) or ("finding" in low) or ("pass" in low and "board" in name)):
            s.write(ln[:400] + u"\n")
    s.write(u"-- tail --\n")
    for ln in tl[-6:]:
        s.write(ln[:400] + u"\n")
    s.write(u"\n")
io.open(os.path.join(BS, ".c3-tmp", "r1108_probes_summary.txt"), "w", encoding="utf-8").write(s.getvalue())
print("summary written")
