# -*- coding: utf-8 -*-
# Re-run probes with byte capture -> UTF-8 files; extract R1354 log line; locate city-spirit asset
import subprocess, os, json, glob, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
out = []
def w(s): out.append(str(s))

for tag, rel in (("board", os.path.join("src", "board_check.py")),
                 ("readiness", os.path.join("src", "readiness.py")),
                 ("loop", os.path.join("src", "os", "loop_health.py"))):
    r = subprocess.run(["python", rel], cwd=ROOT, capture_output=True, env=env)
    data = (r.stdout or b"") + b"\n[STDERR]\n" + (r.stderr or b"")
    open(os.path.join(ROOT, "r1357_probe_%s.txt" % tag), "wb").write(data)
    w("probe %s: rc=%s bytes=%d" % (tag, r.returncode, len(data)))

st = json.load(open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("== full R1354 log line ==")
for line in st.get("log", []):
    if "R1354" in line[:30] or line.startswith("2026-10-05 11:5"):
        w(line)

w("== city-spirit files ==")
for pat in ("data/**/*spirit*", "data/**/*city-spirit*", "**/*spirit*"):
    for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
        if ".git" in p or "node_modules" in p:
            continue
        w("  %s (%d bytes, mtime %s)" % (os.path.relpath(p, ROOT), os.path.getsize(p),
           __import__("datetime").datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")))

open(os.path.join(ROOT, "r1357_r1354log.txt"), "w", encoding="utf-8").write("\n".join(out))
print("OK")
