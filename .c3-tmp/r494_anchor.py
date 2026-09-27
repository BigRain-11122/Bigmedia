# r494_anchor.py - dump exact anchor texts from status-export.json for r494_account (OUTP new, utf-8)
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r494_anchor.txt")
se = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), "r", encoding="utf-8"))
L = []
L.append("export_ts=" + repr(se["export_ts"]))
L.append("outs_len=%d outs0_len=%d" % (len(se["outs"]), len(se["outs"][0])))
L.append("== outs0_1_full ==")
L.append(se["outs"][0][1])
L.append("== outs0_2_head300 ==")
L.append(se["outs"][0][2][:300])
L.append("== outs0_2_len ==")
L.append(str(len(se["outs"][0][2])))
L.append("== results0_full ==")
L.append(json.dumps(se["results"][0], ensure_ascii=False))
L.append("== results0_tick ==")
L.append(repr(se["results"][0][0]))
with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("written=%s" % os.path.basename(OUTP))
