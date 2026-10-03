import json, io

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(p, "r", encoding="utf-8") as f:
    st = json.load(f)

out = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1088_verify.txt", "w", encoding="utf-8")
out.write("tick=%s\nts=%s\nproduction=%s\n" % (st.get("tick"), st.get("ts"), st.get("production")))
out.write("task=%s\n" % st.get("task"))
last = st["log"][-1]
out.write("--- last log entry head 200 chars ---\n%s\n" % last[:200])
out.write("--- last log entry tail 200 chars ---\n%s\n" % last[-200:])
out.close()
print("verify written")
