# -*- coding: utf-8 -*-
"""S1 gate call for BS-001 douyin quick-cut piece (F-006 chain start).

Same channel as .bs005-tmp/s1_call.py (R191/R192 proven): reuses call_expert
registry/build_prompt/call_model/verdict-archive/ledger-row verbatim, only
raises subprocess timeout to 1500s. Run detached (Start-Process) so the 5-min
no-output guard does not cancel it. Result -> .bs001-dy-tmp/s1-result.json.
Material = s1-review-material-douyin.md (v11-trim 12 beats reused verbatim,
F-001 finished-goods script; this gate is the formal S1 v1.5 pass for the
douyin platform piece). ASCII source; Chinese stays in data files.
"""
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
    REPO / "data" / "sources" / "bs001" / "s1-review-material-douyin.md")
RESULT = REPO / ".bs001-dy-tmp" / "s1-result.json"


def main():
    _, experts = ce.load_registry()
    ex = experts[EXPERT_ID]
    prompt = ce.build_prompt(
        (REPO / ex["prompt_file"]).read_text(encoding="utf-8"),
        Path(MATERIAL).read_text(encoding="utf-8"))
    try:
        code, out = ce.call_model(ex["model"], prompt, timeout=1500)
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
        note = "full text=expert-verdicts/%s | %s (1500s wrapper: S1 v1.5 gate, BS-001 douyin F-006 reused v11-trim beats)" % (vname, first_line)
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
