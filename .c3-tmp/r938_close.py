import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r938_logline.txt"), encoding="utf-8").read().strip()

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 937, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 965, "log count drift: %d" % len(sj["log"])

sj["tick"] = 938
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]
sj["focus"] = "R938: 等待态并窗 2/6（五静+探针绿+四查尽·供给闸四路闭+时序闸全列）——下轮 R939 同判承接：①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）②10-03 00:00 跨日先到=日界批收+10-03 日报补产+REACT 10-03 领件③#94①10-04 记忆梳理④W41=10-05（周报+自驱提案窗+CLOUD_LINE 首测）"

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + head-timestamp assertion)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 "), "log-ts head assertion failed"
assert int(sj2["tick"]) == 938 and len(sj2["log"]) == 966
print("CLOSE-OK tick=%s ts=%s task=%r log_entries=%d" % (sj2["tick"], sj2["ts"], sj2["task"], len(sj2["log"])))
