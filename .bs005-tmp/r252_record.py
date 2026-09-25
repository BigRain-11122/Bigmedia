# -*- coding: utf-8 -*-
# R252 leg-2: record Edge dashboard window (silicon meta dashboard).
# Take-1: top fold 40s (contains priority P0-P5 rows = b4 evidence).
# Scroll END -> Take-2: bottom fold 40s (constitution/top-design + machines).
# Scroll HOME to restore. Keyboard-only scroll (no cursor move). Foreground
# verified before each capture. Frames extracted after.
import contextlib
import ctypes
import io
import os
import sys
import time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import record_screen as rs  # noqa: E402

TMP = os.path.join(ROOT, ".bs005-tmp")
FOOT = os.path.join(ROOT, "data", "sources", "footage")
user32 = ctypes.windll.user32
TITLE = "硅基生命元宇宙"
VK_END = 0x23
VK_HOME = 0x24

log = io.StringIO()

def send_key(vk):
    ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk, 0, 2, 0)  # KEYEVENTF_KEYUP

def take(name, seconds):
    hit = rs.find_window(TITLE)
    if not hit:
        log.write("%s: window_not_found\n" % name)
        return -2
    hwnd, rect = hit
    rs.focus_window(TITLE)
    time.sleep(1.5)
    fg = user32.GetForegroundWindow()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = rs.main(["--title", TITLE, "--seconds", str(seconds),
                      "--out", os.path.join(FOOT, name),
                      "--fps", "15"])
    log.write("%s: fg_is_target=%s rc=%d\n%s" % (name, fg == hwnd, rc, buf.getvalue()))
    return rc

rc1 = take("silicon-dashboard-top-raw.mp4", 40)
time.sleep(1.0)
send_key(VK_END)
time.sleep(1.5)
rc2 = take("silicon-dashboard-bottom-raw.mp4", 40)
time.sleep(0.5)
send_key(VK_HOME)
time.sleep(0.5)
send_key(VK_HOME)

with open(os.path.join(TMP, "r252-record-out.txt"), "w", encoding="utf-8") as f:
    f.write(log.getvalue())
    f.write("DONE rc1=%d rc2=%d\n" % (rc1, rc2))
print("rc1=%d rc2=%d" % (rc1, rc2))
