import io

with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8") as f:
    lines = f.readlines()

with io.open(r".c3-tmp\r635_p1019.txt", "w", encoding="utf-8") as f:
    for i in range(163, 173):
        f.write("=== L%d ===\n%s\n" % (i + 1, lines[i].rstrip("\n")))
print("done")
