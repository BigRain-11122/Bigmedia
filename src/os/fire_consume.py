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
  1 = no-fire (window closed, stale verdict, bm-a workday-hours
      dispatch block, or throughput-probe defer tech#135; card cited)
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
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CARD_SCRIPT = REPO / "src" / "os" / "fire_window_card.py"
DEFAULT_LEDGER = REPO / "data" / "pipeline" / "fire-consume-ledger.jsonl"
CARD_TIMEOUT_S = 300

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

# bm-a standing rule (CEO order 2026-10-12 15:0x, the machine-loading
# order): this machine gets ZERO job dispatch during workday working
# hours. Eligible dispatch windows: nightly 00:00-07:59 plus weekends.
# Escalated to a script assertion per the recurrence-escalation law:
# the rule must hold structurally, not as a round-log checklist note.
# The card is not even read while the block is active -- dispatch is
# illegal regardless of GPU state, so probing it is moot.
WORKDAY_BLOCK_START_HOUR = 8

# tech#137 reconciliation (CEO order O-20261012-2025 family): a newer
# CEO order declaring "CEO off work" opens the night window EARLY --
# newer order beats the 15:0x hardcode (new-order-overrides law).
# The loop encodes such a consumption into a repo-local flag file
# (same lifecycle pattern as the AIHOT pause flag): written when a
# CEO-off-work order is consumed, deleted when the CEO returns / at
# the morning self-heal. Freshness = same calendar date as the
# declaration (an evening declaration covers the rest of that day;
# 00:00-07:59 is already eligible via the standing rule). Missing /
# malformed / stale flag NEVER lifts the block -- fail-closed.
CEO_OFF_WORK_FLAG = REPO / "data" / "pipeline" / "ceo-off-work-flag.json"

# Test seam: main()/flag math read the clock through this module
# global (CLI tests must not depend on the wall-clock weekday).
NOW_FN = datetime.datetime.now

USAGE = ("usage: python src/os/fire_consume.py --launch "
        "<staged-launch.py> [--ledger F] [--json] [--cpu-lane]")

LAUNCH_MARGIN_S = 2  # dispatch latency budget inside the TTL

# tech#135 (P-7 pilot): throughput pre-probe before dispatch. Three
# S1 flights burned their full 1500s hats in GPU-starved windows with
# zero verdict (R2012 flight-1 / R2013 flight-2 / R2024 flight-3) --
# the card's gates (VRAM / util / mv / load-class) say nothing about
# ollama's ACHIEVABLE generation rate. The probe runs ONLY on a
# card-GO (no-fire rounds stay zero-cost): one small non-streaming
# generation against the local ollama gives a load-excluded effective
# token rate, extrapolated to a full-verdict ETA. ETA over the
# conservative starve line -> no-fire reason=throughput-starved,
# deferred to the next window (a <=90s probe instead of a 1500s
# burn). Conservative single-direction (tech#136 discipline): this
# face can only demote a GO, never force one. Thresholds are
# deliberately conservative initial values, calibrate from the
# pilot readout (P-7 judge questions pre-registered in §D).
PROBE_MODEL_DEFAULT = "qwen3.8:27b"
PROBE_PROMPT = ("Reply with the numbers from one to twenty, "
                "comma separated.")
PROBE_TOKENS = 96          # num_predict of the micro-generation
PROBE_CAP_S = 90           # P-7: probe budget <= 90s per attempt
ETA_PROMPT_TOKENS = 6000   # conservative S1/E4 material size
ETA_OUTPUT_TOKENS = 900     # conservative verdict size
ETA_STARVED_S = 1200       # P-7: conservative initial starve line
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

# tech#169 (CPU lane): O-20260913-2215 CEO standing order opens the
# fleet CPU face 24/7 and explicitly repeals the workday zero-dispatch
# rule's CPU portion ("工作日工作时间零排单"的 CPU 部分就此废止) --
# new-order-overrides law (tech#137). The GPU 让路律 survives
# untouched: a CPU-lane flight never touches the GPU (num_gpu=0
# asserted inside the generated CPU-variant launcher), and the CEO 10%
# CPU margin law survives as num_thread=4 (enforced both in the probe
# below and in the launcher variant). The GPU card is not run on this
# lane -- its VRAM/util/load-class readings gate a load class the
# CPU-pinned flight never consumes (the R2251 structural backlog:
# F-181..185 E4 legs parked behind a GPU gate while the legal CPU
# lane sat idle). The lane verdict comes from ONE CPU-pinned
# micro-generation: rate -> ETA -> the same single-direction
# throughput demotion (tech#135 discipline preserved).
CPU_LANE_THREADS = 4
CPU_PROBE_CAP_S = 180     # cold-load margin; rate math excludes load
CPU_LANE_NAME_MARK = "_cpu"  # mis-wiring guard: --cpu-lane launches
#                           # only CPU-variant launchers (e.g.
#                           # e4_call_cpu.py). A GPU launcher on the
#                           # CPU lane would fly OUTSIDE every gate --
#                           # the guard makes that wiring error loud.


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


def _expired(expires_at, now_epoch):
    """TTL math shared by the pre-launch and post-probe checks:
    a verdict at/inside the margin is stale, never dispatched."""
    return now_epoch + LAUNCH_MARGIN_S >= expires_at


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
    if _expired(expires_at, now_epoch):
        return "stale", "fire-verdict-expired-at-%d" % expires_at, 1
    return "launch", "fire-fresh", 0


def read_ceo_off_work_flag(path=CEO_OFF_WORK_FLAG):
    """Parse the CEO-off-work flag -> declared datetime or None.

    Fail-closed: missing file, bad JSON, missing/malformed declared_ts
    all read as None (the block stays). A malformed flag never lifts
    the zero-dispatch rule."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        declared = datetime.datetime.strptime(
            payload["declared_ts"], "%Y-%m-%d %H:%M:%S")
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return declared


def workday_dispatch_blocked(dt, flag_declared=None):
    """True when bm-a workday-hours zero-dispatch rule blocks flights.

    Weekends (Sat/Sun) are always eligible; weekdays block from 08:00
    through 23:59 -- EXCEPT when a fresh CEO-off-work flag (tech#137,
    O-20261012-2025 family) declares the night window early-open:
    same-date declaration lifts the block for the rest of that day.
    Pure function -> trivially testable at boundaries."""
    if dt.weekday() >= 5:  # 5=Sat, 6=Sun
        return False
    if dt.hour < WORKDAY_BLOCK_START_HOUR:
        return False  # standing night window 00:00-07:59
    if flag_declared is not None and flag_declared.date() == dt.date():
        return False  # CEO declared off work today (early-open)
    return True


def compute_rate(body):
    """Pure core: ollama generate response -> (rate_tps, eta_s) or
    None.

    Load time is deliberately excluded (prompt_eval_duration +
    eval_duration only): a cold load is not starvation, and after the
    probe the model stays resident for the flight (shared work, not
    extra cost). The rate covers prefill+decode tokens over
    prefill+decode time -- a conservative proxy for a full verdict
    (whose prompt is ~6000 tokens, not 20). Missing/zero counters
    read as None; callers treat that as probe-error fail-closed."""
    prompt_count = body.get("prompt_eval_count") or 0
    eval_count = body.get("eval_count") or 0
    prompt_ns = body.get("prompt_eval_duration") or 0
    eval_ns = body.get("eval_duration") or 0
    elapsed_ns = prompt_ns + eval_ns
    tokens = prompt_count + eval_count
    if elapsed_ns <= 0 or tokens <= 0:
        return None
    rate_tps = tokens / (elapsed_ns / 1e9)
    eta_s = (ETA_PROMPT_TOKENS + ETA_OUTPUT_TOKENS) / rate_tps
    return rate_tps, eta_s


def real_throughput_probe(model=PROBE_MODEL_DEFAULT,
                          cap_s=PROBE_CAP_S, cpu_lane=False):
    """Network seam (injected in tests; never called on no-fire
    paths): one small non-streaming ollama generation -> probe row.

    cpu_lane=True (tech#169) pins the probe to the CPU lane
    (options num_gpu=0 + num_thread=4): the probe then measures the
    lane the flight will actually fly, and its success IS the
    zero-GPU-touch assertion in flight.

    verdict: ok (rate+eta computed) / timeout (cap exceeded -- the
    starved hard case: PROBE_TOKENS did not finish inside cap_s, so
    an ETA_OUTPUT_TOKENS verdict cannot land inside the 1500s flight
    hat) / error (transport/HTTP/JSON failure -- fail-closed at the
    caller for the same reason: an ollama that cannot answer a
    96-token generation cannot deliver a verdict). The probe calls
    ollama directly and NEVER writes expert-calls rows (same
    discipline as the tech#120 wedge probe: probes never pollute
    call accounting)."""
    options = {"num_predict": PROBE_TOKENS}
    if cpu_lane:
        options["num_gpu"] = 0
        options["num_thread"] = CPU_LANE_THREADS
    payload = json.dumps({
        "model": model, "prompt": PROBE_PROMPT, "stream": False,
        # O-20261015-1335: flagship is a thinking model; thinking would
        # wreck the token-rate math this probe exists to measure.
        "think": False,
        "options": options,
    }).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_GENERATE_URL, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=cap_s) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as exc:  # transport errors include the cap
        text = "%s: %s" % (type(exc).__name__, exc)
        verdict = ("timeout"
                   if "timed out" in text.lower() else "error")
        return {"verdict": verdict, "model": model, "cap_s": cap_s,
                "error": text}
    computed = compute_rate(body)
    if computed is None:
        return {"verdict": "error", "model": model, "cap_s": cap_s,
                "error": "probe counters missing/zero",
                "raw_keys": sorted(str(k) for k in body)}
    rate_tps, eta_s = computed
    return {"verdict": "ok", "model": model, "cap_s": cap_s,
            "rate_tps": round(rate_tps, 3), "eta_s": int(eta_s),
            "probe_tokens": PROBE_TOKENS}


def classify_throughput(probe, eta_starved_s=ETA_STARVED_S):
    """Pure core: probe row -> (ok_to_launch, reason).

    Demotion is single-direction: a starved/timeout/error probe turns
    a GO into no-fire rc1 (defer to the next window) -- it can never
    upgrade a card verdict, never error out a valid window."""
    if not isinstance(probe, dict) or not probe.get("verdict"):
        return False, "throughput-probe-error: malformed probe result"
    if probe["verdict"] == "ok":
        eta = probe.get("eta_s")
        if not isinstance(eta, (int, float)) or eta <= 0:
            return False, "throughput-probe-error: ok without eta_s"
        if eta > eta_starved_s:
            return False, ("throughput-starved: eta %ss > %ss line "
                           "(rate %s tok/s)" % (
                               eta, eta_starved_s,
                               probe.get("rate_tps", "n/a")))
        return True, ("throughput-ok: eta %ss <= %ss line" % (
            eta, eta_starved_s))
    if probe["verdict"] == "timeout":
        return False, ("throughput-starved: probe timeout > %ss cap "
                       "(%s tokens unfinished)" % (
                           probe.get("cap_s", PROBE_CAP_S),
                           probe.get("probe_tokens", PROBE_TOKENS)))
    return False, "throughput-probe-error: %s" % probe.get(
        "error", probe.get("verdict"))


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
    parser.add_argument("--probe-model", default=PROBE_MODEL_DEFAULT,
                        help="ollama model for the throughput "
                             "pre-probe (default %(default)s)")
    parser.add_argument("--eta-starved-s", type=float,
                        default=ETA_STARVED_S,
                        help="verdict-ETA starve line in seconds "
                             "(default %(default)s -- P-7 "
                             "conservative initial value)")
    parser.add_argument("--cpu-lane", action="store_true",
                        help="tech#169 CPU lane: skip the GPU card and "
                             "the workday block (O-20260913-2215 CPU-"
                             "face repeal); gate on one CPU-pinned "
                             "(num_gpu=0/num_thread=4) throughput probe; "
                             "launch must be a CPU-variant launcher "
                             "(name contains '%s')" % CPU_LANE_NAME_MARK)
    args = parser.parse_args(argv)

    launch = Path(args.launch)
    if not launch.is_file() or launch.suffix != ".py":
        print(USAGE)
        return 2

    now_dt = NOW_FN()

    if args.cpu_lane:
        # tech#169 CPU lane: the workday zero-dispatch block is NOT
        # applied here -- O-20260913-2215 explicitly repealed the
        # rule's CPU portion (CPU face 24/7), and the GPU card is not
        # run (its VRAM/util/load-class readings gate a load class a
        # CPU-pinned flight never consumes). The lane verdict comes
        # from one CPU-pinned throughput probe; demotion is
        # single-direction (starved/timeout/error -> no-fire rc1).
        if CPU_LANE_NAME_MARK not in launch.name:
            print("USAGE: --cpu-lane requires a CPU-variant launcher "
                  "(name contains '%s') -- a GPU launcher on the CPU "
                  "lane would fly outside every gate"
                  % CPU_LANE_NAME_MARK)
            return 2
        probe_row = real_throughput_probe(
            args.probe_model, cap_s=CPU_PROBE_CAP_S, cpu_lane=True)
        ok, probe_reason = classify_throughput(
            probe_row, args.eta_starved_s)
        action, reason, rc = "no-fire", probe_reason, 1
        launch_pid = None
        if ok:
            try:
                launch_pid = real_launch(launch)
                action, reason, rc = "launch", "cpu-lane-fire-fresh", 0
            except OSError as exc:
                action, reason, rc = ("error", "launch-failed: %s"
                                      % exc, 2)
        result = {
            "tool": "fire_consume",
            "lane": "cpu",
            "ts": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"),
            "action": action,
            "reason": reason,
            "launched": action == "launch",
            "launch_script": str(launch),
            "launch_pid": launch_pid,
            "rc": rc,
        }
        result["throughput_probe"] = probe_row
        if args.ledger:
            append_ledger_row(args.ledger, result)
        print(json.dumps(result, ensure_ascii=False) if args.json else
              "fire-consume: lane=cpu action=%s launched=%s reason=%s%s"
              % (action, result["launched"], reason,
                 " pid=%s" % launch_pid if launch_pid else ""))
        return rc

    if workday_dispatch_blocked(now_dt,
                                read_ceo_off_work_flag()):
        # bm-a workday-hours zero-dispatch (CEO order 2026-10-12):
        # refuse before any card run -- dispatch is illegal regardless
        # of GPU state. Ledger keeps the one-row-per-run trace.
        reason = "bm-a-workday-hours-zero-dispatch"
        result = {"tool": "fire_consume", "action": "no-fire",
                  "reason": reason, "launched": False,
                  "launch_script": str(launch),
                  "ts": now_dt.strftime("%Y-%m-%d %H:%M:%S"), "rc": 1}
        if args.ledger:
            append_ledger_row(args.ledger, result)
        print(json.dumps(result, ensure_ascii=False) if args.json else
              "fire-consume: card=blocked action=no-fire "
              "launched=False reason=%s" % reason)
        return 1

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
    probe_row = None
    if action == "launch":
        # tech#135 (P-7): throughput pre-probe -- the LAST gate before
        # dispatch, and only on a GO (no-fire rounds never pay for
        # it). Demotion is single-direction no-fire rc1.
        probe_row = real_throughput_probe(args.probe_model)
        ok, probe_reason = classify_throughput(
            probe_row, args.eta_starved_s)
        if not ok:
            action, reason, rc = "no-fire", probe_reason, 1
        elif _expired(card["expires_at"],
                      int(datetime.datetime.now().timestamp())):
            # the probe spent window TTL -- never dispatch a verdict
            # at/after expiry (staleness law, defensive re-check)
            action, reason, rc = (
                "stale", "fire-verdict-expired-after-probe-at-%d"
                % card["expires_at"], 1)
        else:
            try:
                launch_pid = real_launch(launch)
            except OSError as exc:
                action, reason, rc = ("error", "launch-failed: %s"
                                     % exc, 2)

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
    if probe_row is not None:
        result["throughput_probe"] = probe_row
    if args.ledger:
        append_ledger_row(args.ledger, result)
    print(json.dumps(result, ensure_ascii=False) if args.json else
          "fire-consume: card=%s action=%s launched=%s reason=%s%s"
          % (card.get("verdict"), action, result["launched"], reason,
             " pid=%s" % launch_pid if launch_pid else ""))
    return rc


if __name__ == "__main__":
    sys.exit(main())
