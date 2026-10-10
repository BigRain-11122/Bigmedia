# r1918_close.py -- stage-2 accounting close for round R1918 (tech#75 CPU leg).
# Pure-ASCII script (encoding law): all Chinese payloads live in data files
# (r1918_log.txt = state log line; r1918_export_patch.json = do/live patch,
#  where an empty live[1] is filled verbatim from the current export).
# Steps: state.json accounting -> export_refresh patch -> embedded commit
# (close_commit.run_close_commit, tech#65/67 law: pycache purge built in).

import datetime
import io
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "src", "os"))

TICK = 1918
ROUND_TAG = "R1918"
LOG_DATA = os.path.join(".c3-tmp", "r1918_log.txt")
PATCH_DATA = os.path.join(".c3-tmp", "r1918_export_patch.json")
STATE_PATH = os.path.join("src", "os", "state.json")
EXPORT_PATH = os.path.join("docs", "status-export.json")
PROBES_EVID = os.path.join(".c3-tmp", "r1918_probes.txt")
STABILITY_EVID = os.path.join(".c3-tmp", "r1918_t75_stability.txt")


def main():
    now = datetime.datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    log_min = now.strftime("%Y-%m-%d %H:%M")

    # 1. state.json accounting
    raw = io.open(LOG_DATA, encoding="utf-8").read().strip()
    log_line = raw.replace("@TS@", now.strftime("%H:%M"))
    assert "@TS@" not in log_line
    body = log_line.split(" %s: " % ROUND_TAG, 1)[1]
    d = json.load(io.open(STATE_PATH, encoding="utf-8"))
    assert d.get("tick") == TICK - 1, "unexpected tick %s" % d.get("tick")
    d["tick"] = TICK
    d["ts"] = ts
    d["task"] = body[:60]
    d["log"].append(log_line)
    with io.open(STATE_PATH, "w", encoding="utf-8", newline="") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("state updated: tick=%s ts=%s task=%s..." % (TICK, ts, body[:24]))

    # 2. export patch (fill live[1] from current export verbatim)
    patch = json.load(io.open(PATCH_DATA, encoding="utf-8"))
    cur = json.load(io.open(EXPORT_PATH, encoding="utf-8"))
    live = patch.get("live")
    if live and live[1] == "":
        live[1] = cur["live"][1]
        with io.open(PATCH_DATA, "w", encoding="utf-8", newline="") as f:
            json.dump(patch, f, ensure_ascii=False, indent=1)
            f.write("\n")
    r = subprocess.run(
        [sys.executable, os.path.join("src", "os", "export_refresh.py"),
         "--patch", PATCH_DATA, "--export", EXPORT_PATH],
        capture_output=True)
    print("export_refresh rc=%s" % r.returncode)
    if r.returncode != 0:
        print(r.stdout.decode("utf-8", errors="replace"))
        print(r.stderr.decode("utf-8", errors="replace"))
        return 2
    fresh = json.load(io.open(EXPORT_PATH, encoding="utf-8"))
    print("export_ts=%s live0=%s..." % (
        fresh.get("export_ts"), fresh["live"][0][:20]))

    # 3. embedded close commit (deliverables already committed stage-1)
    import close_commit
    msg = (
        "R1918 close: state accounting tick=1918 + export refresh "
        "(live-clock writer, plain-language live lines); probes in-band "
        "(board 0F, readiness 3 external CEO blockers 0 findings, "
        "loop_health 2F+228W all in-case history); five-checks quiet "
        "(group_scan truly_new=0 wm131, @BigStream 4==anchor, @liu-si 1 = "
        "10-09 radar order old anchor already consumed); queue replenish: "
        "no genuine new seed this round, true finding consumed into tech#75 "
        "machine face (honest zero-inflation); next R1919: #112 judge "
        "window 10-11 08:00 [via bm-a]")
    files = [STATE_PATH.replace("\\", "/"), EXPORT_PATH.replace("\\", "/"),
             os.path.join(".c3-tmp", "r1918_close.py"),
             LOG_DATA, PATCH_DATA, PROBES_EVID, STABILITY_EVID]
    rc = close_commit.run_close_commit(files, msg)
    print("close rc=%s" % rc)
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
