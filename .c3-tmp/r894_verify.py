# -*- coding: utf-8 -*-
import io, json
s = json.load(io.open(r"src\os\state.json", encoding="utf-8"))
o = []
o.append("tick %s ts %s" % (s["tick"], s["ts"]))
o.append("task: " + s["task"])
last = s["log"][-1]
o.append("last log len %d" % len(last))
o.append("head: " + last[:100])
ok = ("waiting: supply-gated lane held" in last) and ("ETA 2026-10-02" in last) and (last.startswith("2026-10-01 21:"))
o.append("waiting-decl: " + ("OK" if ok else "MISSING"))
io.open(r".c3-tmp\r894_verify.txt", "w", encoding="utf-8").write("\n".join(o))
print("verify written")
