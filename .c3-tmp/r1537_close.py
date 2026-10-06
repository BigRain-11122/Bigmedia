# -*- coding: utf-8 -*-
"""R1537 close: adjudicate the R1536 broken-round drift beat (9th case).

R1452 pre-registered workflow: a new double-body round adds +1 orphan beat ->
loop_health account-lag goes red (3F) -> adjudicate with audit chain ->
baseline +1 -> probe returns to 2F baseline. Pure data adjudication: no code
change; accounting is NOT missing (successor body accounted tick 1536 under
the absorb convention, commit 3acda4a7).

Encoding law: this script is pure ASCII. Chinese payload lives in
.c3-tmp/r1537_payload.json (data file) and lands in src/os/state.json (json
data file). Payload fields: logline / focus / note_append.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
STATE = REPO / "src" / "os" / "state.json"
PAYLOAD = REPO / ".c3-tmp" / "r1537_payload.json"

EXPECTED_TICK = 1536
EXPECTED_ADJ = 8
NEW_TICK = 1537
NEW_ADJ = 9
ROUND_TAG = "R1537: "


def main() -> int:
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))

    # Preconditions: exact round + baseline, refuse on drift (idempotent guard).
    if state["tick"] != EXPECTED_TICK:
        print("FAIL: tick %r != expected %r" % (state["tick"], EXPECTED_TICK))
        return 1
    if state.get("account_drift_adjudicated") != EXPECTED_ADJ:
        print("FAIL: adj %r != expected %r"
              % (state.get("account_drift_adjudicated"), EXPECTED_ADJ))
        return 1

    logline = payload["logline"]
    if ROUND_TAG not in logline:
        print("FAIL: payload logline missing round tag")
        return 1
    tail = logline.split(ROUND_TAG, 1)[1]

    state["tick"] = NEW_TICK
    state["account_drift_adjudicated"] = NEW_ADJ
    state["account_drift_note"] = (state["account_drift_note"]
                                   + payload["note_append"])
    state["log"].append(logline)
    state["focus"] = payload["focus"]
    state["ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["task"] = tail[:60]

    STATE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    print("OK: tick %d -> %d, adj %d -> %d, log %d entries, ts=%s"
          % (EXPECTED_TICK, NEW_TICK, EXPECTED_ADJ, NEW_ADJ,
             len(state["log"]), state["ts"]))
    print("task=%r" % state["task"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
