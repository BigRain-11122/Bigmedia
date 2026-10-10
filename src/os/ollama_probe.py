# -*- coding: utf-8 -*-
"""Fixed ollama generation probe (tech#41 recovery criterion; tech#51, R1881;
tech#52 --ledger JSONL evidence face, R1883).

Recovery criterion for a saturated ollama server (F-20261010-03 family):
generate-probe only. Two trap families this probe permanently retires:

1. /api/tags stays 200 under saturation (R1877 trap) -> never a signal.
2. PS 5.1 inline JSON loses its quotes through the shell wrapper ->
   ollama answers 400 Bad Request (R1880 operation red). That 400 was a
   TRANSPORT ARTIFACT, not a server signal. This probe builds the body with
   json.dumps inside Python (no shell quoting surface), so a 400 observed
   through it is genuine server-side rejection and stays classified rc=2.

Exit codes:
  0 = generation returned 200 (recovered)
  1 = saturated (503 / 'maximum pending requests exceeded')
  2 = other transport/server error (ambiguous, raw status surfaced)

Usage:
  python src/os/ollama_probe.py [--model M] [--timeout S] [--base-url URL] [--json] [--ledger [PATH]]

The per-round recovery check (tech#41) uses this fixed probe; ad-hoc rewrites
are retired. --json emits one machine-readable line for evidence files.

--ledger (tech#52, R1883) appends one JSONL row (ts/rc/status/http_status/
model) per real probe flight to the given path (bare --ledger = default
data/pipeline/ollama-probe-ledger.jsonl). Opt-in only: without the flag the
existing call surface is untouched. Best-effort (whisper-ledger tech#19
pattern): a failed append WARNs on stderr and never changes the exit code.
No probe flight (bad timeout) -> no row.

Rows also carry gpu_util/gpu_mem context columns (tech#54, R1888): a
best-effort nvidia-smi CSV read so a saturation row shows whether the GPU
was actually generating at probe time (the R1883-R1885 wedged-slot case was
only diagnosable by hand because 503 rows carried no GPU context). Any
read failure -> "NONE" markers; never raises, never changes the exit code.

tech#55 (R1889): advisory `face` column -- the three-face reading discipline
for probe rows consumed by GPU-window scheduling decisions (gap anchor:
the R1888 10:59 flight read rc2 timeout during a 100%/11348MiB generation
window; without a face label that is one manual misread away from
"service broken"). Faces, advisory only, rc semantics never move:
  rc=0                    -> ok
  503 + GPU idle (<80%)   -> slot-wedged      (queue wedged, R1883-85 family)
  503 + GPU busy (>=80%)   -> saturated-busy   (genuine queue-full, generating)
  timeout + GPU busy      -> busy-contended   (server healthy, slow under load: YIELD, not broken)
  timeout + GPU idle + gpu_mem < 4000MiB
                          -> cold-reload      (no ollama model resident: the probe itself started
                                               a cold load that outran the request cap; service
                                               may still be healthy -- tech#56, R1889 11:28:48
                                               anchor rc2/gpu_mem=2012 13 min after a clean GEN-OK)
  timeout + GPU idle (model resident)
                          -> service-anomaly  (genuine service trouble face)
  rc=2 non-timeout        -> error
  GPU context unavailable -> gpu-ctx-none
GPU busy threshold util>=80 aligns with the tech#44 defer threshold. The
face lands on the --json line, the human line (non-ok) and every --ledger
row, so window judgments read the discipline straight off the evidence.

tech#56 (R1890): cold-reload face. The 4000MiB residency line sits below
the smallest ollama model we probe (qwen2.5:7b needs ~4.7GB VRAM), so a
timeout row with gpu_mem under the line means no model was resident at
probe time -- the probe itself triggered the cold load and the 60s cap
expired mid-load. That is a scheduling fact (wait for residency), not a
service fault; mislabeling it service-anomaly invites a pointless service
restart. Unreadable mem stays the conservative anomaly face.

tech#77 (R1928): residency pre-check via /api/ps before the generation
  flight (probe-gate order contamination, R1927 anchor: a cold 14b-8k load
  with free 4.2GB < 9GB model crawls in CPU offload, spikes util to 100
  during the load, times out the probe AND pollutes the gpu_window_gate
  samples taken right after -- the R1927/R1928-pre-fix "busy-contended"
  readings were partially the probe's own load, misattributed to the MV
  lane). Three retirements:
  - /api/ps pre-check (status endpoint, never enters the generation
    queue -- same family as the R1877 /api/tags trap, safe under
    saturation): model not resident + free VRAM < model footprint ->
    SKIP the cold flight, report face=not-resident (rc=2, status=
    skipped-not-resident). No wasted cold load, no self-polluted util.
    Model not resident but free >= footprint -> proceed (full-VRAM cold
    load is fast and the flight still means something for tech#41);
    a timeout there with the GPU busy gets face=probe-coldload (our own
    load is the load) instead of busy-contended. ps unreadable -> old
    behavior, no regression. --no-precheck forces the legacy flight.
  - gate ordering discipline lives in the tech#75 判断位正法 (tech.md):
    gpu_window_gate samples FIRST, probe SECOND -- with the pre-check
    skip the probe no longer loads anything, so gate readings carry zero
    probe self-load either way.
  - footprint estimates per model (COLD_SKIP_MODEL_VRAM_MB): only known
    models can trigger the skip; unknown models keep the legacy flight
    (conservative). --cold-skip-free-mb N overrides (0 = never skip).

tech#78 (R1929): consume the /api/ps size_vram reading (R1928 dogfood
  anchor: ps reported the model loaded -- resident -- but generation
  crawled at gpu_mem 1843 << the 9000MB envelope, i.e. the model was
  mostly CPU-offloaded, and the probe still burned its 60s cap to learn
  what the pre-check payload already knew). The pre-check now extracts
  size_vram (bytes -> MiB) for the loaded target model and surfaces it
  plus an advisory offloaded_resident flag (size_vram below half the
  per-model footprint estimate) on the --json line and on --ledger rows
  (columns only when a real /api/ps read succeeded, so ps-unavailable
  rows keep their exact shape). ADVISORY ONLY, deliberately not a skip:
  a loaded model may still generate successfully (just slowly), so the
  probe always flies when resident -- skip semantics untouched. The
  "don't burn" decision belongs to the judgment position (tech#75 正法
  note in tech.md): an offloaded_resident=true reading pre-judges the
  window unusable for the long review flights, and the next rounds may
  cite the prior reading instead of re-flying. rc/face semantics never
  move.

tech#82 (R1934): eviction-aware cold-skip envelope. Gap anchor:
  R1929/R1931/R1932/R1933 -- the gate read GO three rounds running while
  the probe cold-skipped every time: the static free reading (~5.6GB)
  sits below the 14b envelope (9000MB), but ollama auto-evicts the
  resident 7b keep-warm (~4888MiB) LRU-style when a load needs the VRAM,
  making ~10.5GB reachable in practice -- the static arithmetic made the
  dual-GO fire condition structurally unreachable. Two faces, one
  discipline:
  - Advisory counterfactual (always on when ps evidence exists): every
    --json line and ps-ok ledger row carries evictable_mb (summed
    size_vram of the OTHER resident models) and eviction_aware_verdict
    ("fly"/"skip"/None) = what the eviction-aware arithmetic WOULD say.
    This is the dual-reading evidence (real-window side-by-side): one
    skip row shows both verdicts, zero extra GPU cost, no flight either
    way.
  - Opt-in decision change: --eviction-aware switches the actual
    cold-skip test to free + evictable >= envelope. YIELD DISCIPLINE
    (让路律) is encoded by the default-OFF posture: evicting e.g. the
    MV keep-warm model mid-sprint starves that lane, so the judgment
    position passes the flag ONLY when the lanes owning the resident
    models are judged non-active; the active window keeps the skip.
    Entries with a missing/unparseable size_vram contribute 0
    (conservative under-credit: never claim more room than provable).
    Skip/rc/face semantics unchanged when the flag is off.
"""

