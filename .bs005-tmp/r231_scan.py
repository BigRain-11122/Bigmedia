# -*- coding: utf-8 -*-
"""R231 quick-path scans: group ledger @BigStream lines, group decisions non-empty lines, window titles, tmp dir inventory."""
import io, os, re, json

OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.bs005-tmp\r231_scan.txt"
lines_out = []

# 1) group ledger: strict lines containing @BigStream / @七线全司 / @全司 / @六司
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
tokens = ("@BigStream", "@七线全司", "@全司", "@六司")
if os.path.exists(LEDGER):
    txt = io.open(LEDGER, "r", encoding="utf-8", errors="replace").read()
    hits = [ln for ln in txt.splitlines() if any(t in ln for t in tokens)]
    lines_out.append("LEDGER matched lines: %d (anchor=14)" % len(hits))
    for ln in hits[-3:]:
        lines_out.append("  tail: " + ln[:160])
else:
    lines_out.append("LEDGER missing")

# 2) group decisions: UTF-8 non-empty line count (anchor=24)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
if os.path.exists(DEC):
    dtxt = io.open(DEC, "r", encoding="utf-8", errors="replace").read()
    n = len([ln for ln in dtxt.splitlines() if ln.strip()])
    lines_out.append("GROUP decisions non-empty lines: %d (anchor=24)" % n)
else:
    lines_out.append("GROUP decisions missing")

# 3) window titles enumeration (material-window check)
try:
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    titles = []
    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def _cb(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                t = buf.value.strip()
                if t:
                    titles.append(t)
        return True

    user32.EnumWindows(EnumWindowsProc(_cb), 0)
    lines_out.append("WINDOWS visible: %d" % len(titles))
    biggame = [t for t in titles if ("总控" in t) or ("Biggame" in t.lower()) or ("biggame" in t)]
    lines_out.append("BIGGAME master-control windows: %d" % len(biggame))
    tuanjie = [t for t in titles if "Tuanjie" in t or "Unity" in t]
    lines_out.append("Tuanjie/Unity states: " + " | ".join(tuanjie[:8]))
    lines_out.append("all titles: " + " | ".join(titles))
except Exception as e:
    lines_out.append("window enum error: %r" % e)

# 4) sc001-05-v1-tmp inventory
TMP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\audio\sc001-05-v1-tmp"
if os.path.isdir(TMP):
    entries = sorted(os.listdir(TMP))
    lines_out.append("sc001-05-v1-tmp entries %d: %s" % (len(entries), ", ".join(entries)))
else:
    lines_out.append("sc001-05-v1-tmp missing")

# 5) audio dir key files mtime
AUD = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\audio"
for name in ("SC-001-05-v1.mp3", "SC-001-05-v1.srt", "SC-001-05-v1.beats.txt", "README.md"):
    p = os.path.join(AUD, name)
    if os.path.exists(p):
        lines_out.append("audio/%s mtime=%s size=%d" % (name, os.path.getmtime(p), os.path.getsize(p)))
    else:
        lines_out.append("audio/%s MISSING" % name)

# 6) novel/comic progress check (bm-a lanes)
NOVEL = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\novel"
COMIC = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\comic"
if os.path.isdir(NOVEL):
    lines_out.append("novel: " + ", ".join(sorted(os.listdir(NOVEL))))
else:
    lines_out.append("novel dir missing")
if os.path.isdir(COMIC):
    lines_out.append("comic: " + ", ".join(sorted(os.listdir(COMIC))))
else:
    lines_out.append("comic dir missing")

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines_out) + "\n")
print("written", OUT)
