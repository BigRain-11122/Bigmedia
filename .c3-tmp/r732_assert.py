# -*- coding: utf-8 -*-
# R732 trim-chain constraint assertions (R728 law: col2 zero-change + creed
# zero-change + fact-digit preservation + mechanical-only col3 deltas)
import io, re, subprocess, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
def load(v):
    lines = io.open("%s\\data\\sources\\lc016\\voiceover-%s.beats.txt" % (ROOT, v),
                   encoding="utf-8").read().splitlines()
    out = []
    for l in lines:
        if not l.strip():
            continue
        parts = [p.strip() for p in l.split("|")]
        out.append((parts[0], parts[1], parts[2]))
    return out

v1, v2, v3 = load("v1"), load("v2"), load("v3")
report = []
report.append("beats_count v1=%d v2=%d v3=%d" % (len(v1), len(v2), len(v3)))
assert len(v1) == len(v2) == len(v3) == 12, "beat count drift"

# 1. col1+col2 (type + card anchor) zero-change across v1->v2->v3
drift = 0
for i, (a, b, c) in enumerate(zip(v1, v2, v3)):
    if a[0] != b[0] or a[0] != c[0] or a[1] != b[1] or a[1] != c[1]:
        drift += 1
        report.append("COL2_DRIFT beat%d: %r | %r | %r" % (i, a[1], b[1], c[1]))
report.append("col2_zero_change=%s (drift=%d)" % (drift == 0, drift))

# 2. creed line (close beat col3) zero-change
close1 = [b[2] for b in v1 if b[0] == "close"][0]
close3 = [b[2] for b in v3 if b[0] == "close"][0]
report.append("creed_zero_change=%s (%r)" % (close1 == close3, close3))

# 3. fact-digit preservation in v3 spoken column (digits spelled out)
v3all = "".join(b[2] for b in v3)
FACTS = ["六十八岁", "四点半", "第三年", "一九九二年", "每周三", "半个月", "一壶", "一盘"]
missing = [f for f in FACTS if f not in v3all]
report.append("fact_digits_missing=%s" % (missing if missing else "NONE"))

# 4. per-beat col3 char deltas v1->v2->v3
def cnt(s): return len(re.sub(r"\s", "", s))
report.append("--- per-beat col3 char counts (v1/v2/v3, delta v3-v1) ---")
tot = [0, 0, 0]
for i, (a, b, c) in enumerate(zip(v1, v2, v3)):
    ca, cb, cc = cnt(a[2]), cnt(b[2]), cnt(c[2])
    tot[0] += ca; tot[1] += cb; tot[2] += cc
    report.append("b%02d %-6s v1=%3d v2=%3d v3=%3d delta=%+d" % (i, a[0], ca, cb, cc, cc - ca))
report.append("TOTAL v1=%d v2=%d v3=%d delta=%+d" % (tot[0], tot[1], tot[2], tot[2] - tot[0]))

# 5. M1 plain-language check v2 + v3
for v in ("v2", "v3"):
    r = subprocess.run([sys.executable, "src/plain_language_check.py",
                        "--beats", "data/sources/lc016/voiceover-%s.beats.txt" % v],
                       cwd=ROOT, capture_output=True, timeout=120)
    txt = r.stdout.decode("utf-8", errors="replace") + r.stderr.decode("utf-8", errors="replace")
    m = re.search(r"(?:summary|RESULT).*", txt)
    report.append("M1_%s exit=%d %s" % (v, r.returncode, (m.group(0) if m else txt[-200:]).replace("\n", " | ")))

io.open("%s\\.c3-tmp\\r732_assertions.txt" % ROOT, "w", encoding="utf-8").write("\n".join(report))
print("ASSERTIONS_DONE")
