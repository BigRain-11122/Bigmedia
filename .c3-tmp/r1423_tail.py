# -*- coding: utf-8 -*-
import io, codecs
out = io.open(r".c3-tmp\r1423_probes_tail.txt", "w", encoding="utf-8")
for f in ["board", "readiness", "lh"]:
    p = r".c3-tmp\r1423_probe_%s.txt" % f
    raw = open(p, "rb").read()
    if raw.startswith(codecs.BOM_UTF16_LE) or (len(raw) > 4 and raw[1:2] == b"\x00"):
        txt = raw.decode("utf-16", errors="replace")
    else:
        try:
            txt = raw.decode("utf-8")
        except UnicodeDecodeError:
            txt = raw.decode("gbk", errors="replace")
    lines = [l for l in txt.splitlines() if l.strip()]
    out.write("=== %s (tail 16 non-empty) ===\n" % f)
    for l in lines[-16:]:
        out.write(l.rstrip()[:220] + "\n")
    out.write("\n")
out.close()
print("ok")
