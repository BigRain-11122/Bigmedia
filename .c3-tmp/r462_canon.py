# r462: canonical ledger scan (r460_canon method) + mode breakdown + r461_check diff probe
import io, re, os
from collections import Counter

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
P1 = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
OUTP = os.path.join(ROOT, ".c3-tmp", "r462_canon.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = [l.rstrip('\n') for l in io.open(P1, encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_matches=%d" % len(hits))
w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode('ascii', 'replace').decode('ascii'))
c = Counter()
for l in hits:
    for m in pat.findall(l):
        c[m] += 1
w("ledger_modes=%s" % dict(c))

# diff probe: what pattern does on-disk r461_check.py actually carry?
src = io.open(os.path.join(ROOT, ".c3-tmp", "r461_check.py"), "rb").read()
try:
    text = src.decode("utf-8")
    enc_note = "utf8_ok"
except UnicodeDecodeError:
    text = src.decode("gbk", errors="replace")
    enc_note = "utf8_decode_FAILED_gbk_fallback"
w("r461_check_encoding=%s bytes=%d" % (enc_note, len(src)))
for line in text.splitlines():
    if "re.compile" in line:
        w("r461_check_pattern_line_ascii=%s" % line.strip()[:120].encode('ascii', 'replace').decode('ascii'))
        w("r461_check_pattern_line_repr=%r" % (line.strip()[:120],))
        m = re.search(r're\.compile\(r"([^"]*)"\)', line)
        if m:
            p2 = re.compile(m.group(1))
            hits2 = [l for l in io.open(P1, encoding='utf-8', errors='replace') if p2.search(l)]
            w("r461_check_pattern_hits=%d" % len(hits2))
out.close()
print("OK")
