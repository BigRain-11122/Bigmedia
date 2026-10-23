# -*- coding: utf-8 -*-
"""Group-transfer scan probe -- fixed single-truth face for the task-book
group-scan step (state/queue/tech#50).

Why (R1849 + R1879 incident family): the group-scan step used to be rebuilt
as an ad-hoc python one-liner every round, and two regex slips produced
false-quiet readings (R1849: a ``2026\\d{3}`` month-face pattern missed the
1010+ date family; R1879: a two-digit-month pattern failed the whole 8-digit
date family and read CUR=0 as quiet). This probe locks the dnum regex to the
8-digit date family, diffs the token set against the state watermark, and
FAILS loudly on read errors instead of falling back silent
(PT-20260928-01 family).

Faces:
  DECISIONS  dnum watermark diff (TRULY_NEW breaks silence -> rc 1;
            watermark-only tokens are the slim/inline-consumed family and
            are never reported as new)
  LEDGER     transfer-marker line anchors (@BigStream family + the
            @七线全司/@全司/@六司/@八线全量 patrol markers)
  ORDERS     HQ orders.md row watermark (tech#103): |-row count + last-row
            first-cell fingerprint vs state.json orders_row_watermark
            {rows, tail_key}; any deviation breaks silence (rc 1); a
            MISSING watermark is first-run rc 1 with a watermark-missing
            note (consume-then-store once). Root fix: R1975-R1977 rounds
            judged the orders face quiet by mtime-anchor MEMORY comparison
            while three new CEO rows had not yet landed in the local tree
            -- the orders face had no content-addressing judgment at all
            (structural second-class citizen vs the decisions dnum
            watermark).
  DIGEST-SUPPLY  supply-gap advisory backstop for the DIGEST 史源 trigger
            law (#67, tech#129): orders-row dates NEWER than the latest
            DIGEST card date that have sat unconsumed for >2 days break
            silence as a WARN. Historical root: R870/R1095/R1303/R1536/
            R2050 -- five manual "supply-blindspot correction" rounds
            where a new CEO-order cluster dropped and no round re-derived
            it into the DIGEST pool. Machine = hint surface only; the
            creative judgment (A-grade + number-density grading) stays
            with the loop body (no-auto-trigger law). Day-granularity
            note: same-day-evening clusters (e.g. 10-11 晚 vs v18 10-11)
            are below this face's resolution -- the >2d WARN is the
            chronic-blindness backstop, the age<=2d advisory line keeps
            the unconsumed cluster in per-round view. tech#202 (R2337
            anchor) closes the same-day hole two ways: the "latest card"
            orders by captured vNN (v22 no longer shadows v23 by
            iteration order), and coverage is ALSO judged row-level
            against the card's cards.json consumption frontier ("rows
            N-M") -- rows beyond the frontier surface as advisory even
            when same-day, and escalate to WARN via their row dates once
            past the threshold. Cards dir missing = face inactive
            (quiet) -- the DIGEST production line itself is absent then.
  ORDERS-ORIGIN-DELTA  origin-only rows advisory (tech#133, R2059/R2064):
            git fetch + git show origin/main row count vs the worktree
            count (D-20261001-03 read-only consumption canon). origin >
            worktree = rows the canonical worktree face cannot see ->
            WARN breaks silence (consume via git show NOW; D-13 SLA must
            not wait for the FleetLink pull window). Root: R2059 caught
            one origin-only row by manual luck; R2064 found the SAME row
            still origin-only ~3h later (the "pull-in-flight ~40min"
            hypothesis disproven -- durable worktree gap), plus the
            17:4x 鬼相排查令 which the worktree face only gained minutes
            after origin had it. Any git/network failure degrades to the
            worktree-only behavior (pre-registered) -- never a probe
            FAIL.             Real git binary only: the PATH git on this machine is
            the gitsilent stdout-swallowing wrapper, which would read as
            0 rows and silently kill the face (R-1952 family).
            tech#208 (R2341 anchor): dual readings -- anchor-count
            (content face) is reported side by side with delta (count
            face); divergence classifies into insert-family vs
            edit-family candidates (a worktree row whose content
            origin lacks pairs with one anchor). Count-quiet with
            content edits stays rc-quiet with an advisory note.
  MTIME      HQ orders/decisions/ledger anchors + own orders newest file

Usage:
    python src/os/group_scan.py                # print full report
    python src/os/group_scan.py --out FILE      # + UTF-8 (no BOM) evidence
    python src/os/group_scan.py --out FILE --echo

Exit codes: 0 quiet / 1 new dnum tokens / 2 usage error / 3 face read
error. Task-book wiring of this probe is an operator-domain submission
(mandate); the loop itself does not edit the mandate file.
"""

import io
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _orders_stat(root):
    """(dev, ino, mtime, path) for <root>/docs/orders.md, or None."""
    path = Path(root) / "docs" / "orders.md"
    try:
        stat = path.stat()
    except OSError:
        return None
    return (stat.st_dev, stat.st_ino, stat.st_mtime, path)


