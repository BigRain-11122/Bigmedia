import json
d = json.load(open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json", encoding="utf-8"))
print("keys:", list(d.keys()))
print("log_len:", len(d["log"]) if "log" in d else "NO-log")
if "log" in d:
    print("last_prefix:", d["log"][-1][:50])
    print("tick:", d["tick"], "| ts:", d["ts"])
