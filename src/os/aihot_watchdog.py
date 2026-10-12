"""AIHOT stack autoheal watchdog (tech#127).

Gap anchor (R2046): the 10-08 node-kill case family struck a 4th time
(08:59 healthy probe -> 10:34 all-refused = ~1.6h blind window, ~20min
manual recovery). R2048 case-5 (PG started on the wrong port 5432 ->
api pool 503) extended the family to the PG role. This watchdog turns
that family from "found at next probe round + manual heal" into
"blind window <= one PT5M cadence + canonical heal channel + ledger
row".

Design laws baked in:
- Identity law first (tech#125): node-role healing is decided ONLY on
  aihot_procs verdicts; the watchdog never names a pid itself.
- Pause law (O-20261012-1115 CEO yield): the worker is INTENTIONALLY
  stopped during a CEO pause. The repo-local pause flag
  (data/pipeline/aihot-watchdog-state.json -> "pause" object) makes
  the watchdog skip worker restarts while the flag stands; flag
  removal is a documented step of the resume procedure (main#21).
  Fail-closed: an unparseable flag file counts as paused.
- Light services (PG 55432 / api / proxy-web) are the "standing
  light footprint" the yield order keeps alive, so their heal
  branches are NOT gated by the pause flag.
- Silence law (U060): the scheduled task runs this script under
  pythonw.exe (GUI subsystem, no console). Every console-subsystem
  child (python/netstat/powershell/cmd) is spawned with
  CREATE_NO_WINDOW so no window can flash; bat children additionally
  get a new process group and stripped stdio handles.

Consumption law: ledger = data/pipeline/aihot-watchdog-ledger.jsonl
(tech#52 family, best-effort). Row kinds: heartbeat (1/day),
skip-pause (worker missing + pause flag; 1/6h), probe-error (1/h),
heal (every action, with before/after verdicts), lock-skip.

rc contract: 0 = clean run (heartbeat, skip, or full heal),
1 = heal attempted but post-heal verify still not complete,
2 = topology probe error face (fail-closed -- never acts on nodes).
"""
import datetime
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AIHOT_ROOT = REPO_ROOT / "data" / "assets" / "aihot-poc"
PROCS_CLI = REPO_ROOT / "src" / "os" / "aihot_procs.py"
LEDGER_PATH = REPO_ROOT / "data" / "pipeline" / "aihot-watchdog-ledger.jsonl"
STATE_PATH = REPO_ROOT / "data" / "pipeline" / "aihot-watchdog-state.json"

PG_HOST = "127.0.0.1"
PG_PORT = 55432
PG_PROBE_TIMEOUT_S = 3
TOPO_TIMEOUT_S = 90
POST_HEAL_WAIT_S = 25
LOCK_STALE_S = 600
HEARTBEAT_PERIOD = "day"
PAUSE_LOG_THROTTLE_S = 6 * 3600
ERR_LOG_THROTTLE_S = 3600

CREATE_NO_WINDOW = 0x08000000
CREATE_NEW_PROCESS_GROUP = 0x00000200

# node-role -> canonical restart bat (topology single truth, tech#125)
ROLE_BATS = {
    "api": AIHOT_ROOT / "api-restart.bat",
    "proxy": AIHOT_ROOT / "web-restart.bat",
    "worker": AIHOT_ROOT / "worker-restart.bat",
}
PG_BAT = AIHOT_ROOT / "pg-restart.bat"


