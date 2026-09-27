import io

lines = io.open(r"data\storylines\cards\README.md", encoding="utf-8").read().splitlines()
with io.open(r".c3-tmp\r575_readme_tail.txt", "w", encoding="utf-8") as f:
    f.write("TOTAL %d\n" % len(lines))
    f.write("\n".join(lines[-25:]))
print("OK")
