# -*- coding: utf-8 -*-
# R696 selection probe: unsplit CENSUS candidates - name-drops in LC-001~006 beats,
# anchor cross-refs, E4 reading anchors
import io, os, re, glob
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LIFE = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
out = []

split_cards = {"C-00016": "LC-001", "C-00017": "LC-002", "C-00022": "LC-003",
               "C-00025": "LC-004", "C-00026": "LC-005", "C-00028": "LC-006"}
names = ["顾阿凤", "朱鸿奎", "沈佩兰", "林之恒", "周浩宇", "陈雅雯", "罗大壮", "老晶振",
         "苏梓涵", "王多多", "潘志明", "缪一", "邓建国", "咪喱", "感知塔", "梅花",
         "对时铺", "像素画匠", "引擎医生", "伴居灵", "灯灵", "守夜"]

# 1. name-drops of unsplit chars in LC-001~006 final beats (production-probability payoff check)
out.append("=== name-drops of unsplit characters in LC beats ===")
for src in sorted(glob.glob(os.path.join(ROOT, "data/sources/lc00*/voiceover-v*.beats.txt"))):
    with io.open(src, encoding="utf-8") as f:
        txt = f.read()
    hits = [n for n in names if n in txt]
    out.append("%s: %s" % (os.path.basename(os.path.dirname(src)) + "/" + os.path.basename(src), hits))

# 2. anchor cards of top candidates: full read of C-00027, C-00029, C-00021, C-00011 (cross-ref + fields)
for cid in ["C-00027", "C-00029", "C-00021", "C-00011", "C-00028"]:
    fp = os.path.join(LIFE, cid + ".md")
    out.append("=== anchor %s ===" % cid)
    try:
        with io.open(fp, encoding="utf-8") as f:
            out.extend([l.rstrip() for l in f.readlines()][:40])
    except Exception as e:
        out.append("err=%s" % e)

# 3. E4 readings for unsplit candidate source cards from cards README (F-020~F-040 census rows w/ E4)
with io.open(os.path.join(ROOT, "data/storylines/cards/README.md"), encoding="utf-8") as f:
    cr = f.readlines()
out.append("=== cards README rows with E4 readings (census v1-v20) ===")
for l in cr:
    if "CENSUS" in l and ("E4" in l):
        out.append(l.rstrip()[:400])

with io.open(os.path.join(ROOT, ".c3-tmp/r696_cand.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("DUMP_DONE lines=%d" % len(out))
