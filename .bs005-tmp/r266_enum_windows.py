# -*- coding: utf-8 -*-
# R266: enumerate visible top-level window titles (biggame console
# window-not-found state-change verification probe).
import ctypes
import io

user32 = ctypes.windll.user32
titles = []


def enum_cb(hwnd, _lparam):
    if not user32.IsWindowVisible(hwnd):
        return True
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return True
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    titles.append(buf.value)
    return True


WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
out = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.bs005-tmp\r266-enum-windows.txt", "w", encoding="utf-8")
for t in titles:
    out.write(t + "\n")
out.close()
print("count=%d" % len(titles))
