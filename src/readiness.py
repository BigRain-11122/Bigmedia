# -*- coding: utf-8 -*-
"""BigStream publish-readiness probe (backlog#10, capability C-19).

Single-command aggregate of the distance to first publish. Ownership:
platform-ops dept (org-structure.md). Pure read-only over four sources:

    docs/accounts.md    per-platform account lights; the status flow is
                        parsed from the ledger's own flow line (same
                        data-driven rule as board_check)
    data/drafts/*.md    per-draft M4 GATE verdicts (GATE_RE reused from
                        draft_lint - one source of truth for the format)
    output/renders/     pipeline-test artifacts; every media file must
                        be annotated in README.md with the test-piece
                        mark (O-20260923-1756-bm-a discipline)
    src/os/backlog.md   [needs-CEO] / [suspended...] decision items

Encoding rule: this script is pure ASCII. The few Chinese words it
must match (flow marker, test-piece mark, batch words) appear only
as \\uXXXX escapes; all other Chinese flows from the parsed data.

Findings (machine-discipline breaches; FAIL or WARN):
    accounts-flow   no parseable status-flow line in accounts ledger
    accounts-row    a row status is not in the declared flow
    accounts-batch  no first-batch row found in the accounts table (WARN)
    gate-dir        drafts directory missing
    gate-missing    a draft carries no GATE line (draft_lint domain,
                    repeated here so the report is self-contained)
    render-dir      renders directory missing
    render-ledger   media files exist but no README.md ledger
    render-unannot  media file not annotated with a test-piece/production/
                    disposed mark
    render-stale    ledger row references a media file not on disk

Blockers (distance to first publish - the honest pre-launch state,
not failures): first-batch accounts still at the first flow state,
drafts not yet GATE PASS, [needs-CEO] decision items. Suspended items
are regime state (CEO-directed holds): listed, never counted.

Report: markdown rendered from src/os/readiness_template.md (Chinese
data file). stdout by default; --out FILE also writes the report.

Usage:
    python src/readiness.py                     # real repo, stdout
    python src/readiness.py --out FILE          # also write report
    python src/readiness.py --root DIR [...]    # alternate repo tree

Exit codes: 0 = publish-ready (no blockers, no findings),
            1 = blockers and/or findings (normal pre-launch state),
            2 = usage/source error.
"""
import re
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ACCOUNTS = REPO / "docs" / "accounts.md"
DRAFTS = REPO / "data" / "drafts"
RENDERS = REPO / "output" / "renders"
BACKLOG = REPO / "src" / "os" / "backlog.md"
TEMPLATE = REPO / "src" / "os" / "readiness_template.md"
LEDGER_NAME = "README.md"

from board_check import FLOW_MARKER, FLOW_ARROW  # noqa: E402
from draft_lint import GATE_RE  # noqa: E402
from weekly_report import DONE_RE, ITEM_RE, first_clause  # noqa: E402

# board_check's FLOW_RE stops at a fullwidth semicolon - fine for the
# ideas ledger, but the accounts flow line carries no semicolon, so the
# capture would run across paragraphs. readiness bounds it to one line.
FLOW_LINE_RE = re.compile(FLOW_MARKER + r"[\uff1a:]\s*([^\uff1b;\n]+)")

TEST_MARK = "\u6d4b\u8bd5\u4ef6\u00b7\u975e\u6210\u54c1"  # test-piece mark
PRODUCT_MARK = "\u6210\u54c1\u00b7\u6279\u6b21"  # production-piece mark (D-BS-06 gate-open era; covers .mp4 only rows)
# superseded historical piece (2026-09-25 #23 v14 batch era): rectification
# re-renders replace registered goods but the old mp4s stay on disk as
# historical archive rows - "superseded by <new>" cells are a third legal
# state, not an unannotated leak. Both substrings together avoid false
# hits from prose that merely says "replaced" ("...beit v2 取代清盘" lines
# lack the 已被 prefix).
SUPERSEDED_A = "\u5df2\u88ab"  # "has been" prefix
SUPERSEDED_B = "\u53d6\u4ee3"  # "superseded/replaced" word
# disposed piece (2026-09-25 D-BS-08 era): escalation-disposal renders stay
# on disk as archive rows - "弃件...留档" cells are a fourth legal state,
# not an unannotated leak. Both substrings together avoid false hits from
# prose that merely mentions discarding ("弃件" alone in narrative lines).
DISPOSED_A = "\u5f03\u4ef6"  # "disposed/discarded" mark
DISPOSED_B = "\u7559\u6863"  # "archived on disk" qualifier
STATUS_WORD = "\u72b6\u6001"  # status column header word
BATCH_WORD = "\u6279\u6b21"  # batch word in accounts remark
BATCH1_MARK = "\u2460"  # circled-one first-batch marker
NEEDS_CEO_RE = re.compile(r"\[needs-CEO[^\]]*\]")
SUSPENDED_RE = re.compile(r"\[suspended[^\]]*\]")
MEDIA_RE = re.compile(r"[\w.\-]+\.(?:mp4|mov|avi|wav)\b", re.I)
MEDIA_SUFFIXES = (".mp4", ".mov", ".avi", ".wav")

