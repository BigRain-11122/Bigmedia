# -*- coding: utf-8 -*-
"""On-call departmental expert invoker (O-20260924-1033-bm-a).

Every department keeps dedicated expert roles (functional identities,
org-structure S3 "not personified" law). This tool makes "ready to be
called at any time" literal:

    python src/call_expert.py --expert hot-intel --material data/intel/daily/2026-09-24.md [--timeout S] [--gpu-guard]

Registry = data/experts/registry.json (id/dept/role/prompt_file/model).
Prompts live as UTF-8 data files (encoding rule); the model is the local
Ollama (default qwen2.5:14b - zero API, zero token). The call goes through
subprocess stdin in UTF-8, which also fixes the PS5.1 GBK pipe garbling
that hit raw `ollama run` piping on 2026-09-23.

Every call is appended to docs/reviews/expert-calls.md (audit trail).

ASCII rule: this source is pure ASCII; Chinese lives in the registry /
prompt / material data files.

Exit codes: 0 ok; 2 bad args / unknown expert / missing files;
            3 ollama call failed; 4 ledger append failed (verdict kept);
            5 GPU guard defer (only with --gpu-guard; advisory, see
              read_gpu_headroom / defer_decision).

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
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "data" / "experts" / "registry.json"
LEDGER = REPO / "docs" / "reviews" / "expert-calls.md"
VERDICT_DIR = REPO / "docs" / "reviews" / "expert-verdicts"
DEFER_LEDGER = REPO / "data" / "pipeline" / "gpu-guard-defer-ledger.jsonl"
DEFAULT_TIMEOUT = 300
# GPU pre-flight guard thresholds (tech#44): defer when the card is
# clearly occupied by another lane (training/render window) or when
# free VRAM is too tight for a local LLM seat.
GPU_DEFER_UTIL_PCT = 80
GPU_DEFER_FREE_MB = 2048
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


def call_model(model, prompt, timeout=DEFAULT_TIMEOUT):
    """Run local ollama with UTF-8 stdin/stdout (pure subprocess wrapper).
    Returns (returncode, stdout_text). Chinese-safe on PS5.1."""
    p = subprocess.run(["ollama", "run", model],
                       input=prompt.encode("utf-8"),
                       capture_output=True, timeout=timeout)
    out = _ANSI_RE.sub("", p.stdout.decode("utf-8", "replace"))
    out = _SPINNER_RE.sub("", out)
    return p.returncode, out


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
    gpu_guard = gpu_force = False
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
        elif argv[i] == "--gpu-force":
            gpu_force = True
        i += 1
    if not (expert_id and material):
        print("usage: call_expert.py --expert ID --material FILE "
              "[--timeout S] [--gpu-guard] [--gpu-force]")
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
                return 5
        elif reading is None:
            print("WARN gpu probe unavailable; proceeding (advisory guard)")
        else:
            print("GPU-OK util=%d%% free=%dMB"
                  % (reading["util_pct"], reading["free_mb"]))
    prompt = build_prompt(prompt_path.read_text(encoding="utf-8"),
                          material_path.read_text(encoding="utf-8"))
    try:
        code, out = call_model(ex["model"], prompt, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        print("FAIL ollama timeout (%ds)" % timeout_s)
        code, out = 3, ""
    if code != 0:
        print("FAIL ollama exit %d" % code)
        print(out[-500:])
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
        if not LEDGER.exists():
            LEDGER.write_text(
                "# 专职专家调用台账（Expert Calls Ledger）\n\n"
                "> 机制=`docs/expert-roster.md`（O-20260924-1033-bm-a）。"
                "行级追加禁改写；每次 call_expert.py 真调自动落一行"
                "（结论全文=expert-verdicts/ 目录·本表只存首行）。\n\n"
                "| 时间 | 专家 | 身份（部门） | 材料 | 退出 | 结论首行 |\n"
                "|---|---|---|---|---|---|\n", encoding="utf-8")
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(row)
    except OSError as e:
        print("WARN ledger append failed: %s (verdict kept above)" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
