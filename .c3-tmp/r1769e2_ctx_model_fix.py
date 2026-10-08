"""R1769e (byte-capture redo): verify derived model, point .env, restart worker.

PS5.1 GBK reader-thread crash ate the first run's output (r1769e step 1 may have
succeeded); byte capture + manual utf-8 decode per known ops-red family.
"""
import os
import subprocess


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    out = (r.stdout or b"").decode("utf-8", "replace").strip()
    err = (r.stderr or b"").decode("utf-8", "replace").strip()
    return r.returncode, out, err


ENV_PATH = r"data/assets/aihot-poc/AIHOT/.env"

rc, out, err = run(["ollama", "list"])
print(f"[list] rc={rc}")
for ln in out.splitlines():
    if "qwen3.5" in ln:
        print("  " + ln)
if "qwen3.5:9b-16k" not in out:
    rc, out, err = run(["ollama", "create", "qwen3.5:9b-16k", "-f", r".c3-tmp/r1769_modelfile.txt"])
    print(f"[create] rc={rc} out={out[:200]} err={err[:200]}")
    if rc != 0:
        raise SystemExit(1)
else:
    print("[create] already present")

lines = open(ENV_PATH, encoding="utf-8").readlines()
outl = ["LLM_MODEL=qwen3.5:9b-16k\n" if ln.startswith("LLM_MODEL=") else ln for ln in lines]
with open(ENV_PATH, "w", encoding="utf-8", newline="") as f:
    f.writelines(outl)
txt = open(ENV_PATH, encoding="utf-8").read()
assert "LLM_MODEL=qwen3.5:9b-16k" in txt and "LLM_REASONING_TOKENS=4096" in txt
print("[env] OK model=qwen3.5:9b-16k headroom=4096")

# kill current worker 69204 if still alive, start fresh
run(["taskkill", "/PID", "69204", "/T", "/F"])
cwd = os.path.abspath(r"data/assets/aihot-poc/AIHOT/apps/worker")
log = os.path.abspath(r"data/assets/aihot-poc/worker2.log")
env = dict(os.environ)
env["NODE_ENV"] = "production"
with open(log, "ab") as lf:
    p = subprocess.Popen(
        ["node", "--env-file-if-exists=../../.env", "src/main.ts"],
        cwd=cwd, env=env, stdout=lf, stderr=lf,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        close_fds=True)
print(f"[worker] started pid={p.pid}")
