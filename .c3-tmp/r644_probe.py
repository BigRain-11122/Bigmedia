import json, os, re, subprocess, glob, io, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
CPH4 = r'C:\Users\sjs20\Desktop\FluxGroup\cph4'
HQDOCS = r'C:\Users\sjs20\Desktop\FluxGroup\docs'

os.makedirs(os.path.join(ROOT, '.c3-tmp'), exist_ok=True)
f = io.open(os.path.join(ROOT, '.c3-tmp', 'r644_summary.txt'), 'w', encoding='utf-8')

# 1. state.json
s = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
f.write(f"tick={s.get('tick')} production={s.get('production')} ts={s.get('ts')}\n")
f.write(f"task={s.get('task')}\n")
log = s.get('log', [])
f.write(f"log_len={len(log)}\n")
for line in log[-4:]:
    f.write("LOG| " + line + "\n")

# 2. orders latest
odir = os.path.join(ROOT, 'orders')
files = [(os.path.getmtime(os.path.join(odir, x)), x) for x in os.listdir(odir)]
files.sort()
f.write("\nORDERS (newest 6):\n")
for mt, x in files[-6:]:
    f.write(f"  {datetime.datetime.fromtimestamp(mt).strftime('%m-%d %H:%M')} {x}\n")

# 3. git status
r = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True)
f.write("\nGIT_STATUS:\n" + (r.stdout.strip() or '(clean)') + "\n")
r2 = subprocess.run(['git', 'log', '--oneline', '-3'], cwd=ROOT, capture_output=True, text=True)
f.write("GIT_LOG:\n" + r2.stdout)

# 4. ledger scan
led = os.path.join(CPH4, 'evolution-ledger.md')
pat = re.compile(r'@BigStream|@七线全司|@全司|@六司|@八线')
lines = io.open(led, encoding='utf-8').read().splitlines()
hits = [(i + 1, l) for i, l in enumerate(lines) if pat.search(l)]
f.write(f"\nLEDGER total_lines={len(lines)} strict_at_hits={len(hits)}\n")
for i, l in hits[-3:]:
    f.write(f"  L{i}: {l[:130]}\n")

# 5. decisions count
dec = os.path.join(HQDOCS, 'decisions.md')
dl = [l for l in io.open(dec, encoding='utf-8').read().splitlines() if l.strip()]
f.write(f"\nDECISIONS nonempty_lines={len(dl)}\n")
for l in dl[-3:]:
    f.write(f"  {l[:130]}\n")

# 6. E4 pending results (files modified since 09-28)
f.write("\nE4/e4-ish files mtime>=09-28:\n")
cands = glob.glob(os.path.join(ROOT, '**', 'e4*'), recursive=True)
now = datetime.datetime.now()
for p in sorted(cands, key=os.path.getmtime):
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(p))
    if mt >= datetime.datetime(2026, 9, 28):
        f.write(f"  {mt.strftime('%m-%d %H:%M')} {os.path.relpath(p, ROOT)}\n")

evdirs = [d for d in glob.glob(os.path.join(ROOT, '**', 'expert-verdicts'), recursive=True) if os.path.isdir(d)]
for ev in evdirs[:1]:
    evf = [(os.path.getmtime(os.path.join(ev, x)), x) for x in os.listdir(ev)]
    evf.sort()
    f.write("EXPERT_VERDICTS (newest 6):\n")
    for mt, x in evf[-6:]:
        f.write(f"  {datetime.datetime.fromtimestamp(mt).strftime('%m-%d %H:%M')} {x}\n")
if not evdirs:
    f.write("EXPERT_VERDICTS dir not found\n")

# 7. routine files
f.write("\nROUTINE:\n")
f.write(f"daily_brief_0929={os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-29.md'))}\n")
aud = glob.glob(os.path.join(ROOT, 'docs', 'audits', '*self-audit*.md'))
aud.sort(key=os.path.getmtime)
for p in aud[-3:]:
    f.write(f"  audit: {os.path.basename(p)}\n")

# 8. global benchmarks update record
gb = os.path.join(ROOT, 'docs', 'global-benchmarks.md')
if os.path.exists(gb):
    txt = io.open(gb, encoding='utf-8').read()
    m = re.search(r'更新记录[^\n]*\n(.{0,400})', txt)
    if m:
        f.write("GB_UPDATE_RECORD_HEAD:\n")
        for l in m.group(1).splitlines()[:3]:
            f.write("  " + l[:130] + "\n")

# 9. src py list
f.write("\nSRC_PY:\n")
for x in sorted(os.listdir(os.path.join(ROOT, 'src'))):
    if x.endswith('.py'):
        f.write("  " + x + "\n")

f.close()
print('done')
