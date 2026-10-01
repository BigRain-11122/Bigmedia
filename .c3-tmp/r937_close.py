import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r937_logline.txt"), encoding="utf-8").read().strip()

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 936, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 964, "log count drift: %d" % len(sj["log"])

sj["tick"] = 937
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + head-timestamp assertion)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 "), "log-ts head assertion failed"
assert int(sj2["tick"]) == 937 and len(sj2["log"]) == 965
print("CLOSE-OK tick=%s ts=%s task=%r log_entries=%d" % (sj2["tick"], sj2["ts"], sj2["task"], len(sj2["log"])))
