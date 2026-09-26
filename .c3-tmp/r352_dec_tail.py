# R352: verify group decisions.md unchanged (mtime + tail rows D-ids per line, ASCII-safe)
import os, io, re
from datetime import datetime

dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
print("mtime", datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%Y-%m-%d %H:%M:%S"))
with io.open(dec, encoding="utf-8") as f:
    dl = [l for l in f.read().splitlines() if l.strip()]
print("nonempty_lines", len(dl))
for l in dl[-3:]:
    ids = re.findall(r"D-20260\d{3}-\d+", l)
    print("row_ids", ids if ids else "none", "| head:",
          l[:60].encode("unicode_escape").decode("ascii", "backslashreplace"))
