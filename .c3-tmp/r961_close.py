import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r961_logline.txt"), encoding="utf-8").read().strip()
now = datetime.datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M")
line = line.replace("2026-10-02 08:5x R961", "%s R961" % stamp, 1)
assert line.startswith("2026-10-02 08:"), "logline ts head: %s" % line[:22]
assert "1/6" in line and "waiting: supply-gated lane held" in line, "shape markers missing"
assert "done963>tick960" in line, "account-lag numbers missing"
assert "r961_check.py" in line and "r961_probes.py" in line, "evidence script refs missing"
assert line.endswith("REACT 10-03 领件"), "logline tail shape"

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 960, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 988, "log count drift: %d" % len(sj["log"])
assert sj["log"][-1].startswith("2026-10-02 08:43 R960"), "prev tail mismatch: %s" % sj["log"][-1][:28]

sj["tick"] = 961
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]
sj["focus"] = ("R961: 声明窗新窗 1/6（实况变化即转全任务书）："
               "①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）"
               "②10-03 00:00 跨日先到=日界批收+10-03 日报补产+REACT 10-03 领件"
               "③#94 ① 10-04 记忆 ≤10KB 梳理窗④W41 周轮件=10-05（周报+自驱提案窗+CLOUD_LINE 首测）")

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + assertions)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 08:"), "log-ts head assertion failed"
assert int(sj2["tick"]) == 961 and len(sj2["log"]) == 989
assert sj2["ts"] and sj2["task"].startswith("R961:")
assert sj2["production"] == "open"
print("CLOSE-OK tick=%s ts=%s log_entries=%d" % (sj2["tick"], sj2["ts"], len(sj2["log"])))
