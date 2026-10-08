"""R1769 AIHOT 9b reasoning-burn fix: add LLM_EXTRA_JSON think-off + restart worker.

Evidence chain (R1769):
- qwen3.5:9b receipts 11/11 failed: reasoning model burns output budget
  (finish_reason=length) before emitting JSON -> "No JSON object in model output".
- Probe r1769_think_probe.py: {"think": false} -> finish=stop, clean JSON, 4.6s.
  enable_thinking ignored by ollama 0.40.1; baseline reproduces the burn.
Ops reds honored: .env rewritten via python (R1710 PS5.1 Set-Content line-swallow),
worker started python-direct DETACHED|CREATE_NEW_PROCESS_GROUP (R1768 bat-lock bypass).
"""
import os
import subprocess
import sys

ENV_PATH = r"data/assets/aihot-poc/AIHOT/.env"
NEW_LINE = 'LLM_EXTRA_JSON={"think": false}\n'


def rewrite_env():
    with open(ENV_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    out, seen = [], False
    for ln in lines:
        if ln.startswith("LLM_EXTRA_JSON="):
            out.append(NEW_LINE)
            seen = True
        else:
            out.append(ln)
    if not seen:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        out.append(NEW_LINE)
    with open(ENV_PATH, "w", encoding="utf-8", newline="") as f:
        f.writelines(out)
    # verify readback
    with open(ENV_PATH, encoding="utf-8") as f:
        txt = f.read()
    assert 'LLM_EXTRA_JSON={"think": false}' in txt, "env rewrite failed"
    assert "LLM_MODEL=qwen3.5:9b" in txt, "model line clobbered"
    assert "COLLECT_ENABLED=true" in txt, "collect flag clobbered"
    print("[env] OK LLM_EXTRA_JSON={\"think\": false} in place; model=9b; collect=true")


def stop_old_worker():
    r = subprocess.run(
        ["taskkill", "/PID", "664", "/T", "/F"], capture_output=True, text=True)
    print(f"[taskkill 664] rc={r.returncode} out={(r.stdout or r.stderr).strip()[:120]}")


def start_worker():
    cwd = os.path.abspath(r"data/assets/aihot-poc/AIHOT/apps/worker")
    log = os.path.abspath(r"data/assets/aihot-poc/worker2.log")
    env = dict(os.environ)
    env["NODE_ENV"] = "production"
    # R1768 method: node direct, env-file flag, detached, append-mode log handles.
    cmd = ["node", "--env-file-if-exists=../../.env", "src/main.ts"]
    with open(log, "ab") as lf:
        p = subprocess.Popen(
            cmd, cwd=cwd, env=env, stdout=lf, stderr=lf,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
            close_fds=True,
        )
    print(f"[worker] started pid={p.pid} log={log}")
    return p.pid


if __name__ == "__main__":
    rewrite_env()
    stop_old_worker()
    pid = start_worker()
    sys.exit(0)
