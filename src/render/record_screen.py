# -*- coding: utf-8 -*-
"""Screen-capture station (R-S, O-20260924-1115-bm-a real-footage order).

Records a live app window by title using pure-python window lookup
(ctypes user32) + FFmpeg gdigrab region capture (zero install, local).
Output = raw landscape mp4 for the vertical pre-process + renderer
--bgvideo pipeline.

Helpers:
    find_window(title_part)  -> (hwnd, (x, y, w, h)) or None   [pure-ish]
    open_edge_app(url)       -> launches Edge app-mode window    [action]
    close_window(title_part)-> graceful close by title           [action]

CLI:
    python src/render/record_screen.py --open-app URL --title T \
        --seconds 45 --out FILE [--fps 15] [--close]

ASCII rule: source pure ASCII; window titles/URLs arrive as argv data.
Exit codes: 0 ok; 2 bad args/window not found; 3 ffmpeg failed.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

import ctypes
from ctypes import wintypes


def find_window(title_part):
    """Enumerate visible top-level windows, return the first whose title
    contains title_part -> (hwnd, (x, y, w, h)); None if not found."""
    user32 = ctypes.windll.user32
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def on_enum(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        if title_part in buf.value:
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            found.append((hwnd, (rect.left, rect.top,
                                 rect.right - rect.left,
                                 rect.bottom - rect.top)))
            return False  # stop enumeration
        return True

    user32.EnumWindows(on_enum, 0)
    return found[0] if found else None


def close_window(title_part):
    """Graceful close of the first window whose title contains the part.
    Returns True if a window was found and asked to close."""
    hit = find_window(title_part)
    if not hit:
        return False
    ctypes.windll.user32.PostMessageW(hit[0], 0x0010, 0, 0)  # WM_CLOSE
    return True


def focus_window(title_part):
    """Bring the window to front before capture. gdigrab records the
    desktop REGION, not the window - if another app (e.g. a maximized
    editor) sits on top, the recording shows the wrong app. 2026-09-24:
    the CityWatch and fleet-monitor shots captured a Unity editor."""
    hit = find_window(title_part)
    if not hit:
        return False
    user32 = ctypes.windll.user32
    user32.ShowWindow(hit[0], 9)   # SW_RESTORE
    user32.SetForegroundWindow(hit[0])
    return True


def open_edge_app(url):
    """Launch Edge in app mode (clean window, no tabs). Best effort."""
    subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Start-Process msedge -ArgumentList @('--app=%s')" % url],
        capture_output=True)
    time.sleep(4.0)  # engine boot + canvas first frames


def record_region(rect, seconds, out, fps=15):
    """gdigrab region capture -> mp4 (libx264 crf 23).
    NB: region w/h are floored to even - libx264+yuv420p rejects odd
    dims (first-run crash exit 3752568763 on a 1366x1079 window)."""
    x, y, w, h = rect
    w -= w % 2
    h -= h % 2
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "gdigrab",
           "-framerate", str(int(fps)),
           "-offset_x", str(int(x)), "-offset_y", str(int(y)),
           "-video_size", "%dx%d" % (int(w), int(h)),
           "-draw_mouse", "1",
           "-i", "desktop",
           "-t", "%.2f" % float(seconds),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-pix_fmt", "yuv420p", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stderr


def main(argv=None):
    ap = argparse.ArgumentParser(description="screen-capture station R-S")
    ap.add_argument("--open-app", help="URL to open in Edge app mode first")
    ap.add_argument("--title", required=True,
                    help="window title part to capture")
    ap.add_argument("--seconds", type=float, default=45.0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--close", action="store_true",
                    help="close the captured window afterwards")
    ap.add_argument("--wait", type=float, default=2.0,
                    help="settle time after window is found")
    args = ap.parse_args(argv)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.open_app:
        open_edge_app(args.open_app)
    for _ in range(10):
        hit = find_window(args.title)
        if hit:
            break
        time.sleep(1.0)
    if not hit:
        print("FAIL window not found: %s" % args.title)
        return 2
    hwnd, rect = hit
    print("OK window hwnd=%s rect=%s" % (hwnd, rect))
    focus_window(args.title)   # gdigrab records the region, front it (2026-09-24 lesson)
    time.sleep(args.wait)
    code, err = record_region(rect, args.seconds, out, args.fps)
    if code != 0:
        print("FAIL ffmpeg exit %d" % code)
        print(err[-600:])
        return 3
    if args.close:
        close_window(args.title)
        print("OK window closed")
    size_kb = out.stat().st_size // 1024
    print("OK recorded %s (%ds @%dfps, %dKB)" % (out, args.seconds, args.fps, size_kb))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
