import os, re, json, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(ROOT)  # media/
FLUX = os.path.dirname(BASE)  # FluxGroup
out = []
A = out.append

# 1. orders: new or edited since anchor (top = O-20260927-1050-HQ-C.md, mtime 12:36:52)
orders_dir = os.path.join(ROOT, 'orders')
files = [(f, os.path.getmtime(os.path.join(orders_dir, f))) for f in os.listdir(orders_dir) if f != 'README.md']
files.sort(key=lambda x: x[1], reverse=True)
top_name, top_mt = files[0]
A(f"orders: count={len(files)} top={top_name} mtime={datetime.datetime.fromtimestamp(top_mt)}")
anchor = datetime.datetime(2026, 9, 27, 12, 36, 53)
recent = [(f, datetime.datetime.fromtimestamp(m)) for f, m in files if m > anchor.timestamp()]
A(f"orders new/edited since R511 anchor: {recent if recent else 'NONE'}")

# 2. ledger five-mode line count (anchor=31)
ledger = os.path.join(FLUX, 'cph4', 'evolution-ledger.md')
try:
    with open(ledger, encoding='utf-8') as fh:
        lines = fh.readlines()
    pats = ('@BigStream', '@七线全司', '@全司', '@六司', '@八线全量')
    hits = [l for l in lines if any(p in l for p in pats)]
    A(f"ledger five-mode lines={len(hits)} (anchor 31) new={'YES' if len(hits)!=31 else 'no'}")
    if len(hits) != 31:
        A("NEW LINES:")
        for l in hits[-5:]:
            A("  " + l.strip()[:200])
except Exception as e:
    A(f"ledger ERR {e}")

# 3. group decisions.md non-empty UTF8 line count (anchor=56)
dec = os.path.join(FLUX, 'docs', 'decisions.md')
try:
    with open(dec, encoding='utf-8-sig') as fh:
        dl = [l for l in fh if l.strip()]
    A(f"decisions non-empty lines={len(dl)} (anchor 56) new={'YES' if len(dl)!=56 else 'no'}")
    if len(dl) > 56:
        A("NEW TAIL:")
        for l in dl[56:]:
            A("  " + l.strip()[:200])
except Exception as e:
    A(f"decisions ERR {e}")

# 4. index.lock
lock = os.path.join(ROOT, '.git', 'index.lock')
A(f"index.lock exists={os.path.exists(lock)}")

# 5. production flag self-heal check
with open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8') as fh:
    st = fh.read()
m = re.search(r'"production"\s*:\s*"(\w+)"', st)
A(f"production={m.group(1) if m else 'NOT-FOUND'}")

# 6. #78 FluxVerse footage arrival check (anchor: nothing after 09-25 19:46 in data/sources/footage/)
foot = os.path.join(ROOT, 'data', 'sources', 'footage')
entries = []
for f in os.listdir(foot):
    p = os.path.join(foot, f)
    entries.append((f, datetime.datetime.fromtimestamp(os.path.getmtime(p))))
entries.sort(key=lambda x: x[1], reverse=True)
cut = datetime.datetime(2026, 9, 25, 19, 47)
fresh = [(f, m) for f, m in entries if m > cut]
A(f"footage total={len(entries)} fresh-after-0925-1946={fresh if fresh else 'NONE'}")
A(f"footage top3: {entries[:3]}")

# 7. CENSUS supply gate: anchors C-00030/31
anchors_dir = os.path.join(FLUX, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(anchors_dir):
    ids = sorted(f for f in os.listdir(anchors_dir) if f.startswith('C-'))
    A(f"anchors top={ids[-3:]} C-00030-in={'C-00030.md' in ids} C-00031-in={'C-00031.md' in ids}")

# 8. daily brief 09-27 / 09-28
A(f"daily 09-27 exists={os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-09-27.md'))}")
A(f"daily 09-28 exists={os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-09-28.md'))}")

# 9. W40 audit existence
adir = os.path.join(ROOT, 'docs', 'audits')
if os.path.isdir(adir):
    A(f"W40 audit exists={any('2026-W40' in f for f in os.listdir(adir))}")
else:
    A("audits dir missing")

# 10. HQ-FEEDBACK today lines (last logged action F-20260927-05 in R511)
hq = os.path.join(ROOT, 'HQ-FEEDBACK.md')
with open(hq, encoding='utf-8') as fh:
    hl = [l for l in fh if 'F-20260927' in l]
A(f"HQ-FEEDBACK 09-27 lines={len(hl)} last={hl[-1].strip()[:150] if hl else 'NONE'}")

# 11. global-benchmarks refresh date (next ~10-01)
gb = os.path.join(ROOT, 'docs', 'global-benchmarks.md')
with open(gb, encoding='utf-8') as fh:
    gl = fh.read()
m2 = re.search(r'2026-(\d{2})-(\d{2})', gl)
A(f"global-benchmarks first-date={m2.group(0) if m2 else 'NONE'}")

with open(os.path.join(ROOT, '.c3-tmp', 'r516_check_out.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print("OK", len(out))
