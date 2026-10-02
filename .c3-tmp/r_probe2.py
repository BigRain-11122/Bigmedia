import json, io, os, re

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(BS, ".c3-tmp", "r_probe2_out.txt")

st = json.load(io.open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
log = st.get("log", [])
r989 = [l for l in log if " R989:" in l][-1]

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("== R989 full ==\n" + r989 + "\n\n")
    # queue §E section
    q = os.path.join(BS, "docs", "self-improvement-queue.md")
    qt = io.open(q, encoding="utf-8", errors="replace").read()
    i = qt.find("§E")
    if i < 0:
        i = qt.find("E. ")
    f.write("== queue §E region ==\n" + qt[i:i+3500] + "\n\n")
    # finished.md F-105 / F-106 context
    fm = io.open(os.path.join(BS, "output", "finished.md"), encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"F-10[567]\b", fm):
        s = max(0, m.start()-150)
        f.write("== F-105/106/107 ctx ==\n" + fm[s:m.end()+300] + "\n---\n")
        break
    # find lines mentioning F-106
    for line in fm.splitlines():
        if "F-106" in line or "F-202" in line:
            f.write("LINE: " + line[:400] + "\n")
print("OK")
