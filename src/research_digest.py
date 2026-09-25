# -*- coding: utf-8 -*-
"""P4 research digest pipeline - minimal viable build (R307, backlog #54).

Group transfer P-2026-09-25-07 (CEO order 2026-09-25 ~19:00: systematize
the local LLM production pipeline). Program P4 per cph4/local-llm-pipeline.md
sec.3: "research draft pre-screen / digest compression". Advisory
pre-filter only (sec.6 honest boundary): it saves read-side tokens, it
never replaces reading the source when a decision cites it.

    python src/research_digest.py --input research/R-20260925-fan-ops-architecture.md

Channel = local Ollama via call_expert.call_model (UTF-8 subprocess pipe,
ANSI/braille-spinner cleaned, zero API tokens). The prompt lives as a
UTF-8 data file (encoding rule). Output = <input stem>.digest-v1.md next
to the input, carrying the model digest plus a tool-written verification
statement (criteria J1/J2 machine checks, docs/local-llm-p4-criteria.md).
Every run appends one row to data/pipeline/p4-ledger.md (replacement-rate
bookkeeping; first report due 2026-10-07 governance day).

Exit codes: 0 ok; 2 bad args / missing files; 3 ollama call failed;
            4 self-check FAIL (digest kept on disk for human review).
ASCII rule: this source is pure ASCII; Chinese lives in the prompt data
file, the digest output, and the ledger (md data files).
"""
import argparse
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from call_expert import call_model  # noqa: E402  (src/ sibling module)

REPO = Path(__file__).resolve().parents[1]
PROMPT_FILE = REPO / "data" / "pipeline" / "prompts" / "p4-digest.txt"
LEDGER = REPO / "data" / "pipeline" / "p4-ledger.md"
DEFAULT_MODEL = "qwen2.5:7b-instruct"  # ladder: digest = 7b resident tier
DEFAULT_TIMEOUT = 600                 # J3: <=10 min per item
DEFAULT_MAX_LINES = 60                # J2 line cap
DEFAULT_MAX_INPUT_CHARS = 6000        # 7b ctx budget; clipping is declared
CITE_RE = re.compile(r"\[L(\d+)\]")
_VERIF_MARK = "## " + "\u9a8c\u8bc1\u58f0\u660e"  # tool-written section

_LEDGER_HEADER = (
    "# P4 \u8c03\u7814\u6458\u8981\u53f0\u8d26\uff08research digest ledger\uff09\n\n"
    "> \u673a\u5236=docs/local-llm-p4-criteria.md\uff08"
    "P-2026-09-25-07 \u00b7 backlog #54\uff09\u3002"
    "\u884c\u7ea7\u8ffd\u52a0\u7981\u6539\u5199\uff1b"
    "\u66ff\u4ee3\u7387\u9996\u62a5=2026-10-07 \u6cbb\u7406\u65e5"
    "\uff08\u5468\u8f6e\u6c47 L2/(L2+L3)\uff09\u3002\n\n"
    "| \u65f6\u95f4 | \u8f93\u5165\u4ef6 | \u6a21\u578b | \u6458\u8981\u4ef6 "
    "| \u884c\u6570 | \u5f15\u7528 | \u622a\u65ad | \u65f6\u957f | \u5224\u5b9a |\n"
    "|---|---|---|---|---|---|---|---|---|\n")


def number_source(text):
    """Prefix every line with an L<n> marker. Returns (text, line_count)."""
    lines = text.splitlines()
    numbered = "\n".join("L%d\t%s" % (i + 1, ln) for i, ln in enumerate(lines))
    return numbered, len(lines)


def clip_text(text, max_chars):
    """Clip to max_chars on a line boundary. Returns (text, clipped_bool)."""
    if len(text) <= max_chars:
        return text, False
    cut = text[:max_chars]
    nl = cut.rfind("\n")
    if nl > 0:
        cut = cut[:nl]
    return cut, True