import argparse
import datetime
import json
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "qwen2.5:14b-8k"
DEFAULT_TIMEOUT = 60
DEFAULT_BASE_URL = "http://localhost:11434"
GEN_PATH = "/api/generate"
DEFAULT_LEDGER = Path(__file__).resolve().parents[2] / "data" / "pipeline" / "ollama-probe-ledger.jsonl"


def build_request_body(model):
    """Build the JSON request body as bytes (no shell-quoting surface)."""
    return json.dumps({"model": model, "prompt": "hi", "stream": False}).encode("utf-8")


def _http_post(base_url, body, timeout):
    """Single injection seam for tests: real call is urllib, never inline PS."""
    req = urllib.request.Request(
        base_url.rstrip("/") + GEN_PATH,
        data=body,
        headers={"Content-Type": "application/json"},
    )
    return urllib.request.urlopen(req, timeout=timeout)


def classify(http_status, detail):
    """Pure classifier: 503 or the saturation message -> 1, else 2."""
    if http_status == 503 or "maximum pending requests" in (detail or ""):
        return 1
    return 2


def _is_timeout(exc):
    """True when the transport exception family is a timeout (tech#55).

    urllib surfaces request timeouts either as a bare TimeoutError/
    socket.timeout, or wrapped as URLError(reason=...). Pure substring
    fallback on the rendered message keeps exotic wrappers honest.
    """
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return True
    reason = getattr(exc, "reason", None)
    if reason is not None:
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return True
        if "timed out" in str(reason).lower():
            return True
    return "timed out" in str(exc).lower()


