# -*- coding: utf-8 -*-
# r615_focusfix.py -- patch focus: add explicit window range R615-R620 (verify check face alignment)
import io, json

SP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
st = json.load(io.open(SP, encoding="utf-8"))
f = st["focus"]
old = u"idle-fast 一行收账（窗 2/6·本窗不 commit·满 6=R620 或跨日 09-29 00:00 先到即 batch commit）"
new = u"idle-fast 一行收账（窗 2/6=R615-R620·本窗不 commit·满 6=R620 或跨日 09-29 00:00 先到即 batch commit）"
assert old in f, "focus patch anchor not found"
st["focus"] = f.replace(old, new)
json.dump(st, io.open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FOCUS_PATCH OK")
