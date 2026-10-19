"""AIHOT stack one-key recovery runbook (tech#238).

Gap anchor (R2381): a dead web face (3100) cost ~6 minutes of
prose-ledger archaeology to recover -- and the manual WMI spawn
turned out to be REDUNDANT: the PT5M watchdog (tech#127) had already
healed the full stack that morning (watchdog ledger 2026-10-19:
10:20:30 pg+api / 10:25:29 proxy / 10:30:28 worker). The operator
hazard is not a missing restart channel (the aihot-poc bats are the
canonical channel, tech#125) but acting on a probe WARN while the
watchdog owns the heal: duplicate spawns and heal fights.

Laws baked in:
- Identity law (tech#125): role/verdict facts come ONLY from
  src/os/aihot_procs.py; this script never names a pid and never
  touches a live face (zero fratricide, R2381 duplicate anchor).
- Watchdog standoff: a fresh watchdog heal row (<= STANDOFF_WINDOW_S)
  means the watchdog owns the healing; stand down unless --force.
- Pause law (O-20260912-1115 CEO yield): worker restart stays gated
  on the repo-local pause flag exactly like the watchdog (imported
  pause_face, fail-closed on a malformed flag).
- Job escape (R2381 live anchor): loop-session children live inside
  the CLI Job object (Popen CREATE_BREAKAWAY -> WinError 5), so face
  restarts go through WMI Win32_Process.Create (the WmiPrvSE host
  runs outside the Job) and survive the round process.
- Zero hardcode drift: api/web/pg ports derive from
  data/assets/aihot-poc/AIHOT/.env (API_PORT / WEB_PORT /
  DATABASE_URL), falling back to the aihot_procs defaults.

Consumption law: run on any aihot dead-face WARN; the standoff check
decides whether a loop/human hand is needed at all. Every run
appends one row to data/assets/aihot-poc/restart-runbook.log.

rc contract: 0 = healthy no-op / standoff / pause terminal / dry-run
plan / heal verified complete; 1 = heal attempted but post-verify
not complete; 2 = probe error face (fail-closed -- never acts).

Run:
    python tools/aihot_restart.py [--dry-run] [--force] [--json]
"""
import argparse
import datetime
import json
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.os.aihot_procs import DEFAULT_API_PORT, DEFAULT_WEB_PORT  # noqa: E402
from src.os.aihot_watchdog import (  # noqa: E402
    AIHOT_ROOT,
    LEDGER_PATH,
    PG_HOST,
    PG_PORT,
    PROCS_CLI,
    STATE_PATH,
    load_state,
    pause_face,
    parse_ts,
)

AIHOT_ENV = AIHOT_ROOT / "AIHOT" / ".env"
RUNBOOK_LOG = AIHOT_ROOT / "restart-runbook.log"

# ~3 PT5M watchdog cycles: the observed multi-node heal span
# (2026-10-19 10:20 -> 10:30, R2055 supplement-loop family anchor).
STANDOFF_WINDOW_S = 420
TOPO_TIMEOUT_S = 90
WMI_TIMEOUT_S = 30
PG_PROBE_TIMEOUT_S = 3

CREATE_NO_WINDOW = 0x08000000

# role -> canonical restart bat (topology single truth, tech#125;
# mirrors watchdog ROLE_BATS -- zero drift by import-adjacency).
ROLE_BATS = {
    "pg": "pg-restart.bat",
    "api": "api-restart.bat",
    "proxy": "web-restart.bat",
    "worker": "worker-restart.bat",
}


def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(path):
    """Best-effort read; missing/unreadable -> '' (never raises)."""
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def parse_env_ports(env_text):
    """AIHOT/.env text -> ({api, web, pg}, notes).

    Ports come from API_PORT / WEB_PORT / the DATABASE_URL port
    segment; any defaulted port carries a note so drift is never
    silent (zero-hardcode-drift law)."""
    ports = {"api": DEFAULT_API_PORT, "web": DEFAULT_WEB_PORT, "pg": PG_PORT}
    notes = []
    derived = set()
    kv = {}
    for line in (env_text or "").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        kv[key.strip().upper()] = value.strip()
    for key, role in (("API_PORT", "api"), ("WEB_PORT", "web")):
        raw = kv.get(key)
        if raw is None:
            continue
        try:
            ports[role] = int(raw)
            derived.add(role)
        except ValueError:
            notes.append("env %s=%r unparseable -> default %d"
                         % (key, raw, ports[role]))
    url = kv.get("DATABASE_URL") or ""
    match = re.search(r"://(?:[^@/]+@)?[^:/]+:(\d+)/", url)
    if match:
        try:
            ports["pg"] = int(match.group(1))
            derived.add("pg")
        except ValueError:
            notes.append("DATABASE_URL port unparseable -> default %d"
                         % ports["pg"])
    for role in ("api", "web", "pg"):
        if role not in derived:
            notes.append("port %s: no env source -> default %d"
                         % (role, ports[role]))
    return ports, notes


