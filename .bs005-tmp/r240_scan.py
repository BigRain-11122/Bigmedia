# R240 fast-path scan: ledger/decisions anchors, storylines progress, window enum
# ASCII-only script (encoding law); outputs UTF-8 file
import io, os, ctypes

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".bs005-tmp", "r240-scan.txt")
lines = []

def add(s):
    lines.append(s)

# 1) Group ledger scan: strict line-contains @ for four modes
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
count = 0
matches = []
try:
    with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if ("@BigStream" in ln) or ("@七线全司" in ln) or ("@全司" in ln) or ("@六司" in ln):
                count += 1
                matches.append(ln.strip()[:120])
    add("LEDGER matches: %d (anchor=14)" % count)
    for m in matches[-6:]:
        add("  LED: " + m)
except Exception as e:
    add("LEDGER ERROR: %r" % e)

# 2) Group decisions UTF8 non-empty count (anchor 24 nonempty / 27 total)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8", errors="replace") as f:
        all_lines = f.read().splitlines()
    nonempty = sum(1 for l in all_lines if l.strip())
    add("DECISIONS nonempty: %d total: %d (anchor=24 nonempty / 27 total)" % (nonempty, len(all_lines)))
except Exception as e:
    add("DECISIONS ERROR: %r" % e)

# 3) storylines progress: novel ch.6? comic ep.3? audio latest?
novel_dir = os.path.join(ROOT, "data", "storylines", "novel")
comic_dir = os.path.join(ROOT, "data", "storylines", "comic")
audio_dir = os.path.join(ROOT, "data", "storylines", "audio")
for d, tag in ((novel_dir, "NOVEL"), (comic_dir, "COMIC"), (audio_dir, "AUDIO")):
    try:
        fs = sorted(os.listdir(d))
        add("%s files: %d -> %s" % (tag, len(fs), ", ".join(fs[-8:])))
    except Exception as e:
        add("%s ERROR: %r" % (tag, e))

# 4) Window enumeration (Biggame master-control window?)
try:
    user32 = ctypes.windll.user32
    titles = []
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, l):
        if user32.IsWindowVisible(h):
            n = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(h, n, 512)
            t = n.value.strip()
            if t:
                titles.append(t)
        return True
    user32.EnumWindows(EnumWindowsProc(cb), 0)
    add("WINDOWS visible: %d" % len(titles))
    for t in titles:
        add("  WIN: " + t[:100])
    hit = [t for t in titles if "Biggame" in t or "总控" in t]
    add("BIGGAME-MASTER-CONTROL-HIT: %s" % (hit if hit else "NONE"))
except Exception as e:
    add("WINDOWS ERROR: %r" % e)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK -> %s (%d lines)" % (OUT, len(lines)))
