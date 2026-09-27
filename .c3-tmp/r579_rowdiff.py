# r579: ledger matching-row dump + row-level diff vs r576_newdump (post-00:10:41 state)
import io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
tags = ["\u0040BigStream", "\u0040\u4e03\u7ebf\u5168\u53f8", "\u0040\u5168\u53f8", "\u0040\u516d\u53f8"]

rows = []
with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if any(t in line for t in tags):
            rows.append((i, line.rstrip("\n")))

out = []
out.append("current matching rows=%d" % len(rows))
for i, l in rows:
    out.append("L%d| %s" % (i, l))
with io.open(os.path.join(ROOT, ".c3-tmp", "r579_lednew.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))

# row-level diff vs r576_newdump (which has "Lxx| " prefixes from R576 era)
base = os.path.join(ROOT, ".c3-tmp", "r576_newdump.txt")

def rowids(path, prefixed):
    ids = []
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            l = line
            if prefixed:
                m = re.match(r"L\d+\| (.*)", l.rstrip("\n"))
                l = m.group(1) if m else l
            m2 = re.search(r"P-\d{4}-\d{2}-\d{2}-\d{2}", l[:60])
            if m2:
                ids.append(m2.group(0))
            elif "\u503c\u5b88\u8f6e" in l[:30] or "\u603b\u7ed3\u884c" in l[:30]:
                ids.append("DUTY/" + l[:20])
            else:
                m3 = re.search(r"P-\d{4}-\d{2}-\d{2}-\d{2}", l)
                ids.append("INLINE-LEAD?" + (m3.group(0) if m3 else l[:30]))
    return ids

if os.path.exists(base):
    b_ids = rowids(base, prefixed=True)
    n_ids = rowids(os.path.join(ROOT, ".c3-tmp", "r579_lednew.txt"), prefixed=True)
    out2 = []
    out2.append("baseline rows=%d new rows=%d" % (len(b_ids), len(n_ids)))
    out2.append("LOST rows=%s" % [x for x in b_ids if x not in n_ids])
    out2.append("ADDED rows=%s" % [x for x in n_ids if x not in b_ids])
    with io.open(os.path.join(ROOT, ".c3-tmp", "r579_rowdiff.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out2))
    print("DIFF rows: base=%d new=%d lost=%d added=%d" % (len(b_ids), len(n_ids), len([x for x in b_ids if x not in n_ids]), len([x for x in n_ids if x not in b_ids])))
else:
    print("BASE MISSING r576_newdump.txt")
