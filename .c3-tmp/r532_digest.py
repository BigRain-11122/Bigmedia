# -*- coding: utf-8 -*-
# Decode probe outputs (PS 5.1 > redirection = UTF-16LE) and write UTF-8 digest
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r532_probe_digest.txt")
out = []

def sniff(p):
    with open(p, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16-le", errors="replace")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig", errors="replace")
    try:
        return raw.decode("utf-8")
    except Exception:
        return raw.decode("gbk", errors="replace")

for name in ("r532_board", "r532_readiness", "r532_loop"):
    p = os.path.join(ROOT, ".c3-tmp", name + ".txt")
    if not os.path.exists(p):
        out.append(name + "=MISSING")
        continue
    text = sniff(p)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    out.append("=== " + name + " total_lines=" + str(len(lines)) + " ===")
    keys = ("FAIL", "WARN", "PASS", "blocker", "findings", "tick", "done", "beats", "exit",
            "阻塞", "发现", "探针", "对账")
    if name == "r532_board":
        out.extend("  " + ln for ln in lines[-6:])
    elif name == "r532_readiness":
        out.extend("  " + ln for ln in lines[-22:])
    else:
        for ln in lines:
            if any(k in ln for k in keys):
                out.append("  " + ln[:200])

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("DIGEST_OK lines=" + str(len(out)))
