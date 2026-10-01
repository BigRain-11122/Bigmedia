import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r953_logline.txt"), encoding="utf-8").read().strip()
now = datetime.datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M")
line = line.replace("2026-10-02 07:3x R953", "%s R953" % stamp, 1)
assert line.startswith("2026-10-02 0"), "logline ts head: %s" % line[:22]
assert "并窗第 5/6 轮" in line and "waiting: supply-gated lane held" in line, "shape markers missing"
assert line.endswith("REACT 10-03 领件"), "logline tail shape"
assert "done955>tick952" in line, "account-lag numbers missing"

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 952, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 980, "log count drift: %d" % len(sj["log"])
assert sj["log"][-1].startswith("2026-10-02 07:25 R952"), "prev tail mismatch: %s" % sj["log"][-1][:24]

sj["tick"] = 953
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]
sj["focus"] = ("R953: 等待态声明收轮（并窗 5/6·承 R952）毕——下轮 R954（实况变化即转全任务书）"
               "=声明窗满 6/6 batch close（区间 R949-R954·commit 注区间）或 10-03 00:00 跨日先到"
               "=日界批收+10-03 日报补产+REACT 10-03 领件；OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）")

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + assertions)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 0"), "log-ts head assertion failed"
assert int(sj2["tick"]) == 953 and len(sj2["log"]) == 981
assert sj2["ts"] and sj2["task"].startswith("R953:")
assert sj2["production"] == "open"
print("CLOSE-OK tick=%s ts=%s log_entries=%d" % (sj2["tick"], sj2["ts"], len(sj2["log"])))