FACE_GPU_BUSY_UTIL = 80  # tech#44 defer threshold
# tech#56: below this much VRAM in use no probed ollama model can be
# resident (the smallest we run, qwen2.5:7b, needs ~4.7GB), so a timeout
# with gpu_mem under the line means the probe itself started a cold load.
FACE_COLD_RELOAD_VRAM_MB = 4000

PS_PATH = "/api/ps"
PS_TIMEOUT = 10  # status endpoint: fast even under saturation (R1877 family)
# tech#77: full-VRAM footprint estimates for the models we actually probe.
# Below the estimate a cold load spills into CPU offload and crawls (R1927
# anchor: free 4.2GB < 14b-8k ~9GB -> partial-offload slow load, util 100
# during load, probe cap burned mid-load). Unknown models -> no estimate ->
# legacy flight always (conservative).
COLD_SKIP_MODEL_VRAM_MB = {
    "qwen2.5:14b-8k": 9000,
    "qwen2.5:7b": 4700,
}

# tech#78: a loaded model whose ps size_vram sits below this fraction of
# its full-VRAM footprint estimate is substantially CPU-offloaded (R1928
# anchor: resident per ps, gpu_mem 1843 << 9000 envelope -> slow CPU-offload
# generation that burned the probe cap). Advisory only -- generation may
# still succeed, so the probe never skips on it (免烧属判断位面非闸面).
OFFLOADED_RESIDENT_FRACTION = 0.5


def compute_face(result, gpu_ctx, precheck=None):
    """Advisory face reading (tech#55 + tech#56 + tech#77). Never moves rc.

    Faces: ok / not-resident / probe-coldload / slot-wedged /
    saturated-busy / busy-contended / cold-reload / service-anomaly /
    error / gpu-ctx-none (see module docstring). precheck carries the
    tech#77 /api/ps reading (None = no pre-check ran; legacy callers
    unchanged): when it saw the model NOT resident, a timeout with the GPU
    busy is our own cold load in flight -> probe-coldload, not
    busy-contended (R1927 misattribution anchor).
    """
    rc = result.get("rc")
    if rc == 0:
        return "ok"
    # tech#77 pre-check skip: the flight never happened; the scheduling
    # fact (model not resident, cold load would crawl) is the whole face.
    if result.get("status") == "skipped-not-resident":
        return "not-resident"
    util = (gpu_ctx or {}).get("gpu_util", "NONE")
    try:
        busy = int(util) >= FACE_GPU_BUSY_UTIL
    except (TypeError, ValueError):
        return "gpu-ctx-none"
    if rc == 1:
        return "saturated-busy" if busy else "slot-wedged"
    if rc == 2 and result.get("timeout"):
        if busy:
            # tech#77: pre-check evidence says the model was NOT resident ->
            # the busy GPU includes our own cold load (probe-coldload), not
            # just the other lanes (busy-contended). No pre-check evidence ->
            # honest unknown, keep the legacy face.
            if precheck and precheck.get("ps_ok") and not precheck.get("resident"):
                return "probe-coldload"
            return "busy-contended"
        # tech#56 cold-reload face: timeout + GPU idle + no model resident
        # (gpu_mem below the smallest model's footprint) = the probe itself
        # triggered a cold load that outran the request cap; the service can
        # still be healthy (R1889 11:28:48 anchor: rc2/gpu_mem=2012, 13 min
        # after a clean GEN-OK). Unreadable mem -> conservative anomaly.
        mem = (gpu_ctx or {}).get("gpu_mem", "NONE")
        try:
            return "cold-reload" if int(mem) < FACE_COLD_RELOAD_VRAM_MB else "service-anomaly"
        except (TypeError, ValueError):
            return "service-anomaly"
    return "error"


