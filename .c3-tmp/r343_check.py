# R343 fast-path check: group anchors, census anchor, storylines, lock
import os, json, glob

REPORT = []

# 1. ledger four-mode token line count (anchor = 21)
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
tokens = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8"]
n = 0
with open(ledger, encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(t in line for t in tokens):
            n += 1
REPORT.append(("ledger_fourmode_lines", n, 21))

# 2. decisions.md non-empty line count (anchor = 33, tail = D-20260926-04)
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with open(dec, encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
nonempty = [l for l in lines if l.strip()]
tail_ids = [l for l in nonempty if l.strip().startswith("D-20260926-04")]
REPORT.append(("decisions_nonempty", len(nonempty), 33))
REPORT.append(("decisions_tail_D-20260926-04", len(tail_ids) >= 1, True))

# 3. census anchors C-00030 / C-00031 (supply gate, canonical position only)
anchors_dir = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
REPORT.append(("anchor_C-00030", os.path.exists(os.path.join(anchors_dir, "C-00030.md")), False))
REPORT.append(("anchor_C-00031", os.path.exists(os.path.join(anchors_dir, "C-00031.md")), False))
anchors = sorted(glob.glob(os.path.join(anchors_dir, "C-*.md")))
REPORT.append(("anchors_last", os.path.basename(anchors[-1]) if anchors else "none", "C-00029.md"))

# 4. storylines new writes on 09-26 (ch.5 v3 / ch.6 landing check, bm-a surface)
story_root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines"
today_hits = []
newest = None
for root, dirs, files in os.walk(story_root):
    for fn in files:
        p = os.path.join(root, fn)
        m = os.path.getmtime(p)
        if newest is None or m > newest[1]:
            newest = (p, m)
        if m >= 1789008000:  # 2026-09-26 00:00 local approx sentinel; refine below
            today_hits.append(p)
# refine: only count files modified after 2026-09-26 00:00 local time
import time
cutoff = time.mktime((2026, 9, 26, 0, 0, 0, 0, 0, -1))
today_hits = []
for root, dirs, files in os.walk(story_root):
    for fn in files:
        p = os.path.join(root, fn)
        if os.path.getmtime(p) >= cutoff:
            today_hits.append(os.path.relpath(p, story_root))
REPORT.append(("storylines_writes_0926", len(today_hits), 0))
REPORT.append(("storylines_newest", time.strftime("%m-%d %H:%M", time.localtime(newest[1])) if newest else "none", "pre-0926"))

# 5. git lock
REPORT.append(("git_index_lock", os.path.exists(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.git\index.lock"), False))

# 6. state.json production field (self-heal check)
st = json.load(open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json", encoding="utf-8"))
REPORT.append(("production", st.get("production"), "open"))
REPORT.append(("tick", st.get("tick"), 342))

ok = True
for name, got, want in REPORT:
    match = (got == want)
    ok = ok and match
    print(f"{name}: got={got!r} want={want!r} {'OK' if match else 'DIFF'}")
print("ALL_OK" if ok else "HAS_DIFF")
