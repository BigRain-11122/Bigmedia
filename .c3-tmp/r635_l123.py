import io, re

pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8") as f:
    lines = f.readlines()
l = lines[122]
out = ["LINE123_HEAD: " + l[:600]]
for p in pats:
    out.append("PAT[%s] -> %s" % (p, p in l))
toks = re.findall(r"@\S{0,14}", l)
out.append("TOKENS: " + " | ".join(toks))
with io.open(r".c3-tmp\r635_l123.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("done")
