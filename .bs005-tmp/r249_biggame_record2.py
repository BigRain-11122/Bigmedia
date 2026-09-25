# -*- coding: utf-8 -*-
# R249: re-record Biggame console window - scene now fully loaded (f2 probe
# evidence). Foreground verified BEFORE capture; 40s overwrite raw.
import contextlib
import ctypes
import io
import os
import sys
import time
from ctypes import wintypes

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import record_screen as rs  # noqa: E402

TMP = os.path.join(ROOT, ".bs005-tmp")
user32 = ctypes.windll.user32
TITLE = "小游戏公司总控"
log = io.StringIO()

hit = rs.find_window(TITLE)
if not hit:
    with open(os.path.join(TMP, "r249-record2-out.txt"), "w", encoding="utf-8") as f:
        f.write("window_not_found\n")
    print("FAIL window gone")
    sys.exit(2)

hwnd, rect = hit
rs.focus_window(TITLE)
time.sleep(1.5)
fg = user32.GetForegroundWindow()
log.write("foreground_is_target=%s\n" % (fg == hwnd))

buf = io.StringIO()
rc = -99
t0 = time.time()
with contextlib.redirect_stdout(buf):
    rc = rs.main(["--title", TITLE, "--seconds", "40",
                  "--out", os.path.join(ROOT, "data", "sources", "footage",
                                        "biggame-console-raw.mp4"),
                  "--fps", "15"])
dur = time.time() - t0
log.write("rc=%d dur=%.1fs\n%s" % (rc, dur, buf.getvalue()))
with open(os.path.join(TMP, "r249-record2-out.txt"), "w", encoding="utf-8") as f:
    f.write(log.getvalue())
    f.write("DONE\n")
print("rc=%d fg_ok written" % rc)