def pick_group_root(primary, extra=None, env_root=None):
    """Return (root, note) for the group tree that actually holds the news.

    R2422 anchor: this machine carries two FluxGroup path forms -- the live
    tree (Desktop) and a stale mirror (D:). The script path decides which one
    REPO.parent.parent names, so a round launched through the mirror read a
    10-21 orders.md while the canonical tree already held 10-23 CEO rows: the
    worktree face reported QUIET and the ORDERS-ORIGIN-DELTA face could not
    see them either (origin/main was still behind). Picking the tree with the
    newest orders.md -- and saying so loud -- removes that blind spot.
    Explicit env root wins outright; identical files never produce a note.
    """
    primary = Path(primary)
    keys = {}
    for cand in [env_root, primary] + list(extra or []):
        if not cand:
            continue
        key = _orders_stat(cand)
        if key is None:
            continue
        keys.setdefault(key[:2], (Path(cand), key))
    if not keys:
        return primary, None
    if env_root:
        env_key = _orders_stat(env_root)
        if env_key is not None:
            return Path(env_root), None
    primary_key = _orders_stat(primary)
    if primary_key is None:
        cand, key = max(keys.values(), key=lambda v: v[1][2])
        return cand, ("primary %s has no docs/orders.md; using %s"
                      % (primary, cand))
    best = max(keys.values(), key=lambda v: v[1][2])
    if best[1][:2] == primary_key[:2]:
        return primary, None
    if best[1][2] <= primary_key[2]:
        return primary, None
    hours = (best[1][2] - primary_key[2]) / 3600.0
    note = ("using %s (orders.md %.1fh newer than primary %s; a stale mirror "
            "read hides new CEO rows)" % (best[0], hours, primary))
    return best[0], note


_PRIMARY_GROUP_ROOT = REPO.parent.parent
GROUP_ROOT, GROUP_ROOT_NOTE = pick_group_root(
    _PRIMARY_GROUP_ROOT,
    extra=[Path.home() / "Desktop" / "FluxGroup"],
    env_root=os.environ.get("FLUX_GROUP_ROOT") or None,
)
# Alias candidates are machine-local (bm-a keeps a Desktop copy next to the
# mirror); on hosts without them the picker degrades to the primary root.

# 8-digit date family (YYYYMMDD). The two incident patterns (2026\d{3} and a
# 2-digit-month face) both under-matched real dnums; this one is locked by
# tests/test_group_scan.py regression cases.
DNUM_RE = re.compile(r"\b[DC]-20\d{6}-\d{1,3}(?!\d)")
# Orders first-cell date shapes: "10-12 13:5x" (MM-DD, current year assumed)
# and the full-date "2026-09-28 18:1x" family (6 live rows). Full-date arm
# first so the 2-digit face cannot steal a slice of it.
ORDERS_CELL_DATE_RE = re.compile(
    r"^(20\d{2})-(\d{2})-(\d{2})(?!\d)|^(\d{2})-(\d{2})(?!\d)")
# DIGEST card dir name: MC-YYYYMMDD-DIGEST-vNN[-tmp]. -tmp staging dirs are a
# legitimate consumption signal (CPU pre-stage counts -- the cluster has been
# derived even while the F-registration waits for a GPU fire window). The
# vNN number is captured (tech#202): same-date cards must order by version,
# not by directory iteration order (R2337 anchor: v22/v23 same-day pair
# reported v22 as "latest" while v23 + F-193 were already in the ledger).
DIGEST_CARD_RE = re.compile(r"^MC-(20\d{2})(\d{2})(\d{2})-DIGEST-v(\d+)")
DIGEST_SUPPLY_GAP_DAYS = 2
# tech#202 (R2337 anchor): a card's cards.json meta declares its consumed
# orders row range ("rows 514-521"); the range END is the row-level
# consumption frontier. Requires the literal "row"/"rows" prefix so sibling
# window notes ("（455-514·60 行）") never pose as consumption claims.
CARD_ROWS_RANGE_RE = re.compile(r"\brows?\s*(\d{1,4})\s*[-–—~]\s*(\d{1,4})")
# Only whitespace / list / heading markers may precede a row-anchored token.
ANCHOR_PREFIX_RE = re.compile(r"^(?:\s|[-*#>]+|\d{1,3}[.)])*$")
LEDGER_MARKERS = ("@BigStream", "@七线全司", "@全司", "@六司", "@八线全量")
PREVIEW_LEN = 110
# tech#165 (R2241 seed): origin-only rows echo a content anchor so the
# consuming round quotes verbatim content, never a guessed identity.
ORIGIN_ANCHOR_PREVIEW_LEN = 80
ORIGIN_ANCHOR_CAP = 5
# tech#133 (R2059/R2064): real git binaries only -- the PATH git on this
# machine is the gitsilent stdout-swallowing wrapper (R-1952), which would
# read as 0 rows and silently kill the origin face.
GIT_CANDIDATES = (
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
)
GIT_FETCH_TIMEOUT_S = 20

RC_QUIET, RC_NEW, RC_USAGE, RC_READ_FAIL = 0, 1, 2, 3
USAGE = ("usage: python src/os/group_scan.py [--out FILE] [--echo] "
         "[--decisions P] [--hq-orders P] [--ledger P] "
         "[--own-orders-dir P] [--state P] [--cards-dir P] "
         "[--check-anchor-file P]")

DEFAULTS = {
    "decisions": GROUP_ROOT / "docs" / "decisions.md",
    "hq_orders": GROUP_ROOT / "docs" / "orders.md",
    "ledger": GROUP_ROOT / "cph4" / "evolution-ledger.md",
    "own_orders_dir": REPO / "orders",
    "state": REPO / "src" / "os" / "state.json",
    "cards_dir": REPO / "data" / "storylines" / "cards",
}


def read_text(path):
    """Return (text, mtime_str, size); raise OSError so callers FAIL loud."""
    path = Path(path)
    stat = path.stat()
    with io.open(str(path), encoding="utf-8-sig", errors="replace") as fh:
        text = fh.read()
    mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return text, mtime, stat.st_size


