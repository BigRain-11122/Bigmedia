# -*- coding: utf-8 -*-
# R684: post-close probe re-run + state verify
import subprocess, os, io, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

rep = []
for name, cmd, out in [
    ("board", ["python", "src/board_check.py"], "r684_board2.txt"),
    ("readiness", ["python", "src/readiness.py"], "r684_readiness2.txt"),
    ("loop_health", ["python", "src/os/loop_health.py"], "r684_health2.txt"),
]:
    r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True)
    txt = (r.stdout.decode("utf-8", "replace") + "\n[stderr]\n" + r.stderr.decode("utf-8", "replace"))
    io.open(os.path.join(TMP, out), "w", encoding="utf-8").write(txt)
    tail = [l for l in txt.splitlines() if l.strip()][-2:]
    rep.append("%s exit=%d tail=%s" % (name, r.returncode, " | ".join(tail)[:200]))

# state verify (authoritative): tick/ts/task/logN/focus + json validity + renders row presence
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
se = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
rr = io.open(os.path.join(ROOT, "output", "renders", "README.md"), encoding="utf-8").read()
checks = [
    ("state_valid_json", True),
    ("tick_684", st["tick"] == 684),
    ("log_tail_R684", "R684" in st["log"][-1]),
    ("task_len", 30 <= len(st.get("task", "")) <= 80),
    ("ts_fresh", st["ts"].startswith("2026-09-29 13:")),
    ("se_results_684", se["results"][-1][0] == "684"),
    ("se_os_tick684", "tick 684" in se["outs"][0][1]),
    ("se_export_ts_fresh", se["export_ts"].startswith("2026-09-29T13:")),
    ("renders_row_lc003", "lc-003-v1-shipinhao-60s.mp4" in rr),
    ("renders_row_inchain", rr.count("| lc-003-v1-shipinhao-60s.mp4") == 1),
]
for n, ok in checks:
    rep.append("%s=%s" % (n, "PASS" if ok else "FAIL"))
io.open(os.path.join(TMP, "r684_verify.txt"), "w", encoding="utf-8").write("\n".join(rep))
print("\n".join(rep))
