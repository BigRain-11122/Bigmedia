# -*- coding: utf-8 -*-
# R299 fast-path scan: orders top, group ledger/decisions anchors, production-line anchors
import io, os, re, glob

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = os.path.join(base, "media", "BigStream")

# 1) orders latest
orders = sorted(glob.glob(os.path.join(repo, "orders", "*.md")))
print("ORDERS_TOP:", os.path.basename(orders[-1]) if orders else "NONE", "| total:", len(orders))

# 2) group ledger strict @-prefix scan (four modes)
ledger = os.path.join(base, "cph4", "evolution-ledger.md")
pat = re.compile(r"@(BigStream|七线全司|全司|六司)")
n = 0
with io.open(ledger, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if pat.search(line):
            n += 1
print("LEDGER_MATCH_LINES:", n, "(anchor 17)")

# 3) decisions.md non-empty / total lines
dec = os.path.join(base, "docs", "decisions.md")
nonempty = total = 0
with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        total += 1
        if line.strip():
            nonempty += 1
print("DECISIONS_NONEMPTY:", nonempty, "(anchor 29) | TOTAL:", total, "(anchor 32)")

# 4) production-line anchors
c18 = os.path.join(base, "life", "BigLife", "census", "anchors", "C-00018.md")
print("C00018_ANCHOR:", os.path.exists(c18))
if os.path.exists(c18):
    with io.open(c18, "r", encoding="utf-8", errors="replace") as f:
        head = [next(f, "") for _ in range(12)]
    print("--- C00018_HEAD ---")
    print("".join(head))
    print("--- END ---")

# 5) novel ch.5 v3 draft check (bm-a face)
nov = os.path.join(repo, "data", "storylines", "novel")
hits = sorted(os.listdir(nov)) if os.path.isdir(nov) else []
print("NOVEL_FILES:", [h for h in hits if "SC-001-05" in h or "ch5" in h.lower()] or hits[-8:])

# 6) audio latest (audio-line priority check)
aud = os.path.join(repo, "data", "storylines", "audio")
ah = sorted(os.listdir(aud)) if os.path.isdir(aud) else []
print("AUDIO_LATEST:", ah[-6:] if ah else "NONE")

# 7) comic latest
cmc = os.path.join(repo, "data", "storylines", "comic")
ch = sorted(os.listdir(cmc)) if os.path.isdir(cmc) else []
print("COMIC_LATEST:", ch[-4:] if ch else "NONE")
