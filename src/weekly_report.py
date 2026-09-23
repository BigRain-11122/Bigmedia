# -*- coding: utf-8 -*-
"""BigStream weekly report generator (backlog#6, capability C-09).

Ownership: data-analysis dept (org-structure.md M6 lane). Assembles
the weekly ops report from four machine sources - no hand editing:

    src/os/state.json    round log entries inside the ISO week window
    git log              commits authored inside the same window
    src/os/backlog.md    done-in-week items + open item list
    orders/              CEO order files dated inside the window

Encoding rule: this script is pure ASCII. The report itself is a
Chinese data file rendered from src/os/report_template.md - all
Chinese lives in that data file and in the parsed ledgers.

Ledger discipline: reports land in output/reports/ as
weekly-<ISOyear>-W<ww>.md; rerunning a week overwrites the file with
current truth (honesty over history). output/reports/ is un-ignored
in .gitignore; the rest of output/ stays local-only.

Round-entry model: state.json log lines look like
    "2026-09-23 15:36 R1: <one-liner>"
A line whose tail (after date+time) starts with R<n> counts as one
round; "idle" in a round tail marks an idle round; anything else is
bookkeeping (counted separately, never hidden). Entries outside the
week window are excluded on both ends.

Usage:
    python src/weekly_report.py                       # current week
    python src/weekly_report.py ANCHOR_DATE           # e.g. 2026-09-23
    python src/weekly_report.py ANCHOR_DATE OUT_DIR   # explicit output dir

Exit codes: 0 = report written, 2 = usage/source error.
"""
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "src" / "os" / "state.json"
BACKLOG = REPO / "src" / "os" / "backlog.md"
ORDERS = REPO / "orders"
TEMPLATE = REPO / "src" / "os" / "report_template.md"
OUT_DIR = REPO / "output" / "reports"

LOG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*)$")
ROUND_RE = re.compile(r"^R\d+\b")
ITEM_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
DONE_RE = re.compile(r"\[done (\d{4}-\d{2}-\d{2})\]")
ORDER_RE = re.compile(r"^O-(\d{8})-\d{4}-\S+\.md$")
# first-clause cut marks: fullwidth colon, em-dash pair, fullwidth paren, ascii colon
CLAUSE_CUTS = ("\uff1a", "\u2014\u2014", "\uff08", ":")
CLAUSE_CAP = 80

PLACEHOLDERS = (
    "WEEK_LABEL", "GEN_TS", "SINCE", "UNTIL", "ROUNDS", "TICK", "IDLE",
    "OTHER", "COMMITS_N", "DONE_N", "OPEN_N", "ORDERS_N",
    "ROUNDS_LOG", "COMMITS_LOG", "DONE_LOG", "OPEN_LOG", "ORDERS_LOG",
)


def week_bounds(anchor):
    """ISO week window for anchor date -> (monday, sunday, label)."""
    iso = anchor.isocalendar()
    year, week = iso[0], iso[1]
    monday = date.fromisocalendar(year, week, 1)
    return monday, monday + timedelta(days=6), "%04d-W%02d" % (year, week)


def in_window(day_str, since, until):
    """True if day_str (YYYY-MM-DD) parses and lies inside [since, until]."""
    try:
        d = date.fromisoformat(day_str)
    except ValueError:
        return False
    return since <= d <= until


