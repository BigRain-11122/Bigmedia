"""AIHOT window-read probe: poison-proof title channel (tech#159).

Gap anchor (R2231 authoritative-window read): the cross-source top-N section
died with "invalid byte sequence for encoding UTF8" on left(title, N) style
clipping. R2235 forensics (both psql and node-pg channels) nailed the
empirical law:

- Character-clipping text functions (left() / substring(x FROM a FOR b), with
  or without COLLATE "C") throw "invalid byte sequence" on this DB
  INTERMITTENTLY across (row, length, query-shape) triples, always citing a
  CJK lead byte, while the very same titles decode perfectly with python's
  strict UTF-8 decoder and pass plain SELECT / length / octet_length /
  upper / LIKE / equality / ORDER BY. The throw is server-side (identical via
  node-pg). Root cause is a server/collation interaction, not broken data.
- `encode(col::bytea,'hex')` NEVER throws, on every tested shape (full-table
  join, 4518-row scored scan, single-row, top-N). Hex transport + client-side
  tolerant decode is therefore the only structurally reliable title channel.

Channel laws baked in:
- psql argv GBK law: SQL sent on the command line must be pure ASCII
  (CJK literals get mangled by the Windows ANSI codepage face). assert_ascii
  is a hard gate, and all queries here are ASCII-only (source ids are ASCII).
- Hex transport (not base64): base64 output wraps at 76 chars and corrupts
  naive row parsing (R2235 false-positive census lesson).
- Read-only face: SELECT-only queries; the worker/stack is never touched.

Sections (A-E window on analyses.created_at; F windows on publications.timeline_at,
the column composeDaily judgedReports actually consults; tz Asia/Shanghai):
  A per-source scored/max/ge60/ge55/selected census           (created_at face)
  B focus-source top-N (score, selected, title)                (created_at face)
  C top-N any-source (score, source, title)  <- previously broken read (created_at face)
  D selected ledger (+ prompt_version = tech#92 anchor-version evidence) (created_at face)
  E focus-source score bands                                   (created_at face)
  F judged-window total + per-source census (timeline_at face; tech#179)

tech#179 semantics law: A-E measure the analysis pipeline face (when analyses
rows were created). F mirrors judgedReports in reports/edition.ts exactly —
publications p WHERE visibility='public' AND eligible AND (NOT selected OR
visible_after <= end) AND score IS NOT NULL AND NOT backfill AND
timeline_at in [start,end). It is the count behind the daily
"nothing judged in its window" throw. Predicting daily green/red from A
caused the R2283 forecast/empiricism fork; consumers must read F for that.

rc contract: 0 = all sections ran (bad_utf8 markers are data annotations,
not failures), 1 = one or more sections errored (ERR lines kept per section),
2 = usage/psql-unreachable (zero sections ran).
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PSQL = os.path.join(REPO_ROOT, "data", "assets", "aihot-poc", "pg17",
                    "pgsql", "bin", "psql.exe")
DSN = "postgres://aihot@127.0.0.1:55432/aihot"
DEFAULT_SOURCE = "json-zhihu-hot"
DEFAULT_EVIDENCE_DIR = os.path.join(REPO_ROOT, "data", "pipeline", "aihot-evidence")


def assert_ascii(sql):
    """Hard gate: non-ASCII SQL dies before it can mangle via psql argv."""
    for ch in sql:
        if ord(ch) > 127:
            raise ValueError("non-ascii SQL char %r (psql argv GBK law)" % ch)


def run_query(runner, sql, timeout=180):
    assert_ascii(sql)
    return runner(sql, timeout)


def default_runner(sql, timeout):
    env = dict(os.environ)
    env["PGCLIENTENCODING"] = "UTF8"
    env["PGTZ"] = "Asia/Shanghai"
    p = subprocess.run([PSQL, DSN, "-A", "-t", "-v", "ON_ERROR_STOP=1",
                        "-P", "null=NULL", "-c", sql],
                       capture_output=True, timeout=timeout, env=env)
    out = p.stdout.decode("utf-8", "replace")
    err = ""
    if p.returncode:
        err = p.stderr.decode("utf-8", "replace").strip().splitlines()[-1][:200]
    return p.returncode, out, err


def decode_hex_title(hexstr):
    """Hex -> tolerant UTF-8 text + bad-byte flag (never raises)."""
    try:
        raw = bytes.fromhex(hexstr.strip())
    except ValueError:
        return "<HEX-ERR>", True
    text = raw.decode("utf-8", errors="replace")
    return text, ("\ufffd" in text)


def _win(since, until):
    return ("a.created_at >= '%s' AND a.created_at < '%s'" % (since, until))


def _pub_win(since, until):
    return ("p.timeline_at >= '%s' AND p.timeline_at < '%s'" % (since, until))


def _judged_face(since, until):
    """WHERE of judgedReports (reports/edition.ts) verbatim: the count the
    daily 'nothing judged in its window' throw consults (tech#179)."""
    return ("p.visibility = 'public' AND p.eligible "
            "AND (NOT p.selected OR p.visible_after <= '%s') "
            "AND p.score IS NOT NULL AND NOT p.backfill AND %s"
            % (until, _pub_win(since, until)))


def section_a(since, until):
    return ("SELECT art.source_id, count(*), max(a.score), "
            "count(*) FILTER (WHERE a.score >= 60), "
            "count(*) FILTER (WHERE a.score >= 55), "
            "count(*) FILTER (WHERE a.selected) "
            "FROM analyses a JOIN articles art ON art.id = a.article_id "
            "WHERE a.score IS NOT NULL AND %s "
            "GROUP BY art.source_id ORDER BY art.source_id;" % _win(since, until))


def section_b(since, until, source, top):
    return ("SELECT a.score, a.selected, encode(art.title::bytea,'hex') "
            "FROM analyses a JOIN articles art ON art.id = a.article_id "
            "WHERE a.score IS NOT NULL AND art.source_id = '%s' AND %s "
            "ORDER BY a.score DESC LIMIT %d;"
            % (source, _win(since, until), top))


def section_c(since, until, top):
    return ("SELECT a.score, art.source_id, encode(art.title::bytea,'hex') "
            "FROM analyses a JOIN articles art ON art.id = a.article_id "
            "WHERE a.score IS NOT NULL AND %s "
            "ORDER BY a.score DESC LIMIT %d;" % (_win(since, until), top))


def section_d(since, until):
    return ("SELECT a.score, art.source_id, a.prompt_version, a.created_at, "
            "encode(art.title::bytea,'hex') "
            "FROM analyses a JOIN articles art ON art.id = a.article_id "
            "WHERE a.selected AND %s "
            "ORDER BY a.created_at DESC;" % _win(since, until))


def section_e(since, until, source):
    return ("SELECT floor(a.score)::int, count(*) "
            "FROM analyses a JOIN articles art ON art.id = a.article_id "
            "WHERE a.score IS NOT NULL AND art.source_id = '%s' AND %s "
            "GROUP BY 1 ORDER BY 1 DESC;" % (source, _win(since, until)))


def section_f_total(since, until):
    """Exact mirror of judgedReports(start,end): one number, timeline_at face."""
    return ("SELECT count(*) FROM publications p WHERE %s;"
            % _judged_face(since, until))


def section_f_census(since, until):
    """Same shape as section A, but on the judged (timeline_at) face, so
    A vs F reads side-by-side as the dual-window comparison."""
    return ("SELECT p.source_id, count(*), max(p.score), "
            "count(*) FILTER (WHERE p.score >= 60), "
            "count(*) FILTER (WHERE p.score >= 55), "
            "count(*) FILTER (WHERE p.selected) "
            "FROM publications p WHERE %s "
            "GROUP BY p.source_id ORDER BY p.source_id;"
            % _judged_face(since, until))


def _rows(out):
    return [ln for ln in out.strip().splitlines() if ln]


def render_section(header, lines, bad_count):
    body = "\n".join(lines)
    tail = "" if not bad_count else "\n[bad_utf8 rows in section: %d]" % bad_count
    return "== %s ==\n%s%s" % (header, body if body else "(no rows)", tail)


def collect(runner, since, until, source, top):
    """Run all five sections; return (report_text, errs, bad_total).

    Each spec row: (header, sql, hex_field_index or None, line_formatter).
    hex_field_index names the encode(...,'hex') column so the bad-byte count
    is exact per row (C/D carry hex titles; A/E carry none).
    """
    parts, errs, bad_total = [], [], 0

    spec = [
        ("A per-source", section_a(since, until), None,
         lambda f: json.dumps({
             "source_id": f[0], "scored": f[1], "max_score": f[2],
             "ge60": f[3], "ge55": f[4], "selected_n": f[5]}, ensure_ascii=False)),
        ("B %s top" % source, section_b(since, until, source, top), 2,
         lambda f, t: json.dumps({
             "score": f[0], "selected": f[1], "title": t}, ensure_ascii=False)),
        ("C top%d any" % top, section_c(since, until, top), 2,
         lambda f, t: json.dumps({
             "score": f[0], "source_id": f[1], "title": t,
             "bad_utf8": "\ufffd" in t}, ensure_ascii=False)),
        ("D selected_ledger", section_d(since, until), 4,
         lambda f, t: json.dumps({
             "score": f[0], "source_id": f[1],
             "prompt_version": None if f[2] == "NULL" else f[2],
             "created_at": f[3], "title": t}, ensure_ascii=False)),
        ("E %s band" % source, section_e(since, until, source), None,
         lambda f: json.dumps({"s_band": f[0], "count": f[1]})),
        ("F judged_total (timeline_at face)", section_f_total(since, until), None,
         lambda f: json.dumps({"judged_total": f[0]})),
        ("F judged_census (timeline_at face)", section_f_census(since, until), None,
         lambda f: json.dumps({"source_id": f[0], "judged": f[1],
                               "max_score": f[2], "ge60": f[3],
                               "ge55": f[4], "selected_n": f[5]})),
    ]

    for header, sql, hex_idx, fmt in spec:
        rc, out, err = run_query(runner, sql)
        if rc:
            errs.append(header)
            parts.append("== %s == ERR %s" % (header, err))
            continue
        bad, lines = 0, []
        for ln in _rows(out):
            fields = ln.split("|")
            title, row_bad = (None, False)
            if hex_idx is not None:
                if len(fields) <= hex_idx:
                    continue
                title, row_bad = decode_hex_title(fields[hex_idx])
                bad += 1 if row_bad else 0
                lines.append(fmt(fields, title))
            else:
                lines.append(fmt(fields))
        bad_total += bad
        parts.append(render_section(header, lines, bad))

    head = ("== AIHOT window read (since %s -> until %s, tz Asia/Shanghai) ==\n"
            "window semantics: A-E = analyses.created_at (tool/analysis face); "
            "F = publications.timeline_at (composeDaily judgedReports face - "
            "the count behind the daily nothing-judged throw). "
            "Daily green/red prediction reads F, not A (tech#179, R2283 fork lesson)."
            % (since, until))
    return "\n\n".join([head] + parts), errs, bad_total


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    default_since = (datetime.datetime.now()
                     - datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
    ap.add_argument("--since", default=default_since, help="window start YYYY-MM-DD HH:MM")
    ap.add_argument("--until", default=now, help="window end YYYY-MM-DD HH:MM")
    ap.add_argument("--source", default=DEFAULT_SOURCE, help="focus source id")
    ap.add_argument("--top", type=int, default=15, help="top-N for B/C sections")
    ap.add_argument("--out", default=None, help="evidence file (UTF-8 no BOM)")
    args = ap.parse_args(argv)

    out_path = args.out or os.path.join(
        DEFAULT_EVIDENCE_DIR,
        "window-read_%s_%s.txt" % (args.since.replace(":", "").replace(" ", "_"),
                                   args.until.replace(":", "").replace(" ", "_")))
    try:
        report, errs, bad_total = collect(default_runner, args.since,
                                          args.until, args.source, args.top)
    except (subprocess.TimeoutExpired, OSError) as e:
        print("psql unreachable: %s" % e)
        return 2

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(report + "\n")
    print("wrote %s sections=%d bad_utf8_rows=%d errs=%d"
          % (out_path, 7, bad_total, len(errs)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
