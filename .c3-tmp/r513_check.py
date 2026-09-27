# -*- coding: utf-8 -*-
"""R513 fast-path five-check probe (write_file created, OUTP=new file, zero PS roundtrip).
Anchors: orders O- 35 (top O-20260927-1050-HQ-C mtime 12:14:29=R510 footprint);
ledger @ five-mode line count 31 (R511 new anchor); decisions non-empty 56;
C-00030/C-00031 anchors absent; interchat ledger consumed R512; daily 09-27 in case.
"""
import io, os, json, glob, datetime

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r513_check.txt")
lines = []

def w(s):
    lines.append(s)

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"

# 1. orders: O- prefix count + new/edited since anchor
orders_dir = os.path.join(ROOT, "orders")
o_files = [f for f in os.listdir(orders_dir) if f.startswith("O-")]
o_files.sort(key=lambda f: os.path.getmtime(os.path.join(orders_dir, f)))
w("orders_O_count=%d" % len(o_files))
w("orders_top=%s mtime=%s" % (o_files[-1], datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(orders_dir, o_files[-1]))).strftime("%H:%M:%S")))
anchor = os.path.join(orders_dir, "O-20260927-1050-HQ-C.md")
am = os.path.getmtime(anchor)
new_o = [f for f in o_files if os.path.getmtime(os.path.join(orders_dir, f)) > am and f != "O-20260927-1050-HQ-C.md"]
edited = [f for f in o_files if f != "O-20260927-1050-HQ-C.md" and os.path.getmtime(os.path.join(orders_dir, f)) > am]
# anchor itself edited since 12:14:29+delta? record its mtime only
w("orders_new_after_anchor=%s" % (new_o if new_o else "NONE"))
w("orders_edited_since_anchor=%s" % (edited if edited else "NONE"))

# 2. ledger five-mode @ prefix line count (strict, case-sensitive)
ledger = os.path.join(GRP, "cph4", "evolution-ledger.md")
cnt = 0
tail_hits = []
with io.open(ledger, "r", encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        s = ln.strip()
        for m in ("@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"):
            if m in s:
                cnt += 1
                tail_hits.append(s[:80])
                break
w("ledger_at_count=%d (anchor 31)" % cnt)
for t in tail_hits[-3:]:
    w("  ledger_tail=%s" % t)

# 3. decisions non-empty count
dec = os.path.join(GRP, "docs", "decisions.md")
n = 0
with io.open(dec, "r", encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        if ln.strip():
            n += 1
w("decisions_nonempty=%d (anchor 56)" % n)

# 4. C-00030/C-00031 anchors in BigLife census/anchors
anchors_dir = r"C:\Users\sjs20\Desktop\FluxGroup\biglife\data\census\anchors"
if not os.path.isdir(anchors_dir):
    anchors_dir = r"C:\Users\sjs20\Desktop\FluxGroup\BigLife\data\census\anchors"
a30 = os.path.isfile(os.path.join(anchors_dir, "C-00030.md"))
a31 = os.path.isfile(os.path.join(anchors_dir, "C-00031.md"))
all_a = sorted([f for f in os.listdir(anchors_dir) if f.endswith(".md")]) if os.path.isdir(anchors_dir) else []
w("anchor_C00030=%s anchor_C00031=%s last3=%s" % (a30, a31, all_a[-3:] if all_a else []))

# 5. daily brief 09-27 / 09-28 presence
d27 = os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")
d28 = os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md")
w("daily_0927=%s daily_0928=%s" % (os.path.isfile(d27), os.path.isfile(d28)))

# 6. production state + index.lock
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8"))
w("production=%s tick=%d" % (st.get("production"), st.get("tick")))
w("index_lock=%s" % os.path.isfile(os.path.join(ROOT, ".git", "index.lock")))

# 7. storylines new writes after 09-27 04:44 (R512 window)
cut = datetime.datetime(2026, 9, 27, 4, 44).timestamp()
for sub in ("novel", "audio", "comic", "video"):
    p = os.path.join(ROOT, "data", "storylines", sub)
    if not os.path.isdir(p):
        w("storyline_%s=MISSING_DIR" % sub)
        continue
    fresh = [f for f in os.listdir(p) if os.path.getmtime(os.path.join(p, f)) > cut]
    w("storyline_%s_fresh=%s" % (sub, len(fresh)))

# 8. interchat ledger window item (BigLife) - consumed R512, presence only
il = glob.glob(r"C:\Users\sjs20\Desktop\FluxGroup\biglife\data\cognition\interchat-ledger.jsonl") or glob.glob(r"C:\Users\sjs20\Desktop\FluxGroup\BigLife\data\cognition\interchat-ledger.jsonl")
w("interchat_present=%s" % bool(il))

# 9. drafts pool for BS-006 selection
dr = os.path.join(ROOT, "data", "drafts")
if os.path.isdir(dr):
    w("drafts_files=%s" % sorted(os.listdir(dr)))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("OK wrote %d lines" % len(lines))
