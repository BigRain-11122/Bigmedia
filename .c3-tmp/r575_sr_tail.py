import io

lines = io.open(r"docs\reviews\station-reviews.md", encoding="utf-8").read().splitlines()
with io.open(r".c3-tmp\r575_sr_tail.txt", "w", encoding="utf-8") as f:
    f.write("TOTAL %d\n" % len(lines))
    f.write("\n".join(lines[-6:]))
print("OK")