def extract_dnums(text):
    """Token set over the 8-digit date family (R1849/R1879 regression lock)."""
    return set(DNUM_RE.findall(text))


def is_anchor_prefix(prefix):
    """True when only whitespace/list/heading markers precede the token."""
    return ANCHOR_PREFIX_RE.match(prefix) is not None


def classify_tokens(text):
    """token -> 'row' | 'inline' (inline-only = pseudo-diff annotation)."""
    kinds = {}
    for line in text.splitlines():
        for match in DNUM_RE.finditer(line):
            token = match.group(0)
            if kinds.get(token) == "row":
                continue
            kinds[token] = "row" if is_anchor_prefix(line[:match.start()]) else "inline"
    return kinds


def diff_watermark(cur_tokens, watermark):
    """(truly_new, wm_only): watermark-only tokens are slim/inline-consumed."""
    wm = set(watermark)
    cur = set(cur_tokens)
    return sorted(cur - wm), sorted(wm - cur)


def load_watermark(state_path):
    """Watermark dnum list from state.json; missing field = empty (loud side)."""
    with io.open(str(state_path), encoding="utf-8") as fh:
        data = json.load(fh)
    return list(data.get("decisions_watermark", {}).get("dnums", []))


def load_orders_watermark(state_path):
    """{rows, tail_key} from state.json; missing/bad shape -> None.

    None is the loud side: face_orders then reports watermark-missing and
    breaks silence (first-run consume-then-store semantics, tech#103).
    """
    with io.open(str(state_path), encoding="utf-8") as fh:
        data = json.load(fh)
    wm = data.get("orders_row_watermark")
    if not isinstance(wm, dict) or "rows" not in wm or "tail_key" not in wm:
        return None
    return {"rows": wm.get("rows"), "tail_key": wm.get("tail_key")}


def _orders_first_cell(line):
    """First cell of a |-row (caller guarantees the leading '|')."""
    rest = line.strip()[1:]
    nxt = rest.find("|")
    cell = rest if nxt < 0 else rest[:nxt]
    return cell.strip()


def orders_row_stats(text):
    """(rows, tail_key) over the |-row family (tech#103 fingerprint).

    rows counts every line whose first non-space char is '|'; tail_key is
    the first cell of the LAST such row. Appends bump rows and (almost
    always) move tail_key; removals bump rows down; last-row edits move
    tail_key. Any deviation from the stored watermark breaks silence
    (fail-closed direction, tech#50 philosophy).
    """
    rows = 0
    tail_key = ""
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            rows += 1
            tail_key = _orders_first_cell(line)
    return rows, tail_key


def current_orders_watermark(hq_orders_path=None):
    """Turnkey {rows, tail_key} for the close step (consumption anchor).

    CAUTION (tech#251, R2393 anchor): this reads the file's CURRENT
    mechanical value. Passing it to finalize_state at CLOSE time is the
    heal-race trap: FleetLink can heal rows into the worktree after the
    round's scan, and the stored watermark then absorbs never-scanned
    rows (rows 616-617 escaped every ORDERS-NEW diff that way). The
    close step must pass the round-START group_scan ORDERS-face boundary
    (the "current: rows=N | tail_key=..." line captured at round open),
    optionally double-checked by finalize_state's orders_wm_scanned
    guard. This helper stays for probes/echo faces only - not a
    finalize_state turnkey.
    """
    path = Path(hq_orders_path) if hq_orders_path else DEFAULTS["hq_orders"]
    text, _, _ = read_text(path)
    rows, tail_key = orders_row_stats(text)
    return {"rows": rows, "tail_key": tail_key}


def orders_row_dates(text, year=None):
    """Set of dates parsed from orders |-row first cells (tech#129 face).

    Both live shapes: "10-12 13:5x" (MM-DD, ``year`` assumed = current
    year -- the orders file is a rolling 2026 ledger) and the full-date
    "2026-09-28 18:1x" family. Non-date cells (header/separator) yield
    nothing.
    """
    if year is None:
        year = datetime.now().year
    found = set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cell = _orders_first_cell(line)
        match = ORDERS_CELL_DATE_RE.match(cell)
        if not match:
            continue
        if match.group(1):
            found.add(date(int(match.group(1)), int(match.group(2)),
                           int(match.group(3))))
        else:
            found.add(date(year, int(match.group(4)), int(match.group(5))))
    return found


def latest_digest_card(cards_dir):
    """(date, dir_name) of the newest MC-YYYYMMDD-DIGEST-vNN card, or None.

    Ordering is (date, version, non-tmp): same-date cards compare by the
    captured vNN first (tech#202 -- iteration order used to let v22 shadow
    v23); staging dirs (``-tmp`` suffix) are valid consumption signal and
    only lose to the non-tmp twin at equal (date, version).
    """
    cards_dir = Path(cards_dir)
    best = None
    try:
        entries = list(cards_dir.iterdir())
    except OSError:
        return None
    for entry in entries:
        match = DIGEST_CARD_RE.match(entry.name)
        if not match:
            continue
        when = date(int(match.group(1)), int(match.group(2)),
                    int(match.group(3)))
        version = int(match.group(4))
        is_tmp = entry.name.endswith("-tmp")
        key = (when, version, not is_tmp)
        if best is None or key > best[0]:
            best = (key, entry.name)
    if best is None:
        return None
    return best[0][0], best[1]


