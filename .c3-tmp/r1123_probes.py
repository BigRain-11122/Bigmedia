import subprocess, os, io

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CT = os.path.join(BS, ".c3-tmp")

probes = [
    ("board", os.path.join(BS, "src", "board_check.py"), "r1123_board.txt"),
    ("readiness", os.path.join(BS, "src", "readiness.py"), "r1123_rd.txt"),
    ("loop", os.path.join(BS, "src", "os", "loop_health.py"), "r1123_loop.txt"),
]

for name, cmd, out in probes:
    p = subprocess.run(["python", cmd], capture_output=True, cwd=BS)
    text = (p.stdout.decode("utf-8", "replace") + "\n[stderr]\n" + p.stderr.decode("utf-8", "replace")).strip()
    io.open(os.path.join(CT, out), "w", encoding="utf-8").write(text + "\n")
    print("== %s rc=%d -> %s ==" % (name, p.returncode, out))

s = io.StringIO()
for name, _, out in probes:
    t = io.open(os.path.join(CT, out), encoding="utf-8").read()
    tl = t.splitlines()
    s.write(u"### %s (rc lines=%d)\n" % (name, len(tl)))
    warn = 0
    for ln in tl:
        low = ln.lower()
        if "[warn]" in low:
            warn += 1
        if ("fail" in low) or ("finding" in low) or ("blocker" in low) or ("not ready" in low) or ("summary" in low and name == "board"):
            s.write(ln[:400] + u"\n")
    if warn:
        s.write(u"warn count=%d\n" % warn)
    s.write(u"-- tail --\n")
    for ln in tl[-6:]:
        s.write(ln[:400] + u"\n")
    s.write(u"\n")
io.open(os.path.join(CT, "r1123_probes_summary.txt"), "w", encoding="utf-8").write(s.getvalue())
print("summary written")
