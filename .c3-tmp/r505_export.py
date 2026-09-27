# -*- coding: utf-8 -*-
"""R505 status-export refresh: export_ts + results derived update (P-61)."""
import io, json, datetime

FP = r"docs\status-export.json"
d = json.load(io.open(FP, encoding="utf-8"))
now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
d["export_ts"] = now

# preview structure of results/outs (derived faces)
def show(k):
    v = d.get(k)
    if isinstance(v, list):
        print(k, "list len", len(v))
        for it in v[-2:]:
            print("  -", json.dumps(it, ensure_ascii=False)[:200])
    else:
        print(k, json.dumps(v, ensure_ascii=False)[:200])

buf = io.open(r".c3-tmp\r505_export_preview.txt", "w", encoding="utf-8")
def p(*a):
    s = " ".join(str(x) for x in a)
    buf.write(s + "\n")

for k in ("results", "outs"):
    v = d.get(k)
    if isinstance(v, list):
        p(k, "list len", len(v))
        for it in v[-3:]:
            p("  -", json.dumps(it, ensure_ascii=False)[:220])
    else:
        p(k, json.dumps(v, ensure_ascii=False)[:300])
p("keys:", list(d.keys()))

# append derived result row for R505 (agenda-3 sample script delivered)
res = d.get("results")
if isinstance(res, list):
    res.append({
        "ts": now,
        "round": "R505",
        "agenda": "O-20260927-1050-HQ-C agenda-3",
        "delivered": "city-narrative first sample script SC-003-01-v1 (data/storylines/video/): 12-beat shipinhao-60s script on C-00010 real-anchor card, charter gates consumed (factual-line triple-label + T1-T9 + cyber-register + plain-language), 13-entry field-level source list, U243 merge slot reserved",
        "window": "ahead of <=09-29 10:50"
    })
    d["results"] = res[-30:]

json.dump(d, io.open(FP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
buf.close()
print("export_ts ->", now)
