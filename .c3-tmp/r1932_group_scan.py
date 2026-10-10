# R1932 five-check group scan (ASCII output only)
import json, re, os, datetime

HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = []

def mtime(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "ERR:%s" % e

# 1) decisions dnum content-addressed diff vs watermark
dec_path = os.path.join(HQ, "docs", "decisions.md")
state = json.load(open(r"src\os\state.json", encoding="utf-8"))
wm = set(state.get("decisions_watermark", {}).get("dnums", []))
raw = open(dec_path, encoding="utf-8", errors="replace").read()
toks = set(re.findall(r"[DC]-\d{8}-\d{2}", raw))
truly_new = sorted(toks - wm)
OUT.append("=== DECISIONS ===")
OUT.append("file mtime=%s tokens=%d watermark=%d truly_new=%d" % (mtime(dec_path), len(toks), len(wm), len(truly_new)))
if truly_new:
    OUT.append("TRULY_NEW: %s" % ", ".join(truly_new))

# 2) ledger @BigStream strict rows + group tags
led_path = os.path.join(HQ, "cph4", "evolution-ledger.md")
led_raw = open(led_path, encoding="utf-8", errors="replace").read()
bs_lines = [l for l in led_raw.splitlines() if "@BigStream" in l]
OUT.append("=== LEDGER ===")
OUT.append("mtime=%s @BigStream lines=%d" % (mtime(led_path), len(bs_lines)))
for tag in ["@七线全司", "@全司", "@六司", "@八线全量"]:
    n = sum(1 for l in led_raw.splitlines() if tag in l and "BigStream" not in l)
    if n:
        OUT.append("group-tag %s lines=%d (non-BigStream)" % (tag, n))

# 3) mtimes
OUT.append("=== MTIME ===")
for label, p in [
    ("hq-orders", os.path.join(HQ, "docs", "orders.md")),
    ("hq-decisions", dec_path),
    ("ledger", led_path),
]:
    OUT.append("%s %s size=%d" % (label, mtime(p), os.path.getsize(p)))

# own orders top file
own_dir = r"orders"
own = sorted(os.listdir(own_dir))
own_top = "\n".join(own[-3:])
OUT.append("own-orders-list-tail: %s" % own_top.replace("\n", " | "))
p = os.path.join("orders", "O-20260908-1105-bm-a.md")
OUT.append("own-orders-top O-20260908-1105 mtime=%s" % mtime(p))

# 4) HQ orders tail lines (mtime anchor check)
ho = open(os.path.join(HQ, "docs", "orders.md"), encoding="utf-8", errors="replace").read()
tail = [l for l in ho.splitlines() if l.strip()][-3:]
OUT.append("hq-orders-tail:")
for l in tail:
    OUT.append("  | %s" % l[:120].encode("ascii", "replace").decode("ascii"))

txt = "\n".join(OUT)
open(r".c3-tmp\r1932_group_scan.txt", "w", encoding="utf-8").write(txt)
print(txt.encode("ascii", "replace").decode("ascii"))
