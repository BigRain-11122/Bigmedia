# r1920_close.py -- stage-2 accounting close for round R1920 (waiting round:
# tech#75 judge position executed per canon -> oscillating-regime single-GO gap
# correctly held by the preregistered consecutive-2 gate; four legs stay
# fire-ready gated). Pure-ASCII script (encoding law); CJK payloads live in
# data files (r1920_log.txt = state log line). No export refresh this round
# (export_ts 20:56:29 <24h, zero CEO-visible change, product-law throttle).
# Steps: tech.md #75 sequence note -> state.json accounting -> embedded commit
# (close_commit.run_close_commit, tech#65/67 law).

import datetime
import io
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "src", "os"))

TICK = 1920
ROUND_TAG = "R1920"
LOG_DATA = os.path.join(".c3-tmp", "r1920_log.txt")
STATE_PATH = os.path.join("src", "os", "state.json")
TECH_PATH = os.path.join("state", "queue", "tech.md")

EVIDENCE = [
    os.path.join(".c3-tmp", "r1920_probes.txt"),
    os.path.join(".c3-tmp", "r1920_gpu_gate.txt"),
    os.path.join("data", "pipeline", "ollama-probe-ledger.jsonl"),
]

FOCUS_NEW = (
    "R1921 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件"
    "+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+GPU C-37 fresh 四腿点火判断"
    "〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13〕"
    "+tech#75 判断位照正法〔双 GO 连续 ≥2 方飞〕"
    "+meme V1 成片/全曲 MV 查看位随轮盯）"
)

TECH_NOTE = (
    "——**[R1920 判断位照正法执行=振荡域单 GO 间隙实战拦住]**：22:54 读数 free "
    "1105MB（9216/2048 双守卫皆败）→22:57 读数三闸单过 GO（评审腿 2048 守卫 "
    "worst-case free 8832/util 31/band 176=fire 候选）→22:58 第二连读 NO-GO"
    "（util worst-case 98>80+band 5131 振荡域 advisory）→预注册门「连续 ≥2 读数"
    "方飞」正确拦住=**稳定性面首战实战价值实证**（单 GO=Krea2 载入周期间隙·无"
    "连续门则 1500s E4 长飞烧进抖动窗=R1876 争抢双损族）·序列数据点续记"
    "（fire 稳定窗等待位维持）"
)


def main():
    now = datetime.datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")

    # 1. tech.md #75 sequence note (anchor = current tail of entry 75)
    with io.open(TECH_PATH, encoding="utf-8") as f:
        lines = f.read().split("\n")
    hit = 0
    for i, ln in enumerate(lines):
        if ln.startswith("75. ") and ln.rstrip().endswith("fire 窗等待位维持）"):
            lines[i] = ln.rstrip() + TECH_NOTE
            hit += 1
            break
    assert hit == 1, "tech#75 entry not anchored uniquely (hit=%d)" % hit
    with io.open(TECH_PATH, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    print("tech.md 75 note appended")

    # 2. state.json accounting
    raw = io.open(LOG_DATA, encoding="utf-8").read().strip()
    log_line = raw.replace("@TS@", now.strftime("%H:%M"))
    assert "@TS@" not in log_line and log_line.startswith("2026-10-10 ")
    body = log_line.split(" %s: " % ROUND_TAG, 1)[1]
    d = json.load(io.open(STATE_PATH, encoding="utf-8"))
    assert d.get("tick") == TICK - 1, "unexpected tick %s" % d.get("tick")
    d["tick"] = TICK
    d["ts"] = ts
    d["task"] = body[:60]
    d["focus"] = FOCUS_NEW
    d["log"].append(log_line)
    with io.open(STATE_PATH, "w", encoding="utf-8", newline="") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("state updated: tick=%s ts=%s task=%s..." % (TICK, ts, body[:24]))

    # 3. embedded close commit (no deliverable stage this round; waiting round)
    import close_commit
    msg = (
        "R1920 close: waiting-round tick=1920; tech#75 judge per canon: "
        "oscillating single-GO gap held by consecutive-2 prereg gate "
        "(22:57 GO free8832/u31/band176 -> 22:58 NO-GO u98/band5131; stability "
        "face first real catch); four legs fire-ready gated (v17 materials "
        "turnkey verified); five-checks quiet (wm131, @BigStream 4==anchor); "
        "watch roots zero new; probes in-band (board 0F, readiness 3 ext 0 "
        "findings, lh 2F+229W in-case); export skip (<24h zero change); "
        "replenish: no genuine seed; next R1921: #112 window 10-11 08:00 "
        "due-date claim [via bm-a]")
    files = [STATE_PATH.replace("\\", "/"), TECH_PATH.replace("\\", "/"),
             os.path.join(".c3-tmp", "r1920_close.py"), LOG_DATA] + EVIDENCE
    rc, lines = close_commit.run_close_commit(files, msg)
    for ln in lines:
        print(ln)
    print("close rc=%s" % rc)
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
