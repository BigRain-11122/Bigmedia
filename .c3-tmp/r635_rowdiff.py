import io, re

BASE = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
PAT = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")

cur = []
with io.open(BASE, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.rstrip("\n")
        if PAT.search(line):
            cur.append("L%d\t%s" % (i, line))

with io.open(r".c3-tmp\r635_lednew5.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(cur) + "\n")

with io.open(r".c3-tmp\r633_lednew5.txt", encoding="utf-8") as f:
    old = set(l.rstrip("\n") for l in f if l.strip())

cur_set = set(cur)
new_rows = sorted(cur_set - old)
gone_rows = sorted(old - cur_set)

with io.open(r".c3-tmp\r635_rowdiff.txt", "w", encoding="utf-8") as f:
    f.write("COUNT=%d NEW=%d GONE=%d\n" % (len(cur), len(new_rows), len(gone_rows)))
    for r in new_rows:
        f.write("NEW: " + r + "\n")
    for r in gone_rows:
        f.write("GONE: " + r + "\n")

print("COUNT=%d NEW=%d GONE=%d" % (len(cur), len(new_rows), len(gone_rows)))
for r in new_rows:
    print("NEW: " + r[:400])
