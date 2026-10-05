import json, re, os, subprocess, glob

out = []
def w(s):
    out.append(str(s))

st = json.load(open("src/os/state.json", encoding="utf-8"))
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % str(st.get("task"))[:150])
w("production=%s" % st.get("production"))
log = st.get("log", [])
w("log_len=%d" % len(log))
for line in log[-3:]:
    w("LOG: " + line[:500])
wm = st.get("decisions_watermark", {})
w("watermark_dnums=%s" % json.dumps(wm.get("dnums", [])))

r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, encoding="utf-8")
w("git_status_begin")
w(r.stdout[:2000])
w("git_status_end")
w("index_lock=%s" % os.path.exists(".git/index.lock"))

orders = sorted(glob.glob("orders/*"), key=os.path.getmtime)
for f in orders[-4:]:
    w("ORDER: %s mtime=%s" % (f, os.path.getmtime(f)))

ledger_path = r"C:/Users/sjs20/Desktop/FluxGroup/cph4/evolution-ledger.md"
try:
    txt = open(ledger_path, encoding="utf-8").read()
    pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
    hits = [l for l in txt.splitlines() if pat.search(l)]
    w("ledger_hits=%d" % len(hits))
    for l in hits[-4:]:
        w("LEDGER_TAIL: " + l[:180])
except Exception as e:
    w("ledger_err=%s" % e)

dec_path = r"C:/Users/sjs20/Desktop/FluxGroup/docs/decisions.md"
try:
    txt = open(dec_path, encoding="utf-8").read()
    dnums = set(re.findall(r"[DC]-\d{8}-\d{2}", txt))
    old = set(wm.get("dnums", []))
    new = sorted(dnums - old)
    w("dec_count=%d old_count=%d new=%s" % (len(dnums), len(old), new[:20]))
    top = "\n".join(txt.splitlines()[:40])
    w("DEC_TOP_BEGIN")
    w(top)
    w("DEC_TOP_END")
except Exception as e:
    w("dec_err=%s" % e)

w("daily_1005=%s" % os.path.exists("data/intel/daily/2026-10-05.md"))
w("daily_1004=%s" % os.path.exists("data/intel/daily/2026-10-04.md"))

open("r_cur_probe2_out.txt", "w", encoding="utf-8").write("\n".join(out))
print("probe done")