def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_ts(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- state

def load_state(path=STATE_PATH):
    """Best-effort read; malformed -> {} (never raises)."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(state, path=STATE_PATH):
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(state, ensure_ascii=True, indent=1),
                     encoding="ascii")
        return True
    except OSError as exc:
        sys.stderr.write("WARN state save failed: %s\n" % exc)
        return False


def pause_face(state, now_fn=None):
    """-> (active, note). Fail-closed: unparseable flag = paused."""
    now = now_fn or datetime.datetime.now
    pause = state.get("pause")
    if pause is None:
        return False, None
    if not isinstance(pause, dict):
        return True, "pause flag present but malformed (fail-closed)"
    if not pause.get("worker_restart_paused"):
        return False, None
    note = str(pause.get("reason") or "unspecified")
    ts = parse_ts(pause.get("ts"))
    if ts is not None:
        age_h = (now() - ts).total_seconds() / 3600.0
        if age_h > 72:
            note += " [STALE >72h - review resume procedure main#21]"
    return True, note


def lock_fresh(state, now_fn=None):
    now = now_fn or datetime.datetime.now
    ts = parse_ts(state.get("lock_ts"))
    return ts is not None and (now() - ts).total_seconds() < LOCK_STALE_S


# ------------------------------------------------------------- probing

def _pythonw_sibling():
    exe = Path(sys.executable)
    return exe.with_name("pythonw.exe") if exe.name.lower() == "python.exe" else exe


def probe_pg(host=PG_HOST, port=PG_PORT):
    try:
        with socket.create_connection((host, port), timeout=PG_PROBE_TIMEOUT_S):
            return True
    except OSError:
        return False


def _real_topology_runner():
    """Real seam: run aihot_procs --json as a CREATE_NO_WINDOW child.

    Child gets an invisible console, which its own powershell/netstat
    children then inherit -- zero window flash under pythonw."""
    exe = _pythonw_sibling()
    if exe.name.lower() == "pythonw.exe":
        exe = exe.with_name("python.exe")
    try:
        p = subprocess.run(
            [str(exe), str(PROCS_CLI), "--json"],
            capture_output=True, timeout=TOPO_TIMEOUT_S,
            creationflags=CREATE_NO_WINDOW)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode not in (0, 1, 2):
        return None
    try:
        return json.loads(p.stdout.decode("utf-8", "replace").strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


# -------------------------------------------------------------- decide

def decide_actions(topo, pg_ok, pause_active):
    """Pure core -> (actions, skip_note).

    actions = list of (kind, bat_path). kind in {'pg','api','proxy','worker'}.
    skip_note = 'pause' when the worker is missing but pause-flagged."""
    actions = []
    skip_note = None
    if not pg_ok:
        actions.append(("pg", PG_BAT))
    if topo is None or topo.get("rc") == 2:
        return actions, skip_note  # fail-closed: never act on nodes
    if topo.get("rc") == 0:
        return actions, skip_note
    verdict = topo.get("verdict")
    if verdict == "missing-api":
        actions.append(("api", ROLE_BATS["api"]))
    elif verdict == "missing-proxy":
        actions.append(("proxy", ROLE_BATS["proxy"]))
    elif verdict == "missing-worker":
        if pause_active:
            skip_note = "pause"
        else:
            actions.append(("worker", ROLE_BATS["worker"]))
    return actions, skip_note


def _real_spawn(bat_path):
    """Fire-and-forget a canonical restart bat. The bat runs its node
    in the foreground (it IS the service wrapper), so spawn detached,
    no-window, new process group, stdio stripped (handle-inheritance
    law)."""
    try:
        # CREATE_NO_WINDOW (not DETACHED_PROCESS): cmd gets an invisible
        # console that the bat's node child inherits -- proven zero-flash
        # combination, and the two flags are mutually exclusive by contract.
        subprocess.Popen(
            ["cmd.exe", "/c", str(bat_path)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP)
        return True
    except OSError as exc:
        sys.stderr.write("WARN spawn %s failed: %s\n" % (bat_path, exc))
        return False


# --------------------------------------------------------------- ledger

def append_row(row, path=LEDGER_PATH):
    row = dict(row)
    row.setdefault("ts", now_str())
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    except OSError as exc:
        sys.stderr.write("WARN ledger append failed: %s\n" % exc)


# ----------------------------------------------------------------- run

def run_once(topology_runner=None, pg_runner=None, spawn=None,
             state_path=STATE_PATH, ledger_path=LEDGER_PATH,
             clock=None, wait=None):
    """One watchdog cycle. Returns rc (0 ok / 1 heal-verify-failed /
    2 probe-error face)."""
    run_topo = topology_runner or _real_topology_runner
    run_pg = pg_runner or probe_pg
    do_spawn = spawn or _real_spawn
    do_wait = wait or time.sleep
    now = clock or datetime.datetime.now

    state = load_state(state_path)
    if lock_fresh(state, now):
        append_row({"event": "lock-skip",
                    "note": "previous run still in flight"}, ledger_path)
        return 0
    state["lock_ts"] = now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(state, state_path)

    topo = run_topo()
    pg_ok = run_pg()
    pause_active, pause_note = pause_face(state, now)
    actions, skip_note = decide_actions(topo, pg_ok, pause_active)

    rc = 0
    if topo is None or topo.get("rc") == 2:
        last = parse_ts(state.get("last_err_log"))
        fresh = last is not None and (now() - last).total_seconds() < ERR_LOG_THROTTLE_S
        if not fresh:
            append_row({"event": "probe-error",
                        "pg_ok": pg_ok,
                        "note": "topology face unreadable (fail-closed)"},
                       ledger_path)
            state["last_err_log"] = now().strftime("%Y-%m-%d %H:%M:%S")
        rc = 2
    elif skip_note == "pause":
        last = parse_ts(state.get("last_pause_log"))
        fresh = last is not None and (now() - last).total_seconds() < PAUSE_LOG_THROTTLE_S
        if not fresh:
            append_row({"event": "skip-pause",
                        "pg_ok": pg_ok,
                        "note": "worker missing + CEO pause flag: "
                                "skip restart (%s)" % (pause_note or "")},
                       ledger_path)
            state["last_pause_log"] = now().strftime("%Y-%m-%d %H:%M:%S")
    elif not actions:
        today = now().strftime("%Y-%m-%d")
        if state.get("last_heartbeat") != today:
            append_row({"event": "heartbeat",
                        "pg_ok": pg_ok,
                        "verdict": (topo or {}).get("verdict")},
                       ledger_path)
            state["last_heartbeat"] = today
    else:
        spawned = []
        for kind, bat in actions:
            if do_spawn(bat):
                spawned.append(kind)
        if spawned:
            do_wait(POST_HEAL_WAIT_S)
            topo2 = run_topo()
            pg2 = run_pg()
            append_row({"event": "heal",
                        "actions": spawned,
                        "before": {"verdict": (topo or {}).get("verdict"),
                                   "rc": (topo or {}).get("rc"),
                                   "pg_ok": pg_ok},
                        "after": {"verdict": (topo2 or {}).get("verdict"),
                                  "rc": (topo2 or {}).get("rc"),
                                  "pg_ok": pg2}},
                       ledger_path)
            complete = (topo2 is not None and topo2.get("rc") == 0
                        and topo2.get("verdict") == "complete" and pg2)
            rc = 0 if complete else 1

    state.pop("lock_ts", None)
    save_state(state, state_path)
    return rc


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--dry-run" in argv:
        topo = _real_topology_runner()
        pg_ok = probe_pg()
        state = load_state()
        pause_active, pause_note = pause_face(state)
        actions, skip_note = decide_actions(topo, pg_ok, pause_active)
        print(json.dumps({
            "ts": now_str(), "topology_rc": (topo or {}).get("rc"),
            "verdict": (topo or {}).get("verdict"), "pg_ok": pg_ok,
            "pause_active": pause_active,
            "actions": [k for k, _ in actions],
            "skip_note": skip_note,
        }, ensure_ascii=True))
        return 0
    return run_once()


if __name__ == "__main__":
    sys.exit(main())
