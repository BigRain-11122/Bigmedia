import io, os
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
dec = os.path.join(GRP, "docs", "decisions.md")

# --- ledger scan (R644 rowdiff format law: L<lineno> + tab prefix) ---
base_lines = io.open(r".c3-tmp/r644_lednew5.txt", encoding="utf-8").read().splitlines()
base_set = set(l.split("\t", 1)[1] if "\t" in l else l for l in base_lines if l.strip())
lines = io.open(led, encoding="utf-8").read().splitlines()
pats = ("@BigStream", "@七线全司", "@全司", "@六司", "@八线")
cur = ["L%d\t%s" % (i, l.strip()) for i, l in enumerate(lines, 1) if any(p in l for p in pats)]
cur_set = set(l.split("\t", 1)[1] for l in cur)
new = [l for l in cur if l.split("\t", 1)[1] not in base_set]
gone = len(base_set - cur_set)
io.open(r".c3-tmp/r653_lednow.txt", "w", encoding="utf-8").write("\n".join(cur) + "\n")
print("ledger_match_lines:", len(cur))
print("baseline_lines:", len([l for l in base_lines if l.strip()]))
print("rowdiff_NEW:", len(new), "GONE:", gone)
for l in new[:8]:
    print("NEW>>", l[:220])
# last 2 matching lines for freshness eyeball
print("last2:")
for l in cur[-2:]:
    print("  ", l[:200])

# --- decisions.md non-empty count vs anchor 68 (R637) ---
dl = [l for l in io.open(dec, encoding="utf-8").read().splitlines() if l.strip()]
print("decisions_nonempty:", len(dl), "(anchor=68)")
if len(dl) > 68:
    for l in dl[-6:]:
        print("D>>", l[:180])
