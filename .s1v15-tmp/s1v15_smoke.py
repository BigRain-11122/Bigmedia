# -*- coding: utf-8 -*-
"""S1 v1.5 prompt smoke validation (backlog #24, mechanism PoC).

Reuses call_expert internals verbatim (same channel as .bs004-tmp/s1_call.py,
R176-proven 1500s wrapper). Purpose: verify the new scoring format (baseline
10, deduction flags, PASS/FAIL verdict) is followed by the local model on a
CLOSED batch-1 material (BS-004 v3, already passed by adjudication R185).
NOT a gate verdict for BS-004 (closed item) - format validation only.
Result -> .s1v15-tmp/smoke-result.json. ASCII source (encoding law)."""
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
    REPO / "data" / "sources" / "bs004" / "s1-review-material.md")
RESULT = REPO / ".s1v15-tmp" / "smoke-result.json"


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
              "verdict": out.strip(),
              "note": "S1 v1.5 smoke (backlog #24): format validation on "
                      "closed BS-004 v3 material, not a gate verdict"}
    if code == 0 and out.strip():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        vname = ce.verdict_file_name(EXPERT_ID, stamp)
        ce.save_verdict(ce.VERDICT_DIR, vname, EXPERT_ID, ex["role"],
                        ex["dept"], ex["model"], MATERIAL, out.strip())
        first_line = out.strip().splitlines()[0][:120]
        note = ("full text=expert-verdicts/%s | %s (S1 v1.5 smoke: format "
                "validation, closed BS-004 material, not gate verdict)"
                % (vname, first_line))
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
