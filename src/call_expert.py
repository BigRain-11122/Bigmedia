# -*- coding: utf-8 -*-
"""On-call departmental expert invoker (O-20260924-1033-bm-a).

Every department keeps dedicated expert roles (functional identities,
org-structure S3 "not personified" law). This tool makes "ready to be
called at any time" literal:

    python src/call_expert.py --expert hot-intel --material data/intel/daily/2026-09-24.md [--timeout S] [--gpu-guard]

Registry = data/experts/registry.json (id/dept/role/prompt_file/model).
Prompts live as UTF-8 data files (encoding rule). tech#186 wire v3
(origin row 432, canon cph4/fleet/qwen38-rollout-20261015.md v3): the
seat stack flies the external brain lane -- :8090 Qwen3.6-35B-A3B over
the OpenAI wire (BRAIN_URL env; model name from the registry default)
with chat_template_kwargs.enable_thinking:false. Liveness probe:
<brain-base>/health 2s -> rc 3 BEFORE any flight cap burns (s1
doctrine R2257). The dormant ollama qwen3.8:27b (measured pathological
prompt_eval 0.16tok/s) is no longer referenced. Zero API, zero token.

Every call is appended to docs/reviews/expert-calls.md (audit trail).

ASCII rule: this source is pure ASCII; Chinese lives in the registry /
prompt / material data files.

Exit codes: 0 ok; 2 bad args / unknown expert / missing files;
            3 ollama call failed; 4 ledger append failed (verdict kept);
            5 GPU guard defer (only with --gpu-guard; advisory, see
              read_gpu_headroom / defer_decision);
            6 wedge probe fast-fail (only with --wedge-probe; the
              ollama generation face is wedged/contended - bail BEFORE
              the long flight burns, see WEDGE_PROBE_* below).

GPU pre-flight guard (tech#44): two E4 reference flights burned 2x1500s
to TIMEOUT during a jman-LoRA training window with zero verdicts (R1847).
Long wrapper flights (s1_call / e4_call pattern, timeout=1500) should
probe headroom before takeoff:

    reading = ce.read_gpu_headroom()
    defer, reason = ce.defer_decision(reading)
    if defer and not FORCE: sys.exit(...)  # print reason first

The guard is advisory: a missing/failing nvidia-smi probe never blocks,
and --gpu-force overrides the CLI gate. Every DEFER also lands one
JSONL row in data/pipeline/gpu-guard-defer-ledger.jsonl (tech#89
fire->defer conversion telemetry; best-effort, never blocks the defer).

--timeout S (tech#45): per-call subprocess timeout in seconds, default
300 (DEFAULT_TIMEOUT) - existing surface unchanged. The S1/E4 long-
review flights historically needed hand-rolled s1_call/e4_call wrapper
copies of this file solely to raise the cap (R176 wrapper lineage);
future pieces fly the CLI directly:

    python src/call_expert.py --expert S1-script \
        --material <review-material.md> --timeout 1500 --gpu-guard

(--gpu-guard recommended on every long flight: it defers cheaply when
another lane owns the card instead of burning the full cap.)
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "data" / "experts" / "registry.json"
LEDGER = REPO / "docs" / "reviews" / "expert-calls.md"
VERDICT_DIR = REPO / "docs" / "reviews" / "expert-verdicts"
DEFER_LEDGER = REPO / "data" / "pipeline" / "gpu-guard-defer-ledger.jsonl"
# tech#377 (R2428): a seat that never ran must leave a trace. Before
# this, every failure path (liveness dead / wire error / wedge bail /
# GPU defer) exited with a clean message and nothing in any ledger, so
# "the review never ran" and "the review ran and failed" looked
# identical to the next round - the only evidence was somebody
# remembering that the model was down. NOT_EXECUTED_MARK is the single
# constant readiness matches on.
NOT_EXECUTED_LEDGER = REPO / "data" / "pipeline" / "expert-not-executed-ledger.jsonl"
NOT_EXECUTED_MARK = "NOT-EXECUTED"
# O-20261015-1335 fleet rollout: the 14b-era 300s default cannot fund a
# cold-ish 17G partial-offload flagship on the 12G card (canon precedent:
# gen_storyboard 420->600 for the same model on this same machine).
DEFAULT_TIMEOUT = 600
# GPU pre-flight guard thresholds (tech#44): defer when the card is
# clearly occupied by another lane (training/render window) or when
# free VRAM is too tight for a local LLM seat.
GPU_DEFER_UTIL_PCT = 80
GPU_DEFER_FREE_MB = 2048
# tech#186 wire v3 (origin row 432): the expert seat stack flies the
# external brain lane -- :8091 Qwen3.5-35B-A3B over the OpenAI wire.
# BRAIN_URL is env-driven (canon cph4/fleet/qwen38-rollout-20261015.md
# v3 -- BRAIN_URL/BRAIN_MODEL "one line per machine"); the health URL
# derives from the same base. The dormant ollama qwen3.8:27b (measured
# pathological prompt_eval 0.16tok/s) is no longer referenced.
# D-20261024-01 (R2431): the seat was regenerated on :8091 (the old
# :8090 name is retired and must not be reused), so both faces move
# together or "probe says up" and "call can fly" would drift apart.
BRAIN_URL = os.environ.get(
    "BRAIN_URL", "http://127.0.0.1:8091/v1/chat/completions")


def resolve_health_url(brain_url, override=None):
    """Liveness URL for a seat; an explicit override wins (pure).

    tech#379 (R2430): a provider that answers the OpenAI wire but has
    no /health endpoint (ollama serves /api/version and 404s /health)
    was indistinguishable from a dead seat - both returned rc 3 - so no
    substitute seat could ever be measured. BRAIN_HEALTH_URL lets the
    probe point at a URL that provider does answer, keeping "seat
    answers" and "seat can fly" the same question.
    """
    if override:
        return override
    return brain_url.split("/v1/")[0].rstrip("/") + "/health"


BRAIN_HEALTH_URL = resolve_health_url(
    BRAIN_URL, os.environ.get("BRAIN_HEALTH_URL"))
BRAIN_DEFAULT_MODEL = os.environ.get("BRAIN_MODEL", "qwen3.6-35b")
LIVENESS_CAP_S = 2
# tech#120 wedge fast-fail probe: two 1500s S1 flights burned through
# wedged/contended windows with zero verdicts (R2012 flight-1 /
# R2013 flight-2 anchor). A tiny generation either returns in seconds
# (healthy seat) or burns the cap (wedged seat) -> bail with rc 6
# BEFORE the main long flight. The probe itself never lands in
# expert-calls (verdict/ledger writes only happen on the main call
# path). tech#186 lane: the micro-probe flies the brain lane's own
# seat (the resident server answers a micro generation in <1s, R2297
# smoke wall=0.5s); the 240s cap stays as the hard hat only.
WEDGE_PROBE_MODEL = BRAIN_DEFAULT_MODEL
WEDGE_PROBE_CAP = 240
# ollama streams ANSI line-erase codes on slow generations (cold-load
# case); without stripping they land verbatim in verdict archives
# (2026-09-24 BS-003 S1 case). Braille spinner glyphs (U+2800 block)
# are a second pollution class seen on long generations (2026-09-25
# BS-004 E4 case).
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_SPINNER_RE = re.compile(r"[\u2800-\u28ff]")


def load_registry(path=REGISTRY):
    """Load registry -> (default_model, {id: expert}). Pure."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    experts = {}
    for e in data.get("experts", []):
        experts[str(e["id"])] = {
            "id": str(e["id"]),
            "dept": str(e["dept"]),
            "role": str(e["role"]),
            "prompt_file": str(e["prompt_file"]),
            "model": str(e.get("model") or data.get("model", "")),
        }
    return data.get("model", ""), experts


