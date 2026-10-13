"""R2125 round close: state.json tick/log/ts/task/focus update.

Content lives in UTF-8 side files (encoding law). Fail-closed guards:
- tick must be 2124 (single-writer check)
- log entry idempotence (R2125 round line must not already exist)
- ts/task stamped from the live clock inside this script
"""
import datetime
import io
import json
import sys

STATE = "src/os/state.json"
LOG_FILE = ".c3-tmp/r2125_logline.txt"
FOCUS_FILE = ".c3-tmp/r2125_focus.txt"
ROUND = "R2125"
EXPECT_TICK = 2124

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig", errors="strict") as fh:
        return fh.read().rstrip("\n")

def main():
    with io.open(STATE, "r", encoding="utf-8-sig", errors="strict") as fh:
        data = json.load(fh)
    if data.get("tick") != EXPECT_TICK:
        print("ANCHOR-MISSING tick=%s want %s" % (data.get("tick"), EXPECT_TICK))
        return 2
    body = read_utf8(LOG_FILE)
    focus = read_utf8(FOCUS_FILE)
    now = datetime.datetime.now()
    prefix = "%s %s %s: " % (now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), ROUND)
    entry = prefix + body
    if any(ROUND + ": " in str(l)[:30] for l in data.get("log", [])[-3:]):
        print("ANCHOR-ALREADY-APPLIED log tail has %s" % ROUND)
        return 2
    data["tick"] = EXPECT_TICK + 1
    data["focus"] = focus
    data.setdefault("log", []).append(entry)
    data["ts"] = now.strftime("%Y-%m-%d %H:%M:%S")
    data["task"] = body[:60]
    with io.open(STATE, "w", encoding="utf-8", newline="") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("STATE-CLOSED tick=%d log=%d ts=%s" % (data["tick"], len(data["log"]), data["ts"]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
