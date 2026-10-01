import json, re, os

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
tmp = os.path.join(root, ".c3-tmp")
os.makedirs(tmp, exist_ok=True)
out = []

state = json.load(open(os.path.join(root, "src/os/state.json"), encoding="utf-8"))
out.append("tick: %s" % state.get("tick"))
out.append("ts: %s" % state.get("ts"))
out.append("task: %s" % state.get("task"))
out.append("production: %s" % state.get("production"))
log = state.get("log", [])
out.append("log_len: %s" % len(log))
out.append("=== LOG TAIL 3 ===")
for line in log[-3:]:
    out.append("--- " + line)

wm = state.get("decisions_watermark", {})
dnums = wm.get("dnums", [])
out.append("=== WATERMARK ===")
out.append("dnums_count: %s" % len(dnums))
out.append("dnums_tail: %s" % dnums[-12:])

# decisions.md D/C set (content-addressed)
dec = open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8").read()
dec_set = set(re.findall(r"\b([DC]-\d{8}-\d{2})\b", dec))
new_dec = sorted(dec_set - set(dnums))
out.append("dec_new_vs_watermark: %s" % new_dec)

# evolution-ledger @BigStream / all-company lines
led = open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8").read().splitlines()
pat = re.compile(r"@BigStream|@八线全司|@八线全量|@七线全司|@全司|@六司")
at_lines = [(i + 1, l) for i, l in enumerate(led) if pat.search(l)]
out.append("ledger_at_count: %s" % len(at_lines))
out.append("ledger_at_last5_nos: %s" % [n for n, _ in at_lines[-5:]])
for n, l in at_lines[-3:]:
    out.append("L%s: %s" % (n, l[:300]))

# orders latest 6 by mtime
orders_dir = os.path.join(root, "orders")
files = sorted(((os.path.getmtime(os.path.join(orders_dir, f)), f) for f in os.listdir(orders_dir)), reverse=True)
out.append("orders_top6: %s" % [f for _, f in files[:6]])

open(os.path.join(tmp, "r_probe_qc.txt"), "w", encoding="utf-8").write("\n".join(out))
print("OK lines=%d" % len(out))
