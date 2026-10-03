import io

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
L = io.open(p, encoding="utf-8").read().splitlines(True)
ln = L[1282]  # line 1283 (1-based)
print("line1283_len=%d" % len(ln))
seg = ln[2420:2540]
io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1104_inspect.txt", "w", encoding="utf-8").write(
    "len=%d\nSEG2420_2540:\n%s\n\nQUOTE_POS=%s\n" % (len(ln), seg, [i for i, c in enumerate(ln) if c == '"']))
print("written, quotes=%d" % len([c for c in ln if c == '"']))
