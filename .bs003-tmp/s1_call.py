# -*- coding: utf-8 -*-
"""S1 gate call for BS-003 (wrapper around call_expert internals).

Why: call_expert.main() hard-binds a 300s subprocess timeout; on this
machine a cold 9GB load plus long-prompt eval exceeds it (R175 x2 FAIL,
R176 x1 auto-cancel). This wrapper reuses call_expert registry/prompt/
verdict-archive/ledger-row code verbatim, and only raises the subprocess
timeout to 1500s and detaches the run from the shell 5-min no-output
guard (background invocation + result file). Same ollama CLI channel as
call_model. Result -> .bs003-tmp/s1-result.json. ASCII source; Chinese
stays in data files (encoding law)."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
import call_expert as ce

EXPERT_ID = "S1-script"
MATERIAL = sys.argv[1]
RESULT = REPO / ".bs003-tmp" / "s1-result.json"


def main():
    _, experts = ce.load_registry()
    ex = experts[EXPERT_ID]
    prompt = ce.build_prompt(
        (REPO / ex["prompt_file"]).read_text(encoding="utf-8"),
        Path(MATERIAL).read_text(encoding="utf-8"))
    try:
        p = subprocess.run(["ollama", "run", ex["model"]],
                           input=prompt.encode("utf-8"),
                           capture_output=True, timeout=1500)
        out = p.stdout.decode("utf-8", "replace")
        code = p.returncode
    except subprocess.TimeoutExpired:
        code, out = 3, ""
    result = {"exit": code, "expert": EXPERT_ID, "material": MATERIAL,
              "verdict": out.strip()}
    if code == 0 and out.strip():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        vname = ce.verdict_file_name(EXPERT_ID, stamp)
        ce.save_verdict(ce.VERDICT_DIR, vname, EXPERT_ID, ex["role"],
                        ex["dept"], ex["model"], MATERIAL, out.strip())
        first_line = out.strip().splitlines()[0][:120]
        note = "full text=expert-verdicts/%s | %s (1500s wrapper: cold-load fix)" % (vname, first_line)
        row = ce.ledger_row(EXPERT_ID, ex["role"], ex["dept"], MATERIAL,
                            0, note)
        with ce.LEDGER.open("a", encoding="utf-8") as f:
            f.write(row)
        result["verdict_file"] = str(ce.VERDICT_DIR / vname)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    print(json.dumps({"exit": code}))


if __name__ == "__main__":
    main()
