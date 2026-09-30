# -*- coding: utf-8 -*-
import io
t = io.open(r".c3-tmp/r691_readiness2.txt", encoding="utf-8", errors="replace").read()
lines = [l for l in t.splitlines() if ("blocker" in l or "finding" in l or "render-unannot" in l
                                       or "lc-005" in l or "发现" in l)]
io.open(r".c3-tmp/r691_readiness_sum.txt", "w", encoding="utf-8").write("\n".join(lines))
print("ok", len(lines))
