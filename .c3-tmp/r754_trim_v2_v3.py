# -*- coding: utf-8 -*-
# R754 LC-021 trim v2/v3 machine assertions (r752_trim_v2/v3.py precedent)
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/sources/lc021"

def parse(ver):
    rows = []
    for ln in (SRC / ("voiceover-%s.beats.txt" % ver)).read_text(encoding="utf-8").splitlines():
        parts = ln.split(" | ")
        assert len(parts) == 3, "bad row %r" % ln[:40]
        rows.append((parts[0], parts[1], parts[2]))
    return rows

def nchars(s):
    return len(re.sub(r"[，。：；——、·！？「」『』,.\s]", "", s))

v1, v2, v3 = parse("v1"), parse("v2"), parse("v3")
assert len(v1) == len(v2) == len(v3) == 12, "row count"

# col1 type + col2 card-anchor verbatim zero-touch (v1<->v2<->v3)
for a, b, c in zip(v1, v2, v3):
    assert a[0] == b[0] == c[0], "col1 drift %s" % a[0]
    assert a[1] == b[1] == c[1], "col2 drift: %r" % a[1][:30]

v3vo = "".join(r[2] for r in v3)
# creed verbatim
assert "队形不能乱，人心更不能散" in v3vo, "creed"
# factual numbers preserved in spoken column
for tok in ["五十八", "十九年", "七个人", "四十三", "三分贝", "三块糖"]:
    assert tok in v3vo, "factual num lost: %s" % tok
# anchor names preserved
for tok in ["沈佩兰", "沈老师", "老对头"]:
    assert tok in v3vo, "name lost: %s" % tok
# CTA audience phrase
assert "起得比太阳早" in v3vo, "cta audience phrase"
# hook syslog marker
assert v3[0][2].startswith("系统日志："), "hook syslog marker"
# spoken char chain v1->v2->v3 (no-punct) monotonically decreasing
c1 = nchars("".join(r[2] for r in v1))
c2 = nchars("".join(r[2] for r in v2))
c3 = nchars("".join(r[2] for r in v3))
assert c1 > c2 > c3, "char chain %d %d %d" % (c1, c2, c3)
print("OK col1/col2 verbatim 12/12 x2-basis; creed verbatim; nums 五十八/十九年/七个人/四十三/三分贝/三块糖 kept; names 沈佩兰/沈老师/老对头 kept; cta phrase kept; syslog hook kept")
print("CHARS v1=%d v2=%d v3=%d" % (c1, c2, c3))