def build_prompt(prompt_text, material_text):
    """Assemble the expert call prompt (pure)."""
    return (prompt_text.rstrip() +
            "\n\n===== \u6750\u6599 =====\n" +
            material_text.strip() + "\n")


def brain_health_ok(cap_s=LIVENESS_CAP_S):
    """True when the brain lane answers <brain-base>/health inside the
    cap. Never raises -- an unreachable server reads as not-ok."""
    try:
        with urllib.request.urlopen(BRAIN_HEALTH_URL,
                                    timeout=cap_s) as resp:
            resp.read()
        return True
    except Exception:
        return False


def call_model(model, prompt, timeout=DEFAULT_TIMEOUT):
    """Fly the expert call on the brain lane (tech#186 OpenAI wire,
    same contract as src/e4_ref_call.py): liveness <base>/health 2s
    probe first, then one non-streaming /v1/chat/completions POST with
    chat_template_kwargs.enable_thinking:false (the fleet flagship is
    a thinking model; verdict formats like S1 v1.5 scoring need clean
    output).
    Returns (returncode, text): 0 ok; 3 liveness/transport/timeout
    failure. Never raises -- main()/wedge callers hold their own rc
    contracts on the (rc, text) pair."""
    if not brain_health_ok():
        return 3, ("brain /health unreachable (%ds cap) - liveness"
                   " fail-closed, no flight cap burned"
                   % LIVENESS_CAP_S)
    payload = json.dumps({
        "model": model,
        "stream": False,
        "messages": [{"role": "user", "content": prompt}],
        "chat_template_kwargs": {"enable_thinking": False},
    }).encode("utf-8")
    request = urllib.request.Request(
        BRAIN_URL, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as exc:  # transport errors include the cap
        text = "%s: %s" % (type(exc).__name__, exc)
        if "timed out" in text.lower() or "timeout" in text.lower():
            return 3, "brain wire timeout (%ds cap)" % timeout
        return 3, "brain wire transport error: %s" % text
    choices = body.get("choices") or []
    content = ""
    if choices:
        content = (choices[0].get("message") or {}).get("content") or ""
    # defense-in-depth strip (ollama-CLI era pollution classes; the
    # wire returns clean JSON but the strip is zero-cost)
    content = _ANSI_RE.sub("", content)
    content = _SPINNER_RE.sub("", content)
    return 0, content


def parse_headroom(raw_output):
    """Pure: first CSV row of `nvidia-smi --query-gpu=utilization.gpu,
    memory.free --format=csv,noheader,nounits` -> reading dict, or None
    when the output is empty / malformed (probe face, never raises)."""
    lines = (raw_output or "").strip().splitlines()
    if not lines:
        return None
    try:
        util_s, free_s = [t.strip() for t in lines[0].split(",")[:2]]
        return {"util_pct": int(util_s), "free_mb": int(free_s),
                "raw": lines[0]}
    except (IndexError, ValueError):
        return None


def read_gpu_headroom():
    """Probe nvidia-smi for GPU utilization + free VRAM (advisory face).

    Returns a reading dict or None when nvidia-smi is missing / errors /
    is not parseable - a broken probe must never block an expert call."""
    try:
        p = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.free",
             "--format=csv,noheader,nounits"],
            capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode != 0:
        return None
    return parse_headroom(p.stdout.decode("utf-8", "replace"))


