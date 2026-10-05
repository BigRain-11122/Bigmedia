# r1440_check: quick five-still checks (content-addressed D-num diff + ledger hits + orders top)
import re, json, os
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = ROOT + r"\media\BigStream"
d = open(ROOT + r"\docs\decisions.md", encoding="utf-8").read()
s = set(re.findall(r"[DC]-\d{8}-\d+", d))
st = json.load(open(BS + r"\src\os\state.json", encoding="utf-8"))
w = set(st["decisions_watermark"]["dnums"])
print("DEC_TOTAL:", len(s))
print("WMARK_TOTAL:", len(w))
print("NEW_DNUMS:", sorted(s - w))
l = open(ROOT + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
hits = re.findall("@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8", l)
print("LEDGER_HITS:", len(hits))
orders = sorted(os.listdir(BS + r"\orders"))
print("ORDERS_TOP:", orders[-1])
lock = os.path.exists(BS + r"\.git\index.lock")
print("INDEX_LOCK:", lock)
