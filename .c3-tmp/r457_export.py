import json, io
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
def read_utf8(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read().strip()
outs_new = read_utf8(ROOT + r"\.c3-tmp\r457_outs.txt")
res0 = read_utf8(ROOT + r"\.c3-tmp\r457_res0.txt")
res2 = read_utf8(ROOT + r"\.c3-tmp\r457_res2.txt")
chip = read_utf8(ROOT + r"\.c3-tmp\r457_chip.txt")
p = ROOT + r"\docs\status-export.json"
with io.open(p, "r", encoding="utf-8") as f:
    d = json.load(f)
assert d["results"][0][0] == "456", "unexpected results[0] anchor: %s" % d["results"][0][0]
assert d["results"][2][0] == "291", "unexpected results[2] anchor: %s" % d["results"][2][0]
assert str(d["outs"][0][1]).startswith("tick 456"), "unexpected outs anchor head"
d["outs"][0][1] = outs_new
d["results"][0] = ["457", res0]
d["results"][2] = ["297", res2]
d["chips"].append([chip, "live"])
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("OK results0=%s results2=%s chips=%d" % (d["results"][0][0], d["results"][2][0], len(d["chips"])))