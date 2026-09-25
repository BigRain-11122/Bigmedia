import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
titles = []

@ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
def cb(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            titles.append(buf.value)
    return True

user32.EnumWindows(cb, 0)
with open(r".bs005-tmp\windows-R218.txt", "w", encoding="utf-8") as f:
    for t in titles:
        f.write(t + "\n")
print("count:", len(titles))
print("biggame_window:", any("Biggame" in t for t in titles))
print("tuanjie_titles:")
for t in titles:
    if "Tuanjie" in t or "Unity" in t or "Game" in t:
        print(" -", t[:60])
