import json, os, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SP = os.path.join(BS, "src", "os", "state.json")

line = open(os.path.join(BS, ".c3-tmp", "r939_logline.txt"), encoding="utf-8").read().strip()
assert line.startswith("2026-10-02 05:1") and line.endswith("R940 同判承接。"), "logline shape"

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 938, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 966, "log count drift: %d" % len(sj["log"])

sj["tick"] = 939
sj["log"].append(line)
sj["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
parts = line.split(" ", 2)
sj["task"] = (parts[2] if len(parts) >= 3 else line)[:60]
sj["focus"] = ("R939: 等待态并窗 3/6（五查 mtime 锚定静+三探针在案基线——下轮 R940 同判承接："
               "①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）"
               "②10-03 00:00 跨日先到=日界批收 R937-R939 声明窗+10-03 日报补产+REACT 10-03 领件"
               "③#94=10-04 记忆梳理④W41=10-05 周报+提案窗）")

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + head-timestamp assertion)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == line, "appended line mismatch after reload"
assert sj2["log"][-1].startswith("2026-10-02 "), "log-ts head assertion failed"
assert int(sj2["tick"]) == 939 and len(sj2["log"]) == 967
assert sj2["ts"] and sj2["task"].startswith("R939:")
print("CLOSE-OK tick=%s ts=%s log_entries=%d" % (sj2["tick"], sj2["ts"], len(sj2["log"])))
