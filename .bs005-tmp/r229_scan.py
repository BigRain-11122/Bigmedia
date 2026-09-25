import os, re, glob, io, ctypes
from ctypes import wintypes

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
OUT = []

# 1. orders latest
orders = sorted(glob.glob(os.path.join(BS, "orders", "*.md")))
OUT.append("ORDERS_TOP: " + (os.path.basename(orders[-1]) if orders else "none"))

# 2. ledger strict @-prefix four-mode scan
ledger = os.path.join(ROOT, "cph4", "evolution-ledger.md")
pat = re.compile(r"@(BigStream|七线全司|全司|六司)")
n = 0
with io.open(ledger, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if pat.search(line):
            n += 1
OUT.append("LEDGER_AT_LINES: %d (anchor 14)" % n)

# 3. decisions.md UTF8 non-empty lines
dec = os.path.join(ROOT, "docs", "decisions.md")
with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
    lines = [l for l in f.read().splitlines() if l.strip()]
OUT.append("DECISIONS_NONEMPTY: %d (anchor 24)" % len(lines))

# 4. novel/comic progress
nov = sorted(glob.glob(os.path.join(BS, "data", "storylines", "novel", "*.md")))
OUT.append("NOVEL_FILES: " + ", ".join(os.path.basename(p) for p in nov))
com = sorted(glob.glob(os.path.join(BS, "data", "storylines", "comic", "*")))
OUT.append("COMIC_FILES: " + ", ".join(os.path.basename(p) for p in com))

# 5. window enumeration (material window check: Biggame console)
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
OUT.append("WINDOW_COUNT: %d" % len(titles))
OUT.append("BIGGAME_CONSOLE: %s" % any("Biggame" in t for t in titles))
OUT.append("WINDOW_TITLES:")
OUT.extend(" - " + t for t in titles)

res = os.path.join(BS, ".bs005-tmp", "r229_scan.txt")
with io.open(res, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("OK lines:", len(OUT))
