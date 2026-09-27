import json, os, subprocess
from datetime import datetime

R = {}
def w(k, v): R[k] = v

# 1. orders anchor (expect 35 O- files, anchor mtime 13:53:11 = R515 footprint)
orders_dir = "orders"
o_files = [f for f in os.listdir(orders_dir) if f.startswith("O-") and f.endswith(".md")]
w("orders_o_count", len(o_files))
anchor = os.path.join(orders_dir, "O-20260927-1050-HQ-C.md")
am = os.path.getmtime(anchor)
w("orders_anchor_mtime", datetime.fromtimestamp(am).strftime("%Y-%m-%d %H:%M:%S"))
newer = [f for f in o_files if os.path.getmtime(os.path.join(orders_dir, f)) > am]
w("orders_newer_than_anchor", newer)

# 2. ledger five-pattern line count (expect 31)
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
cnt, hits = 0, []
with open(ledger, encoding="utf-8") as fh:
    for line in fh:
        if any(p in line for p in pats):
            cnt += 1
            hits.append(line.strip()[:100])
w("ledger_lines", cnt)
w("ledger_last2", hits[-2:])
w("ledger_mtime", datetime.fromtimestamp(os.path.getmtime(ledger)).strftime("%Y-%m-%d %H:%M:%S"))

# 3. decisions UTF-8 non-empty lines (expect 56)
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with open(dec, encoding="utf-8") as fh:
    dcount = sum(1 for line in fh if line.strip())
w("decisions_nonempty", dcount)
w("decisions_mtime", datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%Y-%m-%d %H:%M:%S"))

# 4. production self-heal check
with open("src/os/state.json", encoding="utf-8") as fh:
    st = json.load(fh)
w("production", st.get("production"))
w("tick", st.get("tick"))

# 5. footage top (#78 FluxVerse 实录到位核验; expect top=census-card-v7-vertical 09-27 12:32 R511 self-produced)
foot = "data/sources/footage"
entries = sorted(((os.path.getmtime(os.path.join(foot, f)), f) for f in os.listdir(foot)), reverse=True)
w("footage_top3", [(datetime.fromtimestamp(t).strftime("%m-%d %H:%M"), n) for t, n in entries[:3]])

# 6. BigLife anchors (#63 supply gate; expect top C-00029, C-00030/31 absent)
anchors = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
a = sorted(os.listdir(anchors)) if os.path.isdir(anchors) else []
w("anchors_top", a[-3:] if len(a) >= 3 else a)
w("anchor_c00030", os.path.exists(os.path.join(anchors, "C-00030.md")))
w("anchor_c00031", os.path.exists(os.path.join(anchors, "C-00031.md")))

# 7. index.lock
w("index_lock", os.path.exists(".git/index.lock"))

# 8. daily brief (09-27 in place, 09-28 = tomorrow window)
w("daily_0927", os.path.exists("data/intel/daily/2026-09-27.md"))
w("daily_0928", os.path.exists("data/intel/daily/2026-09-28.md"))

# 9. storylines newest write per subdomain (expect video 09-27 12:49, novel/audio/comic 09-25)
for sub in ["novel", "audio", "comic", "video"]:
    d = os.path.join("data/storylines", sub)
    newest = 0
    for root, _, files in os.walk(d):
        for f in files:
            newest = max(newest, os.path.getmtime(os.path.join(root, f)))
    w("story_" + sub, datetime.fromtimestamp(newest).strftime("%m-%d %H:%M") if newest else "empty")

# 10. interchat ledger (#72 consumed R512; mtime watch)
ic = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\interchat-ledger.jsonl"
w("interchat_mtime", datetime.fromtimestamp(os.path.getmtime(ic)).strftime("%m-%d %H:%M") if os.path.exists(ic) else "absent")

# 11. ledger surfaces: backlog / HQ-FEEDBACK mtime (bm-a write-sign watch)
w("backlog_mtime", datetime.fromtimestamp(os.path.getmtime("src/os/backlog.md")).strftime("%m-%d %H:%M"))
w("hqfb_mtime", datetime.fromtimestamp(os.path.getmtime("HQ-FEEDBACK.md")).strftime("%m-%d %H:%M"))

# 12. git HEAD (expect 630bcf9 R524 batch)
head = subprocess.run(["git", "log", "-1", "--format=%h %s"], capture_output=True, text=True, encoding="utf-8")
w("head", head.stdout.strip())

print(json.dumps(R, ensure_ascii=False, indent=1))
