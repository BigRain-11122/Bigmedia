#!/usr/bin/env python3
"""Atomic fire-window consumer (tech#112): run the card and dispatch
the staged launch in ONE command.

Why: R1995 lost the first true fire window to a ~2-minute intermediate
read; R1999 lost a second GO (20:34:07 B-eviction-credit, expired
during pre-launch material discovery). Same root both times: agent
latency between the card verdict and the flight launch. Per the
experience-ledger escalation law (CEO 2026-10-13 13:07: recurrence =
the note lying in the ledger is not a gate -> escalate checklist to
script assertion), the R1995 "zero intermediate steps after GO"
checklist note is escalated into this atomic gate: the consumer runs
the card and dispatches the staged launch target in the same process,
so no material discovery, no command assembly, no intermediate read
can ever happen inside the 120s fire TTL again.

Staging contract: --launch points at a turnkey launcher (.py) that
already knows its own expert/material/timeout (s1_call pattern,
R191/R1995). The consumer never inspects the payload -- it only
gates on the card and dispatches, keeping the fire decision and the
launch atomic.

Staleness law (tech#89/#90): the card stamps expires_at on every fire
verdict; the consumer refuses to dispatch on a verdict at/after
expiry even though it produced that verdict itself (defensive against
future re-plumbings that would cache the card line).

rc contract (mirrors the card; consumers gate on rc):
  0 = fire consumed, staged launch dispatched
  1 = no-fire (window closed or stale verdict; card cited)
  2 = usage/tooling error (fail-closed; NEVER launches)

Usage:
  python src/os/fire_consume.py --launch <staged-launch.py> [--ledger F]
      [--json]

--ledger [PATH]: opt-in one-row-per-run JSONL (bare --ledger = default
data/pipeline/fire-consume-ledger.jsonl). The ledger is the only
durable trace that a dispatch happened -- round logs cite it.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CARD_SCRIPT = REPO / "src" / "os" / "fire_window_card.py"
DEFAULT_LEDGER = REPO / "data" / "pipeline" / "fire-consume-ledger.jsonl"
CARD_TIMEOUT_S = 300

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

USAGE = ("usage: python src/os/fire_consume.py --launch "
        "<staged-launch.py> [--ledger F] [--json]")

LAUNCH_MARGIN_S = 2  # dispatch latency budget inside the TTL


class CardError(Exception):
    """The card could not run or its JSON line was unparseable."""


def _child_env():
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def real_run_card():
    """Run fire_window_card --json and return the parsed card dict.

    Fail-closed: launch failure, timeout, empty stdout, or an
    unparseable line raise CardError -- a missing reading must never
    read as fire."""
    try:
        proc = subprocess.run(
            [sys.executable, str(CARD_SCRIPT), "--json"],
            cwd=str(REPO), env=_child_env(), capture_output=True,
            timeout=CARD_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CardError("card failed: %s" % exc)
    text = (proc.stdout or b"").decode("utf-8", "replace").strip()
    if not text:
        raise CardError("card rc=%d, no stdout" % proc.returncode)
    try:
        payload = json.loads(text.splitlines()[-1])
    except ValueError as exc:
        raise CardError("card JSON unparseable: %s" % exc)
    if not isinstance(payload, dict):
        raise CardError("card JSON not an object")
    return payload


def decide(card, now_epoch):
    """Pure core -> (action, reason, rc).

    action in {"launch", "no-fire", "stale", "error"}; consumers gate
    on rc (0 launch / 1 closed / 2 fail-closed). A fire verdict
    without expires_at is fail-closed: the staleness law needs the
    TTL stamp, and a card that omits it is not a consumable verdict.
    """
    verdict = (card or {}).get("verdict")
    if not verdict or verdict == "error":
        return "error", "card-verdict-error-or-missing", 2
    if verdict != "fire":
        reasons = (card or {}).get("reasons") or []
        return "no-fire", "card-no-fire: %s" % (
            ";".join(str(r) for r in reasons) if reasons
            else "no-reasons"), 1
    expires_at = card.get("expires_at")
    if not isinstance(expires_at, int):
        return "error", "fire-verdict-without-expires_at-fail-closed", 2
    if now_epoch + LAUNCH_MARGIN_S >= expires_at:
        return "stale", "fire-verdict-expired-at-%d" % expires_at, 1
    return "launch", "fire-fresh", 0


def real_launch(script_path):
    """Dispatch the staged launcher detached (U060 zero-window law).

    stdout/stderr are redirected to <script>.out/.err next to the
    launcher so no handle inheritance can tie the flight to this
    process (5-min-kill handle chain, platform memory). Returns pid.
    """
    script = Path(script_path)
    out = script.with_name(script.name + ".out")
    err = script.with_name(script.name + ".err")
    with out.open("wb") as fo, err.open("wb") as fe:
        proc = subprocess.Popen(
            [sys.executable, str(script)], cwd=str(REPO),
            stdout=fo, stderr=fe, env=_child_env(),
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    return proc.pid


def append_ledger_row(path, row):
    """Best-effort JSONL append; a ledger failure never changes rc
    (WARN to stderr) -- the dispatch itself is the outcome."""
    try:
        ledger_path = Path(path)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as exc:
        sys.stderr.write("WARN fire-consume-ledger append failed: %s\n"
                         % exc)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    parser = argparse.ArgumentParser(
        description="Atomic fire-window consumer (tech#112): run the "
                    "card and dispatch the staged launch in one "
                    "command. rc 0=dispatched, 1=no-fire/stale, "
                    "2=fail-closed.")
    parser.add_argument("--launch", required=True,
                        help="staged turnkey launcher (.py) to "
                             "dispatch when the card says fire")
    parser.add_argument("--ledger", nargs="?", const=str(DEFAULT_LEDGER),
                        default=None,
                        help="opt-in JSONL ledger (bare --ledger = "
                             "default %s)" % DEFAULT_LEDGER)
    parser.add_argument("--json", action="store_true",
                        help="single machine-readable line")
    args = parser.parse_args(argv)

    launch = Path(args.launch)
    if not launch.is_file() or launch.suffix != ".py":
        print(USAGE)
        return 2

    try:
        card = real_run_card()
    except CardError as exc:
        result = {"tool": "fire_consume", "action": "error",
                  "reason": str(exc), "launched": False,
                  "ts": datetime.datetime.now().strftime(
                      "%Y-%m-%d %H:%M:%S")}
        print(json.dumps(result, ensure_ascii=False)
              if args.json else
              "fire-consume: verdict=error reason=%s" % exc)
        return 2

    now_epoch = int(datetime.datetime.now().timestamp())
    action, reason, rc = decide(card, now_epoch)
    launch_pid = None
    if action == "launch":
        try:
            launch_pid = real_launch(launch)
        except OSError as exc:
            action, reason, rc = "error", "launch-failed: %s" % exc, 2

    result = {
        "tool": "fire_consume",
        "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "card_ts": card.get("ts"),
        "card_verdict": card.get("verdict"),
        "card_path": card.get("path"),
        "action": action,
        "reason": reason,
        "launched": action == "launch",
        "launch_script": str(launch),
        "launch_pid": launch_pid,
        "expires_at": card.get("expires_at"),
        "rc": rc,
    }
    if args.ledger:
        append_ledger_row(args.ledger, result)
    print(json.dumps(result, ensure_ascii=False) if args.json else
          "fire-consume: card=%s action=%s launched=%s reason=%s%s"
          % (card.get("verdict"), action, result["launched"], reason,
             " pid=%s" % launch_pid if launch_pid else ""))
    return rc


if __name__ == "__main__":
    sys.exit(main())