def run_probe(model=DEFAULT_MODEL, timeout=DEFAULT_TIMEOUT, base_url=DEFAULT_BASE_URL):
    """Run one generate probe. Returns a dict result; never raises."""
    result = {
        "rc": 2,
        "status": "error",
        "http_status": None,
        "detail": "",
        "model": model,
        "base_url": base_url,
        "timeout": False,
    }
    body = build_request_body(model)
    try:
        with _http_post(base_url, body, timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
        result["rc"] = 0
        result["status"] = "ok"
        result["detail"] = str(payload.get("done_reason", ""))
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")[:300]
        except Exception:
            detail = ""
        result["http_status"] = exc.code
        result["detail"] = detail.replace("\n", " ")
        result["rc"] = classify(exc.code, detail)
        result["status"] = "saturated" if result["rc"] == 1 else "error"
    except Exception as exc:  # transport-level (connection refused, timeout, ...)
        result["detail"] = repr(exc)[:300]
        result["timeout"] = _is_timeout(exc)
        result["status"] = "error"
    return result


def _human_line(result):
    face = " face=%s" % result["face"] if result.get("face") and result["rc"] != 0 else ""
    if result["status"] == "ok":
        return "GEN-OK done_reason=%s model=%s" % (result["detail"], result["model"])
    if result["status"] == "skipped-not-resident":
        # tech#77: the flight never happened -- say so, never mimic a
        # server signal.
        return "GEN-SKIP not-resident %s%s" % (result.get("detail", ""), face)
    if result["status"] == "saturated":
        return "GEN-SATURATED status=%s detail=%s%s" % (
            result["http_status"], result["detail"], face)
    if result["http_status"] is not None:
        return "GEN-ERROR status=%s detail=%s%s" % (
            result["http_status"], result["detail"], face)
    return "GEN-ERROR transport=%s%s" % (result["detail"], face)


def _nvidia_smi_query():
    """Injection seam for tests: run the nvidia-smi CSV query, return stdout.

    Raises on any failure (binary missing, timeout, bad rc) - the caller
    converts every failure into NONE markers.
    """
    out = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True, timeout=15)
    if out.returncode != 0:
        raise RuntimeError("nvidia-smi rc=%s" % out.returncode)
    return out.stdout


def read_gpu_context():
    """Best-effort GPU context for ledger rows (tech#54).

    Returns {"gpu_util": ..., "gpu_mem": ...} parsed from the first
    nvidia-smi CSV row; any failure -> "NONE" markers. Never raises.
    """
    try:
        text = _nvidia_smi_query()
        first = text.strip().splitlines()[0] if text.strip() else ""
        parts = [p.strip() for p in first.split(",")]
        if len(parts) < 2 or not parts[0] or not parts[1]:
            raise ValueError("unparseable nvidia-smi csv: %r" % first[:80])
        return {"gpu_util": parts[0], "gpu_mem": parts[1]}
    except Exception:
        return {"gpu_util": "NONE", "gpu_mem": "NONE"}


def _nvidia_smi_free_query():
    """Injection seam for tests: nvidia-smi total/used CSV query, or raise."""
    out = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.total,memory.used",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True, timeout=15)
    if out.returncode != 0:
        raise RuntimeError("nvidia-smi rc=%s" % out.returncode)
    return out.stdout


