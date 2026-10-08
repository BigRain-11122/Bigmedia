"""R1769b: add LLM_REASONING_TOKENS=4096 headroom (the error-prescribed fix).

Evidence: worker 52620 had LLM_EXTRA_JSON think:false correctly loaded and sent
(node env-file parse verified), yet real-article prefilter still burned
completion 512/512 on reasoning (content="", reasoning="Thinking...") ->
ollama /v1 does not reliably short-circuit thinking for qwen3.5:9b.
llm.ts: maxTokens = max(opts.maxTokens, 512) + (spec.reasoningTokens ?? 0)
-> LLM_REASONING_TOKENS=4096 gives every call reasoning headroom; JSON lands
in content after thinking completes (ollama splits reasoning/content fields).
"""
import os
import subprocess

ENV_PATH = r"data/assets/aihot-poc/AIHOT/.env"
NEW_LINE = "LLM_REASONING_TOKENS=4096\n"


def rewrite_env():
    with open(ENV_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    out, seen = [], False
    for ln in lines:
        if ln.startswith("LLM_REASONING_TOKENS="):
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
    txt = open(ENV_PATH, encoding="utf-8").read()
    assert "LLM_REASONING_TOKENS=4096" in txt
    assert 'LLM_EXTRA_JSON={"think": false}' in txt
    assert "LLM_MODEL=qwen3.5:9b" in txt
    print("[env] OK reasoning headroom 4096 + think:false + model 9b")


def main():
    rewrite_env()
    r = subprocess.run(["taskkill", "/PID", "52620", "/T", "/F"],
                       capture_output=True, text=True)
    print(f"[taskkill 52620] rc={r.returncode} {(r.stdout or r.stderr).strip()[:100]}")
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
