import io

with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8") as f:
    lines = f.readlines()

with io.open(r".c3-tmp\r635_zone.txt", "w", encoding="utf-8") as f:
    for i in range(159, min(230, len(lines))):
        f.write("L%d: %s\n" % (i + 1, lines[i].rstrip("\n")[:150]))
print("done")