def defer_decision(reading, util_threshold=GPU_DEFER_UTIL_PCT,
                   free_threshold=GPU_DEFER_FREE_MB):
    """Pure: should this expert call be deferred given the GPU reading?

    Returns (defer, reason). None reading -> (False, "") - probe
    unavailable means the guard stays silent (advisory only)."""
    if reading is None:
        return False, ""
    if reading["util_pct"] > util_threshold:
        return True, "gpu util %d%% > %d%% (occupied window)" % (
            reading["util_pct"], util_threshold)
    if reading["free_mb"] < free_threshold:
        return True, "gpu free %dMB < %dMB" % (
            reading["free_mb"], free_threshold)
    return False, ""


def defer_row(expert_id, material, reason, reading, now=None):
    """Pure: one JSONL row for a GPU-guard DEFER (tech#89 telemetry).

    R1943 anchor: two guard defers in one fire window were visible only
    as hand-written round-log notes. Rows make the fire->defer
    conversion a readable ledger (symmetric with the ollama-probe /
    mv-sprint JSONL ledgers). Exact field set, one defer = one line."""
    stamp = (now or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "ts": stamp,
        "event": "defer",
        "expert": expert_id,
        "material": str(material),
        "reason": reason,
        "util_pct": reading.get("util_pct") if reading else None,
        "free_mb": reading.get("free_mb") if reading else None,
        "rc": 5,
    }
    return json.dumps(payload, ensure_ascii=False)