def parse_state(path, since, until):
    """Windowed round stats from state.json.

    Returns dict: tick (current ledger tick), lines (report bullets,
    date + verbatim tail), rounds / idle / other counts.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    lines, rounds, idle, other = [], 0, 0, 0
    for entry in data.get("log", []):
        m = LOG_RE.match(entry.strip())
        if not m or not in_window(m.group(1), since, until):
            continue
        rest = m.group(2).strip()
        parts = rest.split(None, 1)
        tail = parts[1].strip() if len(parts) == 2 else ""
        if ROUND_RE.match(tail):
            rounds += 1
            if "idle" in tail.lower():
                idle += 1
        else:
            other += 1
        lines.append("- %s %s" % (m.group(1), rest))
    return {"tick": data.get("tick"), "lines": lines,
            "rounds": rounds, "idle": idle, "other": other}


def commits_in_window(repo, since, until):
    """git log rows inside the window -> [(hash, date, subject)]."""
    out = subprocess.run(
        ["git", "-C", str(repo), "log",
         "--since", since.isoformat() + " 00:00",
         "--until", until.isoformat() + " 23:59:59",
         "--date=format:%Y-%m-%d %H:%M",
         "--pretty=format:%h%x1f%ad%x1f%s"],
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True)
    rows = []
    for line in out.stdout.splitlines():
        parts = line.split("\x1f")
        if len(parts) == 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def first_clause(body):
    """Short clause of a backlog item for report bullets."""
    body = DONE_RE.sub("", body).replace("**", "")
    cut = len(body)
    for mark in CLAUSE_CUTS:
        i = body.find(mark)
        if i != -1:
            cut = min(cut, i)
    clause = body[:cut].strip()
    if len(clause) > CLAUSE_CAP:
        clause = clause[:CLAUSE_CAP].rstrip() + "..."
    return clause


def parse_backlog(path, since, until):
    """Backlog burn-down -> (done-this-week bullets, open bullets).

    done marker outside the window = done earlier (excluded here);
    no marker = open (suspended items stay open - honest direction).
    """
    done_lines, open_lines = [], []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = ITEM_RE.match(line)
        if not m:
            continue
        num, body = m.group(1), m.group(2).strip()
        dm = DONE_RE.search(body)
        if dm:
            if in_window(dm.group(1), since, until):
                done_lines.append("- #%s %s" % (num, first_clause(body)))
        else:
            open_lines.append("- #%s %s" % (num, first_clause(body)))
    return done_lines, open_lines


def parse_orders(orders_dir, since, until):
    """CEO order files dated inside the window -> sorted filename list."""
    names = []
    if orders_dir.is_dir():
        for p in sorted(orders_dir.iterdir()):
            m = ORDER_RE.match(p.name)
            if not m:
                continue
            raw = m.group(1)
            day = "%s-%s-%s" % (raw[:4], raw[4:6], raw[6:8])
            if in_window(day, since, until):
                names.append(p.name)
    return names


def build_report(template_text, week_label, since, until, state, commits,
                  done_lines, open_lines, order_names, gen_ts):
    """Fill the template -> report text (data file, Chinese content)."""
    def bullets(seq):
        return "\n".join(seq) if seq else "-"
    values = {
        "WEEK_LABEL": week_label,
        "GEN_TS": gen_ts,
        "SINCE": since.isoformat(),
        "UNTIL": until.isoformat(),
        "ROUNDS": str(state["rounds"]),
        "TICK": str(state["tick"]),
        "IDLE": str(state["idle"]),
        "OTHER": str(state["other"]),
        "COMMITS_N": str(len(commits)),
        "DONE_N": str(len(done_lines)),
        "OPEN_N": str(len(open_lines)),
        "ORDERS_N": str(len(order_names)),
        "ROUNDS_LOG": bullets(state["lines"]),
        "COMMITS_LOG": bullets(["- %s %s %s" % r for r in commits]),
        "DONE_LOG": bullets(done_lines),
        "OPEN_LOG": bullets(open_lines),
        "ORDERS_LOG": bullets(["- %s" % n for n in order_names]),
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
    if len(args) > 2:
        print("usage: python src/weekly_report.py [ANCHOR_DATE] [OUT_DIR]")
        return 2
    try:
        anchor = date.fromisoformat(args[0]) if args else date.today()
    except ValueError:
        print("bad anchor date: %r (expected YYYY-MM-DD)" % (args[0],))
        return 2
    out_dir = Path(args[1]) if len(args) >= 2 else OUT_DIR
    monday, sunday, label = week_bounds(anchor)
    try:
        state = parse_state(STATE, monday, sunday)
        commits = commits_in_window(REPO, monday, sunday)
        done_lines, open_lines = parse_backlog(BACKLOG, monday, sunday)
        order_names = parse_orders(ORDERS, monday, sunday)
        template_text = TEMPLATE.read_text(encoding="utf-8")
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        print("source error: %s" % e)
        return 2
    gen_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = build_report(template_text, label, monday, sunday, state,
                          commits, done_lines, open_lines, order_names, gen_ts)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / ("weekly-%s.md" % label)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(report)
    print("weekly report: %s" % out_path)
    print("week %s: %d rounds, %d commits, %d done, %d open, %d orders"
          % (label, state["rounds"], len(commits), len(done_lines),
             len(open_lines), len(order_names)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
