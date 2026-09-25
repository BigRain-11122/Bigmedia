# -*- coding: utf-8 -*-
# R264 fast-path scan: ledger @ four-mode line count + group decisions line counts
# + daily report presence + index.lock check. ASCII-only output (PS5.1 GBK console safe).
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HQ = os.path.join(ROOT, "..", "..")
LEDGER = os.path.join(HQ, "cph4", "evolution-ledger.md")
DECISIONS = os.path.join(HQ, "docs", "decisions.md")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-09-25.md")
LOCK = os.path.join(ROOT, ".git", "index.lock")

TOKENS = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8"]

def main():
    n_match = 0
    ledger_mtime = "missing"
    if os.path.exists(LEDGER):
        ledger_mtime = os.path.getmtime(LEDGER)
        with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if any(t in line for t in TOKENS):
                    n_match += 1
    d_total = d_nonempty = -1
    if os.path.exists(DECISIONS):
        d_total = d_nonempty = 0
        with io.open(DECISIONS, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                d_total += 1
                if line.strip():
                    d_nonempty += 1
    print("ledger_match_lines=%d" % n_match)
    print("decisions_total=%d" % d_total)
    print("decisions_nonempty=%d" % d_nonempty)
    print("daily_0925=%s" % ("yes" if os.path.exists(DAILY) else "no"))
    print("index_lock=%s" % ("yes" if os.path.exists(LOCK) else "no"))

if __name__ == "__main__":
    main()