def append_defer_row(row, path=None):
    """Best-effort JSONL append (tech#19/52 law: a write failure WARNs,
    it never changes the guard outcome). Returns True on success.
    path=None resolves DEFER_LEDGER at call time (hermetic tests patch
    the module global; a def-time default would bind the real path)."""
    try:
        target = Path(path) if path is not None else DEFER_LEDGER
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(row + "\n")
        return True
    except OSError:
        return False


def not_executed_row(expert_id, material, reason, exit_code, now=None):
    """Pure: one JSONL row for a seat call that produced no verdict
    (tech#377). Field set mirrors defer_row so a reader can tell the
    two apart by `mark` alone:
      - NOT-EXECUTED = the review face never ran (this file)
      - event=defer    = the guard stopped it before takeoff
    Both are recorded; neither may be read as a review verdict."""
    stamp = (now or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "ts": stamp,
        "mark": NOT_EXECUTED_MARK,
        "expert": expert_id,
        "material": str(material),
        "reason": reason,
        "rc": int(exit_code),
    }
    return json.dumps(payload, ensure_ascii=False)


def append_not_executed(row, path=None):
    """Best-effort JSONL append (same law as append_defer_row: a write
    failure WARNs, it never changes the call's exit code). path=None
    resolves NOT_EXECUTED_LEDGER at call time so tests can patch it."""
    try:
        target = Path(path) if path is not None else NOT_EXECUTED_LEDGER
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(row + "\n")
        return True
    except OSError:
        return False


LEDGER_HEADER = (
    "# \u4e13\u804c\u4e13\u5bb6\u8c03\u7528\u53f0\u8d26\uff08"
    "Expert Calls Ledger\uff09\n\n"
    "> \u673a\u5236=`docs/expert-roster.md`\uff08O-20260924-1033-bm-a\uff09\u3002"
    "\u884c\u7ea7\u8ffd\u52a0\u7981\u6539\u5199\uff1b\u6bcf\u6b21 "
    "call_expert.py \u771f\u8c03\u81ea\u52a8\u843d\u4e00\u884c"
    "\uff08\u7ed3\u8bba\u5168\u6587=expert-verdicts/ \u76ee\u5f55\u00b7"
    "\u672c\u8868\u53ea\u5b58\u9996\u884c\uff09\u3002\n\n"
    "| \u65f6\u95f4 | \u4e13\u5bb6 | \u8eab\u4efd\uff08\u90e8\u95e8\uff09 | "
    "\u6750\u6599 | \u9000\u51fa | \u7ed3\u8bba\u9996\u884c |\n"
    "|---|---|---|---|---|---|\n")


def append_ledger_row(row, path=None):
    """Best-effort append to the human audit ledger, creating the table
    header on first write. Returns True on success."""
    try:
        target = Path(path) if path is not None else LEDGER
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(LEDGER_HEADER, encoding="utf-8")
        with target.open("a", encoding="utf-8") as f:
            f.write(row)
        return True
    except OSError:
        return False


def record_not_executed(expert_id, role, dept, material, reason, exit_code,
                        ledger=None, jsonl=None):
    """Leave the not-executed trace on both faces (tech#377).

    The markdown ledger keeps the audit trail free of a silent hole
    (same table shape as a real call, exit code + reason visible); the
    JSONL row is the machine face readiness reads. Both best-effort.
    Returns (jsonl_ok, ledger_ok)."""
    jsonl_ok = append_not_executed(
        not_executed_row(expert_id, material, reason, exit_code), jsonl)
    note = "%s rc=%d: %s" % (NOT_EXECUTED_MARK, int(exit_code), reason)
    ledger_ok = append_ledger_row(
        ledger_row(expert_id, role, dept, str(material), int(exit_code),
                   note), ledger)
    return jsonl_ok, ledger_ok


