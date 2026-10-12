"""AIHOT stack process-topology probe (tech#125).

Gap anchor (R2038): apps/worker and apps/api run the SAME relative
cmdline ('node --env-file-if-exists=../../.env src/main.ts'), so the
R2037 "double worker" misread killed the API as a side effect of the
worker activation step (proxy 502, repaired same round). Win32_Process
exposes no CWD, so identity proof here = port binding (netstat) plus
cmdline shape; an ambiguous same-shape set is refused, never guessed.

Consumption law: run BEFORE any kill/restart of an AIHOT-domain node
process; only act on pids whose role is proven (verdict 'complete').
The canonical restart channels are data/assets/aihot-poc/
worker-restart.bat and api-restart.bat (topology single truth).

rc contract: 0=topology complete, 1=topology anomaly (advisory -- do
NOT operate any same-shape pid), 2=probe error (fail-closed; a missing
reading must never read as complete).
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = REPO_ROOT / "data" / "pipeline" / "aihot-procs-ledger.jsonl"

DEFAULT_API_PORT = 3101
DEFAULT_WEB_PORT = 3100

PS_TIMEOUT_S = 30
NETSTAT_TIMEOUT_S = 15

# Same self-match guard as comfy_activity (tech#106): the PS query
# process itself carries the 'env-file-if-exists' token in its own
# CommandLine, but its Name is powershell.exe, not node.exe -- the
# Name filter keeps it out of the match set.
PS_COMMAND = (
    "Get-CimInstance Win32_Process -Filter \"Name = 'node.exe'\" | "
    "Where-Object { $_.CommandLine -match 'env-file-if-exists' } | "
    "Select-Object ProcessId, CommandLine | ConvertTo-Json -Compress"
)

API_SHAPE = "src/main.ts"
PROXY_SHAPE = "server.ts"

RC_COMPLETE = 0
RC_ANOMALY = 1
RC_ERROR = 2


def _real_ps_runner(command):
    """Real seam: -> (ok, stdout_str). ok=False on spawn failure,
    timeout, or nonzero rc (fail-closed: never a fake empty)."""
    try:
        p = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", command],
            capture_output=True, timeout=PS_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return False, ""
    if p.returncode != 0:
        return False, ""
    return True, p.stdout.decode("utf-8", "replace")


def _real_netstat_runner():
    try:
        p = subprocess.run(["netstat", "-ano"], capture_output=True,
                           timeout=NETSTAT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return False, ""
    if p.returncode != 0:
        return False, ""
    return True, p.stdout.decode("utf-8", "replace")


def parse_ps_procs(stdout):
    """ConvertTo-Json output -> [(pid, cmdline), ...].

    Empty stdout -> [] (query ran, zero matching processes). Junk /
    bad shape / missing keys -> None (unreadable)."""
    if stdout is None:
        return None
    s = stdout.strip()
    if not s:
        return []
    try:
        data = json.loads(s)
    except ValueError:
        return None
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return None
    out = []
    for item in data:
        if not isinstance(item, dict):
            return None
        try:
            pid = int(item["ProcessId"])
        except (KeyError, TypeError, ValueError):
            return None
        cmd = item.get("CommandLine") or ""
        out.append((pid, cmd))
    return out


def parse_netstat_listeners(stdout, ports):
    """netstat -ano output -> {port: [owner pids]} for LISTENING rows.

    Only rows whose local address ends ':<port>' count; the colon
    boundary keeps 31010 from matching 3101. Junk -> None."""
    if stdout is None:
        return None
    wanted = {int(p) for p in ports}
    owners = {p: [] for p in wanted}
    for raw in stdout.splitlines():
        parts = raw.split()
        if len(parts) < 5 or parts[3] != "LISTENING" or parts[0] != "TCP":
            continue
        local = parts[1]
        try:
            pid = int(parts[4])
        except ValueError:
            return None
        for port in wanted:
            if local.endswith(":%d" % port):
                owners[port].append(pid)
    return owners


def classify_topology(procs, port_owners,
                       api_port=DEFAULT_API_PORT,
                       web_port=DEFAULT_WEB_PORT):
    """Pure core: (pid, cmdline) list + netstat owners -> role map.

    Identity law: port binding outranks cmdline shape; a same-shape
    pid bound to no known port is a worker CANDIDATE only -- more
    than one candidate means ambiguity and the verdict refuses to
    name a worker (never guess)."""
    roles = {"proxy": None, "api": None, "worker": None}
    evidence = []
    notes = []
    pid_set = {pid for pid, _ in procs}

    api_owners = [p for p in port_owners.get(api_port, []) if p in pid_set]
    if len(api_owners) == 1:
        roles["api"] = api_owners[0]
        evidence.append("api pid %d: owns 127.0.0.1:%d (netstat binding)"
                        % (api_owners[0], api_port))
    elif len(api_owners) > 1:
        notes.append("api port %d owned by multiple pids %s -- refusing"
                     % (api_port, sorted(api_owners)))

    proxy_owners = [p for p in port_owners.get(web_port, [])
                    if p in pid_set and p != roles["api"]]
    if len(proxy_owners) == 1:
        roles["proxy"] = proxy_owners[0]
        evidence.append("proxy pid %d: owns 127.0.0.1:%d (netstat binding)"
                        % (proxy_owners[0], web_port))

    if roles["proxy"] is None:
        for pid, cmd in procs:
            if PROXY_SHAPE in cmd and pid != roles["api"]:
                roles["proxy"] = pid
                evidence.append(
                    "proxy pid %d: '%s' cmdline shape (no %d binding)"
                    % (pid, PROXY_SHAPE, web_port))
                break

    if roles["api"] is not None:
        bound = set(port_owners.get(api_port, []) +
                    port_owners.get(web_port, []))
    else:
        bound = set()
    worker_candidates = [pid for pid, cmd in procs
                         if API_SHAPE in cmd
                         and pid != roles["api"]
                         and pid != roles["proxy"]
                         and pid not in bound]

    if len(worker_candidates) == 1:
        roles["worker"] = worker_candidates[0]
        evidence.append(
            "worker pid %d: '%s' cmdline shape, bound to no known port"
            % (worker_candidates[0], API_SHAPE))
    elif len(worker_candidates) > 1:
        notes.append("same-shape pids %s match no port -- worker identity"
                     " ambiguous, refusing to name one"
                     % sorted(worker_candidates))

    if roles["api"] is None:
        verdict = "missing-api"
    elif roles["proxy"] is None:
        verdict = "missing-proxy"
    elif roles["worker"] is None:
        verdict = "missing-worker"
    else:
        verdict = "complete"

    return {
        "roles": roles,
        "verdict": verdict,
        "evidence": evidence,
        "notes": notes,
        "worker_candidates": sorted(worker_candidates),
    }


def run_probe(ps_runner=None, netstat_runner=None,
              api_port=DEFAULT_API_PORT, web_port=DEFAULT_WEB_PORT):
    """Orchestrate both faces -> result dict. Fail-closed: any
    unreadable face yields rc 2, verdict None (never 'complete')."""
    run_ps = ps_runner or _real_ps_runner
    run_net = netstat_runner or _real_netstat_runner
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ok_ps, out_ps = run_ps(PS_COMMAND)
    if not ok_ps:
        return {"ts": ts, "status": "error", "rc": RC_ERROR,
                "verdict": None, "roles": {}, "evidence": [],
                "notes": ["ps face unreadable (fail-closed)"],
                "worker_candidates": []}
    procs = parse_ps_procs(out_ps)
    if procs is None:
        return {"ts": ts, "status": "error", "rc": RC_ERROR,
                "verdict": None, "roles": {}, "evidence": [],
                "notes": ["ps face output unparseable (fail-closed)"],
                "worker_candidates": []}

    ok_net, out_net = run_net()
    if not ok_net:
        return {"ts": ts, "status": "error", "rc": RC_ERROR,
                "verdict": None, "roles": {}, "evidence": [],
                "notes": ["netstat face unreadable (fail-closed)"],
                "worker_candidates": []}
    owners = parse_netstat_listeners(out_net, (api_port, web_port))
    if owners is None:
        return {"ts": ts, "status": "error", "rc": RC_ERROR,
                "verdict": None, "roles": {}, "evidence": [],
                "notes": ["netstat face unparseable (fail-closed)"],
                "worker_candidates": []}

    topo = classify_topology(procs, owners, api_port, web_port)
    rc = RC_COMPLETE if topo["verdict"] == "complete" else RC_ANOMALY
    return {"ts": ts, "status": "ok", "rc": rc, **topo}


def append_ledger_row(path, result):
    """Best-effort JSONL append (tech#52 family): one row per probe
    run. Error rows still land -- fail-closed is data. WARN on write
    failure, never raises, never changes the exit code."""
    row = {
        "ts": result.get("ts"),
        "verdict": result.get("verdict"),
        "rc": result.get("rc"),
        "api_pid": result.get("roles", {}).get("api"),
        "worker_pid": result.get("roles", {}).get("worker"),
        "proxy_pid": result.get("roles", {}).get("proxy"),
    }
    try:
        ledger_path = Path(path)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    except OSError as exc:
        sys.stderr.write("WARN aihot-procs-ledger append failed: %s\n"
                         % exc)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="AIHOT stack process-topology probe (tech#125): "
                    "prove worker/api/proxy pid identity via port "
                    "binding + cmdline shape before any AIHOT-domain "
                    "kill/restart. rc 0=complete, 1=anomaly, 2=error.")
    parser.add_argument("--api-port", type=int, default=DEFAULT_API_PORT,
                        help="API health port (default %d)"
                             % DEFAULT_API_PORT)
    parser.add_argument("--web-port", type=int, default=DEFAULT_WEB_PORT,
                        help="site-proxy port (default %d)"
                             % DEFAULT_WEB_PORT)
    parser.add_argument("--json", action="store_true",
                        help="single machine-readable line")
    parser.add_argument("--ledger", nargs="?", const=str(DEFAULT_LEDGER),
                        default=None,
                        help="append one JSONL row per probe run (tech#52 "
                             "family; bare --ledger = default %s)"
                             % DEFAULT_LEDGER)
    args = parser.parse_args(argv)

    result = run_probe(api_port=args.api_port, web_port=args.web_port)
    if args.ledger:
        append_ledger_row(args.ledger, result)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("aihot_procs %s: verdict=%s rc=%d"
              % (result["ts"], result["verdict"], result["rc"]))
        roles = result.get("roles") or {}
        for role in ("proxy", "api", "worker"):
            pid = roles.get(role)
            print("  %s: %s" % (role,
                                ("pid %d" % pid) if pid else "unproven"))
        for line in result.get("evidence", []):
            print("  evidence: %s" % line)
        for note in result.get("notes", []):
            print("  note: %s" % note)
        if result["rc"] == RC_COMPLETE:
            print("judgment law (R2038): roles proven -- safe to "
                  "operate the named pid; restart via the canonical "
                  "worker-restart.bat / api-restart.bat")
        elif result["rc"] == RC_ANOMALY:
            print("judgment law (R2038): topology anomaly -- do NOT "
                  "kill/restart any AIHOT-domain pid until identity "
                  "is proven (never guess a same-shape pid)")
        else:
            print("fail-closed: no coherent topology reading -- a "
                  "missing face must never read as complete")
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
