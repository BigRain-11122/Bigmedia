import json, os, re, subprocess

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []

# 1. state.json core + log tail 3
with open(os.path.join(root, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
out.append(f"tick={st.get('tick')} production={st.get('production')} ts={st.get('ts')}")
out.append(f"task={st.get('task')}")
log = st.get("log", [])
out.append(f"log_len={len(log)}")
out.append("LOG_TAIL_3:")
for line in log[-3:]:
    out.append("  " + line[:500])

# 2. orders latest 8 by mtime
od = os.path.join(root, "orders")
files = sorted(os.listdir(od), key=lambda x: os.path.getmtime(os.path.join(od, x)))
out.append("ORDERS_LAST8: " + " | ".join(files[-8:]))

# 3. group ledger five-pattern scan
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
if os.path.exists(ledger):
    with open(ledger, encoding="utf-8") as f:
        lines = f.read().splitlines()
    pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
    hits = [(i, l) for i, l in enumerate(lines) if pat.search(l)]
    out.append(f"LEDGER_5PAT_LINES={len(hits)}")
    for i, l in hits[-4:]:
        out.append(f"  L{i}: {l[:180]}")
else:
    out.append("LEDGER_MISSING")

# 4. group decisions non-empty count + tail 3
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
if os.path.exists(dec):
    with open(dec, encoding="utf-8") as f:
        txt = f.read()
    ne = [l for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")]
    out.append(f"DECISIONS_NONEMPTY={len(ne)}")
    for l in ne[-3:]:
        out.append("  D: " + l[:160])
else:
    out.append("DECISIONS_MISSING")

# 5. git status + lock
r = subprocess.run(["git", "status", "--short"], cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
gs = (r.stdout or "").strip()
out.append("GIT_STATUS_CLEAN" if not gs else "GIT_STATUS:")
if gs:
    out.append(gs[:1500])
out.append(f"INDEX_LOCK={'YES' if os.path.exists(os.path.join(root, '.git', 'index.lock')) else 'NO'}")
r2 = subprocess.run(["git", "log", "-1", "--format=%h %s"], cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
out.append("HEAD: " + (r2.stdout or "").strip()[:200])

# 6. routine anchors
out.append(f"INTEL_0927={'YES' if os.path.exists(os.path.join(root, 'data', 'intel', 'daily', '2026-09-27.md')) else 'NO'}")
out.append(f"W39_AUDIT={'YES' if os.path.exists(os.path.join(root, 'docs', 'audits', '2026-W39-self-audit.md')) else 'NO'}")
auds = os.listdir(os.path.join(root, "docs", "audits"))
out.append("AUDITS_RECENT: " + " | ".join(sorted(auds)[-6:]))
# CENSUS anchor check
out.append(f"C00030_ANCHOR={'YES' if os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md') else 'NO'}")

with open(os.path.join(root, ".c3-tmp", "fastpath_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
