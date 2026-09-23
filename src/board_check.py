# -*- coding: utf-8 -*-
"""BigStream board consistency probe (backlog#3, capability C-08).

Cross-checks the idea ledger (data/ideas/ideas.md) against the draft
inventory (data/drafts/): ledger status and on-disk drafts must map
one-to-one. Ownership: topic-research dept (org-structure.md).

Encoding rule: this script is pure ASCII. The few Chinese words it
must know (status-flow marker, arrow, producing state) appear only
as \\uXXXX escapes; the status vocabulary itself is parsed from the
ledger's own declared flow line, so a vocabulary change in the
ledger needs no code change here.

Consistency model - the ledger declares an ordered flow
    pending -> approved -> producing -> finished -> published
Any status at or beyond "producing" requires >= 1 draft on disk;
any draft for an idea still below that state means the ledger is
behind the real work. Honesty rule (CONSTITUTION S5): overstating
progress is the worst direction - both directions FAIL here.

Findings (all FAIL severity):
    vocab        ledger has no parseable status-flow line, or the
                 declared flow lacks the producing state
    dup-id       same idea id appears twice in the ledger
    bad-status   a row status is not in the declared flow
    drafts-dir   drafts directory is missing
    bad-name     draft filename carries no BS id
    orphan       draft exists but its id is not in the ledger
    overstate    ledger says in-production but no draft on disk
    stale        drafts exist but ledger not yet in production

Usage:
    python src/board_check.py                     # real repo board
    python src/board_check.py LEDGER DRAFTS_DIR   # explicit paths

Exit codes: 0 = consistent, 1 = any FAIL, 2 = usage error.
"""
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IDEAS = REPO / "data" / "ideas" / "ideas.md"
DRAFTS = REPO / "data" / "drafts"

FLOW_MARKER = "\u72b6\u6001\u6d41"  # status-flow marker word
FLOW_ARROW = "\u2192"  # arrow separating statuses in the flow line
PROD_STATE = "\u5236\u4f5c\u4e2d"  # producing state: drafts must exist

FLOW_RE = re.compile(FLOW_MARKER + r"[\uff1a:]\s*([^\uff1b;]+)")
ROW_RE = re.compile(r"^\|\s*(BS-\d{3,})\s*\|")
ID_RE = re.compile(r"BS-\d{3,}")


def parse_ideas(path):
    """Parse the ledger; return (vocab, ideas, findings).

    vocab = ordered status list parsed from the declared flow line
    ideas = OrderedDict {id: status}; None marks an unknown status
    """
    findings = []
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FLOW_RE.search(text)
    vocab = [s.strip() for s in m.group(1).split(FLOW_ARROW) if s.strip()] if m else []
    if not vocab:
        findings.append(("FAIL", "vocab", "ledger has no parseable status-flow line"))
        return [], {}, findings
    ideas = OrderedDict()
    for line in text.splitlines():
        rm = ROW_RE.match(line)
        if not rm:
            continue
        idea_id = rm.group(1)
        cells = [c.strip() for c in line.split("|") if c.strip()]
        status = cells[-1] if cells else ""
        if idea_id in ideas:
            findings.append(("FAIL", "dup-id", "duplicate ledger row: %s" % idea_id))
            continue
        if status not in vocab:
            findings.append(("FAIL", "bad-status",
                             "%s: status not in declared flow: %s" % (idea_id, status)))
            ideas[idea_id] = None
            continue
        ideas[idea_id] = status
    return vocab, ideas, findings


def collect_drafts(drafts_dir):
    """Inventory drafts; return (counts, findings). counts = {id: n}."""
    findings = []
    if not drafts_dir.is_dir():
        findings.append(("FAIL", "drafts-dir", "drafts directory missing: %s" % drafts_dir))
        return None, findings
    counts = {}
    for p in sorted(drafts_dir.glob("*.md")):
        m = ID_RE.search(p.stem)
        if not m:
            findings.append(("FAIL", "bad-name", "draft filename has no BS id: %s" % p.name))
            continue
        idea_id = m.group(0)
        counts[idea_id] = counts.get(idea_id, 0) + 1
    return counts, findings


def check_board(ideas_path, drafts_dir):
    """Cross-check ledger vs drafts; return (findings, stats)."""
    findings = []
    vocab, ideas, f = parse_ideas(ideas_path)
    findings += f
    counts, f = collect_drafts(drafts_dir)
    findings += f
    stats = {
        "ideas": len(ideas),
        "drafts": sum(counts.values()) if counts else 0,
        "in_prod": 0,
    }
    if not vocab or counts is None:
        return findings, stats
    for idea_id, n in sorted(counts.items()):
        if idea_id not in ideas:
            findings.append(("FAIL", "orphan",
                             "draft id not in ledger: %s (%d file(s))" % (idea_id, n)))
    if PROD_STATE not in vocab:
        findings.append(("FAIL", "vocab",
                         "declared flow lacks the producing state: %s" % PROD_STATE))
        return findings, stats
    prod_rank = vocab.index(PROD_STATE)
    for idea_id, status in ideas.items():
        if status is None:
            continue
        n = counts.get(idea_id, 0)
        rank = vocab.index(status)
        if rank >= prod_rank:
            stats["in_prod"] += 1
            if n == 0:
                findings.append(("FAIL", "overstate",
                                 "%s is '%s' but has no draft on disk" % (idea_id, status)))
        elif n > 0:
            findings.append(("FAIL", "stale",
                             "%s has %d draft(s) but ledger still says '%s'" % (idea_id, n, status)))
    return findings, stats


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = argv[1:]
    if len(args) > 2:
        print("usage: python src/board_check.py [LEDGER] [DRAFTS_DIR]")
        return 2
    ideas_path = Path(args[0]) if len(args) >= 1 else IDEAS
    drafts_dir = Path(args[1]) if len(args) >= 2 else DRAFTS
    if not ideas_path.is_file():
        print("ledger file not found: %s" % ideas_path)
        return 2
    print("board probe: ledger=%s drafts=%s" % (ideas_path, drafts_dir))
    findings, stats = check_board(ideas_path, drafts_dir)
    for sev, code, msg in findings:
        print("    - %-9s %-11s %s" % (sev, code, msg))
    print("summary: %d ideas, %d drafts, %d in production, %d fail"
          % (stats["ideas"], stats["drafts"], stats["in_prod"], len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
