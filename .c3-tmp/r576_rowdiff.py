# r576: row-level ledger diff (leading row ids) - proper transfer-loss check
import io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
base = os.path.join(ROOT, ".c3-tmp", "r533_lednew.txt")
new = os.path.join(ROOT, ".c3-tmp", "r576_newdump.txt")

def rowids(path, prefixed):
    ids = []
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            l = line
            if prefixed:
                # strip "Lxx| " dump prefix
                m = re.match(r"L\d+\| (.*)", l.rstrip("\n"))
                l = m.group(1) if m else l
            # row-leading id: first "| P-xxxx" occurrence or duty-row marker
            m2 = re.search(r"P-\d{4}-\d{2}-\d{2}-\d{2}", l[:60])
            if m2:
                ids.append(m2.group(0))
            elif "\u503c\u5b88\u8f6e" in l[:30] or "\u603b\u7ed3\u884c" in l[:30]:
                ids.append("DUTY/" + l[:20])
            else:
                m3 = re.search(r"P-\d{4}-\d{2}-\d{2}-\d{2}", l)
                ids.append("INLINE-LEAD?" + (m3.group(0) if m3 else l[:20]))
    return ids

b_ids = rowids(base, prefixed=False)
n_ids = rowids(new, prefixed=True)

out = []
out.append("baseline rows=%d new rows=%d" % (len(b_ids), len(n_ids)))
out.append("BASE: %s" % b_ids)
out.append("NEW : %s" % n_ids)
out.append("LOST rows=%s" % [x for x in b_ids if x not in n_ids])
out.append("ADDED rows=%s" % [x for x in n_ids if x not in b_ids])
with io.open(os.path.join(ROOT, ".c3-tmp", "r576_rowdiff.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
