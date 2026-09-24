# -*- coding: utf-8 -*-
"""S1 gate call for BS-001-DD bilibili deep-dive (wrapper around call_expert).

Same channel as .bs005-tmp/s1_call.py (R176/R182/R191 proven): reuses
call_expert registry/build_prompt/call_model/verdict-archive/ledger-row
verbatim. Timeout raised to 3600s: the deep-dive material is ~6x longer than
the 60s-piece materials and bm-a GPU is under full load (P-20260925-01), so
the qwen2.5:14b verdict may exceed the 1500s window. Run detached
(Start-Process) so the 5-min no-output guard does not cancel it.
Result -> .bs001-dd-tmp/s1-result.json (next round reads it async).
ASCII source; Chinese stays in data files (encoding law)."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
import call_expert as ce

EXPERT_ID = "S1-script"
MATERIAL = sys.argv[1] if len(sys.argv) > 1 else str(
    REPO / "data" / "sources" / "bs001-dd" / "s1-review-material.md")
RESULT = REPO / ".bs001-dd-tmp" / "s1-result.json"


def main():
    _, experts = ce.load_registry()
    ex = experts[EXPERT_ID]
    prompt = ce.build_prompt(
        (REPO / ex["prompt_file"]).read_text(encoding="utf-8"),
        Path(MATERIAL).read_text(encoding="utf-8"))
    try:
        code, out = ce.call_model(ex["model"], prompt, timeout=3600)
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
        note = "full text=expert-verdicts/%s | %s (3600s wrapper: S1 deep-dive gate)" % (vname, first_line)
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
