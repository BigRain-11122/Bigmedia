# R242 fast-path scan: orders top, backlog top, ledger/decisions anchors, storylines, window enum
# ASCII-only script (encoding law); outputs UTF-8 file
import io, os, ctypes, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".bs005-tmp", "r242-scan.txt")
lines = []

def add(s):
    lines.append(s)

# 0) orders dir: latest file by mtime (recorded: O-20260925-1153-BG-C)
od = os.path.join(ROOT, "orders")
try:
    ents = []
    for fn in os.listdir(od):
        p = os.path.join(od, fn)
        if os.path.isfile(p):
            ents.append((os.path.getmtime(p), fn))
    ents.sort(reverse=True)
    add("ORDERS latest 3:")
    for m, fn in ents[:3]:
        add("  ORD: %s  %s" % (datetime.datetime.fromtimestamp(m).strftime("%m-%d %H:%M"), fn))
except Exception as e:
    add("ORDERS ERROR: %r" % e)

# 0b) backlog top lines
bl = os.path.join(ROOT, "src", "os", "backlog.md")
try:
    with io.open(bl, "r", encoding="utf-8", errors="replace") as f:
        bls = f.read().splitlines()
    add("BACKLOG top 6 lines:")
    for l in bls[:6]:
        add("  BL: " + l.strip()[:150])
except Exception as e:
    add("BACKLOG ERROR: %r" % e)

# 1) Group ledger scan: strict line-contains @ for four modes (anchor=15 after P-03)
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
count = 0
matches = []
try:
    with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if ("@BigStream" in ln) or ("@七线全司" in ln) or ("@全司" in ln) or ("@六司" in ln):
                count += 1
                matches.append(ln.strip()[:120])
    add("LEDGER matches: %d (anchor=15)" % count)
    for m in matches[-6:]:
        add("  LED: " + m)
except Exception as e:
    add("LEDGER ERROR: %r" % e)

# 2) Group decisions UTF8 non-empty count (anchor=29 nonempty / 32 total after D-07..11)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8", errors="replace") as f:
        all_lines = f.read().splitlines()
    nonempty = sum(1 for l in all_lines if l.strip())
    add("DECISIONS nonempty: %d total: %d (anchor=29 nonempty / 32 total)" % (nonempty, len(all_lines)))
    if nonempty != 29:
        add("  DEC TAIL:")
        for l in all_lines[-8:]:
            if l.strip():
                add("   D: " + l.strip()[:150])
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
        newest = None
        for fn in fs:
            p = os.path.join(d, fn)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if newest is None or m > newest[0]:
                newest = (m, fn)
        if newest:
            add("  %s newest: %s %s" % (tag, datetime.datetime.fromtimestamp(newest[0]).strftime("%m-%d %H:%M"), newest[1]))
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

# 5) Routine files existence
daily = os.path.join(ROOT, "data", "intel", "daily", "2026-09-25.md")
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
add("DAILY-BRIEF 2026-09-25: %s" % os.path.exists(daily))
ad = os.path.join(ROOT, "docs", "audits")
try:
    fs = sorted(os.listdir(ad))
    add("AUDITS dir: %s" % ", ".join(fs))
except Exception as e:
    add("AUDITS ERROR: %r" % e)
try:
    with io.open(gb, "r", encoding="utf-8", errors="replace") as f:
        gbl = f.read().splitlines()
    for l in gbl:
        if l.strip().startswith("2026-"):
            add("GB first-date-line: " + l.strip()[:80])
            break
except Exception as e:
    add("GB ERROR: %r" % e)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK -> %s (%d lines)" % (OUT, len(lines)))
