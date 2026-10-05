# -*- coding: utf-8 -*-
"""Clone r1450_update_state.py -> r1451_update_state.py (caliber-aligned replacements) and run it."""
import io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")

t = io.open(os.path.join(TMP, "r1450_update_state.py"), encoding="utf-8").read()
t = t.replace("r1450", "r1451")
t = t.replace("R1450", "R1451")
t = t.replace("R1449", "R1450")
t = t.replace("beats1456>tick1449", "beats1457>tick1450")
t = t.replace("tick1450 收账后", "tick1451 收账后")
t = t.replace("tick 1450", "tick 1451")
t = t.replace("== 1449", "== 1450")  # assert st["tick"] == 1450 (pre-state for R1451)
t = t.replace('st["tick"] = 1450', 'st["tick"] = 1451')
t = t.replace("第 15 轮连续", "第 16 轮连续")
t = t.replace("commit 282bf43f", "commit 34b2e632")
io.open(os.path.join(TMP, "r1451_update_state.py"), "w", encoding="utf-8").write(t)
print("cloned r1451_update_state.py")

p = subprocess.run(["python", os.path.join(".c3-tmp", "r1451_update_state.py")], cwd=ROOT,
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("update rc=%d" % p.returncode)
print((p.stdout or "").strip())
if p.returncode != 0:
    print("stderr: %s" % (p.stderr or "")[:600])
