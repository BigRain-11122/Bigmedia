# -*- coding: utf-8 -*-
# R260: visible window enumeration (Biggame console window not found by
# find_window -- record the current desktop state honestly).
import ctypes
import ctypes.wintypes as wt
import io

user32 = ctypes.windll.user32


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                ("right", ctypes.c_long), ("bottom", ctypes.c_long)]


rows = []


def on_enum(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            rect = RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            w, h = rect.right - rect.left, rect.bottom - rect.top
            if w > 200 and h > 150:
                rows.append((buf.value, rect.left, rect.top, w, h))
    return True


WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
user32.EnumWindows(WNDENUMPROC(on_enum), 0)

out = io.StringIO()
out.write("visible_windows=%d\n" % len(rows))
for title, x, y, w, h in rows:
    out.write("%s | %d,%d %dx%d\n" % (title, x, y, w, h))
path = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.bs005-tmp\r260-enum-windows.txt"
io.open(path, "w", encoding="utf-8").write(out.getvalue())
print(out.getvalue())
