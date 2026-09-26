# r460: canonical ledger scan (reuse r459_check method) + last log line tail
import io, re, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
P1 = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
P2 = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
OUTP = os.path.join(ROOT, ".c3-tmp", "r460_canon.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = [l.rstrip('\n') for l in io.open(P1, encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_matches=%d" % len(hits))
w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode('ascii', 'replace').decode('ascii'))
from collections import Counter
c = Counter()
for l in hits:
    for m in pat.findall(l):
        c[m] += 1
w("ledger_modes=%s" % dict(c))

d = [l for l in io.open(P2, encoding='utf-8') if l.strip()]
w("decisions_nonempty=%d" % len(d))

st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
last = st["log"][-1]
w("last_log_tail=%s" % last[-700:])
out.close()
print("OK")
