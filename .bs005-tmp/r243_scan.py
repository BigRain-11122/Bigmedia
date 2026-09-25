import os, json, glob, datetime, ctypes, subprocess, sys

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = []

def sec(t):
    return "\n== " + t + " =="

# 1. orders tail
OUT.append(sec("ORDERS"))
orders = sorted(glob.glob(os.path.join(REPO, 'orders', '*')))
for f in orders[-3:]:
    OUT.append(os.path.basename(f) + " | mtime " + datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m-%d %H:%M'))

# 2. index.lock
OUT.append(sec("GIT"))
OUT.append("index.lock: " + ("YES" if os.path.exists(os.path.join(REPO, '.git', 'index.lock')) else "NO"))
try:
    head = subprocess.run(['git', 'log', '-1', '--format=%h %ad %s', '--date=format:%H:%M'],
                          capture_output=True, text=True, cwd=REPO).stdout.strip()
    OUT.append("HEAD: " + head)
except Exception as e:
    OUT.append("HEAD err " + str(e))

# 3. ledger scan (strict line-contains @ four patterns)
OUT.append(sec("LEDGER"))
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
cnt = 0
tail_hits = []
if os.path.exists(ledger):
    with open(ledger, encoding='utf-8', errors='replace') as fh:
        for ln in fh:
            if ('@BigStream' in ln) or ('@七线全司' in ln) or ('@全司' in ln) or ('@六司' in ln):
                cnt += 1
                tail_hits.append(ln.strip()[:110])
OUT.append("at_lines: %d (anchor 15)" % cnt)
for h in tail_hits[-3:]:
    OUT.append("  hit: " + h)
OUT.append("ledger mtime: " + datetime.datetime.fromtimestamp(os.path.getmtime(ledger)).strftime('%m-%d %H:%M') if os.path.exists(ledger) else "ledger missing")

# 4. decisions non-empty UTF8
OUT.append(sec("DECISIONS"))
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
if os.path.exists(dec):
    with open(dec, encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    ne = [l for l in lines if l.strip()]
    OUT.append("nonempty_utf8: %d (anchor 29) / total: %d (anchor 32)" % (len(ne), len(lines)))
    for l in ne[-2:]:
        OUT.append("  d: " + l.strip()[:100])
    OUT.append("mtime: " + datetime.datetime.fromtimestamp(os.path.getmtime(dec)).strftime('%m-%d %H:%M'))

# 5. storylines progress (bm-a face: novel ch.6 / comic ep.3)
OUT.append(sec("STORYLINES"))
for sub in ['novel', 'comic', 'audio']:
    d = os.path.join(REPO, 'data', 'storylines', sub)
    if os.path.isdir(d):
        names = sorted(os.listdir(d))
        newest = max((os.path.getmtime(os.path.join(d, n)), n) for n in names if os.path.isfile(os.path.join(d, n))) if any(os.path.isfile(os.path.join(d, n)) for n in names) else (0, '-')
        OUT.append(sub + ": " + ", ".join(names[:10]) + (" | newest " + newest[1] + " " + datetime.datetime.fromtimestamp(newest[0]).strftime('%m-%d %H:%M') if newest[1] != '-' else ""))

# 6. backlog head (open items)
OUT.append(sec("BACKLOG_TOP"))
bl = os.path.join(REPO, 'src', 'os', 'backlog.md')
with open(bl, encoding='utf-8', errors='replace') as fh:
    blines = fh.read().splitlines()
shown = 0
for i, l in enumerate(blines):
    s = l.strip()
    if not s:
        continue
    OUT.append("L%02d: %s" % (i, s[:130]))
    shown += 1
    if shown >= 14:
        break

# 7. self-improvement queue mtime
OUT.append(sec("MISC"))
q = os.path.join(REPO, 'docs', 'self-improvement-queue.md')
if os.path.exists(q):
    OUT.append("queue mtime: " + datetime.datetime.fromtimestamp(os.path.getmtime(q)).strftime('%m-%d %H:%M'))
st = os.path.join(REPO, 'src', 'os', 'state.json')
with open(st, encoding='utf-8') as fh:
    s = json.load(fh)
OUT.append("state tick=%s ts=%s" % (s.get('tick'), s.get('ts')))
hq = os.path.join(REPO, 'HQ-FEEDBACK.md')
OUT.append("hq-feedback mtime: " + datetime.datetime.fromtimestamp(os.path.getmtime(hq)).strftime('%m-%d %H:%M') if os.path.exists(hq) else "hq missing")

# 8. window enumeration: Biggame master window?
OUT.append(sec("WINDOWS"))
user32 = ctypes.windll.user32
titles = []
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        n = user32.GetWindowTextLengthW(hwnd)
        if n > 0:
            buf = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(hwnd, buf, n + 1)
            titles.append(buf.value)
    return True
user32.EnumWindows(EnumWindowsProc(cb), 0)
OUT.append("visible_windows: %d" % len(titles))
bg = [t for t in titles if 'Biggame' in t or '总控' in t]
OUT.append("biggame_master_window: " + ("YES -> " + "|".join(bg) if bg else "NO"))
for t in sorted(titles):
    OUT.append("  win: " + t[:80])

# 9. three probes
OUT.append(sec("PROBES"))
probes = [
    ("board", [sys.executable, 'src/board_check.py']),
    ("readiness", [sys.executable, 'src/readiness.py']),
    ("loop_health", [sys.executable, 'src/os/loop_health.py']),
]
for name, cmd in probes:
    r = subprocess.run(cmd, capture_output=True, cwd=REPO)
    out = (r.stdout + r.stderr).decode('utf-8', errors='replace')
    tail = [l for l in out.splitlines() if l.strip()][-8:]
    OUT.append("-- %s exit=%d" % (name, r.returncode))
    for l in tail:
        OUT.append("   " + l.strip()[:150])

with open(os.path.join(REPO, '.bs005-tmp', 'r243-scan-all.txt'), 'w', encoding='utf-8') as fh:
    fh.write("\n".join(OUT))
print("DONE")
