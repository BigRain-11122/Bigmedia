# -*- coding: utf-8 -*-
# r429: dump new ledger @-lines (24th, 25th) UTF-8 safe + loop_health tail
import io, os

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grp = os.path.normpath(os.path.join(repo, "..", ".."))
ledger = os.path.join(grp, "cph4", "evolution-ledger.md")
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
hits = []
with io.open(ledger, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if any(p in line for p in pats):
            hits.append((i, line.rstrip("\n")))

out = io.open(os.path.join(repo, ".c3-tmp", "r429_new_ledger.txt"), "w", encoding="utf-8")
out.write("total_hits=%d\n" % len(hits))
# context: last 3 hits with 2 lines before each
seen = set()
for idx in (len(hits) - 2, len(hits) - 1):
    if idx < 0:
        continue
    ln, txt = hits[idx]
    out.write("\n=== hit #%d at L%d ===\n" % (idx + 1, ln))
    out.write(txt + "\n")
    seen.add(ln)
# also dump the raw tail block of the ledger (last 40 lines) for context of new entries
with io.open(ledger, encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
out.write("\n=== ledger tail (last 45 lines, L%d+) ===\n" % max(1, len(lines) - 44))
for i, l in enumerate(lines[-45:], max(1, len(lines) - 44)):
    out.write("L%d: %s" % (i, l.rstrip("\n") + "\n"))
out.close()

# loop_health probe tail
pf = os.path.join(repo, ".c3-tmp", "r429_probe.txt")
lh = io.open(pf, encoding="utf-8").read()
idx = lh.find("=== loop_health")
out2 = io.open(os.path.join(repo, ".c3-tmp", "r429_loop_tail.txt"), "w", encoding="utf-8")
out2.write(lh[idx:idx + 4000] if idx >= 0 else "loop_health section not found")
out2.close()
print("dumped=r429_new_ledger.txt,r429_loop_tail.txt")
