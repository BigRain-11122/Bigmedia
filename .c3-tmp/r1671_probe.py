import json, re

base = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []

st = json.load(open(base + r"\src\os\state.json", encoding="utf-8"))
scal = {k: v for k, v in st.items() if not isinstance(v, (list, dict))}
out.append("SCALARS " + json.dumps(scal, ensure_ascii=False))
wm = st.get("decisions_watermark", {})
dnums = set(wm.get("dnums", []))
out.append("WM dnums=%d" % len(dnums))
log = st.get("log", [])
out.append("LOG_LEN %d" % len(log))
for line in log[-2:]:
    out.append("LOG>> " + line)

txt = open(base + r"\src\os\backlog.md", encoding="utf-8").read()
lines = txt.splitlines()
items = []
for i, l in enumerate(lines):
    m = re.match(r"^(\d+)\.\s", l)
    if m:
        items.append((int(m.group(1)), i))
out.append("BACKLOG_ITEMS %d" % len(items))
shown = 0
for num, i in items:
    if shown >= 14:
        break
    seg = "\n".join(lines[i:i + 4])
    done = "[done" in seg
    out.append("ITEM %d done=%s :: %s" % (num, done, lines[i][:160]))
    shown += 1

dec = open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8").read()
nums = set(re.findall(r"[DC]-20\d{6}-\d+", dec))
new_nums = sorted(nums - dnums)
out.append("DEC total=%d new_vs_wm=%d new=%s" % (len(nums), len(new_nums), ",".join(new_nums[:25])))
head = dec[:1200]
out.append("DEC_HEAD>> " + head.replace("\n", " | ")[:900])

led = open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8").read()
at_lines = [l for l in led.splitlines() if re.search(r"@BigStream|@七线全司|@全司|@六司", l)]
out.append("LEDGER_AT %d" % len(at_lines))
for l in at_lines[-6:]:
    out.append("LED>> " + l[:220])

open(base + r"\.c3-tmp\r1671_probe_out.txt", "w", encoding="utf-8").write("\n".join(out))
print("OK")