def read_recent_heal(ledger_text, now_dt, window_s=STANDOFF_WINDOW_S):
    """Last watchdog 'heal' row -> (row, age_s) when fresh enough,
    else (None, None).

    Heartbeats/skips do not count. A future-dated row counts as
    fresh (fail-safe: never act over a suspicious clock)."""
    last = None
    for line in (ledger_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict) or row.get("event") != "heal":
            continue
        ts = parse_ts(row.get("ts"))
        if ts is None:
            continue
        last = (row, ts)
    if last is None:
        return None, None
    row, ts = last
    age = (now_dt - ts).total_seconds()
    if age > window_s:
        return None, None
    return row, max(age, 0.0)


def decide(topo, pg_ok, heal_row=None, heal_age=None, pause_active=False,
           force=False, standoff_s=STANDOFF_WINDOW_S):
    """Pure core -> plan dict {actions, notes, terminal}.

    Actions are role names in firing order (pg first: the api pool
    503s without PG, R2048 anchor). Multi-face derivation reads the
    roles dict directly -- the aihot_procs verdict is a single enum
    (api > proxy > worker) and serial consumption is what cost the
    watchdog three PT5M cycles on the 2026-10-19 multi-node kill."""
    if not isinstance(topo, dict) or topo.get("status") != "ok":
        return {"actions": [],
                "notes": ["probe error face -- fail-closed, no action"],
                "terminal": "refused"}
    notes = list(topo.get("notes") or [])
    roles = topo.get("roles") or {}
    missing = [role for role in ("api", "proxy", "worker")
               if roles.get(role) is None]
    if not missing and pg_ok:
        notes.append("all faces alive -- nothing to do")
        return {"actions": [], "notes": notes, "terminal": "healthy"}
    if heal_row is not None and not force:
        notes.append("watchdog heal row ts=%s (age %.0fs <= %ds) owns the "
                     "healing -- stand down, use --force to override"
                     % (heal_row.get("ts"), heal_age or 0, standoff_s))
        return {"actions": [], "notes": notes, "terminal": "standoff"}
    actions = []
    if not pg_ok:
        actions.append("pg")
        notes.append("pg probe down -- pg heal queued first (api pool 503 gate)")
    actions.extend(missing)
    if "worker" in actions and pause_active:
        actions = [role for role in actions if role != "worker"]
        notes.append("pause law: worker restart skipped (CEO yield pause flag)")
        if not actions:
            notes.append("pause terminal: only worker missing -- admissible")
            return {"actions": [], "notes": notes, "terminal": "pause"}
    return {"actions": actions, "notes": notes, "terminal": "heal"}


def build_wmi_snippet(bat_path):
    """-> powershell snippet creating the bat OUTSIDE the caller Job
    (WmiPrvSE host). A path embedding a double quote is refused --
    bat paths live under the repo and must never need quote escapes."""
    text = str(bat_path)
    if '"' in text:
        raise ValueError("bat path embeds a double quote: %r" % text)
    return ("([wmiclass]'Win32_Process')"
            ".Create('cmd /c \"%s\"').ReturnValue" % text)


def run_wmi_create(snippet):
    """-> WMI Create ReturnValue (int) or None on spawn/parse failure.

    0 = successful completion; 2 = access denied; 8/9/21 = other WMI
    failures (documented Win32_Process.Create codes)."""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", snippet],
            capture_output=True, timeout=WMI_TIMEOUT_S,
            creationflags=CREATE_NO_WINDOW)
    except (OSError, subprocess.TimeoutExpired):
        return None
    out = proc.stdout.decode("utf-8", "replace").strip()
    try:
        return int(out)
    except ValueError:
        return None


def probe_topology(api_port, web_port):
    """Run aihot_procs --json (identity law). -> result dict, or None
    when the probe itself could not run/parse (fail-closed)."""
    try:
        proc = subprocess.run(
            [sys.executable, str(PROCS_CLI), "--json",
             "--api-port", str(api_port), "--web-port", str(web_port)],
            capture_output=True, timeout=TOPO_TIMEOUT_S,
            creationflags=CREATE_NO_WINDOW)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode not in (0, 1, 2):
        return None
    try:
        return json.loads(
            proc.stdout.decode("utf-8", "replace").strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def probe_pg(host=PG_HOST, port=PG_PORT, timeout_s=PG_PROBE_TIMEOUT_S):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout_s):
            return True
    except OSError:
        return False


