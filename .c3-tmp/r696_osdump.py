# -*- coding: utf-8 -*-
import io, json
se = json.load(io.open(r"docs\status-export.json", encoding="utf-8"))
out = []
for k, v in se.items():
    if isinstance(v, list):
        for i, r in enumerate(v):
            if isinstance(r, list) and len(r) >= 2 and isinstance(r[1], str) and r[1].startswith("tick "):
                out.append("%s[%d] label=%r text_head=%s" % (k, i, r[0], r[1][:80]))
io.open(r".c3-tmp\r696_osdump3.txt", "w", encoding="utf-8").write("\n".join(out))
print("DONE rows=%d" % len(out))
