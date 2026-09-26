# r462 debug: replicate r461_check.py ledger section exactly vs canon line-iteration
import io, os, re
from collections import Counter

FG = r"C:\Users\sjs20\Desktop\FluxGroup"
P1 = os.path.join(FG, "cph4", "evolution-ledger.md")
OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r462_debug.txt"
out = io.open(OUT, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

# method A: exact r461_check.py logic
raw = io.open(P1, encoding="utf-8", errors="replace").read()
led = raw.splitlines()
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
hitsA = [l for l in led if pat.search(l)]
w("A_read_splitlines: lines=%d hits=%d" % (len(led), len(hitsA)))

# method B: canon line-iteration
hitsB = [l.rstrip("\n") for l in io.open(P1, encoding="utf-8", errors="replace") if pat.search(l)]
w("B_line_iter: hits=%d" % len(hitsB))

setA = set(l.rstrip() for l in hitsA)
setB = set(l.rstrip() for l in hitsB)
onlyB = sorted(setB - setA)
onlyA = sorted(setA - setB)
w("only_in_B=%d" % len(onlyB))
for l in onlyB[:12]:
    w("  B>> %s" % l[:150])
w("only_in_A=%d" % len(onlyA))
for l in onlyA[:12]:
    w("  A>> %s" % l[:150])

# check for unicode line separators that splitlines() splits but io iteration does not
seps = Counter()
for ch, name in [("\x85", "NEL"), ("\u2028", "LS"), ("\u2029", "PS"), ("\x0b", "VT"), ("\x0c", "FF"), ("\r", "CR")]:
    if ch in raw:
        seps[name] = raw.count(ch)
w("sep_chars=%s" % dict(seps))
out.close()
print("OK")
