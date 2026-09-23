# -*- coding: utf-8 -*-
"""BigStream draft linter - the M4 machine gate (content-pipeline.md M4-1).

Usage:
    python src/draft_lint.py            # lint every draft in data/drafts/
    python src/draft_lint.py FILE ...   # lint specific files

Findings severity:
    FAIL  blocks the M4 gate (draft must be fixed, no exceptions)
    WARN  allowed to pass machine gate but requires explicit human review note

Checks:
    structure   required sections (master: titles/sources/AIGC/GATE,
                variant: master-link/GATE/AIGC)                  [FAIL]
    gate        GATE line well-formed                            [FAIL]
    secrets     credential/key patterns anywhere                 [FAIL]
    internal    machine ids / repo slugs / user paths / git URLs [WARN]
    sources     master source list has >= 1 item                 [FAIL]
    aigc        AIGC disclosure sentence present                [FAIL]
    disclaimer  quant-claim drafts need a risk disclaimer        [FAIL]
    duration    voiceover drafts estimated 30-60s (chars/4.0)    [WARN]

Exit codes: 0 = all PASS (WARN allowed), 1 = any FAIL, 2 = usage error.
This tool is a NECESSARY, not sufficient, M4 condition - semantic checks
(title-vs-delivery, fact-vs-ledger) remain human review duties.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRAFTS = REPO / "data" / "drafts"

GATE_RE = re.compile(r"GATE:\s*(PENDING|PASS|FAIL)\b")
MASTER_LINK_RE = re.compile(r"母稿\s*=\s*`?([^`\n]+)`?")
SECTION_RE = re.compile(r"^##\s+(.*)$", re.M)

SECRET_PATTERNS = [
    r"ghp_[A-Za-z0-9]{20,}",
    r"gho_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"sk-[A-Za-z0-9]{20,}",
    r"xox[baprs]-[A-Za-z0-9-]{10,}",
    r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*\S+",
]
INTERNAL_PATTERNS = [
    r"C:\\Users\\",
    r"(?<![A-Za-z0-9])bm-[ab](?![A-Za-z0-9])",
    r"DASHENG",
    r"BigRain-11122",
    r"git@github\.com:",
    r"https?://github\.com/",
]
QUANT_CLAIM_RE = re.compile(r"Sharpe|夏普|年化|全灭|收益率|回测结果")
DISCLAIMER_RE = re.compile(r"投资建议")
AIGC_RE = re.compile(r"AI\s*生成")
SOURCE_ITEM_RE = re.compile(r"^\s*(?:\d+\.|-)\s+\S", re.M)


def sections(text):
    """Return dict {section_title_upper: body} from markdown level-2 headers."""
    out = {}
    matches = list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[m.group(1).strip().upper()] = text[m.end():end]
    return out


def section_body(sec_dict, keyword):
    for title, body in sec_dict.items():
        if keyword in title:
            return body
    return None


def lint_file(path):
    """Return (list_of_findings, stats). Finding = (severity, code, message)."""
    findings = []
    text = path.read_text(encoding="utf-8")
    is_master = "公众号" in path.name  # platform masters carry full review sections
    is_voice = "视频号" in path.name
    sec = sections(text)

    def fail(code, msg):
        findings.append(("FAIL", code, msg))

    def warn(code, msg):
        findings.append(("WARN", code, msg))

    # structure -----------------------------------------------------------
    if is_master:
        for kw in ("标题候选", "来源清单", "AIGC", "GATE"):
            if section_body(sec, kw) is None:
                fail("structure", "missing section: %s" % kw)
        src_body = section_body(sec, "来源清单") or ""
        if src_body and not SOURCE_ITEM_RE.search(src_body):
            fail("sources", "source list is empty (cite sources or do not publish)")
    else:
        if not MASTER_LINK_RE.search(text):
            fail("structure", "variant missing master-draft link (母稿=...)")
        if section_body(sec, "GATE") is None:
            fail("structure", "missing section: GATE")
        if not AIGC_RE.search(text) and "AIGC" not in text:
            fail("aigc", "no AIGC disclosure found in variant")

    # AIGC (master) --------------------------------------------------------
    if is_master:
        if not AIGC_RE.search(text):
            fail("aigc", "no AIGC disclosure sentence (AI 生成)")

    # GATE line ------------------------------------------------------------
    gate = GATE_RE.search(text)
    if not gate:
        fail("gate", "no GATE: PENDING/PASS/FAIL line")
    elif gate.group(1) in ("PASS", "FAIL"):
        tail = text[gate.end():gate.end() + 120]
        if not re.search(r"\d{4}-\d{2}-\d{2}", tail) or "审" not in tail:
            fail("gate", "PASS/FAIL verdict must carry date + reviewer")

    # secrets / internal ---------------------------------------------------
    for pat in SECRET_PATTERNS:
        m = re.search(pat, text)
        if m:
            fail("secrets", "credential-like pattern: %s" % m.group(0)[:40])
    for pat in INTERNAL_PATTERNS:
        m = re.search(pat, text)
        if m:
            warn("internal", "internal identifier in draft: %s" % m.group(0)[:40])

    # quant disclaimer ------------------------------------------------------
    if QUANT_CLAIM_RE.search(text) and not DISCLAIMER_RE.search(text):
        fail("disclaimer", "quant claims present but no 投资建议 disclaimer")

    # duration estimate ------------------------------------------------------
    stats = {}
    if is_voice:
        body = section_body(sec, "口播全文") or ""
        chars = len(re.sub(r"\s", "", body))
        secs = chars / 4.0
        stats["voice_chars"] = chars
        stats["est_seconds"] = round(secs, 1)
        if secs > 60:
            warn("duration", "voiceover est %.0fs > 60s (target 30-60s)" % secs)
        if secs < 25:
            warn("duration", "voiceover est %.0fs < 25s (too short)" % secs)
    else:
        main = section_body(sec, "正文") or ""
        stats["body_chars"] = len(re.sub(r"\s", "", main))

    return findings, stats


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    paths = [Path(a) for a in argv[1:]] or sorted(DRAFTS.glob("*.md"))
    if not paths:
        print("no drafts found under %s" % DRAFTS)
        return 2
    total = failed = warned = 0
    for p in paths:
        total += 1
        findings, stats = lint_file(p)
        bad = [f for f in findings if f[0] == "FAIL"]
        warns = [f for f in findings if f[0] == "WARN"]
        status = "FAIL" if bad else ("WARN" if warns else "PASS")
        if bad:
            failed += 1
        if warns:
            warned += 1
        extra = " ".join("%s=%s" % kv for kv in stats.items())
        print("[%s] %s %s" % (status, p.name, ("(" + extra + ")") if extra else ""))
        for sev, code, msg in findings:
            print("    - %-9s %-9s %s" % (sev, code, msg))
    print("summary: %d drafts, %d pass, %d warn, %d fail" % (total, total - failed - warned, warned, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
