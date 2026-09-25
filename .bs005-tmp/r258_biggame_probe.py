# -*- coding: utf-8 -*-
# R258: Biggame console window frame probe (panel-expansion watch, D-BS-08
# revival clause). Same as R255-R257 probe: capture WITHOUT focus (R252 F11
# incident lesson); caller checks whether CEO F11 overlay still covers.
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
FRAME = os.path.join(TMP, "probe-biggame-r258.png")
LOG = os.path.join(TMP, "r258-biggame-probe.txt")

user32 = ctypes.windll.user32
SW, SH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

log = io.StringIO()
hit = rs.find_window(TITLE)
if not hit:
    log.write("FAIL window not found\n")
    io.open(LOG, "w", encoding="utf-8").write(log.getvalue())
    print("rc=2 window-not-found")
    sys.exit(2)

hwnd, (x, y, w, h) = hit
x0, y0 = max(0, x), max(0, y)
w2 = min(x + w, SW) - x0
h2 = min(y + h, SH) - y0
w2 -= w2 % 2
h2 -= h2 % 2
log.write("desktop=%dx%d raw=(%d,%d,%d,%d) clamped=(%d,%d,%d,%d)\n"
          % (SW, SH, x, y, w, h, x0, y0, w2, h2))
time.sleep(0.5)
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

io.open(LOG, "w", encoding="utf-8").write(log.getvalue())
print("rc=%d frame=%s" % (r.returncode, os.path.basename(FRAME)))
