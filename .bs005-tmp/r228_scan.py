import os, re, glob, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
OUT = []

# 1. orders latest
orders = sorted(glob.glob(os.path.join(BS, "orders", "*.md")))
OUT.append("ORDERS_TOP: " + (os.path.basename(orders[-1]) if orders else "none"))

# 2. ledger strict @-prefix four-mode scan
ledger = os.path.join(ROOT, "cph4", "evolution-ledger.md")
pat = re.compile(r"@(BigStream|七线全司|全司|六司)")
n = 0
with io.open(ledger, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if pat.search(line):
            n += 1
OUT.append("LEDGER_AT_LINES: %d (anchor 14)" % n)

# 3. decisions.md UTF8 non-empty lines
dec = os.path.join(ROOT, "docs", "decisions.md")
with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
    lines = [l for l in f.read().splitlines() if l.strip()]
OUT.append("DECISIONS_NONEMPTY: %d (anchor 24)" % len(lines))

# 4. storylines: novel chapters + comic episodes
nov = sorted(glob.glob(os.path.join(BS, "data", "storylines", "novel", "*.md")))
OUT.append("NOVEL_FILES: " + ", ".join(os.path.basename(p) for p in nov))
com = sorted(glob.glob(os.path.join(BS, "data", "storylines", "comic", "*")))
OUT.append("COMIC_FILES: " + ", ".join(os.path.basename(p) for p in com))

# 5. audio dir state
aud = sorted(glob.glob(os.path.join(BS, "data", "storylines", "audio", "*")))
OUT.append("AUDIO_FILES: " + ", ".join(os.path.basename(p) for p in aud))

# 6. ch4 head peek (first 600 chars of SC-001-04)
ch4 = [p for p in nov if "SC-001-04" in os.path.basename(p)]
if ch4:
    with io.open(ch4[0], "r", encoding="utf-8", errors="replace") as f:
        head = f.read(1200)
    OUT.append("CH4_HEAD_BEGIN")
    OUT.append(head)
    OUT.append("CH4_HEAD_END")
else:
    OUT.append("CH4: NOT ON DISK")

res = os.path.join(BS, ".bs005-tmp", "r228_scan.txt")
with io.open(res, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("OK scan written, lines:", len(OUT))
