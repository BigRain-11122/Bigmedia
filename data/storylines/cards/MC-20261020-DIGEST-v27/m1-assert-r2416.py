# -*- coding: utf-8 -*-
"""M1 verbatim assertions for MC-20261020-DIGEST-v27 (R2416).

Source window = the 58 dated table rows of FluxGroup/docs/orders.md that end
with the latest row (10-20 00:5x). Assertions:
  A1  window row count == 58 and window start == 2026-10-18 23:1x row
  A2  each deck quote core is a contiguous verbatim substring of the window
  A2b no sentence period inside quotes (punctuation transcribed, not added)
  A2c every truncated quote carries the ellipsis marker on the cut side
  A3  CEO-order row count in window == 48 (card numbered claim)
  A4  165 knowledge cards / six phases numbers present in source rows
  A6  no internal jargon on the card face (deck lines)
"""
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
ORDERS = os.path.abspath(os.path.join(REPO, "..", "..", "docs", "orders.md"))
CARD = os.path.join(REPO, "data", "storylines", "cards", "MC-20261020-DIGEST-v27", "cards.json")

FAILS = []


def check(cond, name, detail=""):
    if not cond:
        FAILS.append("%s %s" % (name, detail))
    print(("PASS " if cond else "FAIL ") + name + (" | " + detail if detail else ""))


def main():
    text = open(ORDERS, encoding="utf-8", errors="replace").read().split("\n")
    rows = [l for l in text if l.startswith("| 2026-10-")]
    window = rows[-58:]
    check(len(window) == 58, "A1 window=58", "got %d" % len(window))
    check("2026-10-18 23:1x" in window[0], "A1 window-start", window[0][:40])
    host = "\n".join(window)

    # Strict criterion: the order must OPEN the second table column. Rows that
    # merely cite an earlier order (engineering continuation / closeout rows)
    # are not new CEO orders and must not inflate the card number.
    def col2(line):
        parts = line.split("|")
        return parts[2].strip() if len(parts) > 2 else ""

    ceo = [l for l in window if col2(l).startswith(
        ("CEO 令", "CEO 追令", "CEO 批评令", "CEO 两连令"))]
    decree = [l for l in window if col2(l).startswith(("CEO 亲颁", "CEO 定谳"))]
    check(len(ceo) + len(decree) == 48,
          "A3 ceo-commands=48", "tags=%d decrees=%d" % (len(ceo), len(decree)))

    check("165 卡" in host, "A4 knowledge-165")
    check("Phase 0-1-1.5-2-3-4-5" in host or "六阶段" in host, "A4 six-phases")

    cfg = json.load(open(CARD, encoding="utf-8"))
    lines = cfg["cards"][0]["lines"]
    quotes = [l for l in lines if "\u300c" in l]
    check(len(quotes) == 5, "A2 quote-lines=5", "got %d" % len(quotes))

    for q in quotes:
        body = q.strip("\u300c\u300d")
        core = body.strip("\u2026")
        check(core in host, "A2 verbatim", core)
        check("\u3002" not in body, "A2b no-period", body)
        lead = body.startswith("\u2026")
        tail = body.endswith("\u2026")
        src = host.find(core)
        prev = host[src - 1] if src > 0 else ""
        after = host[src + len(core)] if src + len(core) < len(host) else ""
        # a cut side must carry the ellipsis marker
        if prev not in ("", "\u300c", "\n", "|", "\u300d", "\uff1a"):
            check(lead, "A2c lead-ellipsis", core[:12])
        if after not in ("", "\u300d", "\n", "|", "\uff0c", "\uff01", "\u3002"):
            check(tail, "A2c tail-ellipsis", core[:12])

    jargon = ("\u53f0\u8d26", "\u4ee4\u884c", "\u7c3f\u8bb0", "\u5e2d\u4f4d", "\u6b63\u5178",
              "\u9600", "\u788d", "JSON", "commit")
    for l in lines:
        for j in jargon:
            check(j not in l, "A6 jargon", "%s in %s" % (j, l))

    print("\n%s (%d fails)" % ("ALL GREEN" if not FAILS else "FAILED", len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())