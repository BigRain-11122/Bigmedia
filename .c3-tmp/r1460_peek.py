# -*- coding: ascii -*-
# R1460 state.json structure peek
import io, json

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(P, "r", encoding="utf-8") as f:
    st = json.load(f)
print("TOP_KEYS:", sorted(st.keys()))
print("TOP_TS:", st.get("ts"))
print("TOP_TASK[:60]:", (st.get("task") or "")[:60])
print("TICK:", st.get("tick"))
wm = st.get("decisions_watermark", {})
print("WM_TS:", wm.get("ts"), "WM_DNUMS:", len(wm.get("dnums", [])))
lg = st.get("log", [])
print("LOG_LEN:", len(lg))
print("LOG_LAST_PREFIX:", lg[-1][:40] if lg else None)