def card_orders_frontier(card_dir):
    """Max orders row number the card declares consumed, or None.

    Parses the "rows N-M" consumption range from cards.json meta fields
    (source_pointer / form / source_facts). tech#202 row-level anchor:
    same-day rows landing after the latest card are invisible to day
    granularity, so the card's own recorded frontier is the only honest
    coverage claim. Unreadable / absent cards.json -> None (face falls
    back to day granularity).
    """
    try:
        text = (Path(card_dir) / "cards.json").read_text(encoding="utf-8")
        data = json.loads(text)
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    meta = data.get("meta")
    fields = []
    if isinstance(meta, dict):
        fields = [str(meta.get(key) or "") for key in
                  ("source_pointer", "form", "source_facts")]
    best = None
    for field in fields:
        for match in CARD_ROWS_RANGE_RE.finditer(field):
            start, end = int(match.group(1)), int(match.group(2))
            if 0 < start <= end and (best is None or end > best):
                best = end
    return best


def digest_frontier(cards_dir):
    """Newest parseable row frontier across DIGEST card dirs, or None.

    Walks card dirs newest-first (same ordering as latest_digest_card);
    a cards.json-less staging dir falls through to the next-newest card
    (conservative: an older frontier can only over-report unconsumed rows,
    never hide them)."""
    cards_dir = Path(cards_dir)
    try:
        entries = list(cards_dir.iterdir())
    except OSError:
        return None
    ranked = []
    for entry in entries:
        match = DIGEST_CARD_RE.match(entry.name)
        if not match:
            continue
        when = date(int(match.group(1)), int(match.group(2)),
                    int(match.group(3)))
        version = int(match.group(4))
        is_tmp = entry.name.endswith("-tmp")
        ranked.append(((when, version, not is_tmp), entry.name))
    for _, name in sorted(ranked, reverse=True):
        frontier = card_orders_frontier(cards_dir / name)
        if frontier is not None:
            return frontier
    return None


def orders_row_date_seq(text, year=None):
    """Ordered per-row date list over the |-row family (tech#202).

    Index i holds the date of orders row i+1 (None when the first cell
    is not a live date shape); rows beyond a card frontier slice
    directly: ``seq[frontier:]`` = rows frontier+1..current.
    """
    if year is None:
        year = datetime.now().year
    seq = []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        match = ORDERS_CELL_DATE_RE.match(_orders_first_cell(line))
        if match and match.group(1):
            seq.append(date(int(match.group(1)), int(match.group(2)),
                            int(match.group(3))))
        elif match:
            seq.append(date(year, int(match.group(4)), int(match.group(5))))
        else:
            seq.append(None)
    return seq


def classify_digest_supply_gap(orders_dates, latest, today,
                               threshold_days=DIGEST_SUPPLY_GAP_DAYS,
                               row_frontier=None, current_rows=None,
                               row_dates_seq=None):
    """Pure core for the DIGEST supply-gap advisory face (tech#129).

    Returns a dict: status inactive|quiet|advisory|gap + reading fields.
    - day-level unconsumed = row dates strictly newer than the latest
      DIGEST card (day granularity; same-day clusters are below day
      resolution)
    - row-level unconsumed (tech#202, R2337 anchor): when the latest
      card's recorded orders-row frontier is parseable, rows beyond it
      count as unconsumed even when their dates are same-day -- the
      false-quiet hole where a same-day evening cluster (rows 522-539
      after v23's rows 515-521) read as fully covered
    - advisory: unconsumed exists but oldest age <= threshold (per-round
      hint line, silence NOT broken)
    - gap: oldest unconsumed age > threshold -> WARN breaks silence (the
      chronic-blindness backstop for the R870/R1095/R1303/R1536/R2050
      manual-correction family). Creative judgment stays with the body.
    """
    row_unconsumed = 0
    row_unconsumed_dates = set()
    if (row_frontier is not None and current_rows is not None
            and current_rows > row_frontier):
        row_unconsumed = current_rows - row_frontier
        if row_dates_seq is not None:
            row_unconsumed_dates = set(
                d for d in row_dates_seq[row_frontier:] if d is not None)
    day_unconsumed = set(d for d in orders_dates
                         if latest is None or d > latest)
    unconsumed_set = day_unconsumed | row_unconsumed_dates
    if not unconsumed_set and row_unconsumed == 0:
        return {"status": "quiet", "unconsumed": 0, "oldest": None,
                "age_days": None, "threshold": threshold_days,
                "row_unconsumed": 0, "row_frontier": row_frontier}
    unconsumed = sorted(unconsumed_set)
    if unconsumed:
        oldest = unconsumed[0]
        age_days = (today - oldest).days
        status = "gap" if age_days > threshold_days else "advisory"
    else:
        # Row-unconsumed whose rows carry no parseable dates: undatable
        # residue -- advisory at the day-granularity floor, never quiet.
        oldest = latest
        age_days = max((today - latest).days, 0) if latest else 0
        status = "advisory"
    return {"status": status, "unconsumed": len(unconsumed),
            "oldest": oldest, "age_days": age_days,
            "threshold": threshold_days,
            "row_unconsumed": row_unconsumed, "row_frontier": row_frontier}


