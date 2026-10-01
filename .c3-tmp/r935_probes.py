import subprocess, io, os

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
probes = {
    "board": ["python", "src/board_check.py"],
    "rd": ["python", "src/readiness.py"],
    "loop": ["python", "src/os/loop_health.py"],
}

for name, cmd in probes.items():
    p = subprocess.run(cmd, cwd=root, capture_output=True)
    raw = p.stdout
    # try common encodings
    text = None
    for enc in ("utf-8", "utf-16", "gbk"):
        try:
            text = raw.decode(enc)
            break
        except Exception:
            continue
    if text is None:
        text = raw.decode("utf-8", errors="replace")
    err = p.stderr.decode("gbk", errors="replace")
    with io.open(os.path.join(root, ".c3-tmp", "r935_%s.txt" % name), "w", encoding="utf-8") as f:
        f.write(text)
        if err.strip():
            f.write("\n[stderr]\n" + err)
    print("%s: exit=%d lines=%d" % (name, p.returncode, len(text.splitlines())))

# summary of key lines
def keylines(path, keep):
    with io.open(path, encoding="utf-8") as f:
        t = f.read()
    out = []
    for ln in t.splitlines():
        if any(k in ln for k in keep):
            out.append(ln.strip()[:220])
    return out

with io.open(os.path.join(root, ".c3-tmp", "r935_probe_summary.txt"), "w", encoding="utf-8") as f:
    f.write("== BOARD ==\n")
    f.write("\n".join(keylines(os.path.join(root, ".c3-tmp", "r935_board.txt"), ["summary:", "FAIL"])) + "\n")
    f.write("== READINESS ==\n")
    f.write("\n".join(keylines(os.path.join(root, ".c3-tmp", "r935_rd.txt"), ["FAIL", "PASS", "blocker", "Blocker", "finding", "Finding", "CEO"])) + "\n")
    f.write("== LOOP ==\n")
    lt = None
    with io.open(os.path.join(root, ".c3-tmp", "r935_loop.txt"), encoding="utf-8") as fh:
        lt = fh.read().splitlines()
    fails = [l.strip()[:220] for l in lt if "FAIL" in l]
    warns = [l.strip()[:160] for l in lt if "WARN" in l]
    f.write("lines=%d FAIL=%d WARN=%d\n" % (len(lt), len(fails), len(warns)))
    f.write("\n".join(fails) + "\n")
    f.write("-- WARN sample (last 5) --\n")
    f.write("\n".join(warns[-5:]) + "\n")
print("summary written")
