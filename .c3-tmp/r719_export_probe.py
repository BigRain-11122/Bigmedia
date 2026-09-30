# -*- coding: utf-8 -*-
# R719: probe status-export live/outs/depts structure -> dump to UTF-8 file
import io, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
with io.open(ROOT + r"\docs\status-export.json", encoding="utf-8") as f:
    d = json.load(f)

out = []
out.append("== live (%d rows) ==" % len(d["live"]))
for r in d["live"]:
    out.append(repr(r)[:400])
out.append("")
out.append("== outs ==")
out.append(json.dumps(d["outs"], ensure_ascii=False)[:1500])
out.append("")
out.append("== depts keys ==")
if isinstance(d["depts"], dict):
    out.append(",".join(list(d["depts"].keys())[:30]))
else:
    out.append(json.dumps(d["depts"], ensure_ascii=False)[:800])
out.append("")
out.append("== results len %d, last 2 ==" % len(d["results"]))
for r in d["results"][-2:]:
    out.append(repr(r)[:260])
out.append("")
out.append("== chips ==")
out.append(json.dumps(d["chips"], ensure_ascii=False)[:1200])

with io.open(ROOT + r"\.lc013-tmp\r719_export_dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("dumped ok")
