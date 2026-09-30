# -*- coding: utf-8 -*-
"""Restore results row '684' overwritten by the R696 osfix (collateral hit)."""
import io, json, subprocess
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ep = ROOT + r"\docs\status-export.json"
head = subprocess.run(["git", "show", "HEAD:docs/status-export.json"],
                      cwd=ROOT, capture_output=True).stdout.decode("utf-8")
hse = json.loads(head)
orig = None
for r in hse.get("results", []):
    if r[0] == "684" and isinstance(r[1], str) and r[1].startswith("tick 684"):
        orig = r[1]
        break
assert orig, "HEAD 684 row not found"
se = json.load(io.open(ep, encoding="utf-8"))
fixed = 0
for r in se["results"]:
    if r[0] == "684" and r[1].startswith("tick 696"):
        r[1] = orig
        fixed += 1
io.open(ep, "w", encoding="utf-8").write(json.dumps(se, ensure_ascii=False, indent=1))
se2 = json.load(io.open(ep, encoding="utf-8"))
ok684 = any(r[0] == "684" and r[1].startswith("tick 684") for r in se2["results"])
okos = any(isinstance(r, list) and len(r) >= 2 and r[0] == "OS 循环" and r[1].startswith("tick 696")
           for v in se2.values() if isinstance(v, list) for r in v if isinstance(r, list))
dup696 = sum(1 for r in se2["results"] if r[1].startswith("tick 696，R696"))
io.open(ROOT + r"\.c3-tmp\r696_verify3.txt", "w", encoding="utf-8").write(
    "restored=%d\nrow684_ok=%s\nos_row_ok=%s\nresults_tick696_rows=%d (expect 0 in results)\nresults_count=%d\nresults_tail=%s" % (
        fixed, ok684, okos, dup696, len(se2["results"]), se2["results"][-1][0]))
print("RESTORE_DONE fixed=%d ok684=%s os=%s" % (fixed, ok684, okos))
