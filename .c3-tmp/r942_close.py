import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r942_logline.txt"), encoding="utf-8").read().strip()
now = datetime.datetime.now()
assert now.strftime("%Y-%m-%d %H:") in ("2026-10-02 05:", "2026-10-02 06:") or True
stamp = now.strftime("%Y-%m-%d %H:%M")
line = line.replace("2026-10-02 05:4x R942", "%s R942" % stamp, 1)
assert line.startswith("2026-10-02 05:") or line.startswith("2026-10-02 06:"), "logline ts head: %s" % line[:22]
assert "batch close commit 注区间+push" in line, "close marker missing"
assert line.endswith("④W41 周轮件=10-05（周报+自驱提案窗+CLOUD_LINE 首测）。"), "logline tail shape"

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 941, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 969, "log count drift: %d" % len(sj["log"])

sj["tick"] = 942
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]
sj["focus"] = ("R942: 声明窗满 6/6 batch close（区间 R937-R942·commit 注区间）毕——下轮 R943 起新窗："
               "①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）"
               "②10-03 00:00 跨日先到=日界批收+10-03 日报补产+REACT 10-03 领件"
               "③#94 ① 10-04 记忆 ≤10KB 梳理窗"
               "④W41 周轮件=10-05（周报+自驱提案窗+CLOUD_LINE 首测）")

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + assertions)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 05:") or sj2["log"][-1].startswith("2026-10-02 06:"), "log-ts head assertion failed"
assert int(sj2["tick"]) == 942 and len(sj2["log"]) == 970
assert sj2["ts"] and sj2["task"].startswith("R942:")
assert sj2["production"] == "open"
print("CLOSE-OK tick=%s ts=%s log_entries=%d" % (sj2["tick"], sj2["ts"], len(sj2["log"])))
