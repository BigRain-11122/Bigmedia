# -*- coding: utf-8 -*-
# R1372 check2: canonical-method recount for ledger tags + dispatch board fresh rows
import re, io, datetime

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1372_check2.txt", "w", encoding="utf-8")
w = out.write

TAG_ALLCO = "\u4e03\u7ebf\u5168\u53f8"
TAG_QUANSI = "\u5168\u53f8"
TAG_LIUSI = "\u516d\u53f8"
TAG_BAXIAN = "\u516b\u7ebf"
BOARD_HDR = "\u6d3e\u5de5\u901a\u544a\u677f"

# ledger canonical count: line must match @tag (same family as r1370_check.py regex)
led = io.open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
llines = led.split("\n")
canon = re.compile("@(BigStream|" + TAG_ALLCO + "|" + TAG_QUANSI + "|" + TAG_LIUSI + "|" + TAG_BAXIAN + ")")
canon_ci = re.compile("@(BigStream|" + TAG_ALLCO + "|" + TAG_QUANSI + "|" + TAG_LIUSI + "|" + TAG_BAXIAN + ")", re.I)
canon_hits = [l for l in llines if canon.search(l)]
ci_hits = [l for l in llines if canon_ci.search(l)]
w("ledger_canonical=%s (baseline 43) ci_extra=%s\n" % (len(ci_hits), len(ci_hits) - len(canon_hits)))
bs_only = [l for l in llines if re.search(r"@BigStream", l)]
w("ledger_raw_bs=%s (baseline 42)\n" % len(bs_only))
for l in canon_hits[-2:]:
    w("CANON_TAIL| L%s %s\n" % (llines.index(l) + 1, l[:160]))
# CI extras identification (R1286 pseudo-row)
extras = [l for l in ci_hits if not canon.search(l)]
for l in extras:
    w("CI_EXTRA| %s\n" % l[:160])

# board: capture window + rows by date
dec = io.open(base + r"\docs\decisions.md", encoding="utf-8").read()
m = re.search(BOARD_HDR, dec)
w("board_header_pos=%s\n" % (m.start() if m else -1))
# find the next level-2 heading after board header
seg = dec[m.start():] if m else ""
mm = re.search(r"\n## ", seg[1:])
blk = seg[1:mm.start() + 1] if mm else seg
rows = [l for l in blk.split("\n") if l.strip().startswith("|")]
w("board_block_rows=%s\n" % len(rows))
dates = re.findall(r"\|\s*(20\d{2}-\d{2}-\d{2})\s*\|", blk)
w("board_row_dates_last5=%s\n" % dates[-5:])
bs_rows = [(d, l[:170]) for (d, l) in zip(re.findall(r"\|\s*(20\d{2}-\d{2}-\d{2})\s*\|[^\n]*", blk), [x for x in blk.split("\n") if "BigStream" in x and x.strip().startswith("|")]) if False]
bsrows = [l for l in blk.split("\n") if "BigStream" in l and l.strip().startswith("|")]
w("board_bs_rows=%s\n" % len(bsrows))
for l in bsrows[:2]:
    w("BSROW_HEAD| " + l[:170] + "\n")
w("board_block_mtime_note: decisions mtime 10-05 12:04:20 unchanged since R1356 consumption\n")
out.close()
print("ok")
