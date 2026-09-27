import io

lines = io.open(r"output\finished.md", encoding="utf-8").read().splitlines()
with io.open(r".c3-tmp\r575_fintail.txt", "w", encoding="utf-8") as f:
    f.write("TOTAL %d\n" % len(lines))
    f.write("\n".join(lines[-45:]))
print("OK")
