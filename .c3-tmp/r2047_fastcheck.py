# Fast-path round check: state machine fields + orders dir + ledger/decisions scan
import json, os, re, datetime, io, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .c3-tmp -> repo root
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

st = json.load(open(os.path.join(ROOT, "src/os/state.json"), encoding="utf-8"))
print("TICK", st.get("tick"), "| TS", st.get("ts"), "| TASK", (st.get("task") or "")[:80])
log = st.get("log", [])
print("LOG_LEN", len(log))
for line in log[-3:]:
    print("LOG_TAIL:", line[:240].replace("\n", " "))
wm = st.get("decisions_watermark", {})
print("WM_DNUMS_TAIL", (wm.get("dnums") or [])[-6:])

od = os.path.join(ROOT, "orders")
files = [(f, os.path.getmtime(os.path.join(od, f))) for f in os.listdir(od)]
files.sort(key=lambda x: -x[1])
for f, m in files[:3]:
    print("ORDER:", f, datetime.datetime.fromtimestamp(m).strftime("%m-%d %H:%M"))

led = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
try:
    txt = open(led, encoding="utf-8", errors="replace").read()
    rows = [l for l in txt.splitlines() if re.match(r"^\[\d{4}-", l) and ("@BigStream" in l or "@七线全司" in l or "@全司" in l or "@六司" in l or "@八线全量" in l)]
    print("LEDGER_ROWS", len(rows))
    for r in rows[-2:]:
        print("LEDGER_NEW:", r[:140])
except Exception as e:
    print("LEDGER_ERR", e)

dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    txt = open(dec, encoding="utf-8", errors="replace").read()
    nums = set(re.findall(r"\b[DC]-\d{8}-\d{2}\b", txt))
    wmset = set(wm.get("dnums") or [])
    new = sorted(nums - wmset)
    print("DEC_TOTAL", len(nums), "NEW_VS_WM", new if new else "QUIET")
except Exception as e:
    print("DEC_ERR", e)
print("NOW", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
