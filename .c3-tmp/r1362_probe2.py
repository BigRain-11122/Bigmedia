import io, os, re, glob, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1362_probe2.txt", "w", encoding="utf-8")
w = out.write

# 1. self-improvement queue head
q = repo + r"\docs\self-improvement-queue.md"
if os.path.exists(q):
    lines = io.open(q, encoding="utf-8").read().split("\n")
    w("== queue head 70 (of %d) ==\n" % len(lines))
    for l in lines[:70]:
        w("Q| " + l[:230] + "\n")

# 2. digest v15 review E4 backfill status
rv = repo + r"\docs\reviews\review-20261005-mcdigest-v15.md"
if os.path.exists(rv):
    txt = io.open(rv, encoding="utf-8").read()
    w("\n== v15 review len=%d has E4 backfill: %s ==\n" % (len(txt), ("E4" in txt)))
    for l in txt.split("\n"):
        if "E4" in l:
            w("RV| " + l[:230] + "\n")

# 3. audits dir W40/W41
w("\n== audits 2026-W4x ==\n")
for p in sorted(glob.glob(repo + r"\docs\audits\*self-audit*")):
    w("AU| " + os.path.basename(p) + "\n")

# 4. station reviews tail (find file)
cands = glob.glob(repo + r"\docs\**\station-reviews*") + glob.glob(repo + r"\docs\**\*station*")
w("\nstation files=%s\n" % [c.replace(repo, "") for c in cands][:4])
if cands:
    tl = io.open(cands[0], encoding="utf-8").read().split("\n")
    w("== station tail 10 (of %d) ==\n" % len(tl))
    for l in tl[-10:]:
        w("SR| " + l[:230] + "\n")

# 5. finished.md tail
fin = repo + r"\output\finished.md"
if os.path.exists(fin):
    fl = io.open(fin, encoding="utf-8").read().split("\n")
    w("\n== finished tail 12 (of %d) ==\n" % len(fl))
    for l in fl[-12:]:
        w("F| " + l[:230] + "\n")

# 6. board rows count in decisions.md
dec = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8").read().split("\n")
board = [l for l in dec if re.match(r"^\|\s*D-\d{8}-\d{1,2}", l)]
w("\nboard_rows=%d\n" % len(board))
for l in board[-4:]:
    w("BR| " + l[:200] + "\n")

# 7. cards README tail (F-151 / v15 registration)
cr = glob.glob(repo + r"\data\storylines\cards\README.md")
if cr:
    cl = io.open(cr[0], encoding="utf-8").read().split("\n")
    w("\n== cards README tail 8 (of %d) ==\n" % len(cl))
    for l in cl[-8:]:
        w("CR| " + l[:230] + "\n")

out.close()
print("ok")
