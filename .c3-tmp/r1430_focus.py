import json, re, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
G = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1430_focus_out.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    try:
        out.write(s + "\n")
    except Exception:
        out.write(repr(s) + "\n")

# 1) decisions.md full rows: OSS E1 escalation + D-20261005-05 + any 10-05/10-06 rows
dec = io.open(os.path.join(G, "docs", "decisions.md"), encoding="utf-8").read().splitlines()
w("== decisions.md full rows (D-20261006-xx / D-20261005-05) ==")
for l in dec:
    if ("D-20261006-03" in l) or ("D-20261005-05" in l and l.lstrip().startswith("|")):
        w("ROW| " + l.strip())
w("")
w("== decisions.md dispatch-board rows dated 10-01+ (tail) ==")
rows = [l for l in dec if re.search(r"\|\s*\*?D-20261\d\d\d-\d+", l)]
w("board-style D-rows count=%d, last 10:" % len(rows))
for l in rows[-10:]:
    w("BROW| " + l.strip()[:500])

# 2) state.json full log entries for R1420 / R1427 / R1428
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
lg = st.get("log", [])
w("")
w("== state.json full log entries R1420 / R1427 / R1428 ==")
for e in lg:
    s = str(e)
    for tag in ("R1420:", "R1427:", "R1428:"):
        if tag in s[:40]:
            w("ENTRY| " + s)
            w("")

# 3) HQ-FEEDBACK tail (last 6 non-empty lines)
hq = io.open(os.path.join(ROOT, "HQ-FEEDBACK.md"), encoding="utf-8").read().splitlines()
nz = [l for l in hq if l.strip()]
w("== HQ-FEEDBACK last 6 non-empty lines ==")
for l in nz[-6:]:
    w("HQ| " + l[:400])

out.close()
print("done -> " + OUTP)
