# -*- coding: utf-8 -*-
"""BigStream OS-loop queue compact readout (tech#145, R2119 seed;
backlog face tech#146, R2124).

Gap anchor (R2119 incident): the three self-drive queues are single-long-
line ledgers (tech.md items run ~1700 chars on one physical line). Round
consumption had to dump whole files (3 full reads in one round), and a
280-char truncated view misjudged "[done ...]" marks sitting beyond the
cut as missing -> 6 probe re-scans in one round. The done determination
must run over the FULL line (R2119 fail-closed doctrine: r2119_backfill
ANCHOR-MISS correctly refused to write against a false alarm).

Machine teeth:
  * parse each queue into items: head line `^N. ` at column 0 plus every
    following non-header/non-quote line until the next head (full text
    kept verbatim - no truncation anywhere in classification).
  * done  = full text matches a bracket containing `done YYYY-MM-DD`
    (covers `[done D...]`, `[RNNNN done D...]`, `**[done D...]**` forms
    and marks embedded mid-line or on continuation lines).
  * gated = not done and mentions gated / 观察位 / 到点执行
    (event-window items; not claimable in a normal round).
    tech#189/#190: the waiting-upstream marker family
    (稿落即领 / 稿落即随轮认领 / 等上游源稿 / waits...source
    manuscript) is gated semantics too - rows whose only remaining
    leg waits for an upstream manuscript to land.
  * claimable = the rest. Head = first claimable in file order.
  * --item N fetches ONE full item verbatim (zero full-file reads for
    the consumer); unknown number -> exit 2 fail-closed (ANCHOR-MISS
    doctrine: never guess, never silently return empty).
  * default face is <= 15 lines: per-queue done/gated/claimable counts
    plus one claimable-head preview line.

Exit codes: 0 = readout printed, 2 = usage / item-not-found / no queue
file resolvable (fail-closed, mirrors r2119_backfill).

Pure-parse helpers (parse_items / classify_item / classify_queue /
render / build_json) are unit-tested offline; no git, no network.

Usage:
    python src/os/queue_status.py                 # compact 4-face readout
    python src/os/queue_status.py --item 145      # tech #145 full text
    python src/os/queue_status.py --queue main --item 27
    python src/os/queue_status.py --queue backlog --item 111
    python src/os/queue_status.py --json          # machine face

tech#146 (R2124): the P1 board (src/os/backlog.md) joins the readout as
a fourth face - same single-long-line shape, same full-text done law,
plus the P1-only [needs-CEO] family: those items park on the CEO and
classify into the gated bucket (split shown as "(+needs-CEO N)"). The
claimable-head line doubles as the fast-path "backlog top uncompleted
item" determination, no more full-file dumps.

tech#167 (R2245 seed): --json gains a claimable_nums array per queue
(file order) - the audit/takeover consumer previously had to import
the module and re-derive the list (4 API-signature trial-and-error
calls in one round: load_queue root+name, classify_queue triple,
render_item vs report). Pure additive field; consumers that only read
the existing keys stay green.

tech#176 (R2274 seed, note delivered R2276): claimable is a LITERAL
classification - done/gated detection only reads the row text itself.
A row whose true state is gated by an external threshold (VRAM machine
gate, app-dead, GPU exclusive window) keeps reading claimable until
the row is rewritten with the in-row gated word (leg-state write-back
discipline: when a leg completes or gates, rewrite the row the same
round). Consumers must not trust claimable alone for deep decisions -
R2266-R2274 paid eight false-positive rounds plus a ~15 min deep
audit because rows #78/#151 read claimable while truly gated.

R2276 console hardening: --item crashed live with UnicodeEncodeError
('gbk' codec can't encode '\\u226a') when an item carries characters
outside the console codepage (tech#151's VRAM reading uses the CJK
much-less-than sign). main() now reconfigures stdout/stderr with
encoding="utf-8" (tech#243, R2388: codepage-kept CJK read as mojibake
in the harness and cost a second read_file hop per --item judgment;
group_scan.py parity) plus errors="replace": the rare non-encodable
character degrades to '?' instead of killing the readout. The --json
face is ASCII-only payload, so it is unaffected.

tech#236 (R2383 seed, closed R2385): machine-readable pin suffix. A
new seed whose true state is window/gate-pinned ENDS its line with
`[window:...]` / `[gate:...]` (type vocabulary <= 6 pin words by
design; value = short free text) - classify_item reads the pin
straight off the row into the gated bucket and --item echoes a PIN
marker line. The suffix is LINE-END anchored (re.M), so mid-line
bracket mentions never match and appended prose notes never silently
unpin; old rows keep prose window notes with zero backfill (prose
stays prose, the loop still judges those rows - tech#176); the
tech#210 gate-lift note pair still wins over a stale pin. Rationale:
R2378-R2385 rounds paid 6-10 manual --item reads per round to
rediscover prose window pins (#225/#227 family) - the suffix makes
the pin one canonical readout line (judging-criteria validation:
next-round --item call-count comparison 6-10 -> <= 3).
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

QUEUE_FILES = {
    "main": "state/queue/main.md",
    "tech": "state/queue/tech.md",
    "explore": "state/queue/explore.md",
    "backlog": "src/os/backlog.md",  # tech#146: P1 board shares the
    # single-long-line shape (~81% done); P1-only state family: items
    # marked [needs-CEO] are ~gated semantics (waiting on CEO) and must
    # land in the gated bucket, never claimable.
}
DEFAULT_QUEUE = "tech"
HEAD_PREVIEW_CHARS = 90
MAX_DEFAULT_LINES = 15

_HEAD_RE = re.compile(r"^(\d+)\.\s")
_HEADER_RE = re.compile(r"^[#>]")
# bracket holding `done YYYY-MM-DD` (dated marks only; prose like
# "验读标 done" without a date right after must NOT count as done)
_DONE_RE = re.compile(r"\[[^\[\]]*\bdone\s+(\d{4}-\d{2}-\d{2})[^\[\]]*\]")
# Window-gate markers: literal 'gated', observation/event positions, and
# the two window phrasings that mean gated without the word (calibrated
# against the live queues 2026-10-13: GPU 独占窗即领 / 窗到即领).
# Honest boundary: 判负-closed items (negative verdict, kept on record)
# stay in the claimable bucket on purpose - a bare 判负 mention also
# appears inside OPEN items as a pre-registered judging criterion
# ("不达=判负留痕"), so machine detection would misclassify; the
# preview line surfaces the verdict and the loop still judges.
_GATED_RE = re.compile(r"gated|观察位|到点执行|GPU 独占窗|窗到即领")
# tech#210 (R2343 seed): half-unlocked state rule. A row can keep a
# stale gated head while an in-row progress note has explicitly lifted
# the gate - the loop's append convention writes
# "**[R2340 gate 解除注记 2026-10-18]** ... 转 claimable ...". BOTH signals
# must be present (the explicit gate-lift note bracket AND the
# lift-to-claimable phrase) so ordinary prose never lifts a gate; when
# both are, the note wins and the verdict flips to claimable with a
# HEAD-INCONSISTENT marker - canonical readout stays aligned with the
# row's own state (zero claimant ambiguity) and the drift stays loud.
_GATE_LIFT_NOTE_RE = re.compile(r"\[R\d+\s*gate\s*解除注记[^\]]*\]")
_LIFT_TO_CLAIMABLE_RE = re.compile(r"转\s*claimable")
# tech#189/#190 (R2317/R2319 seeds, closed R2364): waiting-upstream
# family - rows whose only remaining leg waits for an upstream
# manuscript/source written elsewhere (lands later) read claimable
# until rewritten. Literal marker phrases only, no semantic guessing:
# form 1 (backlog #31 shape) 稿落即领 / 稿落即随轮认领; form 3
# (backlog #27 shape) 等上游源稿 / waits ... source manuscript.
# Live audit 2026-10-18: every board hit sits in done-marked rows
# (done wins) or rows already gated by word - zero claimable flips.
_UPSTREAM_WAIT_RE = re.compile(
    r"稿落即领|稿落即随轮认领|等上游源稿"
    r"|waits.{0,60}source\s+manuscript")
# tech#236 (R2383 seed, closed R2385): machine-readable pin suffix.
# A NEW seed whose true state is window/gate-pinned may END its line
# with `[window:...]` / `[gate:...]` so the classifier reads the pin
# straight off the row (type vocabulary is a short fixed word set,
# <= 6 pin types by design; value = short free text, <= 40 chars).
# The suffix must sit at LINE END (re.M covers the head line and
# appended continuation lines alike - appending prose notes never
# silently unpins); mid-line bracket mentions (seed-law doc examples)
# never match. Old rows keep their prose window notes untouched
# (zero backfill by design, seed law): prose stays prose, the loop
# still judges those rows (tech#176 doctrine). Lift discipline for a
# pinned row = rewrite the suffix off the row in the same round
# (leg-state write-back), or the tech#210 gate-lift note pair wins.
_PIN_SUFFIX_RE = re.compile(r"\[(window|gate):([^\]]{1,40})\]\s*$",
                            re.MULTILINE)
# tech#146: P1-board-only gated family - items parked on the CEO (P1
# proposals, sign-off waits). Matches the readiness NEEDS_CEO_RE shape.
NEEDS_CEO_RE = re.compile(r"\[needs-CEO[^\]]*\]")


def parse_items(text):
    """Split queue text into items.

    Returns a list of dicts {num, head, text} in file order. Continuation
    lines (indented follow-ups, embedded notes) stay attached to their
    item so done-marks anywhere in the item are seen. Header/quote lines
    are ignored.
    """
    items = []
    cur = None
    for raw in text.splitlines():
        m = _HEAD_RE.match(raw)
        if m:
            cur = {"num": int(m.group(1)), "head": raw, "text": raw}
            items.append(cur)
        elif cur is not None and not _HEADER_RE.match(raw):
            cur["text"] += "\n" + raw
    return items


def classify_item(item):
    """Return ('done'|'gated'|'claimable', marker_or_None).

    Done determination runs the regex over the FULL item text (never a
    truncated view) - R2119 fail-closed doctrine. tech#146: [needs-CEO]
    items classify into the gated bucket (reported via the needs-ceo
    sub-count so the compact face can show the split).
    """
    m = _DONE_RE.search(item["text"])
    if m:
        return "done", m.group(0)
    if NEEDS_CEO_RE.search(item["text"]):
        return "gated", None
    if (_GATED_RE.search(item["text"])
            or _UPSTREAM_WAIT_RE.search(item["text"])):
        # tech#210: half-unlocked rule - see _GATE_LIFT_NOTE_RE note.
        # Both signals required so prose never lifts a gate silently.
        # (tech#189/#190: the upstream-wait family joins this branch,
        # so a landed-manuscript lift note flips it the same way.)
        if (_GATE_LIFT_NOTE_RE.search(item["text"])
                and _LIFT_TO_CLAIMABLE_RE.search(item["text"])):
            return ("claimable",
                    "HEAD-INCONSISTENT: gate-lift note wins over stale "
                    "gated head (tech#210)")
        return "gated", None
    # tech#236: machine-readable pin suffix at line end - a new seed
    # pins itself out of the claimable bucket without prose guessing.
    # tech#210 doctrine carries over: the explicit gate-lift note pair
    # still wins over a stale machine pin.
    pin = _PIN_SUFFIX_RE.search(item["text"])
    if pin:
        if (_GATE_LIFT_NOTE_RE.search(item["text"])
                and _LIFT_TO_CLAIMABLE_RE.search(item["text"])):
            return ("claimable",
                    "HEAD-INCONSISTENT: gate-lift note wins over pin "
                    "suffix (tech#210/#236)")
        return ("gated",
                "PIN [%s:%s] (tech#236 pin)"
                % (pin.group(1), pin.group(2)))
    return "claimable", None


def classify_queue(items):
    """Bucket items into done/gated/claimable; keep file order.

    tech#146: also returns the needs-CEO sub-set (nums) - those items
    sit in the gated bucket, gated semantics, with a reported split.
    """
    buckets = {"done": [], "gated": [], "claimable": []}
    markers = {}
    needs_ceo = {}
    for it in items:
        state, marker = classify_item(it)
        buckets[state].append(it)
        markers[it["num"]] = marker
        if NEEDS_CEO_RE.search(it["text"]) and state == "gated":
            needs_ceo[it["num"]] = True
    return buckets, markers, needs_ceo


def head_preview(item, limit=HEAD_PREVIEW_CHARS):
    """First claimable-item preview: strip the 'N. ' prefix, truncate."""
    s = item["head"]
    m = _HEAD_RE.match(s)
    if m:
        s = s[m.end():]
    s = s.strip()
    if len(s) > limit:
        s = s[:limit - 3] + "..."
    return s


def load_queue(root, name):
    """Return item list or None when the queue file is missing."""
    path = Path(root) / QUEUE_FILES[name]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    return parse_items(text)


def build_report(root, names):
    """Read the requested queues; missing files are reported, not fatal
    for the other queues."""
    report = {}
    for name in names:
        items = load_queue(root, name)
        if items is None:
            report[name] = {"missing": True}
            continue
        buckets, markers, needs_ceo = classify_queue(items)
        report[name] = {
            "missing": False,
            "total": len(items),
            "done": len(buckets["done"]),
            "gated": len(buckets["gated"]),
            "needs_ceo": len(needs_ceo),
            "claimable": len(buckets["claimable"]),
            "claimable_nums": [it["num"] for it in buckets["claimable"]],
            "claimable_head": (buckets["claimable"][0]
                               if buckets["claimable"] else None),
            "markers": markers,
            "items": items,
        }
    return report


def render(report):
    """Compact face: one line per queue plus totals (<= 15 lines)."""
    lines = ["queue-status %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    tot = {"done": 0, "gated": 0, "claimable": 0}
    for name, face in report.items():
        if face.get("missing"):
            lines.append("%-7s: MISSING (file unreadable)" % name)
            continue
        for k in tot:
            tot[k] += face[k]
        ceo_n = face.get("needs_ceo", 0)
        gated_txt = ("%d" % face["gated"] if ceo_n == 0 else
                     "%d (+needs-CEO %d)" % (face["gated"], ceo_n))
        head = face["claimable_head"]
        head_txt = ("head #%d: %s" % (head["num"], head_preview(head))
                    if head else "head: (none claimable)")
        lines.append("%-7s: %d items | done %d | gated %s | claimable %d | %s"
                     % (name, face["total"], face["done"],
                        gated_txt, face["claimable"], head_txt))
    lines.append("total  : done %d | gated %d | claimable %d"
                 % (tot["done"], tot["gated"], tot["claimable"]))
    return lines


def render_item(face, num):
    """--item face: verdict line plus the FULL item text verbatim."""
    for it in face["items"]:
        if it["num"] == num:
            state, marker = classify_item(it)
            out = ["#%d [%s]" % (num, state.upper())]
            if marker:
                shown = marker if len(marker) <= 60 else marker[:59] + "..."
                out.append("marker: %s" % shown)
            out.append(it["text"])
            return out, 0
    return ["item #%d not found in queue - fail-closed, no guess" % num], 2


def build_json(report):
    """Machine face (no full item texts - stays compact)."""
    data = {}
    for name, face in report.items():
        if face.get("missing"):
            data[name] = {"missing": True}
            continue
        head = face["claimable_head"]
        data[name] = {
            "total": face["total"],
            "done": face["done"],
            "gated": face["gated"],
            "needs_ceo": face.get("needs_ceo", 0),
            "claimable": face["claimable"],
            # tech#167: full claimable number list (file order) - audit
            # consumers take the array straight from --json instead of
            # re-importing the module. .get default keeps hand-built
            # report dicts (older callers/tests) green.
            "claimable_nums": list(face.get("claimable_nums", [])),
            "claimable_head_num": head["num"] if head else None,
        }
    return data


def _harden_console_stdio():
    """R2276/tech#243: CLI prints UTF-8 on any console.

    Live crash anchor: `--item 151` raised UnicodeEncodeError ('gbk'
    codec can't encode '\\u226a') because queue rows carry characters
    outside the console codepage (the VRAM reading uses the CJK
    much-less-than sign). errors="replace" keeps the codepage (CJK
    still displays) and degrades the rare non-encodable char to '?'
    instead of crashing the readout. Guards: pythonw None-stream skip
    (tech#169 family) and the unittest harness (StringIO has no
    reconfigure) both no-op via AttributeError.

    tech#243 (R2388): the reconfigure now pins encoding='utf-8'
    outright (group_scan.py parity). Keeping the console codepage
    shipped CJK readouts as codepage bytes that read as mojibake in
    the harness, forcing a second read_file/grep hop per --item
    judgment (R2385 8-call anchor); UTF-8 output makes the face
    one-shot readable. errors='replace' stays as the last-resort
    guard (R2276 contract).
    """
    for stream in (sys.stdout, sys.stderr):
        if stream is None:  # pythonw / detached: no console attached
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def main(argv=None):
    _harden_console_stdio()
    ap = argparse.ArgumentParser(description="queue compact readout")
    ap.add_argument("--root", default=".",
                    help="repo root (default: cwd)")
    ap.add_argument("--queue", default=None,
                    choices=sorted(QUEUE_FILES),
                    help="queue for --item (default: tech when omitted; "
                         "the --item face line echoes the resolved queue "
                         "and tags defaults, tech#207)")
    ap.add_argument("--item", type=int, default=None,
                    help="print ONE full item verbatim (fail-closed)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable face")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()

    if args.item is not None:
        queue_name = args.queue or DEFAULT_QUEUE
        queue_default = args.queue is None
        items = load_queue(root, queue_name)
        if items is None:
            print("queue %s unreadable - fail-closed" % queue_name,
                  file=sys.stderr)
            return 2
        face = classify_queue(items)  # buckets/markers/needs-ceo unused here
        report_face = {"items": items}
        out, code = render_item(report_face, args.item)
        # tech#207 (R2340 anchor): a bare "--item 124" used to read the
        # tech face silently while the caller meant main#124 (~2min
        # misread). The face line makes the resolved queue explicit on
        # every --item readout; default calls get a loud DEFAULT tag.
        if queue_default:
            others = "|".join(q for q in sorted(QUEUE_FILES)
                             if q != queue_name)
            print("face: %s (DEFAULT - pass --queue %s to disambiguate)"
                  % (queue_name, others))
        else:
            print("face: %s" % queue_name)
        for line in out:
            print(line)
        return code

    names = sorted(QUEUE_FILES)
    report = build_report(root, names)
    if all(f.get("missing") for f in report.values()):
        print("no queue file readable under %s - fail-closed" % root,
              file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(build_json(report), ensure_ascii=False))
        return 0
    lines = render(report)
    for line in lines:
        print(line)
    if len(lines) > MAX_DEFAULT_LINES:
        print("warning: default face exceeded %d lines" % MAX_DEFAULT_LINES,
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
