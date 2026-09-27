# -*- coding: utf-8 -*-
"""R505 fix: results panel is ["N","desc"] stat pairs - revert appended dict; derive outs row for O-1050 instead."""
import io, json, datetime

FP = r"docs\status-export.json"
d = json.load(io.open(FP, encoding="utf-8"))
now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
d["export_ts"] = now

# 1) revert: drop any dict entries from results (keep established pair format)
res = d.get("results", [])
clean = [r for r in res if isinstance(r, (list, tuple))]
dropped = len(res) - len(clean)
if dropped:
    clean = clean[-30:]
d["results"] = clean

# 2) outs: find O-1050 row and refresh status (derived face)
outs = d.get("outs", [])
tag = "O-20260927-1050"
hit = None
for row in outs:
    if isinstance(row, (list, tuple)) and len(row) >= 2 and tag in str(row[0]):
        hit = row
        break
status_txt = ("agenda1 done R504 (R-03 v1.0 four-cut rescan) + agenda2 done R503 (release-schedule-v1) "
              "+ agenda3 kickoff done R505: city-narrative first sample script SC-003-01-v1 delivered "
              "(data/storylines/video/, 12-beat shipinhao-60s on real anchor card C-00010, charter gates "
              "consumed, 13-entry source list, U243 merge slot reserved; production chain S1->M4 next rounds) "
              "+ agenda4 expedited window open (research-dept first topic)")
if hit is not None:
    hit[1] = "in-progress"
    hit[2] = status_txt
    newrow = False
else:
    outs.append(["media-self-drive " + tag, "in-progress", status_txt])
    newrow = True
d["outs"] = outs

json.dump(d, io.open(FP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("reverted %d dict rows; outs updated (new_row=%s); export_ts -> %s" % (dropped, newrow, now))
