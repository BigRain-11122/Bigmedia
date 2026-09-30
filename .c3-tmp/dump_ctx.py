import json, io, os

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
A = out.append

p = os.path.join(repo, "output", "renders", "lc-004-v1-shipinhao-60s.mp4.plan.json")
j = json.load(io.open(p, encoding="utf-8"))
A("=== plan snippet ===")
A(json.dumps({k: j.get(k) for k in ("series", "hits", "s45_dials", "duration", "total_duration")}, ensure_ascii=False, indent=1))

t = io.open(os.path.join(repo, "docs", "reviews", "station-reviews.md"), encoding="utf-8").read().splitlines()
A(f"=== station-reviews tail (total {len(t)} lines) ===")
for ln in t[-12:]:
    A(ln[:400])

A("=== lc004 README ===")
A(io.open(os.path.join(repo, "data", "sources", "lc004", "README.md"), encoding="utf-8").read())

A("=== status-export.json ===")
A(io.open(os.path.join(repo, "docs", "status-export.json"), encoding="utf-8").read())

rr = io.open(os.path.join(repo, "output", "renders", "README.md"), encoding="utf-8").read().splitlines()
A(f"=== renders README: LC-004 lines + table head ===")
for i, ln in enumerate(rr):
    if "lc-004" in ln or "LC-004" in ln:
        A(f"L{i+1}: " + ln[:500])
for i, ln in enumerate(rr):
    if ln.strip().startswith("|") and ("lc-003" in ln or "lc-002" in ln):
        A(f"T{i+1}: " + ln[:400])

q = io.open(os.path.join(repo, "docs", "self-improvement-queue.md"), encoding="utf-8").read().splitlines()
A("=== queue E4 line + burn tail ===")
for i, ln in enumerate(q):
    if "E4 LC-004" in ln:
        A(f"Q{i+1}: " + ln[:700])
A("queue_burn_tail:")
for ln in q[-6:]:
    A(ln[:250])

io.open(os.path.join(repo, ".c3-tmp", "ledger-ctx.txt"), "w", encoding="utf-8").write("\n".join(out))
print("WROTE", len(out))
