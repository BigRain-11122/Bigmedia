import io, re
BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
bl = io.open(BS + r"\src\os\backlog.md", "r", encoding="utf-8").read().splitlines()
out = []
for i, l in enumerate(bl):
    if re.match(r"^(90|91|96)\.", l):
        # print full line + following 6 lines (notes)
        out.append(">>> " + l)
        j = i + 1
        while j < len(bl) and (not re.match(r"^\d+\.", bl[j]) or re.match(r"^(90|91|96)\.", bl[j])):
            if bl[j].strip():
                out.append("    " + bl[j][:500])
            j += 1
            if j - i > 8:
                break
io.open(BS + r"\.c3-tmp\r912_dm.txt", "w", encoding="utf-8").write("\n".join(out))
print("lines", len(out))