def read_gpu_free_mb():
    """Best-effort free VRAM in MiB (tech#77 pre-check input).

    None on any failure -> the pre-check stays permissive (legacy flight).
    """
    try:
        text = _nvidia_smi_free_query()
        first = text.strip().splitlines()[0] if text.strip() else ""
        parts = [p.strip() for p in first.split(",")]
        if len(parts) < 2 or not parts[0] or not parts[1]:
            raise ValueError("unparseable nvidia-smi csv: %r" % first[:80])
        return int(parts[0]) - int(parts[1])
    except Exception:
        return None


def _http_get_ps(base_url, timeout):
    """Injection seam for tests: real call is urllib GET /api/ps."""
    req = urllib.request.Request(base_url.rstrip("/") + PS_PATH)
    return urllib.request.urlopen(req, timeout=timeout)


def _get_ps(base_url, timeout=PS_TIMEOUT):
    """Best-effort /api/ps read (tech#77).

    Returns (payload, True) on a well-shaped response ({models: [...]});
    (None, False) on any transport error or bad shape -- the pre-check is
    never a gate, a failed read falls back to the legacy generation flight.
    """
    try:
        with _http_get_ps(base_url, timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
        if not isinstance(payload, dict) or not isinstance(payload.get("models"), list):
            return None, False
        return payload, True
    except Exception:
        return None, False


def _entry_matches(entry, model):
    """True when a /api/ps models[] entry is the target model.

    Shared predicate for _ps_find_entry / _ps_other_resident_vram
    (tech#82): ollama lists loaded models under models[] with name/model
    fields; a loaded manifest may carry a re-applied tag suffix
    ("qwen2.5:14b-8k:latest"), so exact match or ":"/"-separated prefix
    both count.
    """
    for key in ("name", "model"):
        val = entry.get(key)
        if val == model or (isinstance(val, str) and
                            (val.startswith(model + ":") or val.startswith(model + "/"))):
            return True
    return False


def _ps_find_entry(payload, model):
    """Return the /api/ps models[] entry matching the target model, or None.

    Shared matcher for _ps_resident / _ps_size_vram. Payload shape is
    pre-validated by _get_ps.
    """
    for entry in payload.get("models", []):
        if not isinstance(entry, dict):
            continue
        if _entry_matches(entry, model):
            return entry
    return None


def _ps_resident(payload, model):
    """True when the /api/ps payload shows the target model loaded."""
    return _ps_find_entry(payload, model) is not None


def _ps_size_vram(payload, model):
    """Best-effort loaded target model's ps size_vram in MiB, or None (tech#78).

    ollama /api/ps reports size_vram in BYTES -- the VRAM-resident portion
    of the loaded model. A resident model with size_vram far below its
    full-VRAM footprint is substantially CPU-offloaded (R1928 anchor) --
    the judgment position (tech#75) consumes this reading to pre-judge an
    unusable window; the probe itself never gates on it. Any missing or
    unparseable value -> None (advisory never fires on doubt).
    """
    entry = _ps_find_entry(payload, model)
    if entry is None:
        return None
    try:
        return int(entry.get("size_vram")) // (1024 * 1024)
    except (TypeError, ValueError):
        return None


def _ps_other_resident_vram(payload, model):
    """Summed size_vram (MiB) of the OTHER resident models (tech#82).

    ollama auto-evicts resident models LRU-style when a load needs their
    VRAM, so a not-resident target's reachable envelope is static free +
    the VRAM the other residents would give back. The target model itself
    (tag-suffix forms included) never counts. Entries with a missing or
    unparseable size_vram contribute 0 -- conservative under-credit: the
    arithmetic must never claim more room than provable. A non-dict
    payload (defensive; callers gate on ps_ok) reads as 0.
    """
    if not isinstance(payload, dict):
        return 0
    total = 0
    for entry in payload.get("models", []):
        if not isinstance(entry, dict) or _entry_matches(entry, model):
            continue
        try:
            total += int(entry.get("size_vram")) // (1024 * 1024)
        except (TypeError, ValueError):
            continue
    return total


def compute_offloaded(resident, size_vram_mib, footprint_mb):
    """Pure advisory: is the loaded model substantially CPU-offloaded? (tech#78)

    True only with ps-confirmed residency, a parseable size_vram and a
    known per-model footprint estimate, and size_vram strictly below
    OFFLOADED_RESIDENT_FRACTION x footprint. Every unreadable piece ->
    False (advisory never fires on doubt). Never a skip input: a loaded
    model may still generate successfully (just slowly).
    """
    if not resident or not footprint_mb or size_vram_mib is None:
        return False
    return size_vram_mib < footprint_mb * OFFLOADED_RESIDENT_FRACTION


def compute_eviction_aware_verdict(resident, ps_ok, free_mb, footprint_mb,
                                   evictable_mb):
    """Pure advisory counterfactual: would eviction-aware arithmetic fly?

    (tech#82 gap anchor: R1929-R1933 four rounds read gate GO x3 while the
    probe cold-skipped every time -- static free (~5.6GB) < the 14b
    envelope, but ollama auto-evicts the 7b keep-warm on load, making
    ~10.5GB reachable). "fly"/"skip" only when the cold-skip context has
    full evidence (ps confirmed the target not resident, a footprint
    estimate exists and free is readable -- the envelope here is the
    per-model ESTIMATE, never the --cold-skip-free-mb override, which
    owns the skip decision only); None on any doubt (advisory never fires
    on doubt, tech#78 pattern). Consumed by the judgment position as the
    second reading of the dual-reading discipline; the actual flight only
    changes under the explicit --eviction-aware opt-in.
    """
    if not ps_ok or resident or not footprint_mb or free_mb is None:
        return None
    effective = free_mb + (evictable_mb or 0)
    return "fly" if effective >= footprint_mb else "skip"


def classify_precheck(resident, ps_ok, free_mb, model_vram_mb,
                      evictable_mb=None, eviction_aware=False):
    """Pure decision: run the cold generation flight or skip it (tech#77).

    Order of permissiveness (any doubt -> run the legacy flight, the probe
    itself stays the ground truth):
      ps unreadable -> run (no evidence either way)
      model resident -> run (no cold load exists; faces stay meaningful)
      no footprint estimate for this model -> run (cannot pre-judge)
      free VRAM unreadable -> run (tech#56 cold-reload face catches it
        after the fact)
      not resident + free < footprint -> SKIP: the cold load would spill
        into CPU offload and crawl, burn the request cap and self-pollute
        util (R1927 anchor); report the scheduling fact instead.
      not resident + free >= footprint -> run (full-VRAM cold load is
        fast; a busy timeout there is our own load -> probe-coldload face).

    tech#82: eviction_aware=True switches the envelope test to
    free + evictable (the VRAM ollama reclaims by auto-evicting the OTHER
    resident models on load). Opt-in by the --eviction-aware flag only --
    YIELD DISCIPLINE: evicting e.g. the MV keep-warm model mid-sprint
    starves that lane, so the judgment position passes the flag only when
    the lanes owning those residents are judged non-active; default OFF
    keeps the active-window skip and byte-identical reasons. An evictable
    sum of 0/None under the flag degenerates to the legacy arithmetic
    (the reason still names the +evictable term).

    Returns (proceed: bool, reason: str).
    """
    if not ps_ok:
        return True, "ps-unavailable"
    if resident:
        return True, "resident"
    if not model_vram_mb:
        return True, "no-estimate"
    if free_mb is None:
        return True, "free-unknown"
    credit = evictable_mb or 0
    if eviction_aware:
        effective = free_mb + credit
        if effective < model_vram_mb:
            return False, "cold-skip free=%dMB+evictable=%dMB<model=%dMB" % (
                free_mb, credit, model_vram_mb)
        return True, "cold-run free=%dMB+evictable=%dMB>=model=%dMB" % (
            free_mb, credit, model_vram_mb)
    if free_mb < model_vram_mb:
        return False, "cold-skip free=%dMB<model=%dMB" % (free_mb, model_vram_mb)
    return True, "cold-run free=%dMB>=model=%dMB" % (free_mb, model_vram_mb)


def append_ledger_row(path, result, gpu_ctx=None, precheck=None):
    """Best-effort JSONL append (tech#52): one row per real probe flight.

    Rows carry gpu_util/gpu_mem context columns (tech#54, R1883-R1885
    wedged-slot diagnosis gap: saturation + zero GPU activity is only
    visible when the row records GPU state at probe time) and the advisory
    face column (tech#55, tech#77 not-resident/probe-coldload) so window
    judgments read the face discipline straight off the ledger row.

    gpu_ctx: pre-read context reused when the caller already has it (one
    nvidia-smi per probe flight, not two); None -> read here (tech#52
    call surface). precheck: tech#77 /api/ps evidence for the
    probe-coldload face (None = legacy callers, faces unchanged). WARN on
    failure, never raises, never changes the exit code.
    """
    gpu = gpu_ctx if gpu_ctx is not None else read_gpu_context()
    row = {
        "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rc": result["rc"],
        "status": result["status"],
        "http_status": result["http_status"],
        "model": result["model"],
    }
    row.update(gpu)
    row["face"] = compute_face(result, gpu, precheck)
    # tech#78: ps evidence columns -- only when a real /api/ps read
    # succeeded, so ps-unavailable rows keep their exact shape (the
    # ledger contract test locks that shape byte-for-byte).
    if precheck is not None and precheck.get("ps_ok"):
        row["ps_size_vram"] = precheck.get("size_vram")
        row["offloaded_resident"] = bool(precheck.get("offloaded"))
        # tech#82: dual-reading columns on ps-ok rows only (ps-unavailable
        # rows keep their exact-shape contract byte-stable).
        row["evictable_mb"] = precheck.get("evictable_mb")
        row["eviction_aware_verdict"] = precheck.get("eviction_aware_verdict")
    try:
        ledger_path = Path(path)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    except OSError as exc:
        sys.stderr.write("WARN ollama-probe-ledger append failed: %s\n" % exc)


def build_parser(argv=None):
    parser = argparse.ArgumentParser(
        description="Ollama generation probe (recovery criterion, exit 0/1/2).")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="model to probe (default: %s)" % DEFAULT_MODEL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="per-request timeout seconds (default: %d)" % DEFAULT_TIMEOUT)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help="ollama base url (default: %s)" % DEFAULT_BASE_URL)
    parser.add_argument("--json", action="store_true",
                        help="emit one machine-readable JSON line")
    parser.add_argument("--ledger", nargs="?", const=str(DEFAULT_LEDGER), default=None,
                        help="append one JSONL row per probe flight to this path "
                             "(tech#52; bare --ledger = default %s)" % DEFAULT_LEDGER)
    parser.add_argument("--no-precheck", action="store_true",
                        help="skip the tech#77 /api/ps residency pre-check and always "
                             "run the legacy generation flight")
    parser.add_argument("--cold-skip-free-mb", type=int, default=None,
                        help="tech#77 cold-skip threshold in MiB free VRAM (default: "
                             "per-model estimate for known models, never skip otherwise; "
                             "0 = never skip)")
    parser.add_argument("--eviction-aware", action="store_true",
                        help="tech#82 eviction-aware cold-skip arithmetic: credit the "
                             "summed size_vram of the OTHER ollama-resident models "
                             "(auto-evicted on load) into the free envelope before the "
                             "cold-skip test. YIELD DISCIPLINE, opt-in by design: "
                             "evicting e.g. the MV keep-warm model mid-sprint starves "
                             "that lane -- pass this only when the lanes owning the "
                             "resident models are judged non-active; default off keeps "
                             "the active-window skip (the advisory counterfactual "
                             "columns ride every ps-ok row either way)")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.timeout <= 0:
        print("GEN-ERROR bad-timeout=%s" % args.timeout)
        return 2
    # tech#77 pre-check: /api/ps residency read before any generation
    # flight. Never a gate -- any unreadable piece falls back to the
    # legacy flight. ps_ok=False also feeds the probe-coldload face as
    # "no evidence" (legacy faces unchanged).
    precheck = None
    if not args.no_precheck:
        payload, ps_ok = _get_ps(args.base_url)
        resident = _ps_resident(payload, args.model) if ps_ok else False
        # tech#78: consume the size_vram evidence while the payload is in
        # hand (R1928 anchor: the pre-check knew the model was loaded but
        # CPU-offloaded and threw the reading away). Advisory uses the
        # per-model footprint estimate, never the --cold-skip-free-mb
        # override (that knob owns the skip decision only).
        size_vram = _ps_size_vram(payload, args.model) if ps_ok else None
        # free VRAM only feeds the cold-skip decision, which only exists
        # for a ps-confirmed non-resident model -- read it lazily so the
        # ps-unavailable path costs no extra nvidia-smi call.
        free_mb = read_gpu_free_mb() if (ps_ok and not resident) else None
        # tech#82: evictable VRAM credit (summed size_vram of the OTHER
        # resident models) -- payload already in hand, one dict walk.
        # Feeds the advisory counterfactual always; the decision only
        # under --eviction-aware (yield discipline at the judgment
        # position: the flag is passed only in judged-non-active windows).
        evictable = _ps_other_resident_vram(payload, args.model) if ps_ok else None
        if args.cold_skip_free_mb is not None:
            footprint = args.cold_skip_free_mb
        else:
            footprint = COLD_SKIP_MODEL_VRAM_MB.get(args.model, 0)
        estimate = COLD_SKIP_MODEL_VRAM_MB.get(args.model, 0)
        proceed, reason = classify_precheck(
            resident, ps_ok, free_mb, footprint,
            evictable_mb=evictable, eviction_aware=args.eviction_aware)
        precheck = {"ps_ok": ps_ok, "resident": resident,
                    "size_vram": size_vram,
                    "offloaded": compute_offloaded(resident, size_vram, estimate),
                    "free_mb": free_mb, "reason": reason,
                    "evictable_mb": evictable,
                    "eviction_aware_verdict": compute_eviction_aware_verdict(
                        resident, ps_ok, free_mb, estimate, evictable)}
        if not proceed:
            result = {
                "rc": 2,
                "status": "skipped-not-resident",
                "http_status": None,
                "detail": reason,
                "model": args.model,
                "base_url": args.base_url,
                "timeout": False,
                "skipped": True,
                "gpu_free_mb": free_mb,
                "precheck": reason,
            }
            gpu_ctx = read_gpu_context()
            result["face"] = compute_face(result, gpu_ctx, precheck)
            if args.ledger:
                append_ledger_row(args.ledger, result, gpu_ctx, precheck)
            if args.json:
                result.update(gpu_ctx)
                # tech#78: schema-uniform evidence columns (target not
                # loaded here, so the reading is honestly null).
                result["ps_size_vram"] = precheck.get("size_vram")
                result["offloaded_resident"] = precheck.get("offloaded", False)
                # tech#82: dual-reading columns -- the legacy skip verdict
                # above plus what eviction-aware arithmetic would say.
                result["evictable_mb"] = precheck.get("evictable_mb")
                result["eviction_aware_verdict"] = precheck.get(
                    "eviction_aware_verdict")
                result["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(json.dumps(result, ensure_ascii=True))
            else:
                print(_human_line(result))
            return result["rc"]
    result = run_probe(model=args.model, timeout=args.timeout, base_url=args.base_url)
    gpu_ctx = read_gpu_context()
    result["face"] = compute_face(result, gpu_ctx, precheck)
    if args.ledger:
        append_ledger_row(args.ledger, result, gpu_ctx, precheck)
    if args.json:
        result.update(gpu_ctx)
        if precheck is not None:
            result["precheck"] = precheck["reason"]
            # tech#78 resident evidence face: consumed by the tech#75
            # judgment position to pre-judge unusable windows (advisory
            # only -- flight/rc/face semantics untouched above).
            result["ps_size_vram"] = precheck.get("size_vram")
            result["offloaded_resident"] = precheck.get("offloaded", False)
            # tech#82: dual-reading columns, schema-uniform (honestly null
            # when the ps read itself failed).
            result["evictable_mb"] = precheck.get("evictable_mb")
            result["eviction_aware_verdict"] = precheck.get(
                "eviction_aware_verdict")
        result["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(_human_line(result))
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
