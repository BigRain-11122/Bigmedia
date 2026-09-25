# -*- coding: utf-8 -*-
# R249: record Biggame master-control window (40s, no --close: window is
# another line's physical asset, loop only records). Result -> UTF-8 file.
import contextlib
import io
import os
import sys
import time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import record_screen as rs  # noqa: E402

TMP = os.path.join(ROOT, ".bs005-tmp")
out = os.path.join(TMP, "r249-record-out.txt")
buf = io.StringIO()
t0 = time.time()
rc = -99
try:
    with contextlib.redirect_stdout(buf):
        rc = rs.main(["--title", "小游戏公司总控",
                      "--seconds", "40",
                      "--out", os.path.join(ROOT, "data", "sources", "footage",
                                            "biggame-console-raw.mp4"),
                      "--fps", "15"])
except Exception as e:
    buf.write("exc=%r\n" % e)
dur = time.time() - t0
with open(out, "w", encoding="utf-8") as f:
    f.write("rc=%d dur=%.1fs\n%s" % (rc, dur, buf.getvalue()))
    f.write("DONE\n")
