import json, io, sys

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(p, "r", encoding="utf-8") as f:
    st = json.load(f)

out = {}
for k in ("tick", "ts", "task", "production"):
    if k in st:
        out[k] = st[k]
log = st.get("log", [])
out["log_len"] = len(log)
out["log_tail3"] = log[-3:]

with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r712_state_tail.txt", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# group scan anchors
import re
led = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"

def count_led():
    hits = []
    with io.open(led, "r", encoding="utf-8", errors="replace") as f:
        for i, ln in enumerate(f, 1):
            if re.search(r"@(BigStream|七线全司|全司|六司|八线全量)", ln):
                hits.append((i, ln.strip()[:160]))
    return hits

def count_dec():
    n = 0
    last3 = []
    with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if ln.strip():
                n += 1
                last3.append(ln.strip()[:160])
    return n, last3[-3:]

with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r712_group_scan.txt", "w", encoding="utf-8") as f:
    f.write("== evolution-ledger @-rows ==\n")
    for i, ln in count_led():
        f.write(f"L{i}: {ln}\n")
    n, last3 = count_dec()
    f.write(f"\n== decisions.md non-empty lines: {n} ==\n")
    for ln in last3:
        f.write(ln + "\n")
print("ok")
