import subprocess, io, os, datetime

BASE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
os.chdir(BASE)

clean = io.open(r".bs005-tmp/probe-r221-clean.txt", "w", encoding="utf-8")
exits = {}
for name, cmd in [("board", ["src/board_check.py"]),
                  ("readiness", ["src/readiness.py"]),
                  ("loop", ["src/os/loop_health.py"])]:
    r = subprocess.run(["python"] + cmd, capture_output=True)
    raw = r.stdout + b"\n" + r.stderr
    io.open(r".bs005-tmp/probe-r221-%s.txt" % name, "wb").write(raw)
    exits[name] = r.returncode
    try:
        txt = raw.decode("gbk")
    except Exception:
        txt = raw.decode("utf-8", "replace")
    lines = txt.splitlines()
    clean.write("=== %s exit=%d lines=%d ===\n" % (name, r.returncode, len(lines)))
    clean.write("\n".join(lines[:120]) + "\n")
clean.write("=== exits ===\n" + "\n".join("%s=%d" % kv for kv in exits.items()) + "\n")

# loop_health tail summary lines
raw = io.open(r".bs005-tmp/probe-r221-loop.txt", "rb").read()
try:
    txt = raw.decode("gbk")
except Exception:
    txt = raw.decode("utf-8", "replace")
fail_lines = [l for l in txt.splitlines() if "FAIL" in l or "WARN" in l]
clean.write("=== loop fail/warn lines ===\n" + "\n".join(fail_lines[:20]) + "\n")
clean.close()
print("probes done:", exits)
