# -*- coding: utf-8 -*-
"""r1676_react_probe4.py - full creed dump of all census anchors (no filter)."""
import io, os, glob, re

ANCH = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1676_react_probe4.txt"

lines_out = []
for p in sorted(glob.glob(os.path.join(ANCH, "C-*.md"))):
    txt = io.open(p, encoding="utf-8").read()
    m = re.search(u"信条[^\n「」]*「(.+?)」", txt)
    job = re.search(u"\*\*职业\*\*\s*([^\n—]+)", txt)
    creed = m.group(1).strip() if m else u"(no creed pattern)"
    j = job.group(1).strip() if job else u"?"
    lines_out.append(u"%s | %s | %s" % (os.path.basename(p), j, creed))

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines_out) + "\n")
print("PROBE4 OK -> %s (%d anchors)" % (OUT, len(lines_out)))
