# -*- coding: utf-8 -*-
"""R1854 explore#16: radar embed proposal probes.
1) R1853 round pointer extraction  2) group orders.md path/mtime
3) CORS header probes on /api/v1/dailies/latest  4) field dump for consumption spec.
ASCII console output only; CJK payloads to UTF-8 files.
"""
import io, json, re, os, datetime, urllib.request, urllib.error, urllib.parse

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
FG = r"C:\Users\sjs20\Desktop\FluxGroup"
API = "http://127.0.0.1:3101"

# --- 1. R1853 next-round pointer ---
with io.open(BS + r"\src\os\state.json", encoding="utf-8") as f:
    st = json.load(f)
rows1853 = [l for l in st.get("log", []) if "R1853" in l[:30]]
ptr = ""
if rows1853:
    m = re.search(r"下轮=R1854[^\"”]*", rows1853[-1])
    ptr = m.group(0) if m else "NO_PTR_TOKEN"
with io.open(BS + r"\.c3-tmp\r1854_ptr.txt", "w", encoding="utf-8") as f:
    f.write(ptr)
print("PTR_WRITTEN", len(ptr))

# --- 2. group orders.md path discovery ---
cands = [FG + r"\docs\orders.md", FG + r"\cph4\orders.md", FG + r"\cph4\docs\orders.md"]
found = ""
for c in cands:
    if os.path.exists(c):
        found = c + " | mtime=" + datetime.datetime.fromtimestamp(os.path.getmtime(c)).strftime("%m-%d %H:%M:%S")
        break
print("ORDERS_PATH", found or "NOT_FOUND_IN_CANDIDATES")

# --- 3. CORS probes ---
def req(method, path, headers=None, timeout=10):
    r = urllib.request.Request(API + path, method=method)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:
        return -1, {}, str(e).encode()

s0, h0, b0 = req("GET", "/api/health")
print("HEALTH", s0, b0[:60].decode("utf-8", "replace"))

s2, h2, b2 = req("GET", "/api/v1/dailies/latest", {"Origin": "http://localhost:5500"})
print("GET_WITH_ORIGIN", s2, "| ACAO=", h2.get("Access-Control-Allow-Origin"),
      "| Vary=", h2.get("vary"), "| ACAH=", h2.get("Access-Control-Allow-Headers"))

s3, h3, b3 = req("OPTIONS", "/api/v1/dailies/latest",
                 {"Origin": "http://localhost:5500", "Access-Control-Request-Method": "GET"})
print("OPTIONS_PREFLIGHT", s3, "| ACAO=", h3.get("Access-Control-Allow-Origin"),
      "| ACAM=", h3.get("Access-Control-Allow-Methods"), "| Allow=", h3.get("allow"))

s4, h4, b4 = req("GET", "/api/v1/dailies/latest", {"Origin": "null"})
print("GET_NULL_ORIGIN", s4, "| ACAO=", h4.get("Access-Control-Allow-Origin"))

cors = {
    "health": {"status": s0},
    "get_with_origin": {"status": s2, "acao": h2.get("Access-Control-Allow-Origin"),
                        "vary": h2.get("vary"), "allow_headers": h2.get("Access-Control-Allow-Headers")},
    "options_preflight": {"status": s3, "acao": h3.get("Access-Control-Allow-Origin"),
                          "acam": h3.get("Access-Control-Allow-Methods"),
                          "allow": h3.get("allow"), "body_head": b3[:120].decode("utf-8", "replace")},
    "get_null_origin": {"status": s4, "acao": h4.get("Access-Control-Allow-Origin")},
    "probe_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

# --- 4. field dump ---
latest = {}
if s2 == 200:
    try:
        latest = json.loads(b2.decode("utf-8"))
    except Exception as e:
        print("LATEST_PARSE_ERR", repr(e)[:80])
with io.open(BS + r"\.c3-tmp\r1854_latest.json", "w", encoding="utf-8") as f:
    json.dump(latest, f, ensure_ascii=False, indent=1)
with io.open(BS + r"\.c3-tmp\r1854_cors.json", "w", encoding="utf-8") as f:
    json.dump(cors, f, ensure_ascii=False, indent=1)

def walk(o, d=0, path=""):
    """compact shape summary, lists sampled at first element + count"""
    if d > 4:
        return "..."
    if isinstance(o, dict):
        return {k: walk(v, d + 1, path + "." + k) for k, v in list(o.items())[:24]}
    if isinstance(o, list):
        return {"__len": len(o), "__first": walk(o[0], d + 1, path + "[0]") if o else None}
    return type(o).__name__

print("TOP_KEYS", list(latest.keys()))
rep = latest.get("report")
if isinstance(rep, dict):
    print("REPORT_KEYS", list(rep.keys()))
    for k, v in rep.items():
        if isinstance(v, list):
            print("REPORT_LIST", k, "len=", len(v))
        elif isinstance(v, dict):
            print("REPORT_DICT", k, "keys=", list(v.keys())[:12])
shape = walk(latest)
with io.open(BS + r"\.c3-tmp\r1854_shape.json", "w", encoding="utf-8") as f:
    json.dump(shape, f, ensure_ascii=False, indent=1)
print("SHAPE_WRITTEN")
