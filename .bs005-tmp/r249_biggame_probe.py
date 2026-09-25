# -*- coding: utf-8 -*-
# R249: Biggame window frame probe v2 - clamp region to desktop bounds
# (maximized window rect (-7,-7,...) has offscreen borders; gdigrab
# rejects negative offsets with rc=-5).
import io
import os
import subprocess
import sys
import time

import ctypes

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import record_screen as rs  # noqa: E402

TMP = os.path.join(ROOT, ".bs005-tmp")
TITLE = "小游戏公司总控"
FRAME = os.path.join(TMP, "probe-biggame-r249-f1.png")

user32 = ctypes.windll.user32
SW, SH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

log = io.StringIO()
hit = rs.find_window(TITLE)
if not hit:
    print("FAIL window not found")
    sys.exit(2)

hwnd, (x, y, w, h) = hit
x0, y0 = max(0, x), max(0, y)
w2 = min(x + w, SW) - x0
h2 = min(y + h, SH) - y0
w2 -= w2 % 2
h2 -= h2 % 2
log.write("desktop=%dx%d raw=(%d,%d,%d,%d) clamped=(%d,%d,%d,%d)\n"
          % (SW, SH, x, y, w, h, x0, y0, w2, h2))
rs.focus_window(TITLE)
time.sleep(1.5)
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
       "-f", "gdigrab", "-framerate", "5",
       "-offset_x", str(x0), "-offset_y", str(y0),
       "-video_size", "%dx%d" % (w2, h2),
       "-draw_mouse", "0", "-i", "desktop",
       "-frames:v", "1", FRAME]
r = subprocess.run(cmd, capture_output=True)
log.write("ffmpeg_rc=%d\n" % r.returncode)
if r.stderr:
    log.write("stderr_tail=%s\n" % r.stderr.decode("utf-8", errors="replace")[-300:])
if r.returncode == 0 and os.path.exists(FRAME):
    log.write("frame_kb=%d\n" % (os.path.getsize(FRAME) // 1024))

with open(os.path.join(TMP, "r249-biggame-probe.txt"), "w", encoding="utf-8") as f:
    f.write(log.getvalue())
print("rc=%d clamped=(%d,%d,%d,%d) desktop=%dx%d" % (r.returncode, x0, y0, w2, h2, SW, SH))
