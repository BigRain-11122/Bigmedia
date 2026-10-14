#!/usr/bin/env python3
"""SC-005-07 S1 staged launcher (CPU LANE) - F-180 fire-queue head consumption.

GPU-lane sibling s1_call.py (R2008 prestage, tech#122 launcher-local
hardening) stays untouched; THIS file is the S1 leg of the ADOPTED
CPU-lane dispatch design (tech#169, R2251: E4/S1 seat calls feasible on
CPU - compact 56.6s + extrapolated 110-180s << 1500s window, zero VRAM
increment; tech#166: seat qwen2.5:14b revived per CEO-order model
restoration ruling, ollama list 10-14 ~19:3x). CPU lane laws
(O-20261013-2215 CPU face 24/7 + CEO 10% CPU margin): zero GPU touch
(num_gpu=0 - the assertion IS the flight), so no GPU preflight, no
relief, no seat-probe races vs the MV assembly window (ffmpeg lane,
zero conflict). Liveness = /api/tags 2s probe (dead server -> rc 3,
never burn the 1500s cap on a corpse).
Assembly = call_expert.build_prompt parity: prompt.rstrip() +
"\\n\\n\\u6750\\u6599\\n" - material verbatim (R2007 preload, R197 tail
format anchor in file). Seat model + prompt file from
data/experts/registry.json (never hardcoded, s1_call.py doctrine).
Verdict -> s1-cpu-result.json in THIS dir. tech#173 auto-ledger: the
verdict self-logs its expert-calls row + full-verdict archive at
landing time (read-back round no longer backfills by hand).
rc: 0 = result json written (incl TIMEOUT/EMPTY verdicts) | 3 =
transport/liveness error, NO result file (re-dispatch next window).
"""
import io
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE = <repo>/data/storylines/audio/sc005-07-v1-tmp -> repo root is 4 levels up (parents[4], s1_call.py parity)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REGISTRY = os.path.join(ROOT, "data", "experts", "registry.json")
TIMEOUT = 1500
LANE = "cpu"
CPU_THREADS = 4      # CEO 10% CPU margin law (O-20261013-2215)
TAGS_URL = "http://localhost:11434/api/tags"
GENERATE_URL = "http://localhost:11434/api/generate"
MATERIAL_REL = "data/storylines/audio/SC-005-07-v1-s1-material.md"
EXPERT_ID = "S1-script"
FALLBACK_PROMPT = os.path.join("data", "experts", "prompts", "S1-script.txt")

# ---------- liveness (2s cap) ----------
try:
    urllib.request.urlopen(TAGS_URL, timeout=2).read()
except Exception as exc:
    print("LIVENESS-FAIL %s" % exc, flush=True)
    raise SystemExit(3)

# ---------- seat + prompt from registry (never hardcoded) ----------
reg = json.loads(io.open(REGISTRY, encoding="utf-8").read())
seat = str(reg.get("model", "")) or "qwen2.5:14b"
prompt_file = None
role_dept = "S1 编剧官（内容生产部）"
entries = reg.get("experts") or reg.get("roster") or []
for e in entries:
    if str(e.get("id", "")) == EXPERT_ID:
        if e.get("model"):
            seat = str(e["model"])
        prompt_file = str(e.get("prompt_file") or "") or None
        role_dept = "%s（%s）" % (e.get("role", "S1 编剧官"),
                                  e.get("dept", "内容生产部"))
        break
if not prompt_file:
    prompt_file = FALLBACK_PROMPT
prompt_path = os.path.join(ROOT, prompt_file)
material_path = os.path.join(ROOT, MATERIAL_REL)
if not (os.path.isfile(prompt_path) and os.path.isfile(material_path)):
    print("FAIL input missing: prompt=%s material=%s" % (prompt_path, material_path), flush=True)
    raise SystemExit(3)

prompt_text = io.open(prompt_path, encoding="utf-8").read()
material_text = io.open(material_path, encoding="utf-8").read()
# call_expert.build_prompt parity (verified against src/call_expert.py L106-110)
prompt = (prompt_text.rstrip() +
          "\n\n===== \u6750\u6599 =====\n" +
          material_text.strip() + "\n")

result = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "model": seat,
          "material": MATERIAL_REL, "lane": LANE, "expert": EXPERT_ID}
payload = json.dumps({"model": seat, "prompt": prompt, "stream": False,
                      "options": {"num_gpu": 0,
                                  "num_thread": CPU_THREADS}}).encode("utf-8")
request = urllib.request.Request(GENERATE_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(request, timeout=TIMEOUT) as resp:
        body = json.loads(resp.read().decode("utf-8", "replace"))
    result["verdict"] = (body.get("response") or "").strip() or "EMPTY-RESPONSE"
except Exception as exc:
    text = "%s: %s" % (type(exc).__name__, exc)
    if "timed out" in text.lower() or "timeout" in text.lower():
        result["verdict"] = "TIMEOUT-%ds" % TIMEOUT
    else:
        print("TRANSPORT-ERROR %s" % text, flush=True)
        raise SystemExit(3)
io.open(os.path.join(HERE, "s1-cpu-result.json"), "w", encoding="utf-8").write(
    json.dumps(result, ensure_ascii=False, indent=2))

# ---------- tech#173 auto-ledger: verdict self-logs its expert-calls
# row + full-verdict archive at landing time (aligns with call_expert
# audit behavior; read-back round no longer backfills by hand). Best
# effort: write failure WARNs, never changes verdict/rc.
def _auto_ledger():
    try:
        stamp = time.strftime("%Y-%m-%d %H:%M")
        vname = time.strftime("%Y%m%d-%H%M%S") + "-" + EXPERT_ID + ".md"
        vdir = os.path.join(ROOT, "docs", "reviews", "expert-verdicts")
        if not os.path.isdir(vdir):
            os.makedirs(vdir)
        io.open(os.path.join(vdir, vname), "w", encoding="utf-8").write(
            "# %s - %s结论全文\n\n> 时间=%s · 模型=%s · 材料=%s\n"
            "> 机制=s1_call_cpu.py auto-ledger（tech#173·对齐 "
            "call_expert.py O-20260924-1033·本件为结论存档·台账行="
            "expert-calls.md）\n\n%s\n"
            % (EXPERT_ID, role_dept, stamp, seat, MATERIAL_REL,
               str(result["verdict"]).strip() or "-"))
        first_line = (str(result["verdict"]).strip() or "-").splitlines()[0]
        note = "全文=expert-verdicts/%s ｜ %s" % (vname, first_line)
        note = note.replace("|", "/").replace("\n", " ")[:160]
        row = "| %s | %s | %s | %s | 0 | %s |\n" % (
            stamp, EXPERT_ID, role_dept, MATERIAL_REL, note)
        with io.open(os.path.join(ROOT, "docs", "reviews",
                                  "expert-calls.md"), "a",
                     encoding="utf-8") as fh:
            fh.write(row)
        print("LEDGER-ROW %s (tech#173 auto-ledger)" % EXPERT_ID, flush=True)
    except OSError as exc:
        print("WARN auto-ledger failed: %s (verdict kept)" % exc, flush=True)

def _auto_stage_result():
    # tech#174 auto-stage (generator AUTO_LEDGER_BLOCK parity): the
    # raw verdict json self-stages into the repo index the moment it
    # lands (R2261 9-round residue lesson); best-effort -- an index
    # contention WARNs, verdict/rc untouched (tech#173 contract).
    raw = os.path.join(HERE, "s1-cpu-result.json")
    if not os.path.isfile(raw):
        return
    try:
        import subprocess
        proc = subprocess.run(
            ["git", "add", "--", raw], cwd=ROOT, timeout=30,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode == 0:
            print("STAGED-RESULT %s (tech#174 auto-stage)"
                  % os.path.relpath(raw, ROOT), flush=True)
        else:
            print("WARN auto-stage failed rc=%d: %s (verdict kept)"
                  % (proc.returncode,
                     proc.stdout.decode("utf-8", "replace").strip()),
                  flush=True)
    except Exception as exc:
        print("WARN auto-stage failed: %s (verdict kept)" % exc, flush=True)

_auto_ledger()
_auto_stage_result()
print("DONE" if not str(result["verdict"]).startswith("TIMEOUT") else "TIMEOUT")
