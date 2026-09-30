# -*- coding: utf-8 -*-
import io
se = io.open(r"docs\status-export.json", encoding="utf-8").readlines()
with io.open(r".c3-tmp\r696_osrow.txt", "w", encoding="utf-8") as f:
    for i, l in enumerate(se):
        if "OSLoop" in l or "tick" in l:
            f.write("L%d: %s\n" % (i + 1, l.rstrip()[:200]))
print("DONE")
