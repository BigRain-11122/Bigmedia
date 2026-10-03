import subprocess, io, os
BM = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
T = BM + r"\.c3-tmp"

def run(cmd):
    r = subprocess.run(["python"] + cmd, cwd=BM, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout + r.stderr

board = run(["src/board_check.py"])
open(T + r"\r1114_board.txt", "w", encoding="utf-8").write(board)
rd = run(["src/readiness.py"])
open(T + r"\r1114_rd.txt", "w", encoding="utf-8").write(rd)
loop = run(["src/os/loop_health.py"])
open(T + r"\r1114_loop.txt", "w", encoding="utf-8").write(loop)

summ = io.StringIO()
def pick(txt, pats):
    res = []
    for ln in txt.splitlines():
        for p in pats:
            if p in ln:
                res.append(ln)
                break
    return res

b_lines = pick(board, ["summary:", "FAIL"])
r_lines = pick(rd, ["readiness:", "blocker", "finding"])
l_fail = [ln for ln in loop.splitlines() if "[FAIL]" in ln]
l_warn = [ln for ln in loop.splitlines() if "[WARN]" in ln]
l_sum = [ln for ln in loop.splitlines() if "loop health:" in ln]

summ.write("=== board ===\n" + "\n".join(b_lines) + "\n")
summ.write("=== readiness ===\n" + "\n".join(r_lines) + "\n")
summ.write("=== loop_health fails (%d) ===\n" % len(l_fail) + "\n".join(l_fail) + "\n")
summ.write("=== loop_health warn count: %d ===\n" % len(l_warn))
summ.write("=== loop_health summary ===\n" + "\n".join(l_sum) + "\n")
open(T + r"\r1114_probes_summary.txt", "w", encoding="utf-8").write(summ.getvalue())
print(summ.getvalue())
