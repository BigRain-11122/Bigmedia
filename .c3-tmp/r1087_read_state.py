import json, io, sys

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(p, "r", encoding="utf-8") as f:
    st = json.load(f)

out = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1087_state_head.txt", "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
w("decisions_watermark=%s" % json.dumps(st.get("decisions_watermark"), ensure_ascii=False))
w("--- keys ---")
w(",".join(sorted(st.keys())))
w("--- last 3 log entries ---")
log = st.get("log", [])
for line in log[-3:]:
    w(line)
    w("===")
out.close()
print("ok")
