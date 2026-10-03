# -*- coding: utf-8 -*-
"""R1065 deep probe: claimable-surface enumeration before any declared-idle.
Targets: #86 codex leg supply state, E30 DAILY supply-protection rationale,
queue tail (E17-E30), R1031/R1032/R893/R912/R1064 full log lines."""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
w = out.append

with open(os.path.join(ROOT, "src/os/state.json"), encoding="utf-8") as f:
    state = json.load(f)
log = state.get("log", [])

targets = ["R1030", "R1031", "R1032", "R893", "R912", "R1064"]
w("=== full log lines for %s ===" % targets)
for e in log:
    m = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}[xX]? (R\d+):", e)
    if m and m.group(1) in targets:
        w("--- %s ---" % m.group(1))
        w(e[:4200])

# queue tail beyond line 130 non-empty
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
with open(q, encoding="utf-8") as f:
    qlines = f.read().splitlines()
w("=== queue non-empty lines 131..210 ===")
cnt = 0
picked = 0
for l in qlines:
    s = l.strip()
    if s:
        cnt += 1
        if cnt > 130 and picked < 80:
            w(s[:190])
            picked += 1

# codex file states
for fn in ("city-spirit.md", "city-humanities.md", "city-residents.md"):
    p = os.path.join(ROOT, "docs", fn)
    if not os.path.exists(p):
        # try research/ or other locations
        for cand in (os.path.join(ROOT, "research", fn), os.path.join(ROOT, "docs", "codex", fn)):
            if os.path.exists(cand):
                p = cand
                break
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            lines = f.read().splitlines()
        w("=== %s: %d lines; last 18 ===" % (os.path.basename(p), len(lines)))
        for l in lines[-18:]:
            w(l[:170])
    else:
        w("[codex] %s NOT FOUND at docs/ or research/" % fn)

# interchat ledger count
il = os.path.join(GRP, "media", "BigLife", "cognition", "interchat-ledger.jsonl")
if not os.path.exists(il):
    il = os.path.join(GRP, "media", "BigLife", "cognition", "interchat-ledger.jsonl")
for cand in (
    os.path.join(GRP, "media", "BigLife", "cognition", "interchat-ledger.jsonl"),
    os.path.join(GRP, "media", "BigLife", "cognition", "interchat_ledger.jsonl"),
):
    if os.path.exists(cand):
        il = cand
        break
if os.path.exists(il):
    with open(il, encoding="utf-8") as f:
        n = sum(1 for _ in f)
    w("[interchat] %s lines=%d (R912 baseline=22)" % (os.path.basename(il), n))
else:
    w("[interchat] ledger not found at expected path; globbing...")
    for dirpath, dirnames, filenames in os.walk(os.path.join(GRP, "media", "BigLife", "cognition")):
        for f2 in filenames:
            if "interchat" in f2:
                w("  found: %s" % os.path.join(dirpath, f2))

# LC-019 (E16) registration check
fin = os.path.join(ROOT, "output", "finished.md")
with open(fin, encoding="utf-8") as f:
    fc = f.read()
w("=== LC-019 / lc-019 in finished.md ===")
for m in re.finditer(r"^.*(?:LC-019|lc-019).*$", fc, re.M):
    w(m.group(0)[:200])
w("=== E16/E20 F-reg check: F-074 header ===")
for m in re.finditer(r"^## F-07[0-9].*$", fc, re.M):
    w(m.group(0)[:170])

# cards README DAILY lane ledger
cr = os.path.join(ROOT, "data", "storylines", "cards", "README.md")
if os.path.exists(cr):
    with open(cr, encoding="utf-8") as f:
        clines = f.read().splitlines()
    w("=== cards/README.md %d lines; DAILY-related tail ===" % len(clines))
    didx = [i for i, l in enumerate(clines) if "DAILY" in l or "日签" in l]
    if didx:
        lo = max(0, didx[-1] - 5)
        for l in clines[lo:min(len(clines), didx[-1] + 45)]:
            w(l[:180])
else:
    w("[cards README] not found")

# r1035_scan.py referenced by previous rounds
w("[check] .c3-tmp/r1035_scan.py exists=%s" % os.path.exists(os.path.join(ROOT, ".c3-tmp", "r1035_scan.py")))

with open(os.path.join(ROOT, ".c3-tmp", "r1065_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("probe done:", len(out), "lines")
