# -*- coding: utf-8 -*-
"""BigStream weekly report generator (backlog#6 + #82 self-drive line,
capability C-09).

Ownership: data-analysis dept (org-structure.md M6 lane). Assembles
the weekly ops report from five machine sources - no hand editing:

    src/os/state.json    round log entries inside the ISO week window
    git log              commits authored inside the same window
    src/os/backlog.md    done-in-week items + open item list
    orders/              CEO order files dated inside the window
    docs/self-improvement-queue.md   section-D proposals filed in window

Self-drive metrics (backlog#82, group order P-2026-09-28-02 item 4):
line-share commit touches (three CEO-named lines + extended lanes),
standby queue rows, nvidia-smi utilization sampled at generation time
(12GB GPU is time-sliced here - instant sample, honest N/A fallback),
declared-idle round count and filed-proposal count, plus the 10-05
first-review criteria table. Every leg degrades to "N/A" instead of
guessing.

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
round; a round TITLED "declared-idle" (or legacy "idle-fast") marks an
idle round - prose mentions inside working rounds do not; anything
else is bookkeeping (counted separately, never hidden). Entries
outside the week window are excluded on both ends.

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
import time
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "src" / "os" / "state.json"
BACKLOG = REPO / "src" / "os" / "backlog.md"
ORDERS = REPO / "orders"
TEMPLATE = REPO / "src" / "os" / "report_template.md"
OUT_DIR = REPO / "output" / "reports"
QUEUE = REPO / "docs" / "self-improvement-queue.md"
CLOUD_ATTR = REPO / "data" / "cloud-attribution.json"
# P-33 collected face, read-side consumption (tech#8, self-drive 7.1):
# BigCompute's machine-level GPU util collector appends one JSONL row per
# ~15 min sample on this host (since 2026-09-28). Cross-repo READ ONLY;
# the file lives outside this repo, so clones/other machines degrade to
# the honest N/A / instant-sample fallback.
GPU_SAMPLES = (REPO.parent.parent / "compute" / "BigCompute" /
               "state" / "gpu-util" / "samples.jsonl")

LOG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*)$")
ROUND_RE = re.compile(r"^R\d+\b")
# idle rounds are counted by title position only: a round titled
# "declared-idle" (current regime, P-20260928-02) or "idle-fast"
# (legacy regime, abolished 2026-09-28) - optional dual-tick prefix
# "R<n>+<m>: hole-double-account+declared-idle". Prose mentions of
# these words inside working-round entries must NOT count (#82 made the
# idle count a hard review criterion, so precision is load-bearing).
IDLE_TITLE_RE = re.compile(
    r"^R\d+(?:\+R?\d+)*\s*(?:[:\uff1a]\s*)?"
    r"(?:\u65ad\u6d1e\u53cc\u8bb0\+)?(declared-)?idle", re.IGNORECASE)
ITEM_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
DONE_RE = re.compile(r"\[done (\d{4}-\d{2}-\d{2})\]")
ORDER_RE = re.compile(r"^O-(\d{8})-\d{4}-\S+\.md$")
# queue section-D scoping for the proposal counter (#82): headings toggle
# the in-D state; inside section D only registry table rows (| P-n | ...)
# count, matched by their window column (ISO week label) - a proposal is
# counted for the week it was filed for, regardless of pilot status
QUEUE_SECTION_D_RE = re.compile(r"^##\sD\b")
QUEUE_SECTION_RE = re.compile(r"^##\s")
PROPOSAL_ROW_RE = re.compile(r"^\|\s*P-\d+\s*\|")
# content-line classification for the self-drive share (#82): the three
# CEO-named lines plus the two extended lanes; ledgers, docs and tmp
# evidence fall outside every prefix and count as tooling (no line).
# One commit may touch several lines, so touch counts overlap by design
# and need not sum to the commit total.
LINE_RULES = (
    ("novel", ("data/storylines/novel/",)),
    ("audio", ("data/storylines/audio/",)),
    ("comic", ("data/storylines/comic/",)),
    ("video", ("data/sources/", "data/drafts/", "data/storylines/video/",
               "output/renders/")),
    ("cards", ("data/storylines/cards/",)),
)
# first-clause cut marks: fullwidth colon, em-dash pair, fullwidth paren, ascii colon
CLAUSE_CUTS = ("\uff1a", "\u2014\u2014", "\uff08", ":")
CLAUSE_CAP = 80

PLACEHOLDERS = (
    "WEEK_LABEL", "GEN_TS", "SINCE", "UNTIL", "ROUNDS", "TICK", "IDLE",
    "OTHER", "COMMITS_N", "DONE_N", "OPEN_N", "ORDERS_N",
    "NOVEL_N", "NOVEL_P", "AUDIO_N", "AUDIO_P", "COMIC_N", "COMIC_P",
    "EXT_N", "EXT_P", "GPU_MEAN", "GPU_N", "GPU_MAX", "GPU_INSTANT",
    "PROPOSALS_N", "CLOUD_LINE",
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
            if IDLE_TITLE_RE.match(tail):
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


def parse_line_touch(stdout):
    """Parse `git log --name-only` output -> (total, per-line touch counts).

    Entries are separated by the \\x1e commit marker emitted via
    --pretty=format:%x1e%H; the first non-empty line of each entry is
    the commit hash, the rest are file paths (git emits forward slashes).
    """
    counts = dict.fromkeys([name for name, _ in LINE_RULES], 0)
    total = 0
    for entry in stdout.split("\x1e"):
        rows = [ln.strip() for ln in entry.splitlines() if ln.strip()]
        if not rows:
            continue
        total += 1
        for name, prefixes in LINE_RULES:
            for path in rows[1:]:
                if path.startswith(prefixes):
                    counts[name] += 1
                    break
    return total, counts


def commits_line_touch(repo, since, until):
    """Windowed commit count + per-line touch counts (self-drive #82)."""
    out = subprocess.run(
        ["git", "-C", str(repo), "-c", "core.quotepath=false", "log",
         "--name-only",
         "--since", since.isoformat() + " 00:00",
         "--until", until.isoformat() + " 23:59:59",
         "--pretty=format:%x1e%H"],
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True)
    return parse_line_touch(out.stdout)


def _gpu_query():
    """One nvidia-smi utilization probe -> [int] or None."""
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    vals = []
    for tok in r.stdout.strip().splitlines():
        tok = tok.strip().rstrip("%")
        if tok.isdigit():
            vals.append(int(tok))
    return vals or None


def gpu_util_mean(samples=5, delay=1.0, query=None):
    """Mean GPU utilization sampled at generation time (or None).

    Instant sampling only - a weekly mean cannot be reconstructed
    honestly from one probe, so the report labels it as a generation
    -time sample. The 12GB card is time-sliced on this machine.
    """
    query = query or _gpu_query
    vals = []
    for i in range(samples):
        got = query()
        if got:
            vals.extend(got)
        if i < samples - 1:
            time.sleep(delay)
    if not vals:
        return None
    return int(round(sum(vals) / float(len(vals))))


def gpu_ledger_weekly(path, since, until):
    """Weekly GPU utilization stats from the P-33 collector ledger.

    Rows look like {"ts": "YYYY-MM-DDTHH:MM:SS", "util_pct": 4.0, ...};
    rows dated inside [since, until] feed a sample-count-weighted weekly
    mean (honest replacement for the old generation-time-only probe).
    Malformed/out-of-window lines are skipped, never guessed; a missing
    or unreadable ledger returns None (report prints N/A).
    """
    try:
        rows = path.read_text(encoding="utf-8",
                              errors="replace").splitlines()
    except OSError:
        return None
    vals = []
    for line in rows:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not in_window(str(rec.get("ts", ""))[:10], since, until):
            continue
        v = rec.get("util_pct")
        if isinstance(v, (int, float)):
            vals.append(float(v))
    if not vals:
        return None
    return {"mean": int(round(sum(vals) / len(vals))),
            "n": len(vals), "max": int(round(max(vals)))}


def cloud_attribution(path=CLOUD_ATTR):
    """Cloud billing-task line from the local attribution ledger share
    (C-20260929-01 A/B dispatch item 3; L1 script, zero LLM).

    data/cloud-attribution.json holds this company's share of the
    group attribution ledger: per-entity billing task counts inside
    the recorded window. Missing/invalid file degrades to None (the
    report prints N/A) instead of guessing.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = []
        for ent in data.get("entities", []):
            name = str(ent.get("entity", "?"))
            n = ent.get("billing_tasks_window")
            if not isinstance(n, int):
                continue
            rows.append("%s %d" % (name, n))
        if not rows:
            return None
        return "; ".join(rows)
    except (OSError, ValueError):
        return None


def proposal_count(queue_path, week_label):
    """Self-drive proposals filed for the ISO week (section D registry).

    Counted from the section-D table rows whose window column equals
    week_label - filing counts, pilot status does not filter.
    """
    if not queue_path.is_file():
        return None
    count, in_d = 0, False
    for line in queue_path.read_text(encoding="utf-8",
                                     errors="replace").splitlines():
        if QUEUE_SECTION_RE.match(line):
            in_d = bool(QUEUE_SECTION_D_RE.match(line))
            continue
        if not in_d or not PROPOSAL_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] == week_label:
            count += 1
    return count


def collect_selfdrive(repo, queue_path, since, until, week_label):
    """Self-drive metric inputs (#82): line touches, GPU, proposals.

    Each leg degrades to None ("N/A" in the report) instead of guessing.
    """
    sd = {"total": None, "novel": None, "audio": None, "comic": None,
          "video": None, "cards": None, "gpu": None, "gpu_ledger": None,
          "proposals": None, "cloud": None}
    try:
        total, counts = commits_line_touch(repo, since, until)
        sd["total"] = total
        for name, _ in LINE_RULES:
            sd[name] = counts[name]
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    sd["gpu_ledger"] = gpu_ledger_weekly(GPU_SAMPLES, since, until)
    sd["gpu"] = gpu_util_mean()
    sd["proposals"] = proposal_count(queue_path, week_label)
    sd["cloud"] = cloud_attribution()
    return sd


def build_report(template_text, week_label, since, until, state, commits,
                  done_lines, open_lines, order_names, sd, gen_ts):
    """Fill the template -> report text (data file, Chinese content)."""
    def bullets(seq):
        return "\n".join(seq) if seq else "-"
    total = sd.get("total")
    ext = None
    if sd.get("video") is not None or sd.get("cards") is not None:
        ext = (sd.get("video") or 0) + (sd.get("cards") or 0)

    def _count_n(key):
        return "N/A" if sd.get(key) is None else str(sd[key])

    def _count_p(key):
        v = sd.get(key)
        if v is None or not total:
            return "N/A"
        return "%d%%" % int(round(100.0 * v / total))

    led = sd.get("gpu_ledger") or {}

    def _led(key):
        v = led.get(key)
        return "N/A" if v is None else str(v)

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
        "NOVEL_N": _count_n("novel"), "NOVEL_P": _count_p("novel"),
        "AUDIO_N": _count_n("audio"), "AUDIO_P": _count_p("audio"),
        "COMIC_N": _count_n("comic"), "COMIC_P": _count_p("comic"),
        "EXT_N": "N/A" if ext is None else str(ext),
        "EXT_P": "N/A" if ext is None or not total else
                 "%d%%" % int(round(100.0 * ext / total)),
        "GPU_MEAN": _led("mean"), "GPU_N": _led("n"),
        "GPU_MAX": _led("max"),
        "GPU_INSTANT": "N/A" if sd.get("gpu") is None else str(sd["gpu"]),
        "PROPOSALS_N": "N/A" if sd.get("proposals") is None
                       else str(sd["proposals"]),
        "CLOUD_LINE": "N/A" if sd.get("cloud") is None else str(sd["cloud"]),
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
        sd = collect_selfdrive(REPO, QUEUE, monday, sunday, label)
        template_text = TEMPLATE.read_text(encoding="utf-8")
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        print("source error: %s" % e)
        return 2
    gen_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = build_report(template_text, label, monday, sunday, state,
                          commits, done_lines, open_lines, order_names, sd,
                          gen_ts)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / ("weekly-%s.md" % label)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(report)
    print("weekly report: %s" % out_path)
    print("week %s: %d rounds, %d commits, %d done, %d open, %d orders"
          % (label, state["rounds"], len(commits), len(done_lines),
             len(open_lines), len(order_names)))
    ext = None
    if sd.get("video") is not None or sd.get("cards") is not None:
        ext = (sd.get("video") or 0) + (sd.get("cards") or 0)
    led = sd.get("gpu_ledger") or {}
    print("self-drive: novel=%s audio=%s comic=%s ext=%s gpu_ledger=%s"
          " gpu_instant=%s idle=%d proposals=%s"
          % (sd.get("novel"), sd.get("audio"), sd.get("comic"), ext,
             led or "N/A", sd.get("gpu"), state["idle"], sd.get("proposals")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
