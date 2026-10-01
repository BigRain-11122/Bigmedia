# -*- coding: utf-8 -*-
"""R897: extract key probe summary lines from UTF-16 probe outputs (ASCII-safe)."""
import io

KEYS = ("FAIL", "WARN", "PASS", "blocker", "ideas", "tick", "lag", "outage", "BLOCK", "OK", "GATE", "renders")
for f in ("r897_board.txt", "r897_rd.txt", "r897_loop.txt"):
    print("==", f)
    text = io.open(r".c3-tmp/" + f, encoding="utf-16", errors="replace").read()
    for line in text.splitlines():
        if any(k in line for k in KEYS):
            print(line.encode("unicode_escape").decode("ascii")[:230])
