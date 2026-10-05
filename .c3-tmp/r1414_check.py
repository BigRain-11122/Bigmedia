# -*- coding: utf-8 -*-
# R1414 five-checks fresh (waiting-state round; no re-derivation of waiting object)
import json, re, os, subprocess, glob, io, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
def w(s):
    out.append(str(s))

now_s = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
w("check_time=%s" % now_s)

st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
w("tick=%s ts=%s" % (st.get("tick"), st.get("ts")))
log = st.get("log", [])
w("log_len=%d" % len(log))
for line in log[-2:]:
    w("LOG: " + line[:220])
wm = st.get("decisions_watermark", {})
old = set(wm.get("dnums", []))
w("watermark_count=%d" % len(old))

# [1] orders top (new O order?)
orders = sorted(glob.glob(repo + r"\orders\*"), key=os.path.getmtime)
for f in orders[-2:]:
    w("ORDER: %s mtime=%s" % (os.path.basename(f), datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%m-%d %H:%M:%S")))

# [2] decisions.md content-addressing set-diff (D-20260930-19) + board section
dec_path = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    txt = io.open(dec_path, encoding="utf-8").read()
    dnums = set(re.findall(r"[DC]-\d{8}-\d{2}", txt))
    new = sorted(dnums - old)
    gone = sorted(old - dnums)
    w("dec_mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(dec_path)).strftime("%m-%d %H:%M:%S"))
    w("dec_dnum=%d old=%d NEW=%s GONE=%s" % (len(dnums), len(old), new[:10], gone[:10]))
    lines = txt.splitlines()
    # board section
    b0 = b1 = -1
    for i, l in enumerate(lines):
        if "派工通告板" in l and b0 < 0:
            b0 = i
        elif b0 >= 0 and l.startswith("## ") and i > b0:
            b1 = i
            break
    if b1 < 0:
        b1 = len(lines)
    board = [l for l in lines[b0:b1]]
    w("board_section_lines=%d" % len(board))
    bsrows = [l for l in board if re.search(r"BigStream|七线|全司|六司|八线", l)]
    w("board_bs_rows=%d" % len(bsrows))
    w("board_tail:")
    for l in board[-3:]:
        w("  BT: " + l[:150])
except Exception as e:
    w("dec_err=%s" % e)

# [3] ledger strict @tag scan
ledger_path = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
try:
    txt = io.open(ledger_path, encoding="utf-8").read()
    pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
    hits = [l for l in txt.splitlines() if pat.search(l)]
    w("ledger_hits=%d" % len(hits))
    w("ledger_mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(ledger_path)).strftime("%m-%d %H:%M:%S"))
    for l in hits[-2:]:
        w("  LT: " + l[:160])
except Exception as e:
    w("ledger_err=%s" % e)

# [4] tree + lock + bm-a write signs
r = subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, text=True, encoding="utf-8")
w("git_status=" + r.stdout.replace("\n", " | ")[:400])
w("index_lock=%s" % os.path.exists(repo + r"\.git\index.lock"))

# [5] waiting-object freshness (mtime-only; no re-derive - 禁重扫律)
for name, p in [
    ("backlog", repo + r"\src\os\backlog.md"),
    ("queue", repo + r"\docs\self-improvement-queue.md"),
    ("hq_feedback", repo + r"\HQ-FEEDBACK.md"),
    ("export", repo + r"\docs\status-export.json"),
]:
    if os.path.exists(p):
        w("%s_mtime=%s" % (name, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M:%S")))
    else:
        w("%s=MISSING" % name)

# [6] dailies
w("daily_1005=%s" % os.path.exists(repo + r"\data\intel\daily\2026-10-05.md"))
w("daily_1006=%s" % os.path.exists(repo + r"\data\intel\daily\2026-10-06.md"))

io.open(repo + r"\.c3-tmp\r1414_check.txt", "w", encoding="utf-8").write("\n".join(out))
print("check done -> .c3-tmp/r1414_check.txt")
