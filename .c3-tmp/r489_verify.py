# r489_verify.py - collection validation: json parse gate + freshness + tick/task coherence (ASCII, utf-8 out)
import io, os, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r489_verify.txt")
L = []

sp = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8"))
L.append("state_json=OK tick=%d production=%s" % (sp["tick"], sp["production"]))
L.append("state_ts=%s" % sp["ts"])
last = sp["log"][-1]
L.append("log_len=%d last_prefix_ok=%s" % (len(sp["log"]), last.startswith("2026-09-27 08:36 R489: ")))
rest = last.split("R489: ", 1)[1] if "R489: " in last else ""
L.append("task_matches_log_head=%s (task_len=%d)" % (sp["task"] == rest[:60], len(sp["task"])))
dt = datetime.datetime.strptime(sp["ts"], "%Y-%m-%d %H:%M:%S")
age_min = (datetime.datetime.now() - dt).total_seconds() / 60.0
L.append("ts_age_minutes=%.1f" % age_min)
L.append("log_r488_comma_ok=%s" % ("2026-09-27 08:26 R488:" in sp["log"][-2]))

se = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), "r", encoding="utf-8"))
L.append("export_json=OK export_ts=%s" % se["export_ts"])
L.append("results0=%s" % se["results"][0][0])
L.append("outs0_e1_head=" + se["outs"][0][1][:24])
L.append("outs0_e2_head=" + se["outs"][0][2][:24])

with io.open(OUTP, "w", encoding="utf-8") as fo:
    fo.write("\n".join(L) + "\n")
print("written")
