# -*- coding: utf-8 -*-
"""On-call departmental expert invoker (O-20260924-1033-bm-a).

Every department keeps dedicated expert roles (functional identities,
org-structure S3 "not personified" law). This tool makes "ready to be
called at any time" literal:

    python src/call_expert.py --expert hot-intel --material data/intel/daily/2026-09-24.md

Registry = data/experts/registry.json (id/dept/role/prompt_file/model).
Prompts live as UTF-8 data files (encoding rule); the model is the local
Ollama (default qwen2.5:14b - zero API, zero token). The call goes through
subprocess stdin in UTF-8, which also fixes the PS5.1 GBK pipe garbling
that hit raw `ollama run` piping on 2026-09-23.

Every call is appended to docs/reviews/expert-calls.md (audit trail).

ASCII rule: this source is pure ASCII; Chinese lives in the registry /
prompt / material data files.

Exit codes: 0 ok; 2 bad args / unknown expert / missing files;
            3 ollama call failed; 4 ledger append failed (verdict kept).
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "data" / "experts" / "registry.json"
LEDGER = REPO / "docs" / "reviews" / "expert-calls.md"
VERDICT_DIR = REPO / "docs" / "reviews" / "expert-verdicts"
DEFAULT_TIMEOUT = 300


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
    out = p.stdout.decode("utf-8", "replace")
    return p.returncode, out


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
    expert_id = material = None
    i = 1
    while i < len(argv):
        if argv[i] == "--expert":
            i += 1
            expert_id = argv[i]
        elif argv[i] == "--material":
            i += 1
            material = argv[i]
        i += 1
    if not (expert_id and material):
        print("usage: call_expert.py --expert ID --material FILE")
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
    prompt = build_prompt(prompt_path.read_text(encoding="utf-8"),
                          material_path.read_text(encoding="utf-8"))
    try:
        code, out = call_model(ex["model"], prompt)
    except subprocess.TimeoutExpired:
        print("FAIL ollama timeout (%ds)" % DEFAULT_TIMEOUT)
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