def face_digest_supply(paths, today=None):
    """Face: DIGEST 史源 supply-gap advisory backstop (#67 trigger law).

    rc 0 quiet/advisory/inactive / 1 gap WARN (breaks silence) / 3 read
    error. Cards dir missing = face inactive (the DIGEST production line
    itself is absent) -- never a read failure. tech#202 (R2337 anchor):
    coverage is judged BOTH day-level (row dates vs card date) and
    row-level (current orders rows vs the card's recorded consumption
    frontier in cards.json meta) -- same-day rows beyond the frontier
    kill the false-quiet.
    """
    cards = Path(paths["cards_dir"])
    latest = latest_digest_card(cards)
    if latest is None:
        return RC_QUIET, ("cards: %s | (no DIGEST card dir)\n"
                          "DIGEST-SUPPLY: inactive (no cards dir)"
                          % (cards,))
    try:
        text, mtime, size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    if today is None:
        today = datetime.now().date()
    dates = orders_row_dates(text)
    rows, _tail_key = orders_row_stats(text)
    row_seq = orders_row_date_seq(text)
    frontier = digest_frontier(cards)
    verdict = classify_digest_supply_gap(dates, latest[0], today,
                                         row_frontier=frontier,
                                         current_rows=rows,
                                         row_dates_seq=row_seq)
    lines = ["cards: %s | latest DIGEST card %s (%s) | orders rows "
             "mtime %s | row-dates=%d | rows=%d | frontier=%s"
             % (cards, latest[0].isoformat(), latest[1], mtime, len(dates),
                rows, frontier if frontier is not None else "n/a")]
    if verdict["status"] == "quiet":
        lines.append("DIGEST-SUPPLY: quiet (orders rows covered by "
                     "latest DIGEST card %s)" % latest[0].isoformat())
        return RC_QUIET, "\n".join(lines)
    detail = ("%d unconsumed orders row-date(s) after latest DIGEST card "
              "%s (oldest %s, age %dd)"
              % (verdict["unconsumed"], latest[0].isoformat(),
                 verdict["oldest"].isoformat(), verdict["age_days"]))
    if verdict["row_unconsumed"]:
        detail += (" | row-level: %d row(s) beyond frontier %s "
                   "(same-day clusters are invisible to day granularity)"
                   % (verdict["row_unconsumed"], verdict["row_frontier"]))
    if verdict["status"] == "advisory":
        lines.append("DIGEST-SUPPLY: %s -- advisory (age <= %dd; "
                     "judgment stays with the loop)" % (detail,
                                                       verdict["threshold"]))
        return RC_QUIET, "\n".join(lines)
    lines.append("DIGEST-SUPPLY-GAP: %s -- WARN (age > %dd): supply "
                  "blindspot backstop (R870/R1095/R1303/R1536/R2050 "
                  "manual-correction family; derive-into-pool evaluation "
                  "due)" % (detail, verdict["threshold"]))
    return RC_NEW, "\n".join(lines)


def _resolve_git(explicit=None):
    """Real git binary path, or None.

    An explicit path is an override, not a preference: if it is absent
    (or a gitsilent wrapper) resolution FAILS -- never fall through to
    the default candidates (hermetic-test contract: an explicit bogus
    path must yield git-unresolved even on a machine where the real
    candidates exist). With no explicit path the candidates are tried
    in order; gitsilent wrappers are never used (R-1952 family).
    """
    if explicit:
        if "gitsilent" not in explicit.lower() and Path(explicit).exists():
            return str(explicit)
        return None
    for cand in GIT_CANDIDATES:
        if "gitsilent" not in cand.lower() and Path(cand).exists():
            return str(cand)
    return None


def _subprocess_run_git(argv, timeout=GIT_FETCH_TIMEOUT_S):
    import subprocess
    return subprocess.run(argv, capture_output=True, timeout=timeout)


def orders_origin_rows(group_root=None, runner=None, git_path=None):
    """(origin_rows, source, row_lines) via git fetch + git show
    (D-20260901-03 canon).

    row_lines = the stripped |-row lines of the origin file (tech#165
    content anchors); None when degraded. Any failure ->
    (None, reason, None): the face degrades to the worktree-only
    behavior (tech#133 pre-registered graceful degradation -- a network
    face must never brick the probe).
    """
    root = Path(group_root) if group_root else GROUP_ROOT
    git = _resolve_git(git_path)
    if git is None:
        return None, "git-unresolved", None
    run = runner or _subprocess_run_git
    try:
        fetch = run([git, "-C", str(root), "fetch", "origin"])
    except Exception as exc:  # timeout / binary gone / etc.
        return None, "fetch-error %r" % (exc,), None
    if getattr(fetch, "returncode", 1) != 0:
        return None, "fetch-failed rc=%s" % getattr(fetch, "returncode",
                                                     "?"), None
    try:
        show = run([git, "-C", str(root), "show",
                    "origin/main:docs/orders.md"])
    except Exception as exc:
        return None, "show-error %r" % (exc,), None
    if getattr(show, "returncode", 1) != 0 or not show.stdout:
        return None, "show-failed rc=%s" % getattr(show, "returncode",
                                                    "?"), None
    text = show.stdout.decode("utf-8", "replace")
    rows, _ = orders_row_stats(text)
    row_lines = [line.strip() for line in text.splitlines()
                 if line.lstrip().startswith("|")]
    return rows, "origin/main", row_lines


def classify_orders_origin_delta(origin_rows, local_rows):
    """Pure core (tech#133): origin > local = origin-only rows exist.

    ahead    -> WARN breaks silence (consume the origin-only rows via
                git show now; D-13 SLA must not wait for the pull)
    quiet    -> worktree sees everything origin sees (local ahead of
                origin during a push window is NOT a blind spot)
    degraded -> origin unreadable; worktree-only behavior (pre-registered)
    """
    if origin_rows is None:
        return {"status": "degraded", "delta": None,
                "origin": None, "local": local_rows}
    delta = origin_rows - local_rows
    status = "ahead" if delta > 0 else "quiet"
    return {"status": status, "delta": delta,
            "origin": origin_rows, "local": local_rows}


