import io
base = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp"
s = io.open(base + r"\r1376_check.py", encoding="utf-8").read().replace("r1376_check.txt", "r1377_check.txt")
io.open(base + r"\r1377_check.py", "w", encoding="utf-8").write(s)
s2 = io.open(base + r"\r1376_probes.py", encoding="utf-8").read().replace("r1376_probes.txt", "r1377_probes.txt")
io.open(base + r"\r1377_probes.py", "w", encoding="utf-8").write(s2)
print("cloned")