def build_prompt(template, numbered, max_lines, clipped):
    """Assemble the digest prompt (pure)."""
    head = template.replace("{max_lines}", str(max_lines)).rstrip()
    note = "\n\n[\u8f93\u5165\u8d85\u5e16\u5e45\u5df2\u622a\u65ad\uff1a" \
           "\u4ec5\u524d\u6bb5\u5165\u6458\u8981\uff0c\u5982\u5b9e\u4fdd\u7559]" \
        if clipped else ""
    return (head + "\n\n===== " + "\u8c03\u7814\u7a3f\uff08\u5e26\u884c\u53f7 [L n] \uff09"
            + note + "\n" + numbered + "\n")


def strip_verification_section(digest):
    """Drop any 'verification statement' section the model emitted anyway."""
    idx = digest.find(_VERIF_MARK)
    if idx > 0:
        digest = digest[:idx].rstrip()
    return digest


def check_digest(digest, input_line_count, max_lines):
    """Machine checks for J1 (citation sanity) and J2 (cap/structure).
    Returns a list of (name, ok, detail) tuples."""
    lines = [ln for ln in digest.splitlines()]
    results = []
    results.append(("J2_line_cap", len(lines) <= max_lines,
                    "%d/%d lines" % (len(lines), max_lines)))
    has_sections = any(ln.startswith("## ") for ln in lines)
    results.append(("J2_structure", has_sections,
                    "section headers present" if has_sections
                    else "no section headers"))
    cites = [int(m) for m in CITE_RE.findall(digest)]
    max_cite = max(cites) if cites else 0
    # J1 floor: >=3 citations (degenerate runs collapsed to 1 marker on
    # 2026-09-26 R307 run 2 - a digest without traceable points is not a
    # digest; floor catches that without brittle per-bullet parsing).
    sane = len(cites) >= 3 and max_cite <= input_line_count
    results.append(("J1_citations", sane,
                    "citations=%d max=L%d (input L%d)"
                    % (len(cites), max_cite, input_line_count)))
    return results


def ledger_row(src_name, model, digest_name, out_lines, ncites, clipped,
               dur, verdict):
    """One markdown table row for the P4 ledger (pure)."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return ("| %s | %s | %s | %s | %d | %d | %s | %.0fs | %s |\n"
            % (stamp, src_name, model, digest_name, out_lines, ncites,
               "yes" if clipped else "no", dur, verdict))


def append_ledger(ledger_path, row):
    """Best-effort ledger append; creates the header on first use."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    if not ledger_path.exists():
        ledger_path.write_text(_LEDGER_HEADER, encoding="utf-8")
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(row)


