# -*- coding: utf-8 -*-
"""R1537 export refresh (P-61): status-export.json update from payload.

Pure ASCII script; Chinese payload in .c3-tmp/r1537_payload.json.
Fields: export_osc / export_live / export_results_entry.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT = REPO / "docs" / "status-export.json"
PAYLOAD = REPO / ".c3-tmp" / "r1537_payload.json"

OS_NAME = "OS 循环"
NEW_TICK = "1537"


def main() -> int:
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    data = json.loads(EXPORT.read_text(encoding="utf-8"))

    hits = [e for e in data["outs"] if e and e[0] == OS_NAME]
    if len(hits) != 1:
        print("FAIL: OS loop out entry count %d" % len(hits))
        return 1
    hits[0][1] = payload["export_osc"]

    data["export_ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["live"] = payload["export_live"]
    data["results"].append([NEW_TICK, payload["export_results_entry"]])

    EXPORT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print("OK: export_ts=%s live=%d lines results=%d"
          % (data["export_ts"], len(data["live"]), len(data["results"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
