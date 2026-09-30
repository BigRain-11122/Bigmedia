# -*- coding: utf-8 -*-
# R684: dump backlog #79 rows + status-export head/tail
import io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")

bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
hits = [l for l in bl if re.match(r"^\s*\*{0,2}79\.", l.strip()) or "R683" in l or "R681 收官" in l]
io.open(os.path.join(TMP, "r684_bk79.txt"), "w", encoding="utf-8").write("\n\n".join(hits[-6:]))

se = os.path.join(ROOT, "docs", "status-export.json")
txt = io.open(se, encoding="utf-8").read()
lines = txt.splitlines()
io.open(os.path.join(TMP, "r684_se_head.txt"), "w", encoding="utf-8").write("\n".join(lines[:14]))
io.open(os.path.join(TMP, "r684_se_tail.txt"), "w", encoding="utf-8").write("\n".join(lines[-16:]))
print("done bk79_hits=%d se_lines=%d" % (len(hits), len(lines)))