def run_digest(input_path, model=DEFAULT_MODEL, timeout=DEFAULT_TIMEOUT,
               max_lines=DEFAULT_MAX_LINES,
               max_input_chars=DEFAULT_MAX_INPUT_CHARS,
               prompt_file=PROMPT_FILE, ledger_path=LEDGER):
    """Core pipeline step. Returns a summary dict (never raises for
    model/self-check failures - caller decides the exit code)."""
    src_path = Path(input_path)
    if not src_path.is_absolute():
        src_path = REPO / src_path
    out_path = src_path.parent / (src_path.stem + ".digest-v1.md")
    summary = {"src": str(src_path), "out": str(out_path), "model": model,
               "verdict": "FAIL", "checks": [], "error": None}
    if not src_path.exists():
        summary["error"] = "input file missing"
        return summary
    if not Path(prompt_file).exists():
        summary["error"] = "prompt file missing"
        return summary
    text = src_path.read_text(encoding="utf-8-sig")
    numbered, n_lines = number_source(text)
    clipped_text, clipped = clip_text(numbered, max_input_chars)
    prompt = build_prompt(Path(prompt_file).read_text(encoding="utf-8"),
                          clipped_text, max_lines, clipped)
    t0 = time.time()
    try:
        code, out = call_model(model, prompt, timeout)
    except subprocess.TimeoutExpired:
        summary["error"] = "ollama timeout (%ds)" % timeout
        return summary
    summary["dur"] = time.time() - t0
    if code != 0:
        summary["error"] = "ollama exit %d" % code
        return summary
    digest = strip_verification_section(out.strip())
    if not digest:
        summary["error"] = "empty digest"
        return summary
    checks = check_digest(digest, n_lines, max_lines)
    summary["checks"] = checks
    summary["input_lines"] = n_lines
    summary["input_chars"] = len(text)
    summary["clipped"] = clipped
    summary["out_lines"] = len(digest.splitlines())
    summary["ncites"] = len(CITE_RE.findall(digest))
    ok = all(c[1] for c in checks)
    summary["verdict"] = "PASS" if ok else "FAIL"
    body = [
        "# P4 " + "\u8c03\u7814\u6458\u8981\u2014\u2014%s"
        "\uff08advisory \u9884\u7b5b\u4ef6\uff09" % src_path.name,
        "",
        "> \u751f\u6210=%s \u00b7 \u6a21\u578b=%s \u00b7 "
        "\u6e90\u4ef6=%s" % (
            datetime.now().strftime("%Y-%m-%d %H:%M"), model, src_path.name),
        "> \u673a\u5236=src/research_digest.py\uff08P-2026-09-25-07 \u00b7 "
        "\u5224\u636e=docs/local-llm-p4-criteria.md v0.1\uff09",
        "> \u6027\u8d28=\u672c\u5730 LLM \u751f\u6210\u6458\u8981"
        "\uff08AIGC\u00b7\u5185\u90e8\u9884\u7b5b\u4ef6\uff09\u00b7 "
        "\u4e3b\u8111\u5f15\u7528\u5173\u952e\u7ed3\u8bba\u524d\u987b"
        "\u56de\u539f\u6587\u6838\u5bf9\uff08\u8bda\u5b9e\u8fb9\u754c\uff09"
        + ("\u00b7 \u8f93\u5165\u5df2\u622a\u65ad=\u4ec5\u524d\u6bb5"
           "\u5165\u6458\u8981" if clipped else ""),
        "",
        digest,
        "",
        _VERIF_MARK + "\uff08\u5de5\u5177\u751f\u6210\uff09",
        "- \u8f93\u5165\uff1a%d \u884c / %d \u5b57\u7b26"
        "\uff08\u622a\u65ad=%s\uff09" % (
            n_lines, summary["input_chars"], "yes" if clipped else "no"),
        "- \u8f93\u51fa\uff1a%d \u884c\uff08\u5e3d %d\uff09\u00b7 "
        "\u5f15\u7528 [L] %d \u5904" % (
            summary["out_lines"], max_lines, summary["ncites"]),
        "- \u673a\u68c0\uff1a" + " \u00b7 ".join(
            "%s=%s(%s)" % (n, "PASS" if ok_ else "FAIL", d)
            for n, ok_, d in checks),
        "- \u603b\u5224\u5b9a\uff1a%s \u00b7 \u65f6\u957f %.0fs \u00b7 "
        "\u672c\u5730 Ollama \u96f6 API token \u00b7 "
        "\u53f0\u8d26=data/pipeline/p4-ledger.md" % (
            summary["verdict"], summary["dur"]),
        "",
    ]
    out_path.write_text("\n".join(body), encoding="utf-8")
    append_ledger(ledger_path, ledger_row(
        src_path.name, model, out_path.name, summary["out_lines"],
        summary["ncites"], clipped, summary["dur"], summary["verdict"]))
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    ap.add_argument("--max-input-chars", type=int,
                    default=DEFAULT_MAX_INPUT_CHARS)
    args = ap.parse_args(argv)
    s = run_digest(args.input, model=args.model, timeout=args.timeout,
                   max_lines=args.max_lines,
                   max_input_chars=args.max_input_chars)
    if s["error"]:
        print("FAIL %s" % s["error"])
        return 2 if "missing" in s["error"] else 3
    for name, ok, detail in s["checks"]:
        print("%s %s (%s)" % ("PASS" if ok else "FAIL", name, detail))
    print("%s verdict=%s dur=%.0fs" % (
        "OK" if s["verdict"] == "PASS" else "SELF-CHECK-FAIL",
        s["verdict"], s["dur"]))
    print("digest=%s" % s["out"])
    return 0 if s["verdict"] == "PASS" else 4


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