def origin_only_row_anchors(origin_lines, local_text,
                            preview_len=ORIGIN_ANCHOR_PREVIEW_LEN,
                            cap=ORIGIN_ANCHOR_CAP):
    """Pure core (tech#165): content anchors for origin-only rows.

    Rows present in origin but absent from the worktree, keyed by exact
    stripped-line content. Consumption rounds quote the anchor verbatim
    in log/commit instead of guessing row identity from cph4 commit
    subjects (R2240 misidentification root fix: the two "consumed" O
    numbers were commit subjects, not ledger rows, HITS=0).
    Returns [{"row": <1-based origin index>, "cell": <first cell>,
    "preview": <first preview_len chars>}] capped at ``cap``;
    ``cap=None`` (tech#208) returns the full uncapped list so the face
    can report the true anchor-count next to the count-face delta;
    [] when origin_lines is None/empty or everything is present.
    """
    if not origin_lines:
        return []
    local_rows = set()
    for line in local_text.splitlines():
        if line.lstrip().startswith("|"):
            local_rows.add(line.strip())
    anchors = []
    for idx, line in enumerate(origin_lines, 1):
        if line.strip() in local_rows:
            continue
        anchors.append({"row": idx,
                        "cell": _orders_first_cell(line),
                        "preview": line.strip()[:preview_len]})
        if cap is not None and len(anchors) >= cap:
            break
    return anchors


def classify_anchor_delta_alignment(anchor_count, delta):
    """Pure core (tech#208, R2341 anchor): anchor-count vs delta verdict.

    R2341 live case: the count face read delta=4 while 5 origin-only
    anchors echoed -- one worktree row carried content origin did not
    have, and the count face alone could not explain the split. Set
    algebra: L = (O - A) + E, so E = A - delta >= 0 always, where E is
    the number of worktree-only-content rows (edit-family candidates
    that pair with E of the A anchors). Aligned (E == 0) means every
    origin-only anchor is a pure insert candidate.
    Returns {"anchor_count", "delta", "edit_family", "insert_family",
    "aligned"}.
    """
    edit_family = max(0, anchor_count - delta)
    return {"anchor_count": anchor_count, "delta": delta,
            "edit_family": edit_family,
            "insert_family": anchor_count - edit_family,
            "aligned": edit_family == 0}


def face_orders_origin_delta(paths, runner=None, git_path=None):
    """Face: ORDERS origin-delta advisory (tech#133, R2059/R2064 family).

    rc 0 quiet/degraded / 1 ahead WARN (breaks silence) / 3 local read
    error only (the origin/network side never fails the probe --
    pre-registered graceful degradation). tech#165: ahead echoes
    origin-only row content anchors (row index + first cell + preview)
    so the consuming round anchors on verbatim content, never on a
    guessed identity. tech#208 (R2341 anchor): anchor-count and delta
    are reported side by side with an insert-family vs edit-family
    classification when they diverge; quiet-by-count with content edits
    keeps rc-quiet and gains an advisory edit-family note.
    """
    try:
        text, mtime, size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    local_rows, _ = orders_row_stats(text)
    origin_rows, source, origin_lines = orders_origin_rows(
        group_root=Path(paths["hq_orders"]).parent.parent, runner=runner,
        git_path=git_path)
    verdict = classify_orders_origin_delta(origin_rows, local_rows)
    lines = ["worktree rows=%d (mtime %s) | origin source=%s"
             % (local_rows, mtime, source)]
    if verdict["status"] == "degraded":
        lines.append("ORDERS-ORIGIN-DELTA: degraded (%s) -- worktree-only "
                     "behavior (tech#133 pre-registered)" % source)
        return RC_QUIET, "\n".join(lines)
    lines.append("origin rows=%s | delta=%s" % (verdict["origin"],
                                                verdict["delta"]))
    if verdict["status"] == "quiet":
        # tech#208 (R2341 anchor): quiet is a row-count verdict; the
        # content face can still hold edited rows. Count-quiet with
        # content edits stays rc-quiet -- these are not origin-only
        # inserts, so no D-13 blind spot -- but the advisory note makes
        # the count-vs-content split explainable instead of silent.
        quiet_anchors = origin_only_row_anchors(origin_lines, text,
                                                 cap=None)
        if not quiet_anchors:
            lines.append("ORDERS-ORIGIN-DELTA: quiet "
                         "(origin == worktree rows)")
        else:
            lines.append(
                "ORDERS-ORIGIN-DELTA: quiet (origin == worktree rows; "
                "anchor-count=%d content-edited row(s) = edit-family "
                "candidates -- count aligned but content differs; "
                "FleetLink pull surfaces the edits, not origin-only "
                "inserts) (tech#208)" % len(quiet_anchors))
        return RC_QUIET, "\n".join(lines)
    anchors_all = origin_only_row_anchors(origin_lines, text, cap=None)
    align = classify_anchor_delta_alignment(len(anchors_all),
                                             verdict["delta"])
    for a in anchors_all[:ORIGIN_ANCHOR_CAP]:
        lines.append("origin-only-anchor: row %d | %s | %s"
                     % (a["row"], a["cell"], a["preview"]))
    if len(anchors_all) > ORIGIN_ANCHOR_CAP:
        lines.append("origin-only-anchor: ... %d more below cap %d"
                     % (len(anchors_all) - ORIGIN_ANCHOR_CAP,
                        ORIGIN_ANCHOR_CAP))
    if align["aligned"]:
        lines.append("anchor-count=%d vs delta=%d -- aligned "
                     "insert-family (every origin-only anchor is an "
                     "insert candidate) (tech#208)"
                     % (align["anchor_count"], align["delta"]))
    else:
        lines.append(
            "anchor-count=%d vs delta=%d NOT aligned (tech#208) -- "
            "%d worktree-only-content row(s) = edit-family candidates "
            "(content edits between origin and worktree pair with %d "
            "of the anchors; the other %d anchor(s) are insert "
            "candidates; verify local edits before FleetLink pull)"
            % (align["anchor_count"], align["delta"],
               align["edit_family"], align["edit_family"],
               align["insert_family"]))
    lines.append("ORDERS-ORIGIN-DELTA-WARN: origin %d vs worktree %d "
                 "(%d origin-only row(s), anchor-count %d) -- worktree-face blind spot "
                 "(R2059/R2064 family); consume via git show origin/main "
                 "now (D-13 SLA), anchor log/commit on the origin-only-"
                 "anchor lines above (tech#165), FleetLink pull heals "
                 "the worktree"
                 % (verdict["origin"], verdict["local"], verdict["delta"],
                    align["anchor_count"]))
    return RC_NEW, "\n".join(lines)


