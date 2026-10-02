import json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r1035_verify.txt")
L = []
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
L.append("tick=%s" % st.get("tick"))
L.append("ts=%s" % st.get("ts"))
L.append("task=%s" % st.get("task"))
L.append("log_len=%d" % len(st.get("log", [])))
L.append("== last log line (300 chars) ==")
L.append(st["log"][-1][:300])
with open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8") as f:
    ex = json.load(f)
L.append("export_ts=%s" % ex.get("export_ts"))
L.append("live[0]=%s" % ex["live"][0][0])
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("VERIFY OK tick=%s ts=%s" % (st.get("tick"), st.get("ts")))
