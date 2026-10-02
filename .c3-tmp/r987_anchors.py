# -*- coding: utf-8 -*-
import io

OUT = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r987_anchors.txt", "w", encoding="utf-8")
R = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

def dump(title, path, head=None, tail=None):
    lines = io.open(path, encoding="utf-8").read().splitlines()
    OUT.write(u"== %s (total %d lines) ==\n" % (title, len(lines)))
    if head:
        for ln in lines[:head]:
            OUT.write(u"H| " + ln[:400] + u"\n")
    if tail:
        for ln in lines[-tail:]:
            OUT.write(u"T| " + ln[:400] + u"\n")
    OUT.write(u"\n")

dump(u"station-reviews head", R + r"\docs\reviews\station-reviews.md", head=3)
dump(u"finished tail", R + r"\output\finished.md", tail=2)
dump(u"cards README tail", R + r"\data\storylines\cards\README.md", tail=2)
dump(u"queue tail", R + r"\docs\self-improvement-queue.md", tail=3)

bl = io.open(R + r"\src\os\backlog.md", encoding="utf-8").read().splitlines()
for i, ln in enumerate(bl):
    if ln.startswith(u"97."):
        OUT.write(u"== backlog #97 at line %d of %d ==\n" % (i + 1, len(bl)))
        for x in bl[i:i + 4]:
            OUT.write(u"B| " + x[:400] + u"\n")
        break
OUT.write(u"== backlog last 3 ==\n")
for x in bl[-3:]:
    OUT.write(u"B| " + x[:400] + u"\n")

sr = io.open(R + r"\docs\reviews\station-reviews.md", encoding="utf-8").read().splitlines()
OUT.write(u"\n== station-reviews lines 2-4 (header check) ==\n")
for x in sr[1:4]:
    OUT.write(u"S| " + x[:200] + u"\n")
OUT.close()
print("OK")
