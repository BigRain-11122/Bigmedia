# -*- coding: utf-8 -*-
import io

out = io.StringIO()
for n in ("board", "readiness", "loop_health"):
    p = r".c3-tmp\r1371_%s.txt" % n
    try:
        lines = io.open(p, encoding="utf-8", errors="replace").read().splitlines()
    except Exception as e:
        out.write("=== %s === READ-ERR %s\n" % (n, e))
        continue
    out.write("=== %s === (%d lines)\n" % (n, len(lines)))
    for l in lines[-30:]:
        out.write(l[:250] + "\n")
    out.write("\n")

io.open(r".c3-tmp\r1371_probes_sum.txt", "w", encoding="utf-8").write(out.getvalue())
print("OK")
