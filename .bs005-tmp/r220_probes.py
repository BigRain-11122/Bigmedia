import subprocess, io, os, datetime

BASE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
os.chdir(BASE)

clean = io.open(r".bs005-tmp/probe-r220-clean.txt", "w", encoding="utf-8")
exits = {}
for name, cmd in [("board", ["src/board_check.py"]),
                  ("readiness", ["src/readiness.py"]),
                  ("loop", ["src/os/loop_health.py"])]:
    r = subprocess.run(["python"] + cmd, capture_output=True)
    raw = r.stdout + b"\n" + r.stderr
    io.open(r".bs005-tmp/probe-r220-%s.txt" % name, "wb").write(raw)
    exits[name] = r.returncode
    try:
        txt = raw.decode("gbk")
    except Exception:
        txt = raw.decode("utf-8", "replace")
    lines = txt.splitlines()
    clean.write("=== %s exit=%d lines=%d ===\n" % (name, r.returncode, len(lines)))
    clean.write("\n".join(lines[:120]) + "\n")
clean.write("=== exits ===\n" + "\n".join("%s=%d" % kv for kv in exits.items()) + "\n")

# routine artifacts existence + self-improvement queue mtime anchor
checks = []
checks.append(("daily_report", os.path.exists(r"data/intel/daily/2026-09-25.md")))
aud = glob = None
import glob as _g
aud = _g.glob(r"docs/audits/*self-audit*.md")
checks.append(("self_audit_files", [os.path.basename(x) for x in aud]))
q = r"docs/self-improvement-queue.md"
if os.path.exists(q):
    checks.append(("siq_mtime", datetime.datetime.fromtimestamp(os.path.getmtime(q)).strftime("%m-%d %H:%M")))
gb = r"docs/global-benchmarks.md"
if os.path.exists(gb):
    with io.open(gb, encoding="utf-8") as f:
        first_dates = [l.strip()[:30] for l in f if "2026-" in l][:3]
    checks.append(("gb_first_lines", first_dates))
clean.write("=== checks ===\n" + "\n".join("%s=%s" % (k, v) for k, v in checks) + "\n")
clean.close()
print("probes done:", exits)