def scan_ledger(text):
    """{marker: (lines, occurrences)} plus last @BigStream line preview."""
    stats = {}
    last_line = None
    for line in text.splitlines():
        for marker in LEDGER_MARKERS:
            occ = line.count(marker)
            if occ:
                lines, total = stats.get(marker, (0, 0))
                stats[marker] = (lines + 1, total + occ)
        if "@BigStream" in line and line.strip():
            last_line = line.strip()
    preview = tail_preview(last_line) if last_line else ""
    return stats, preview


def tail_preview(line, limit=PREVIEW_LEN):
    """One-line anchor preview (truncated, never multi-line)."""
    line = (line or "").strip()
    if len(line) > limit:
        return line[:limit] + " ..."
    return line


def last_content_line(text):
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()
    return ""


def own_orders_top(directory):
    """Newest file in own orders dir -> (name, mtime_str, size) or None."""
    directory = Path(directory)
    best = None
    for path in directory.glob("*"):
        if not path.is_file():
            continue
        stat = path.stat()
        if best is None or stat.st_mtime > best[1]:
            best = (path.name, stat.st_mtime, stat.st_size)
    if best is None:
        return None
    name, mtime, size = best
    return (name, datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
            size)


def face_decisions(paths):
    """Face 1: dnum watermark diff. rc 0 quiet / 1 new / 3 read error."""
    try:
        text, mtime, size = read_text(paths["decisions"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: decisions %r" % (exc,)
    try:
        watermark = load_watermark(paths["state"])
    except (OSError, ValueError) as exc:
        return RC_READ_FAIL, "read-fail: state %r" % (exc,)

    tokens = extract_dnums(text)
    kinds = classify_tokens(text)
    truly_new, wm_only = diff_watermark(tokens, watermark)
    lines = [
        "file: %s | mtime %s | %d B | tokens=%d" % (
            paths["decisions"], mtime, size, len(tokens)),
        "watermark=%d | truly_new=%d | wm_only=%d (slim/inline-consumed family)"
        % (len(watermark), len(truly_new), len(wm_only)),
    ]
    if truly_new:
        annotated = ["%s [%s]" % (t, kinds.get(t, "row")) for t in truly_new]
        lines.append("TRULY_NEW: " + ", ".join(annotated))
    else:
        lines.append("TRULY_NEW: (none)")
    if wm_only:
        lines.append("wm_only: " + ", ".join(wm_only))
    return (RC_NEW if truly_new else RC_QUIET), "\n".join(lines)


def face_orders(paths):
    """Face: ORDERS row watermark (tech#103, decisions_watermark sibling).

    rc 0 quiet (watermark matches) / 1 new-or-missing (breaks silence) /
    3 read error. A missing watermark is first-run rc 1 with the
    watermark-missing note so the body must consume-then-store once --
    never read quiet on a missing baseline (false-quiet direction lock).
    """
    try:
        text, mtime, size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    try:
        stored = load_orders_watermark(paths["state"])
    except (OSError, ValueError) as exc:
        return RC_READ_FAIL, "read-fail: state %r" % (exc,)

    rows, tail_key = orders_row_stats(text)
    cur = {"rows": rows, "tail_key": tail_key}
    lines = [
        "file: %s | mtime %s | %d B" % (paths["hq_orders"], mtime, size),
        "current: rows=%d tail_key=%r" % (rows, tail_key),
    ]
    if stored is None:
        lines.append("stored: watermark-missing (first-run: consume then "
                     "store {rows, tail_key})")
        lines.append("ORDERS-NEW: watermark-missing")
        return RC_NEW, "\n".join(lines)
    lines.append("stored: rows=%r tail_key=%r" % (stored["rows"],
                                                  stored["tail_key"]))
    if stored == cur:
        lines.append("ORDERS: quiet (watermark matches)")
        return RC_QUIET, "\n".join(lines)
    lines.append("ORDERS-NEW: rows %r->%r | tail_key %r->%r"
                 % (stored["rows"], rows, stored["tail_key"], tail_key))
    return RC_NEW, "\n".join(lines)


def face_ledger(paths):
    """Face 2: transfer-marker line anchors. rc 0 / 3 read error."""
    try:
        text, mtime, size = read_text(paths["ledger"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: ledger %r" % (exc,)
    stats, preview = scan_ledger(text)
    lines = ["file: %s | mtime %s | %d B" % (paths["ledger"], mtime, size)]
    for marker in LEDGER_MARKERS:
        hit_lines, occ = stats.get(marker, (0, 0))
        lines.append("%s lines=%d occurrences=%d" % (marker, hit_lines, occ))
    if preview:
        lines.append("last-@BigStream: " + preview)
    return RC_QUIET, "\n".join(lines)


def face_mtime(paths):
    """Face 3: HQ + own orders anchor readings. rc 0 / 3 read error."""
    lines = []
    rc = RC_QUIET
    try:
        orders_text, orders_mtime, orders_size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    try:
        dec_text, dec_mtime, dec_size = read_text(paths["decisions"])
        led_mtime_line = ""
    except OSError as exc:
        dec_mtime, dec_size, dec_text = None, None, None
        rc = RC_READ_FAIL
        led_mtime_line = "decisions read-fail: %r" % (exc,)
    try:
        _, led_mtime, led_size = read_text(paths["ledger"])
    except OSError as exc:
        rc = RC_READ_FAIL
        led_mtime = led_size = None
        lines.append("ledger read-fail: %r" % (exc,))

    lines.append("hq-orders | %s | %d B" % (orders_mtime, orders_size))
    lines.append("hq-orders-tail: " + tail_preview(last_content_line(orders_text)))
    if dec_mtime is not None:
        lines.append("hq-decisions | %s | %d B" % (dec_mtime, dec_size))
        lines.append("hq-decisions-tail: " + tail_preview(last_content_line(dec_text)))
    if led_mtime_line:
        lines.append(led_mtime_line)
    if led_mtime is not None:
        lines.append("ledger | %s | %d B" % (led_mtime, led_size))

    own = Path(paths["own_orders_dir"])
    if not own.exists():
        rc = RC_READ_FAIL
        lines.append("own-orders: dir missing")
    else:
        top = own_orders_top(own)
        if top is None:
            lines.append("own-orders: (no files)")
        else:
            lines.append("own-orders-top | %s | %s | %d B" % top)
    return rc, "\n".join(lines)


def render_report(faces, ts):
    lines = ["# group-scan %s" % ts]
    for name, rc, text in faces:
        lines.append("=== %s (rc=%d) ===" % (name, rc))
        if text:
            lines.append(text)
    return "\n".join(lines) + "\n"


def write_report(path, text):
    """UTF-8 without BOM by design (PS 5.1 `>` trap root-fix)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def check_anchor_file(anchor_path, orders_path=None):
    """tech#165 anti-collision assertion: a consumed origin-only row's
    content anchor must be present as a worktree orders row (heal check).

    The anchor prefix travels in a UTF-8 file (first non-empty line --
    PS 5.1 CJK argv is a GBK shredder, never pass CJK on the CLI).
    rc 0 = anchor landed in the worktree (consumed row == real row);
    rc 1 = absent (consumed identity suspect -- re-verify via git show);
    rc 2 = anchor file unreadable/empty.
    """
    path = Path(orders_path) if orders_path else DEFAULTS["hq_orders"]
    try:
        text_in = Path(anchor_path).read_text(encoding="utf-8")
    except OSError as exc:
        return RC_USAGE, "anchor-file unreadable: %r" % (exc,)
    prefix = ""
    for line in text_in.splitlines():
        if line.strip():
            prefix = line.strip()
            break
    if not prefix:
        return RC_USAGE, "anchor-file has no non-empty line"
    try:
        text, _, _ = read_text(path)
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    for line in text.splitlines():
        if line.lstrip().startswith("|") and line.strip().startswith(prefix):
            return RC_QUIET, "ANCHOR-OK: %s" % prefix
    return RC_NEW, "ANCHOR-ABSENT: %s" % prefix


def overall_rc(faces):
    return max([rc for _, rc, _ in faces] + [RC_QUIET])


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    paths = dict(DEFAULTS)
    out_path, echo, anchor_file = None, False, None
    args = argv[1:]
    i = 0
    while i < len(args):
        key = args[i]
        if key in ("--decisions", "--hq-orders", "--ledger", "--own-orders-dir",
                   "--state", "--cards-dir"):
            if i + 1 >= len(args):
                print(USAGE)
                return RC_USAGE
            paths[key[2:].replace("-", "_")] = args[i + 1]
            i += 2
        elif key == "--out" and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        elif key == "--echo":
            echo = True
            i += 1
        elif key == "--check-anchor-file" and i + 1 < len(args):
            anchor_file = args[i + 1]
            i += 2
        else:
            print(USAGE)
            return RC_USAGE

    if anchor_file is not None:
        rc, msg = check_anchor_file(anchor_file,
                                    orders_path=paths.get("hq_orders"))
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
        print(msg)
        return rc

    faces = [
        ("DECISIONS", *face_decisions(paths)),
        ("LEDGER", *face_ledger(paths)),
        ("ORDERS", *face_orders(paths)),
        ("DIGEST-SUPPLY", *face_digest_supply(paths)),
        ("ORDERS-ORIGIN-DELTA", *face_orders_origin_delta(paths)),
        ("MTIME", *face_mtime(paths)),
    ]
    if GROUP_ROOT_NOTE:
        faces.insert(0, ("GROUP-ROOT", RC_QUIET,
                         "GROUP-ROOT-DIVERGENCE: " + GROUP_ROOT_NOTE))
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = render_report(faces, ts)

    if out_path is not None:
        path = write_report(out_path, report)
        print("group-scan: overall_rc=%d" % overall_rc(faces))
        for name, rc, _ in faces:
            print("  %s: rc=%d" % (name, rc))
        print("written: %s (%d bytes, utf-8 no-bom)"
              % (path, len(report.encode("utf-8"))))
        if echo:
            print(report, end="")
    else:
        print(report, end="")
    return overall_rc(faces)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