def log_runbook_row(fields):
    """Best-effort append; never raises (visibility law: every run,
    including no-ops and standoffs, leaves a row for later
    first-real-kill timing evaluation of the <=2min budget)."""
    try:
        line = " | ".join("%s=%s" % (key, value) for key, value in fields)
        with open(RUNBOOK_LOG, "a", encoding="ascii", errors="replace") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="AIHOT stack one-key recovery runbook (tech#238): "
                    "identity-law probe -> watchdog standoff -> WMI "
                    "restart of missing faces only.")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan, never restart anything")
    parser.add_argument("--force", action="store_true",
                        help="override a fresh-watchdog-heal standoff")
    parser.add_argument("--json", action="store_true",
                        help="single machine-readable line")
    parser.add_argument("--api-port", type=int, default=None)
    parser.add_argument("--web-port", type=int, default=None)
    parser.add_argument("--pg-port", type=int, default=None)
    parser.add_argument("--standoff-s", type=int, default=STANDOFF_WINDOW_S)
    parser.add_argument("--wait-s", type=int, default=15,
                        help="post-heal verify poll interval (s)")
    parser.add_argument("--wait-tries", type=int, default=5,
                        help="post-heal verify poll attempts")
    args = parser.parse_args(argv)

    started = datetime.datetime.now()
    ports, env_notes = parse_env_ports(read_text(AIHOT_ENV))
    if args.api_port:
        ports["api"] = args.api_port
    if args.web_port:
        ports["web"] = args.web_port
    if args.pg_port:
        ports["pg"] = args.pg_port

    topo = probe_topology(ports["api"], ports["web"])
    pg_ok = probe_pg(port=ports["pg"])
    heal_row, heal_age = read_recent_heal(read_text(LEDGER_PATH), started,
                                          args.standoff_s)
    state = load_state(STATE_PATH)
    pause_active, pause_note = pause_face(state)
    plan = decide(topo, pg_ok, heal_row, heal_age, pause_active,
                  force=args.force, standoff_s=args.standoff_s)
    if pause_note:
        plan["notes"].append("pause note: %s" % pause_note)

    result = {
        "ts": now_str(),
        "ports": ports,
        "pg_ok": pg_ok,
        "verdict": topo.get("verdict") if isinstance(topo, dict) else None,
        "roles": topo.get("roles") if isinstance(topo, dict) else None,
        "heal_row_ts": heal_row.get("ts") if isinstance(heal_row, dict) else None,
        "pause_active": pause_active,
        "plan": plan,
        "env_notes": env_notes,
        "rc": None,
    }

    terminal = plan["terminal"]
    if terminal == "refused":
        result["rc"] = 2
    elif terminal in ("healthy", "standoff", "pause"):
        result["rc"] = 0
    elif args.dry_run:
        plan["terminal"] = "plan"
        result["rc"] = 0
    else:
        fired = []
        for role in plan["actions"]:
            bat = AIHOT_ROOT / ROLE_BATS[role]
            snippet = build_wmi_snippet(bat)
            wmi_rc = run_wmi_create(snippet)
            fired.append({"role": role, "bat": bat.name, "wmi_rc": wmi_rc})
        result["fired"] = fired
        complete = False
        post = None
        post_pg = None
        for _ in range(max(1, args.wait_tries)):
            time.sleep(max(1, args.wait_s))
            post = probe_topology(ports["api"], ports["web"])
            post_pg = probe_pg(port=ports["pg"])
            if (isinstance(post, dict) and post.get("status") == "ok"
                    and post.get("verdict") == "complete" and post_pg):
                complete = True
                break
        result["post_verdict"] = (post.get("verdict")
                                  if isinstance(post, dict) else None)
        result["post_pg_ok"] = post_pg
        result["rc"] = 0 if complete else 1

    log_runbook_row([
        ("ts", result["ts"]),
        ("terminal", plan["terminal"]),
        ("verdict", result.get("verdict")),
        ("pg_ok", result["pg_ok"]),
        ("actions", ",".join(plan["actions"])),
        ("heal_row_ts", result.get("heal_row_ts")),
        ("rc", result["rc"]),
    ])

    if args.json:
        print(json.dumps(result, ensure_ascii=True))
    else:
        print("aihot_restart %s: terminal=%s rc=%s verdict=%s pg_ok=%s"
              % (result["ts"], plan["terminal"], result["rc"],
                 result.get("verdict"), result["pg_ok"]))
        for role in plan["actions"]:
            print("  plan: restart %s via %s" % (role, ROLE_BATS[role]))
        for item in result.get("fired") or []:
            print("  fired: %s (%s) wmi_rc=%s"
                  % (item["role"], item["bat"], item["wmi_rc"]))
        for note in plan["notes"]:
            print("  note: %s" % note)
        for note in env_notes:
            print("  env: %s" % note)
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
