# -*- coding: utf-8 -*-
# r1409 five-check fresh probe (declared-idle window 2/6; new window after R1401-R1406 batch close 3b5f8e8c; OSS w4 gate 21:40 not yet open at 21:2x pre-check; ASCII-safe per encoding law)
# lineage: r1406_check.py pattern (python io channel clone per R1244/R1288)
import json, re, io, os, glob, datetime, subprocess

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1409_check.txt", "w", encoding="utf-8")
w = out.write

TAG_ALLCO = "\u4e03\u7ebf\u5168\u53f8"  # qi-xian all-company
TAG_QUANSI = "\u5168\u53f8"              # all-company
TAG_LIUSI = "\u516d\u53f8"              # six-company
TAG_BAXIAN = "\u516b\u7ebf"             # eight-line
BOARD_HDR = "\u6d3e\u5de5\u901a\u544a\u677f"  # dispatch board header
PAT = "@(BigStream|" + TAG_ALLCO + "|" + TAG_QUANSI + "|" + TAG_LIUSI + "|" + TAG_BAXIAN + ")"

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
w("NOW: " + now + "\n\n")

st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
w("tick=%s ts=%s production=%s mode=%s\n" % (st.get("tick"), st.get("ts"), st.get("production"), st.get("mode")))
dw = st.get("decisions_watermark", {}) or {}
dnums = dw.get("dnums", []) or []
w("dnums_count=%s\n" % len(dnums))
log = st.get("log", []) or []
w("log_count=%s\n\n== LOG TAIL 1 ==\n" % len(log))
for line in log[-1:]:
    w("LOG| " + line[:300] + "\n\n")

# [1] orders top (latest by mtime)
for p in sorted(glob.glob(repo + r"\orders\*"), key=os.path.getmtime, reverse=True)[:3]:
    w("ORD| %s mtime=%s\n" % (os.path.basename(p), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")))

# [2] decisions.md content-addressed watermark diff (D-20260930-19; no raw line counts)
dec = io.open(base + r"\docs\decisions.md", encoding="utf-8").read()
w("decisions_mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(base + r"\docs\decisions.md")).strftime("%m-%d %H:%M:%S"))
ds = sorted(set(re.findall(r"[DC]-\d{8}-\d{1,2}", dec)))
new = [d for d in ds if d not in set(dnums)]
gone = [d for d in dnums if d not in set(ds)]
w("decisions_set=%s new_vs_watermark=%s gone=%s\n" % (len(ds), new, gone))

# [3] evolution-ledger STRICT @-prefixed tag scan + tail
led = io.open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
llines = led.split("\n")
tags = [(i, l) for i, l in enumerate(llines, 1) if re.search(PAT, l)]
w("ledger_tag_lines_strict=%s mtime=%s\n" % (len(tags), datetime.datetime.fromtimestamp(os.path.getmtime(base + r"\cph4\evolution-ledger.md")).strftime("%m-%d %H:%M:%S")))
for i, l in tags[-2:]:
    w("LED| L%s %s\n" % (i, l[:200]))

# [4] dispatch board BigStream rows
m = re.search(BOARD_HDR + r"(.*?)(?:\n## |\Z)", dec, re.S)
if m:
    brows = [l for l in m.group(1).split("\n") if "BigStream" in l and l.strip().startswith("|")]
    allrows = [l for l in m.group(1).split("\n") if l.strip().startswith("|")]
    w("board_rows_total=%s board_rows_BigStream=%s\n" % (len(allrows), len(brows)))
else:
    w("board=BLOCK_NOT_FOUND\n")

# [5] supply gates + round-relevant facts
for p in [base + r"\life\BigLife\census\anchors\C-00030.md",
          base + r"\life\BigLife\census\anchors\C-00031.md"]:
    w("anchor %s exists=%s\n" % (os.path.basename(p), os.path.exists(p)))
w("index_lock=%s\n" % os.path.exists(repo + r"\.git\index.lock"))
w("oh_w4=%s (window4 opens 21:40, not-built=normal)\n" % os.path.exists(base + r"\cph4\oss-harvest\OH-20261005-bigstream.md"))
w("daily1005=%s daily1006=%s\n" % (os.path.exists(repo + r"\data\intel\daily\2026-10-05.md"), os.path.exists(repo + r"\data\intel\daily\2026-10-06.md")))

pp = base + r"\life\BigLife\cognition\pools.json"
if os.path.exists(pp):
    w("cognition_pools_exists=True mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(pp)).strftime("%m-%d %H:%M"))
else:
    w("cognition_pools=MISSING\n")

ic = base + r"\life\BigLife\cognition\interchat-ledger.jsonl"
if os.path.exists(ic):
    w("interchat_mtime=%s lines=%s\n" % (datetime.datetime.fromtimestamp(os.path.getmtime(ic)).strftime("%m-%d %H:%M"), sum(1 for _ in io.open(ic, encoding="utf-8"))))
else:
    w("interchat=ABSENT\n")

nv = sorted(glob.glob(repo + r"\data\storylines\novel\*v4*.md"))
w("novel_v4_files=%s\n" % [os.path.basename(p) for p in nv])

ev = sorted(glob.glob(repo + r"\docs\reviews\expert-verdicts\*20261005*"))
w("e4_verdicts_1005_canonical=%s\n" % [os.path.basename(p) for p in ev])
w("e4_root_leftover=%s (expect 0 after R1367 git-mv)\n" % len(glob.glob(repo + r"\expert-verdicts\*")))

# R1388 close verify: finished.md F-155 tail + cards README v68 row
fin = io.open(repo + r"\output\finished.md", encoding="utf-8").read()
w("finished_F155_present=%s F-155_in_tail=%s\n" % ("F-155" in fin, "F-155" in fin[-6000:]))

cr = io.open(repo + r"\data\storylines\cards\README.md", encoding="utf-8").read()
w("cards_readme_v68_present=%s\n" % ("v68" in cr))

# export freshness
exp = json.load(io.open(repo + r"\docs\status-export.json", encoding="utf-8"))
w("export_ts=%s\n" % exp.get("export_ts"))

# [6] tree status via git (ASCII out captured to file)
try:
    p = subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, timeout=60)
    w("git_status_rc=%s\n" % p.returncode)
    w((p.stdout or b"").decode("utf-8", "replace"))
    p2 = subprocess.run(["git", "log", "-1", "--format=%h %s"], cwd=repo, capture_output=True, timeout=60)
    w("LAST_COMMIT=" + (p2.stdout or b"").decode("utf-8", "replace").strip()[:150] + "\n")
except Exception as e:
    w("git_status_exc=%s\n" % type(e).__name__)

out.close()
print("ok")
