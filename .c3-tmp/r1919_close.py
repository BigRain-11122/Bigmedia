# r1919_close.py -- stage-2 accounting close for round R1919 (waiting round:
# tech#75 judge-position executed per canon gate -> NO-GO; four legs stay
# fire-ready gated). Pure-ASCII script (encoding law); CJK payloads live in
# data files (r1919_log.txt = state log line). No export refresh this round
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

TICK = 1919
ROUND_TAG = "R1919"
LOG_DATA = os.path.join(".c3-tmp", "r1919_log.txt")
STATE_PATH = os.path.join("src", "os", "state.json")
TECH_PATH = os.path.join("state", "queue", "tech.md")

EVIDENCE = [
    os.path.join(".c3-tmp", "r1919_group_scan.json"),
    os.path.join(".c3-tmp", "r1919_probes.txt"),
    os.path.join(".c3-tmp", "r1919_ollama.json"),
    os.path.join(".c3-tmp", "r1919_gpu_gate.txt"),
]

FOCUS_NEW = (
    "R1920 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件"
    "+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+GPU C-37 fresh 四腿点火判断"
    "〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13〕"
    "+tech#75 判断位照正法〔ollama_probe --json+gate --samples 6 双 GO=fire 窗〕"
    "+meme V1 成片/全曲 MV 查看位随轮盯+live 大白话常设纪律维持）"
)

TECH_NOTE = (
    "——**[R1919 判断位照正法执行]**：22:44 探针 face=ok util76/mem11749"
    "+gate --samples 6 worst-case free 529MB band 15/util 100=**稳态饱和域 NO-GO**"
    "（与 R1918 首读同域·非双 GO 不点火·预注册门照守）·序列数据点续记（fire 窗等待位维持）"
)


def main():
    now = datetime.datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")

    # 1. tech.md #75 sequence note (anchor = current tail of entry 75)
    with io.open(TECH_PATH, encoding="utf-8") as f:
        lines = f.read().split("\n")
    hit = 0
    for i, ln in enumerate(lines):
        if ln.startswith("75. ") and ln.rstrip().endswith("capabilities v1.79"):
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
        "R1919 close: waiting-round accounting tick=1919; GPU C-37 NO-GO "
        "(steady-saturated MV sprint lane, four legs fire-ready gated); "
        "tech#75 judge gate NO-GO per canon (no double-GO, seq point to "
        "tech.md); watch roots zero new arrivals (meme V1 cut in flight); "
        "five-checks quiet (truly_new=0 wm131, @BigStream 4==anchor); "
        "probes in-band (board 0F, readiness 3 external 0 findings, "
        "loop_health 2F+229W all in-case); replenish: no genuine seed "
        "(zero-inflation); next R1920: #112 judge window 10-11 08:00 "
        "due-date claim [via bm-a]")
    files = [STATE_PATH.replace("\\", "/"), TECH_PATH.replace("\\", "/"),
             os.path.join(".c3-tmp", "r1919_close.py"), LOG_DATA] + EVIDENCE
    rc, lines = close_commit.run_close_commit(files, msg)
    for ln in lines:
        print(ln)
    print("close rc=%s" % rc)
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
