# -*- coding: utf-8 -*-
# R252 remediation: focus_window SW_RESTORE broke the silicon dashboard out
# of F11 fullscreen and content area went dark-blank during take-2. Steps:
# 1) probe current state (IsZoomed + 4s capture -> frame)
# 2) send F11 to re-enter fullscreen, wait, probe again
# 3) if still blank, F5 reload (last resort), probe again
# All steps logged to UTF-8 file; frames saved for verification.
import contextlib
import ctypes
import io
import os
import subprocess
import sys
import time
from ctypes import wintypes

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import record_screen as rs  # noqa: E402

TMP = os.path.join(ROOT, ".bs005-tmp")
user32 = ctypes.windll.user32
TITLE = "硅基生命元宇宙"
VK_F11 = 0x7A
VK_F5 = 0x74

log = io.StringIO()


def send_key(vk):
    user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk, 0, 2, 0)


def state_info():
    hit = rs.find_window(TITLE)
    if not hit:
        return None
    hwnd, rect = hit
    zoomed = bool(user32.IsZoomed(hwnd))
    return hwnd, rect, zoomed


def probe(tag):
    st = state_info()
    if not st:
        log.write("%s: window_not_found\n" % tag)
        return False
    hwnd, rect, zoomed = st
    log.write("%s: rect=%s zoomed=%s\n" % (tag, rect, zoomed))
    rs.focus_window(TITLE)
    time.sleep(1.2)
    buf = io.StringIO()
    mp4 = os.path.join(TMP, "r252-probe-%s.mp4" % tag)
    with contextlib.redirect_stdout(buf):
        rc = rs.main(["--title", TITLE, "--seconds", "4",
                      "--out", mp4, "--fps", "10"])
    png = os.path.join(TMP, "r252-probe-%s.png" % tag)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3",
                    "-i", mp4, "-frames:v", "1", png], check=False)
    os.remove(mp4)
    log.write("%s: probe rc=%d png=%s\n" % (tag, rc, os.path.exists(png)))
    return os.path.exists(png)


probe("s1-current")
time.sleep(0.5)
# step 2: re-enter fullscreen via F11
st = state_info()
if st:
    user32.SetForegroundWindow(st[0])
    time.sleep(0.8)
    send_key(VK_F11)
    time.sleep(3.0)
    probe("s2-after-f11")
    # step 3: if still likely blank, reload
    # (cannot verify blank programmatically here - frame check via tool;
    #  do F5 only if s2 png also blank, decided after visual check outside)

with open(os.path.join(TMP, "r252-remediation.txt"), "w", encoding="utf-8") as f:
    f.write(log.getvalue())
    f.write("STEPS_DONE\n")
print("done see r252-remediation.txt")