PLACEHOLDERS = (
    "GEN_TS", "ACC_N", "ACC_FLOW", "ACC_ROWS", "DRAFT_N", "GATE_ROWS",
    "RENDER_N", "RENDER_ROWS", "NEEDS_N", "NEEDS_LIST", "SUSP_N",
    "SUSP_LIST", "BLOCKER_N", "BLOCKERS_LIST", "FINDINGS_LIST",
)


def _clean_state(token):
    """Clean one flow status token: strip code ticks and trailing
    sentence punctuation, cut parenthetical notes."""
    token = token.replace("`", "").strip()
    for cut in ("\uff08", "("):
        i = token.find(cut)
        if i != -1:
            token = token[:i]
    return token.strip("\u3002\uff1b\uff0c\u3001;,.").strip()


def parse_accounts(path):
    """Parse accounts.md -> (flow, rows, findings).

    flow = ordered status list from the declared flow line
    rows = [(platform, status-or-None, remark)]
    """
    findings = []
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FLOW_LINE_RE.search(text)
    flow = [s for s in (_clean_state(t) for t in m.group(1).split(FLOW_ARROW))] if m else []
    flow = [s for s in flow if s]
    if not flow:
        findings.append(("FAIL", "accounts-flow",
                         "accounts ledger has no parseable status-flow line"))
        return [], [], findings
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3 or all(set(c) <= {"-", ""} for c in cells):
            continue
        if STATUS_WORD in cells:
            continue  # header row
        platform, status, remark = cells[0], cells[2], cells[-1]
        if not platform:
            continue
        if status not in flow:
            findings.append(("FAIL", "accounts-row",
                             "row status not in declared flow: %r (%s)" % (status, platform)))
            status = None
        rows.append((platform, status, remark))
    if rows and not any(BATCH_WORD + BATCH1_MARK in r for _, _, r in rows):
        findings.append(("WARN", "accounts-batch",
                         "no first-batch row found in accounts table"))
    return flow, rows, findings


def parse_gates(drafts_dir):
    """GATE verdicts from drafts -> (OrderedDict name->verdict, findings)."""
    findings = []
    if not drafts_dir.is_dir():
        findings.append(("FAIL", "gate-dir", "drafts directory missing: %s" % drafts_dir))
        return OrderedDict(), findings
    gates = OrderedDict()
    for p in sorted(drafts_dir.glob("*.md")):
        m = GATE_RE.search(p.read_text(encoding="utf-8", errors="replace"))
        if not m:
            findings.append(("FAIL", "gate-missing", "draft has no GATE line: %s" % p.name))
            gates[p.name] = None
        else:
            gates[p.name] = m.group(1)
    return gates, findings


def parse_renders(renders_dir, ledger_path):
    """Test-piece inventory -> (rows, findings). rows = [(name, annotated)]."""
    findings = []
    if not renders_dir.is_dir():
        findings.append(("FAIL", "render-dir", "renders directory missing: %s" % renders_dir))
        return [], findings
    media = sorted(p.name for p in renders_dir.iterdir()
                   if p.suffix.lower() in MEDIA_SUFFIXES)
    if media and not ledger_path.is_file():
        findings.append(("FAIL", "render-ledger",
                         "media files exist but annotation ledger missing: %s" % ledger_path))
        return [(name, False) for name in media], findings
    seen = {}
    if ledger_path.is_file():
        text = ledger_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            for m in MEDIA_RE.finditer(line):
                name = m.group(0).lower()
                ok = (TEST_MARK in line or PRODUCT_MARK in line
                      or (SUPERSEDED_A in line and SUPERSEDED_B in line)
                      or (DISPOSED_A in line and DISPOSED_B in line))
                seen[name] = seen.get(name, False) or ok
    rows = []
    for name in media:
        annotated = seen.get(name.lower(), False)
        if not annotated:
            findings.append(("FAIL", "render-unannot",
                             "media file not annotated as test piece: %s" % name))
        rows.append((name, annotated))
    on_disk = {n.lower() for n in media}
    for name in sorted(seen):
        if name not in on_disk:
            findings.append(("FAIL", "render-stale",
                             "ledger row references file not on disk: %s" % name))
    return rows, findings