def ledger_row(expert_id, role, dept, material, exit_code, note):
    """One markdown table row for the call ledger (pure)."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note = (note or "-").replace("|", "/").replace("\n", " ")[:160]
    return "| %s | %s | %s（%s） | %s | %s | %s |\n" % (
        stamp, expert_id, role, dept, material, exit_code, note)


def verdict_file_name(expert_id, stamp=None):
    """Deterministic archive file name for one call's full verdict (pure)."""
    stamp = stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    return "%s-%s.md" % (stamp, expert_id)


def save_verdict(out_dir, file_name, expert_id, role, dept, model,
                 material, verdict):
    """Write the FULL verdict to its archive file; returns the path.
    The ledger only keeps the first line - without this the full text
    only ever existed in a GBK-garbled console (2026-09-24 hot-intel
    case: verdict lost)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / file_name
    body = [
        "# %s - %s（%s）结论全文" % (expert_id, role, dept),
        "",
        "> 时间=%s · 模型=%s · 材料=%s" % (
            datetime.now().strftime("%Y-%m-%d %H:%M"), model, material),
        "> 机制=call_expert.py（O-20260924-1033·本件为结论存档·台账行=expert-calls.md）",
        "",
    ]
    path.write_text("\n".join(body) + verdict + "\n", encoding="utf-8")
    return path


def main(argv):
    expert_id = material = timeout_raw = None
    gpu_guard = gpu_force = wedge_probe = False
    i = 1
    while i < len(argv):
        if argv[i] == "--expert":
            i += 1
            expert_id = argv[i]
        elif argv[i] == "--material":
            i += 1
            material = argv[i]
        elif argv[i] == "--timeout":
            i += 1
            if i >= len(argv):
                print("FAIL --timeout needs a value (seconds)")
                return 2
            timeout_raw = argv[i]
        elif argv[i] == "--gpu-guard":
            gpu_guard = True
        elif argv[i] == "--wedge-probe":
            wedge_probe = True
        elif argv[i] == "--gpu-force":
            gpu_force = True
        i += 1
    if not (expert_id and material):
        print("usage: call_expert.py --expert ID --material FILE "
              "[--timeout S] [--gpu-guard] [--wedge-probe] [--gpu-force]")
        return 2
    timeout_s = DEFAULT_TIMEOUT
    if timeout_raw is not None:
        try:
            timeout_s = int(timeout_raw)
        except ValueError:
            print("FAIL --timeout must be an integer number of seconds: %r"
                  % timeout_raw)
            return 2
        if timeout_s <= 0:
            print("FAIL --timeout must be > 0 seconds: %d" % timeout_s)
            return 2
    try:
        _, experts = load_registry()
    except (OSError, ValueError) as e:
        print("FAIL registry: %s" % e)
        return 2
    if expert_id not in experts:
        print("FAIL unknown expert: %s (known: %s)"
              % (expert_id, ", ".join(sorted(experts))))
        return 2
    ex = experts[expert_id]
    prompt_path = REPO / ex["prompt_file"]
    material_path = Path(material)
    if not prompt_path.exists():
        print("FAIL prompt file missing: %s" % prompt_path)
        return 2
    if not material_path.exists():
        print("FAIL material file missing: %s" % material_path)
        return 2

    def trace_not_executed(reason, code):
        """tech#377: a seat that never ran leaves both faces behind.
        Best-effort - a write failure only WARNs, the exit code stands."""
        jsonl_ok, ledger_ok = record_not_executed(
            expert_id, ex["role"], ex["dept"], material_path, reason, code)
        print("%s rc=%d: %s" % (NOT_EXECUTED_MARK, code, reason))
        if not jsonl_ok or not ledger_ok:
            print("WARN not-executed ledger append failed (exit kept)")
    if gpu_guard:
        # tech#44 pre-flight: probe before burning a (possibly 1500s)
        # local-LLM flight. Advisory - force overrides, probe failure
        # stays silent-but-proceeds.
        reading = read_gpu_headroom()
        defer, reason = defer_decision(reading)
        if defer:
            if gpu_force:
                print("WARN gpu-force override: %s" % reason)
            else:
                print("DEFER %s" % reason)
                print("DEFER note: under an occupied window the 1500s "
                      "wrapper cap burned through twice with zero "
                      "verdicts (R1847 E4 case); retry in a GPU release "
                      "window, or pass --gpu-force to fly anyway.")
                # tech#89 telemetry: defer events land as JSONL rows
                # (best-effort; a write failure never blocks the defer).
                if not append_defer_row(defer_row(expert_id, material,
                                                  reason, reading)):
                    print("WARN defer ledger append failed (defer kept)")
                trace_not_executed("gpu-guard defer: %s" % reason, 5)
                return 5
        elif reading is None:
            print("WARN gpu probe unavailable; proceeding (advisory guard)")
        else:
            print("GPU-OK util=%d%% free=%dMB"
                  % (reading["util_pct"], reading["free_mb"]))
    if wedge_probe:
        # tech#120 fast-fail: micro generation on a small model under a
        # hard cap. Wedged/contended ollama burns the cap -> rc 6
        # BEFORE the main (possibly 1500s) flight. Guard runs first
        # (cheaper probe); probe failure is a hard bail, not advisory -
        # a wedged window produced two zero-verdict 1500s burns
        # (R2012/R2013) and a third would be the same loss.
        try:
            wcode, _ = call_model(WEDGE_PROBE_MODEL,
                                  "Reply with the single word OK",
                                  timeout=WEDGE_PROBE_CAP)
        except subprocess.TimeoutExpired:
            print("WEDGE-FAIL brain micro-probe timed out (%ds cap,"
                  " model %s) - wedged/contended window; re-dispatch"
                  " in a healthy window"
                  % (WEDGE_PROBE_CAP, WEDGE_PROBE_MODEL))
            trace_not_executed(
                "wedge probe timed out (%ds cap)" % WEDGE_PROBE_CAP, 6)
            return 6
        if wcode != 0:
            print("WEDGE-FAIL brain micro-probe exit %d - server"
                  " unhealthy; re-dispatch in a healthy window" % wcode)
            trace_not_executed(
                "wedge probe exit %d (server unhealthy)" % wcode, 6)
            return 6
        print("WEDGE-OK micro-probe alive (model %s, %ds cap)"
              % (WEDGE_PROBE_MODEL, WEDGE_PROBE_CAP))
    prompt = build_prompt(prompt_path.read_text(encoding="utf-8"),
                          material_path.read_text(encoding="utf-8"))
    try:
        code, out = call_model(ex["model"], prompt, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        # call_model never raises on the wire (its (rc, text) contract
        # absorbs timeouts); kept as a hard safety net.
        print("FAIL model call timeout (%ds)" % timeout_s)
        code, out = 3, ""
        trace_not_executed("model call timeout (%ds)" % timeout_s, 3)
        return 3
    if code != 0:
        print("FAIL model call exit %d" % code)
        print(out[-500:])
        trace_not_executed("model call failed: %s"
                           % (" ".join((out or "").split())[:200] or
                              "exit %d" % code), 3)
        return 3
    verdict = out.strip()
    print("OK %s [%s - %s]" % (expert_id, ex["dept"], ex["role"]))
    print("----- verdict -----")
    print(verdict)
    # full verdict archive first (auditability: the console is GBK-lossy)
    try:
        vname = verdict_file_name(expert_id)
        vpath = save_verdict(VERDICT_DIR, vname, expert_id, ex["role"],
                             ex["dept"], ex["model"], str(material_path),
                             verdict)
        print("----- verdict archive -----")
        print(str(vpath))
    except OSError as e:
        print("WARN verdict archive failed: %s" % e)
        vname = ""
    # audit trail: every call lands in the ledger (best effort)
    try:
        first_line = verdict.splitlines()[0][:120] if verdict else "-"
        if vname:
            first_line = "全文=expert-verdicts/%s ｜ %s" % (vname, first_line)
        row = ledger_row(expert_id, ex["role"], ex["dept"],
                         str(material_path), 0, first_line)
        if not append_ledger_row(row):
            print("WARN ledger append failed (verdict kept above)")
    except OSError as e:
        print("WARN ledger append failed: %s (verdict kept above)" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
