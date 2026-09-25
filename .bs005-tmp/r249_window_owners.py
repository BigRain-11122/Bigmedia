# -*- coding: utf-8 -*-
# R249: window ownership probe - which process owns the Biggame console window
# vs the Edge dashboard window; capture a frame of the actual console window.
import ctypes
import io
import os
import subprocess
import sys
import time
from ctypes import wintypes

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".bs005-tmp")
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

log = io.StringIO()
rows = []


@ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
def on_enum(hwnd, _lp):
    if not user32.IsWindowVisible(hwnd):
        return True
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return True
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    rows.append((buf.value, hwnd, (rect.left, rect.top,
                                   rect.right - rect.left,
                                   rect.bottom - rect.top), pid.value))
    return True


user32.EnumWindows(on_enum, 0)

proc_names = {}
for title, hwnd, rect, pid in rows:
    if pid not in proc_names:
        try:
            h = kernel32.OpenProcess(0x0410, False, pid)  # PROCESS_QUERY_INFORMATION|LIMITED
            if h:
                buf = ctypes.create_unicode_buffer(260)
                if kernel32.GetModuleFileNameExW(h, None, buf, 260):
                    proc_names[pid] = os.path.basename(buf.value)
                else:
                    proc_names[pid] = "?"
                kernel32.CloseHandle(h)
        except Exception:
            proc_names[pid] = "err"

for title, hwnd, rect, pid in rows:
    log.write("pid=%d(%s) hwnd=%d rect=%s title=%s\n"
              % (pid, proc_names.get(pid, "?"), hwnd, rect, title))

# focus + frame capture of the console window specifically
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
import record_screen as rs  # noqa: E402

hit = rs.find_window("小游戏公司总控")
if hit:
    hwnd, (x, y, w, h) = hit
    ok = rs.focus_window("小游戏公司总控")
    time.sleep(1.2)
    # re-read rect AFTER focus (window may move/restore)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    x, y, w, h = rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top
    SW, SH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    x0, y0 = max(0, x), max(0, y)
    w2 = min(x + w, SW) - x0
    h2 = min(y + h, SH) - y0
    w2 -= w2 % 2
    h2 -= h2 % 2
    log.write("focus_ok=%s console_rect_after=(%d,%d,%d,%d) capture=(%d,%d,%d,%d)\n"
              % (ok, x, y, w, h, x0, y0, w2, h2))
    fg = user32.GetForegroundWindow()
    log.write("foreground_hwnd=%d is_target=%s\n" % (fg, fg == hwnd))
    frame = os.path.join(TMP, "probe-biggame-r249-f2.png")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "gdigrab", "-framerate", "5",
           "-offset_x", str(x0), "-offset_y", str(y0),
           "-video_size", "%dx%d" % (w2, h2),
           "-draw_mouse", "0", "-i", "desktop",
           "-frames:v", "1", frame]
    r = subprocess.run(cmd, capture_output=True)
    log.write("ffmpeg_rc=%d frame=%s\n" % (r.returncode, os.path.basename(frame)))
else:
    log.write("console_window_not_found\n")

with open(os.path.join(TMP, "r249-window-owners.txt"), "w", encoding="utf-8") as f:
    f.write(log.getvalue())
print("done rows=%d" % len(rows))
