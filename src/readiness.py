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
    review-not-executed  a GATE-PENDING draft's M4 seat call never ran
                    (trace: data/pipeline/expert-not-executed-ledger.jsonl;
                    WARN - distinguishes "not reviewed" from "failed")

Blockers (distance to first publish - the honest pre-launch state,
not failures): first-batch accounts still at the first flow state,
drafts not yet GATE PASS, [needs-CEO] decision items. Suspended items
are regime state (CEO-directed holds): listed, never counted.

Report: markdown rendered from src/os/readiness_template.md (Chinese
data file). stdout by default; --out FILE also writes the report.
--summary prints the routine loop-consumption face instead: per-source
count lines (accounts / gates / render annotation states) plus every
blocker and finding in full - the 78-row ledger table is not repeated
each round. Same analysis, same exit code; full report unchanged.

Usage:
    python src/readiness.py                     # real repo, stdout
    python src/readiness.py --out FILE          # also write report
    python src/readiness.py --summary           # compact loop face
    python src/readiness.py --root DIR [...]    # alternate repo tree

Exit codes: 0 = publish-ready (no blockers, no findings),
            1 = blockers and/or findings (normal pre-launch state),
            2 = usage/source error.
"""
import json
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
# tech#377 (R2428): the machine face src/call_expert.py writes when a
# seat call never produced a verdict. Read here so "the review never
# ran" stops looking identical to "the review ran and failed".
REVIEW_TRACE = REPO / "data" / "pipeline" / "expert-not-executed-ledger.jsonl"
NOT_EXECUTED_MARK = "NOT-EXECUTED"
REVIEW_CALLS = REPO / "docs" / "reviews" / "expert-calls.md"
TEMPLATE = REPO / "src" / "os" / "readiness_template.md"
LEDGER_NAME = "README.md"

from board_check import FLOW_MARKER, FLOW_ARROW  # noqa: E402
from draft_lint import GATE_RE  # noqa: E402
from weekly_report import DONE_RE, ITEM_RE, first_clause  # noqa: E402

# board_check's FLOW_RE stops at a fullwidth semicolon - fine for the
# ideas ledger, but the accounts flow line carries no semicolon, so the
# capture would run across paragraphs. readiness bounds it to one line.
FLOW_LINE_RE = re.compile(FLOW_MARKER + r"[\uff1a:]\s*([^\uff1b;\n]+)")

import render_marks  # noqa: E402

TEST_MARK = render_marks.TEST_MARK  # test-piece mark (canonical vocabulary)
PRODUCT_MARK = render_marks.PRODUCT_MARK  # production-piece mark (D-BS-06 gate-open era)
# slot-filled production piece (2026-09-27 R512 era): release-schedule
# D-slot pre-production goods (LC-001 D15 first case) are a fifth legal
# state - "production.slot-filled" cells. Kept as a distinct full mark so
# prose lines that merely say "落位" without the 成品 prefix stay
# unannotated (false-hit guard).
PRODUCT_SLOT_MARK = render_marks.PRODUCT_SLOT_MARK  # slot-filled production mark
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
# Display-layer status labels (R1802): the 3rd report section shows the
# ledger row's real state instead of hard-coding the test-piece string
# (R1799 finding: all 78 mp4s displayed as test pieces masked the
# production / superseded / disposed rows). Gate legality unchanged.
SUPERSEDED_MARK = render_marks.SUPERSEDED_MARK  # superseded archive display label
DISPOSED_MARK = render_marks.DISPOSED_MARK  # disposed archive display label
MISSING_MARK = "(no legal renders mark)"  # unannotated display cell
STATUS_PRECEDENCE = (PRODUCT_SLOT_MARK, PRODUCT_MARK, SUPERSEDED_MARK,
                    DISPOSED_MARK, TEST_MARK)  # multi-mention rank
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


def _line_status(line):
    """Ledger-line annotation state for the display layer (R1802):
    the real mark the row carries, None when the line has no legal
    mark. The legality set matches the gate exactly (five states)."""
    if PRODUCT_SLOT_MARK in line:
        return PRODUCT_SLOT_MARK
    if PRODUCT_MARK in line:
        return PRODUCT_MARK
    if SUPERSEDED_A in line and SUPERSEDED_B in line:
        return SUPERSEDED_MARK
    if DISPOSED_A in line and DISPOSED_B in line:
        return DISPOSED_MARK
    if TEST_MARK in line:
        return TEST_MARK
    return None


def parse_renders(renders_dir, ledger_path):
    """Render inventory -> (rows, findings). rows = [(name, status)].

    status = the ledger row's real annotation state (production
    slot-filled / production batch / superseded archive / disposed
    archive / test piece), None when unannotated. `status is None`
    feeds the render-unannot gate - gate semantics unchanged; only
    the display stopped hard-coding the test-piece string."""
    findings = []
    if not renders_dir.is_dir():
        findings.append(("FAIL", "render-dir", "renders directory missing: %s" % renders_dir))
        return [], findings
    media = sorted(p.name for p in renders_dir.iterdir()
                   if p.suffix.lower() in MEDIA_SUFFIXES)
    if media and not ledger_path.is_file():
        findings.append(("FAIL", "render-ledger",
                         "media files exist but annotation ledger missing: %s" % ledger_path))
        return [(name, None) for name in media], findings
    seen = {}
    if ledger_path.is_file():
        text = ledger_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            for m in MEDIA_RE.finditer(line):
                name = m.group(0).lower()
                st = _line_status(line)
                cur = seen.get(name)
                if st is not None and (cur is None or
                        STATUS_PRECEDENCE.index(st) < STATUS_PRECEDENCE.index(cur)):
                    seen[name] = st
                elif cur is None and name not in seen:
                    seen[name] = None
    rows = []
    for name in media:
        status = seen.get(name.lower())
        if status is None:
            findings.append(("FAIL", "render-unannot",
                             "media file not annotated with a legal renders mark"
                             " (%s): %s" % (render_marks.legal_vocabulary(), name)))
        rows.append((name, status))
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


def parse_not_executed(path=None):
    """Seat calls that produced no verdict -> [row dict] (tech#377).

    Reads the JSONL face call_expert writes on every failure path
    (liveness dead / wire error / wedge bail / GPU defer). Missing file
    is normal on a fresh tree (nothing failed yet), never an error."""
    p = Path(path) if path is not None else REVIEW_TRACE
    rows = []
    if not p.is_file():
        return rows
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get("mark") == NOT_EXECUTED_MARK:
            rows.append(row)
    return rows


def parse_review_calls(path=None):
    """Successful seat calls from the human ledger -> {basename: ts}.

    tech#377: a not-executed trace is only true until a later call
    actually ran. Without this the WARN would outlive its cause and
    become the same "attached forever" noise the six stale drafts were.
    Row shape: `| ts | expert | role（dept） | material | exit | note |`."""
    p = Path(path) if path is not None else REVIEW_CALLS
    calls = {}
    if not p.is_file():
        return calls
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 7:
            continue
        ts, material, exit_code = cells[1], cells[4], cells[5]
        if exit_code != "0" or not material:
            continue
        name = material.replace("\\", "/").rsplit("/", 1)[-1]
        if ts > calls.get(name, ""):
            calls[name] = ts
    return calls


def not_executed_drafts(rows, gates, calls=None):
    """draft name -> its latest not-executed trace (pure).

    Matches the trace row's material basename against the drafts that
    are still not GATE PASS: those are the pieces whose review could
    not run, as opposed to pieces a reviewer actually failed."""
    pending = set(n for n, v in gates.items() if v != "PASS")
    hit = {}
    for row in rows:
        name = str(row.get("material", "")).replace("\\", "/").rsplit("/", 1)[-1]
        if name not in pending:
            continue
        if calls and calls.get(name, "") >= str(row.get("ts", "")):
            continue  # a later call really ran: the trace is history
        if name not in hit or str(row.get("ts", "")) >= str(hit[name].get("ts", "")):
            hit[name] = row
    return hit


def build_blockers(flow, rows, gates, needs, not_exec=None):
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
        msg = ("M4 gate not green: %d/%d draft(s) not GATE PASS "
               "(M4 = publish precondition; verdicts in section 2)"
               % (len(not_pass), len(gates)))
        never = [n for n in not_pass if not_exec and n in not_exec]
        if never:
            msg += (" - %d of them: review face NOT EXECUTED (seat call "
                    "failed, trace in data/pipeline/"
                    "expert-not-executed-ledger.jsonl)" % len(never))
        blockers.append(msg)
    for num, clause in needs:
        blockers.append("decision pending: #%s %s (needs CEO sign-off)" % (num, clause))
    return blockers


def parse_asr_pin(record_path):
    """P-2 pinned-model observation face (R1302): the git-tracked pin
    record (data/pipeline/asr-pin.json) declares which ASR model weights
    live in the sweep-safe store (data/assets/models/...). Missing
    record = pin not installed (silent: fresh trees, pre-pilot state).
    Record present but any declared weight file gone = disk-sweep
    damage -> WARN (judgment-3 zero-clear alarm)."""
    findings = []
    if not record_path.is_file():
        return findings
    try:
        pin = json.loads(record_path.read_text(encoding="utf-8"))
        base = record_path.parents[2] / pin.get("dir", "")
    except (OSError, ValueError):
        findings.append(("WARN", "asr-pin",
                         "pin record unreadable: %s" % record_path))
        return findings
    for f in pin.get("files", []):
        if not (base / f).is_file():
            findings.append(("WARN", "asr-pin",
                             "pinned ASR model file missing: %s "
                             "(disk-sweep damage? P-2 observation)" % (base / f)))
    return findings


def build_report(template_text, gen_ts, flow, rows, gates, render_rows,
                 needs, suspended, blockers, findings):
    """Fill the template -> report text (data file, Chinese content)."""
    def bullets(seq):
        return "\n".join(seq) if seq else "- none"
    acc_rows = ["| %s | %s | %s |" % (p, s if s else "?", r) for p, s, r in rows]
    gate_rows = ["| %s | %s |" % (n, v if v else "(no GATE line)") for n, v in gates.items()]
    render_lines = ["| %s | %s |" % (n, s if s else MISSING_MARK)
                    for n, s in render_rows]
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


def build_summary(gen_ts, flow, rows, gates, render_rows, needs, suspended,
                  blockers, findings):
    """Compact loop-consumption face (--summary): count lines per source
    plus every blocker/finding in full. ASCII status labels keep the
    routine console safe; the full Chinese report stays the default."""
    lines = ["readiness summary (gen %s)" % gen_ts]
    first = flow[0] if flow else None
    lit = sum(1 for _, s, _ in rows if s and s != first)
    lines.append("- accounts: %d platforms, %d lit beyond first state (%s)"
                 % (len(rows), lit, FLOW_ARROW.join(flow) if flow else "unparsed"))
    counts = OrderedDict()
    for v in gates.values():
        counts[v if v else "(no GATE)"] = counts.get(v if v else "(no GATE)", 0) + 1
    lines.append("- gates: %d drafts -> %s"
                 % (len(gates), ", ".join("%s=%d" % kv for kv in counts.items())))
    st = OrderedDict((k, 0) for k in
                     ("prod-slot", "prod", "superseded", "disposed", "test", "unannot"))
    for _, s in render_rows:
        if s == PRODUCT_SLOT_MARK:
            st["prod-slot"] += 1
        elif s == PRODUCT_MARK:
            st["prod"] += 1
        elif s == SUPERSEDED_MARK:
            st["superseded"] += 1
        elif s == DISPOSED_MARK:
            st["disposed"] += 1
        elif s == TEST_MARK:
            st["test"] += 1
        else:
            st["unannot"] += 1
    lines.append("- renders: %d media -> %s"
                 % (len(render_rows), ", ".join("%s=%d" % kv for kv in st.items())))
    for name, s in render_rows:
        if s is None:
            lines.append("  - unannotated: %s" % name)
    lines.append("- needs-CEO: %d; suspended: %d" % (len(needs), len(suspended)))
    for b in blockers:
        lines.append("- blocker: %s" % b)
    for sev, code, msg in findings:
        lines.append("- [%s] %s: %s" % (sev, code, msg))
    return "\n".join(lines)


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = argv[1:]
    out_path, root, summary = None, REPO, False
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--summary":
            summary = True
            i += 1
        elif args[i] == "--root" and i + 1 < len(args):
            root = Path(args[i + 1])
            i += 2
        else:
            print("usage: python src/readiness.py [--root DIR] [--out FILE] [--summary]")
            return 2
    accounts = root / "docs" / "accounts.md"
    drafts = root / "data" / "drafts"
    renders = root / "output" / "renders"
    backlog = root / "src" / "os" / "backlog.md"
    try:
        flow, rows, findings = parse_accounts(accounts)
        gates, f = parse_gates(drafts)
        findings += f
        never = not_executed_drafts(
            parse_not_executed(root / "data" / "pipeline" /
                               "expert-not-executed-ledger.jsonl"),
            gates,
            parse_review_calls(root / "docs" / "reviews" / "expert-calls.md"))
        if never:
            latest = max(never.values(), key=lambda r: str(r.get("ts", "")))
            findings.append((
                "WARN", "review-not-executed",
                "review face NOT EXECUTED for %d draft(s) [%s]; latest %s: %s"
                % (len(never), ", ".join(sorted(never)),
                   latest.get("ts", "?"), latest.get("reason", "?"))))
        render_rows, f = parse_renders(renders, renders / LEDGER_NAME)
        findings += f
        needs, suspended = parse_backlog_flags(backlog)
        findings += parse_asr_pin(root / "data" / "pipeline" / "asr-pin.json")
        template_text = TEMPLATE.read_text(encoding="utf-8")
    except OSError as e:
        print("source error: %s" % e)
        return 2
    blockers = build_blockers(flow, rows, gates, needs, never)
    gen_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    if summary:
        print(build_summary(gen_ts, flow, rows, gates, render_rows, needs,
                            suspended, blockers, findings))
    else:
        report = build_report(template_text, gen_ts, flow, rows, gates, render_rows,
                              needs, suspended, blockers, findings)
        print(report)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(build_report(template_text, gen_ts, flow, rows, gates,
                                  render_rows, needs, suspended, blockers, findings))
        print("report written: %s" % out_path)
    print("readiness: %d blocker(s), %d finding(s) -> %s"
          % (len(blockers), len(findings),
             "NOT READY" if (blockers or findings) else "READY"))
    return 1 if (blockers or findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
