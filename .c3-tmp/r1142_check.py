# -*- coding: utf-8 -*-
# R1142 round-open fast check: state summary + group transfer scan (content-addressed)
import json, re, os, time, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = os.path.join(ROOT, ".c3-tmp", "r1142_check.txt")

lines = []
def w(s):
    lines.append(s)

state = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("tick=%s" % state.get("tick"))
w("ts=%s" % state.get("ts"))
w("task=%s" % str(state.get("task"))[:150])
w("production=%s" % state.get("production"))
wm = state.get("decisions_watermark", {})
dnums = wm.get("dnums") if isinstance(wm, dict) else wm
if dnums is None:
    dnums = []
w("wm_dnums_count=%d" % len(dnums))

logs = state.get("log", [])
w("log_len=%d" % len(logs))
for entry in logs[-3:]:
    w("---LOG_TAIL---")
    w(str(entry)[:600])

# orders/ newest files
od = os.path.join(ROOT, "orders")
if os.path.isdir(od):
    fs = sorted(((os.path.getmtime(os.path.join(od, f)), f) for f in os.listdir(od)), reverse=True)
    for mt, f in fs[:2]:
        w("ORDER: %s  mtime=%s" % (f, time.strftime("%m-%d %H:%M", time.localtime(mt))))

# group ledger scan: strict @-prefix rows
ledger_path = os.path.join(GRP, "cph4", "evolution-ledger.md")
if os.path.exists(ledger_path):
    lt = io.open(ledger_path, encoding="utf-8").read().splitlines()
    pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
    hits = [(i, l) for i, l in enumerate(lt) if pat.search(l)]
    w("ledger_at_rows=%d" % len(hits))
    for i, l in hits[-2:]:
        w("LEDGER_TAIL L%d: %s" % (i + 1, l[:200]))

# decisions.md: content-addressed D/C diff vs watermark
dec_path = os.path.join(GRP, "docs", "decisions.md")
if os.path.exists(dec_path):
    dt = io.open(dec_path, encoding="utf-8").read()
    nums = set(re.findall(r"[DC]-\d{8}-\d{2}", dt))
    new = sorted(nums - set(dnums))
    w("decisions_nums_total=%d new_vs_wm=%d" % (len(nums), len(new)))
    w("new_nums=%s" % ",".join(new))
    # dispatch board rows touching BigStream (last 80 lines of file may hold board; scan all)
    board_rows = [l for l in dt.splitlines() if l.startswith("|") and ("BigStream" in l or "七司" in l)]
    w("board_bigstream_rows=%d" % len(board_rows))
    for l in board_rows[-3:]:
        w("BOARD_TAIL: %s" % l[:200])

# index.lock check
lock = os.path.join(ROOT, ".git", "index.lock")
w("index_lock=%s" % os.path.exists(lock))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("OK lines=%d" % len(lines))
