"""R1769e: derive qwen3.5:9b-16k (num_ctx 16384) + point pipeline at it + restart worker.

Evidence chain (R1769):
- Receipt 21:07:55: maxTokens=4608 headroom applied, yet total_tokens=4096
  (prompt 1855 + completion 2241) -> truncated by ollama CONTEXT=4096 mid-reasoning.
- r1769d probe: num_ctx in /v1 body ignored (both runs truncate at total 4096).
- Fix: model-level Modelfile PARAMETER num_ctx 16384 (per-model, no serve restart,
  no impact on other lanes using the shared ollama instance).
"""
import os
import subprocess

MODELFILE = r".c3-tmp/r1769_modelfile.txt"
ENV_PATH = r"data/assets/aihot-poc/AIHOT/.env"


def main() -> None:
    with open(MODELFILE, "w", encoding="ascii") as f:
        f.write("FROM qwen3.5:9b\nPARAMETER num_ctx 16384\n")
    r = subprocess.run(["ollama", "create", "qwen3.5:9b-16k", "-f", MODELFILE],
                        capture_output=True, text=True)
    print(f"[create] rc={r.returncode} out={(r.stdout or r.stderr).strip()[:200]}")
    if r.returncode != 0:
        raise SystemExit(1)

    lines = open(ENV_PATH, encoding="utf-8").readlines()
    out = []
    for ln in lines:
        out.append("LLM_MODEL=qwen3.5:9b-16k\n" if ln.startswith("LLM_MODEL=") else ln)
    with open(ENV_PATH, "w", encoding="utf-8", newline="") as f:
        f.writelines(out)
    txt = open(ENV_PATH, encoding="utf-8").read()
    assert "LLM_MODEL=qwen3.5:9b-16k" in txt
    assert "LLM_REASONING_TOKENS=4096" in txt
    print("[env] OK LLM_MODEL=qwen3.5:9b-16k (+headroom 4096 kept)")

    r = subprocess.run(["taskkill", "/PID", "69204", "/T", "/F"], capture_output=True, text=True)
    print(f"[taskkill 69204] rc={r.returncode} {(r.stdout or r.stderr).strip()[:100]}")
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


if __name__ == "__main__":
    main()
