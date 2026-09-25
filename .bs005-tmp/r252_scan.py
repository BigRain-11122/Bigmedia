# R252 fast-path scan: ledger @ lines, group decisions count, novel/comic progress,
# window enumeration (Biggame master-control + Edge dashboard check for leg-2),
# three probes. Output written to UTF-8 files (encoding law: no console-trust for CJK).
import ctypes
import datetime
import glob
import io
import os
import subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".bs005-tmp")
now = datetime.datetime.now()

buf = io.StringIO()
buf.write("now=%s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))

# --- 1. group ledger scan (strict line-contains-@ four modes) ---
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
tokens = ["@BigStream", "@七线全司", "@全司", "@六司"]
hits = []
try:
    with open(ledger, encoding="utf-8", errors="replace") as f:
        for line in f:
            if any(t in line for t in tokens):
                hits.append(line.rstrip("\n")[:160])
    buf.write("ledger_at_lines=%d (anchor=15)\n" % len(hits))
    for h in hits:
        buf.write("  L| " + h + "\n")
except Exception as e:
    buf.write("ledger_err=%r\n" % e)

# --- 2. group decisions count (UTF8 non-empty anchor=29, total=32) ---
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with open(dec, encoding="utf-8", errors="replace") as f:
        dl = f.read().splitlines()
    nonempty = sum(1 for l in dl if l.strip())
    buf.write("decisions_total=%d nonempty=%d (anchor nonempty=29 total=32)\n" % (len(dl), nonempty))
except Exception as e:
    buf.write("decisions_err=%r\n" % e)

# --- 3. novel / comic progress (bm-a lines) ---
novel = sorted(os.path.basename(x) for x in glob.glob(os.path.join(ROOT, "data", "storylines", "novel", "*")))
comic = sorted(os.path.basename(x) for x in glob.glob(os.path.join(ROOT, "data", "storylines", "comic", "*")))
buf.write("novel_files=%s\n" % novel)
buf.write("comic_files=%s\n" % comic)

# --- 4. window enumeration (Biggame master-control + Edge dashboard check) ---
user32 = ctypes.windll.user32
titles = []
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)


def _cb(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            b = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, b, length + 1)
            titles.append(b.value)
    return True


user32.EnumWindows(EnumWindowsProc(_cb), 0)
biggame = [t for t in titles if ("Biggame" in t) or ("总控" in t)]
dashboard = [t for t in titles if ("硅基生命元宇宙" in t) or ("元宇宙" in t)]
buf.write("window_count=%d biggame_hits=%d dashboard_hits=%d\n" % (len(titles), len(biggame), len(dashboard)))
for t in titles:
    buf.write("  W| " + t + "\n")

with open(os.path.join(TMP, "r252-scan.txt"), "w", encoding="utf-8") as f:
    f.write(buf.getvalue())

# --- 5. three probes (capture to UTF-8 files) ---
probes = [
    ("board", [os.path.join(ROOT, "src", "board_check.py")]),
    ("readiness", [os.path.join(ROOT, "src", "readiness.py")]),
    ("loop", [os.path.join(ROOT, "src", "os", "loop_health.py")]),
]
summary = []
for name, args in probes:
    try:
        r = subprocess.run(["python"] + args, capture_output=True, timeout=300, cwd=ROOT)
        text = (r.stdout or b"").decode("utf-8", errors="replace")
        err = (r.stderr or b"").decode("utf-8", errors="replace")
        with open(os.path.join(TMP, "probe-r252-%s.txt" % name), "w", encoding="utf-8") as f:
            f.write("exit=%d\n" % r.returncode)
            f.write(text)
            if err:
                f.write("\n--- stderr ---\n")
                f.write(err)
        summary.append("%s exit=%d" % (name, r.returncode))
    except Exception as e:
        summary.append("%s err=%r" % (name, e))

with open(os.path.join(TMP, "r252-scan.txt"), "a", encoding="utf-8") as f:
    f.write("probes: " + "; ".join(summary) + "\n")

print("OK now=%s ledger=%d biggame=%d dashboard=%d %s" % (
    now.strftime("%H:%M:%S"),
    len(hits), len(biggame), len(dashboard), "; ".join(summary)))
