# R511: extract new ledger row (31st) + new decisions lines (46th+ non-blank)
import io, re

OUTP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r511_new.txt"
lines = []

# 1. ledger: all five-mode matching rows, print the tail 2 (new row = last)
lp = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pat = re.compile(r"@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8|@\u516b\u7ebf\u5168\u91cf")
matches = []
with io.open(lp, encoding="utf-8") as fh:
    for i, l in enumerate(fh, 1):
        if pat.search(l):
            matches.append((i, l.rstrip()))
lines.append("ledger_match_count %d" % len(matches))
for i, l in matches[-2:]:
    lines.append("L%d: %s" % (i, l[:600]))

# 2. decisions: non-blank lines 46+
dp = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
nb = 0
newlines = []
with io.open(dp, encoding="utf-8") as fh:
    for l in fh:
        if l.strip():
            nb += 1
            if nb >= 46:
                newlines.append(l.rstrip())
lines.append("")
lines.append("decisions_nonblank %d new_lines %d" % (nb, len(newlines)))
for l in newlines:
    lines.append("DEC: " + l[:600])

with io.open(OUTP, "w", encoding="utf-8") as out:
    out.write("\n".join(lines) + "\n")
print("done ->", OUTP)
