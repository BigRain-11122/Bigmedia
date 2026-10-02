import io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
o = io.StringIO()

cr = io.open(ROOT + r"\data\storylines\cards\README.md", encoding="utf-8").read().splitlines()
o.write(u"=== cards README: lines containing v50 (last 4) + tail 3 ===\n")
hits = [l for l in cr if u"v50" in l or u"DAILY-v50" in l]
for l in hits[-4:]:
    o.write(l[:700] + u"\n")
for l in cr[-3:]:
    o.write(u"TAIL|" + l[:300] + u"\n")

sr = io.open(ROOT + r"\docs\reviews\station-reviews.md", encoding="utf-8").read().splitlines()
o.write(u"\n=== station-reviews tail 4 ===\n")
for l in sr[-4:]:
    o.write(l[:800] + u"\n")

fin = io.open(ROOT + r"\output\finished.md", encoding="utf-8").read().splitlines()
o.write(u"\n=== finished.md F-135 block (find + 22 lines) ===\n")
for i, l in enumerate(fin):
    if u"F-135" in l:
        for x in fin[i:i+24]:
            o.write(x[:600] + u"\n")
        break

se = io.open(ROOT + r"\docs\status-export.json", encoding="utf-8").read()
o.write(u"\n=== status-export.json (first 2200 chars) ===\n")
o.write(se[:2200])

io.open(ROOT + r"\.c3-tmp\r1020_ledgers.txt", "w", encoding="utf-8").write(o.getvalue())
print("ok")
