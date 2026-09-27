# R511: full L200 row + council seat check
import io

OUTP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r511_row.txt"
lines = []

# full ledger row L200
lp = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
with io.open(lp, encoding="utf-8") as fh:
    for i, l in enumerate(fh, 1):
        if i == 200:
            lines.append("L200_FULL:")
            lines.append(l.rstrip())
            break

with io.open(OUTP, "w", encoding="utf-8") as out:
    out.write("\n".join(lines) + "\n")
print("done ->", OUTP)