def parse_backlog_flags(path):
    """[needs-CEO] / [suspended] items -> (needs, suspended). Each (num, clause).

    Done items are excluded; unmarked open items are plain work, not
    decision blockers. Markers are stripped before the clause clip.
    """
    needs, suspended = [], []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = ITEM_RE.match(line)
        if not m or DONE_RE.search(m.group(2)):
            continue
        num, body = m.group(1), m.group(2).strip()
        if NEEDS_CEO_RE.search(body):
            clean = NEEDS_CEO_RE.sub("", body)
            needs.append((num, first_clause(clean)))
        elif SUSPENDED_RE.search(body):
            clean = SUSPENDED_RE.sub("", body)
            suspended.append((num, first_clause(clean)))
    return needs, suspended


def build_blockers(flow, rows, gates, needs):
    """Distance-to-first-publish lines (English scaffold, parsed tokens)."""
    blockers = []
    if flow:
        first = flow[0]
        launch_closed = [p for p, s, r in rows
                         if (BATCH_WORD + BATCH1_MARK) in r and s == first]
        if launch_closed:
            blockers.append("first-launch accounts not open (%s): opening = CEO "
                            "physical action (batch order in docs/accounts.md)"
                            % ", ".join(launch_closed))
    not_pass = [n for n, v in gates.items() if v != "PASS"]
    if not_pass:
        blockers.append("M4 gate not green: %d/%d draft(s) not GATE PASS "
                        "(M4 = publish precondition; verdicts in section 2)"
                        % (len(not_pass), len(gates)))
    for num, clause in needs:
        blockers.append("decision pending: #%s %s (needs CEO sign-off)" % (num, clause))
    return blockers


def build_report(template_text, gen_ts, flow, rows, gates, render_rows,
                 needs, suspended, blockers, findings):
    """Fill the template -> report text (data file, Chinese content)."""
    def bullets(seq):
        return "\n".join(seq) if seq else "- none"
    acc_rows = ["| %s | %s | %s |" % (p, s if s else "?", r) for p, s, r in rows]
    gate_rows = ["| %s | %s |" % (n, v if v else "(no GATE line)") for n, v in gates.items()]
    render_lines = ["| %s | %s |" % (n, TEST_MARK if ok else "(missing test-piece mark)")
                    for n, ok in render_rows]
    needs_lines = ["- #%s [needs-CEO] %s" % (n, c) for n, c in needs]
    susp_lines = ["- #%s [suspended] %s" % (n, c) for n, c in suspended]
    finding_lines = ["- [%s] %s: %s" % (sev, code, msg) for sev, code, msg in findings]
    values = {
        "GEN_TS": gen_ts,
        "ACC_N": str(len(rows)),
        "ACC_FLOW": FLOW_ARROW.join(flow) if flow else "(unparsed)",
        "ACC_ROWS": bullets(acc_rows),
        "DRAFT_N": str(len(gates)),
        "GATE_ROWS": bullets(gate_rows),
        "RENDER_N": str(len(render_rows)),
        "RENDER_ROWS": bullets(render_lines),
        "NEEDS_N": str(len(needs)),
        "NEEDS_LIST": bullets(needs_lines),
        "SUSP_N": str(len(suspended)),
        "SUSP_LIST": bullets(susp_lines),
        "BLOCKER_N": str(len(blockers)),
        "BLOCKERS_LIST": bullets(["- %s" % b for b in blockers]),
        "FINDINGS_LIST": bullets(finding_lines),
    }
    text = template_text
    for key in PLACEHOLDERS:
        text = text.replace("{" + key + "}", values[key])
    return text


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = argv[1:]
    out_path, root = None, REPO
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--root" and i + 1 < len(args):
            root = Path(args[i + 1])
            i += 2
        else:
            print("usage: python src/readiness.py [--root DIR] [--out FILE]")
            return 2
    accounts = root / "docs" / "accounts.md"
    drafts = root / "data" / "drafts"
    renders = root / "output" / "renders"
    backlog = root / "src" / "os" / "backlog.md"
    try:
        flow, rows, findings = parse_accounts(accounts)
        gates, f = parse_gates(drafts)
        findings += f
        render_rows, f = parse_renders(renders, renders / LEDGER_NAME)
        findings += f
        needs, suspended = parse_backlog_flags(backlog)
        template_text = TEMPLATE.read_text(encoding="utf-8")
    except OSError as e:
        print("source error: %s" % e)
        return 2
    blockers = build_blockers(flow, rows, gates, needs)
    gen_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = build_report(template_text, gen_ts, flow, rows, gates, render_rows,
                          needs, suspended, blockers, findings)
    print(report)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(report)
        print("report written: %s" % out_path)
    print("readiness: %d blocker(s), %d finding(s) -> %s"
          % (len(blockers), len(findings),
             "NOT READY" if (blockers or findings) else "READY"))
    return 1 if (blockers or findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
