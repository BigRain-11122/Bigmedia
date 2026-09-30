# -*- coding: utf-8 -*-
# R719: inspect LC-013 plan.json card drawtext geometry (card00 vs card09)
import json, re, io, sys

PLAN = r"output/renders/lc-013-v1-shipinhao-60s.mp4.plan.json"
with io.open(PLAN, encoding="utf-8") as f:
    plan = json.load(f)

out = []
out.append("plan keys: %s" % sorted(plan.keys()))
for k in plan.keys():
    v = plan[k]
    if isinstance(v, str) and "drawtext" in v:
        out.append("== filtergraph in key: %s (len %d) ==" % (k, len(v)))
        fg = v
        # split into drawtext entries
        parts = fg.split("drawtext=")
        for p in parts[1:]:
            entry = "drawtext=" + p
            if "card00." in entry or "card09." in entry:
                # compact: show textfile name, fontsize, y expr, enable
                tf = re.search(r"textfile='([^']+)'", entry)
                fs = re.search(r"fontsize=(\d+)", entry)
                y = re.search(r"y=([^:]+?)(?::enable|:alpha|$)", entry)
                en = re.search(r"enable='between\(t,([\d.]+),([\d.]+)\)'", entry)
                out.append("  %s fs=%s y=%s enable=%s-%s" % (
                    tf.group(1) if tf else "?",
                    fs.group(1) if fs else "?",
                    (y.group(1) if y else "?")[:80],
                    en.group(1) if en else "?", en.group(2) if en else "?"))
    elif isinstance(v, list):
        out.append("key %s: list len %d" % (k, len(v)))

with io.open(r".lc013-tmp\r719_plan_probe.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out[:60]))
print("... written to .lc013-tmp/r719_plan_probe.txt")
