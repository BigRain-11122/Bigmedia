# r483_fix.py - remove illegal trailing comma on last log element (R477 pitfall family), verify both JSON files
import io, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
P = ROOT + r"\src\os\state.json"
t = io.open(P, encoding="utf-8").read()
broken = '\uff084/6\uff09\u3002",\n ],'
fixed = '\uff084/6\uff09\u3002"\n ],'
n = t.count(broken)
if n == 1:
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace(broken, fixed))
    print("replaced=1")
else:
    print("replaced=%d (no action taken)" % n)
s = json.load(io.open(P, encoding="utf-8"))
print("state JSON_OK tick=%s ts=%s nlog=%d tasklen=%d" % (s["tick"], s["ts"], len(s["log"]), len(s["task"])))
print("logtail_head=%s" % s["log"][-1][:26].encode("ascii", "replace").decode("ascii"))
print("task_head=%s" % s["task"][:46].encode("ascii", "replace").decode("ascii"))
print("logtail_has_r483=%s logtail_has_r482=%s" % (any(x.startswith("2026-09-27 07:34 R483:") for x in s["log"]), any(x.startswith("2026-09-27 07:25:34 R482:") for x in s["log"])))

e = json.load(io.open(ROOT + r"\docs\status-export.json", encoding="utf-8"))
print("export JSON_OK ts=%s outs0_n=%d" % (e["export_ts"], len(e["outs"][0])))
print("outs0_heads=%s" % [x[:9].encode("ascii", "replace").decode("ascii") for x in e["outs"][0]])
print("results0=%s r1_head=%s" % (e["results"][0][0], e["results"][0][1][:10].encode("ascii", "replace").decode("ascii")))
