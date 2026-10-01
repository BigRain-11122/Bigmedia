import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r941_logline.txt"), encoding="utf-8").read().strip()
assert line.startswith("2026-10-02 05:3") and line.endswith("下轮=R942 声明窗满 6/6 batch close（区间 R937-R942·commit 注区间）。"), "logline shape"

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 940, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 968, "log count drift: %d" % len(sj["log"])

sj["tick"] = 941
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]
sj["focus"] = ("R941: 等待态并窗 5/6（五查 mtime 锚定静+三探针基线持平——下轮 R942=声明窗满 6/6 batch close（区间 R937-R942·commit 注区间）或 10-03 00:00 跨日先到即收："
               "①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）"
               "②10-03 00:00 跨日=日界批收+10-03 日报补产+REACT 10-03 领件"
               "③#94=10-04 记忆梳理④W41=10-05 周报+提案窗）")

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + assertions)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 05:3"), "log-ts head assertion failed"
assert int(sj2["tick"]) == 941 and len(sj2["log"]) == 969
assert sj2["ts"] and sj2["task"].startswith("R941:")
assert sj2["production"] == "open"
print("CLOSE-OK tick=%s ts=%s log_entries=%d" % (sj2["tick"], sj2["ts"], len(sj2["log"])))
