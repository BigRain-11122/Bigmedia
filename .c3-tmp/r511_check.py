# R511 quick-path anchor check (canon: r510_check lineage, OUTP to new file)
import io, os, re, glob, datetime

OUTP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r511_check.txt"
lines = []

# 1. orders: O- prefixed files count + latest name + mtime; edits after R510 close anchor 12:15:00
od = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\orders"
ofiles = [f for f in os.listdir(od) if f.startswith("O-")]
lines.append("orders_count %d" % len(ofiles))
lates = sorted(ofiles)[-1]
lines.append("orders_latest %s mtime %s" % (lates, datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(od, lates))).strftime("%H:%M:%S")))
edited = []
for f in ofiles:
    p = os.path.join(od, f)
    if datetime.datetime.fromtimestamp(os.path.getmtime(p)) > datetime.datetime(2026, 9, 27, 12, 15, 0):
        edited.append(f)
lines.append("orders_edited_since_anchor %s" % (edited if edited else "NONE"))

# 2. ledger five-mode row count (canon: @BigStream/@七线全司/@全司/@六司/@八线全量, case-sensitive)
lp = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pat = re.compile(r"@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8|@\u516b\u7ebf\u5168\u91cf")
cnt = 0
with io.open(lp, encoding="utf-8") as fh:
    for l in fh:
        if pat.search(l):
            cnt += 1
lines.append("ledger_fivemode_rows %d (anchor 30)" % cnt)

# 3. decisions non-blank count (anchor 45)
dp = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
nb = 0
with io.open(dp, encoding="utf-8") as fh:
    for l in fh:
        if l.strip():
            nb += 1
lines.append("decisions_nonblank %d (anchor 45)" % nb)

# 4. index.lock + production
lock = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.git\index.lock"
lines.append("index_lock %s" % os.path.exists(lock))
sp = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(sp, encoding="utf-8") as fh:
    st = fh.read()
lines.append("production_open %s" % ('"production": "open"' in st))

# 5. storylines three subdomains newest writes (bm-a activity probe)
for sub in ("novel", "audio", "comic"):
    d = os.path.join(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines", sub)
    if not os.path.isdir(d):
        lines.append("storyline_%s MISSING" % sub)
        continue
    fs = [x for x in glob.glob(os.path.join(d, "**", "*"), recursive=True) if os.path.isfile(x)]
    if not fs:
        lines.append("storyline_%s EMPTY" % sub)
        continue
    newest = max(fs, key=os.path.getmtime)
    lines.append("storyline_%s newest %s %s" % (sub, os.path.basename(newest), datetime.datetime.fromtimestamp(os.path.getmtime(newest)).strftime("%m-%d %H:%M")))

# 6. BigLife interchat ledger probe (#72 window <=09-28 12:00)
hit = []
for root, dirs, files in os.walk(r"C:\Users\sjs20\Desktop\FluxGroup"):
    for f in files:
        if ("\u4e92\u804a" in f) and ("BigLife" in root or "biglife" in root.lower()):
            hit.append(os.path.join(root, f))
    if len(hit) > 5:
        break
lines.append("biglife_interchat_hits %d" % len(hit))

# 7. FluxVerse city-window footage probe (#78 render leg gate)
fd = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\footage"
if os.path.isdir(fd):
    fs = [x for x in glob.glob(os.path.join(fd, "**", "*"), recursive=True) if os.path.isfile(x)]
    if fs:
        newest = max(fs, key=os.path.getmtime)
        lines.append("footage_newest %s %s" % (os.path.basename(newest), datetime.datetime.fromtimestamp(os.path.getmtime(newest)).strftime("%m-%d %H:%M")))
    else:
        lines.append("footage EMPTY")
else:
    lines.append("footage MISSING")

# 8. LC-001 batch state probe (R511 focus: #79 piece-1 render leg)
lt = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc001-tmp"
if os.path.isdir(lt):
    fs = sorted(os.listdir(lt))
    lines.append("lc001_tmp_files %s" % ",".join(fs))
else:
    lines.append("lc001_tmp MISSING")
src = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\lc001"
if os.path.isdir(src):
    fs = sorted(os.listdir(src))
    lines.append("lc001_src_files %s" % ",".join(fs))

# 9. s1 result for LC-001
s1p = os.path.join(lt, "s1-result.json")
if os.path.exists(s1p):
    with io.open(s1p, encoding="utf-8") as fh:
        try:
            j = fh.read()
            lines.append("lc001_s1_result_head %s" % j[:300].replace("\n", " "))
        except Exception as e:
            lines.append("lc001_s1_result unreadable %s" % e)
else:
    lines.append("lc001_s1_result MISSING")

# 10. audio duration of LC-001 final track (ffprobe)
import subprocess
aud = None
for cand in ("audio.mp3",):
    p = os.path.join(lt, cand)
    if os.path.exists(p):
        aud = p
if aud:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1", aud], capture_output=True)
    lines.append("lc001_audio_dur %s" % r.stdout.decode().strip())

with io.open(OUTP, "w", encoding="utf-8") as out:
    out.write("\n".join(lines) + "\n")
print("done ->", OUTP)
