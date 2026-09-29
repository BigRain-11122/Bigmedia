import json, io, re, os, time
root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
d = json.load(io.open(os.path.join(root, "src/os/state.json"), encoding="utf-8"))
print("TICK", d.get("tick"), "TS", d.get("ts"), "PROD", d.get("production"))
print("TASK", str(d.get("task"))[:260])
print("== last 2 state logs ==")
for e in d["log"][-2:]:
    print("HEAD:", e[:350])
    print("TAIL:", e[-850:])
    print("----")
t = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8", errors="ignore").read()
ms = [l for l in t.splitlines() if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线", l)]
print("LEDGER_N", len(ms))
for l in ms[-3:]:
    print("LL:", l[:280])
t2 = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8", errors="ignore").read()
print("DEC_N", len([l for l in t2.splitlines() if l.strip()]))
print("== bm-a codex activity mtime ==")
for p in ["data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"]:
    fp = os.path.join(root, p)
    if os.path.exists(fp):
        print("MTIME", p, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fp))))
print("== pending E4 results (DIGEST-v10 / REACT-v5) ==")
for fp in [r"data\storylines\cards\MC-20260929-DIGEST-v10-tmp\e4-result.json",
           r"data\storylines\cards\MC-20260929-REACT-v5-tmp\e4-result.json"]:
    f = os.path.join(root, fp)
    if os.path.exists(f):
        j = json.load(io.open(f, encoding="utf-8"))
        s = json.dumps(j, ensure_ascii=False)
        print("E4RES", fp.split("\\")[-2], "mtime", time.strftime("%m-%d %H:%M:%S", time.localtime(os.path.getmtime(f))))
        print("E4TEXT", s[:500])
print("== backlog item headers ==")
bk = io.open(os.path.join(root, "src/os/backlog.md"), encoding="utf-8").read().splitlines()
for i, l in enumerate(bk):
    if re.match(r"^\d+\.\s", l):
        print("L%d %s" % (i + 1, l[:130]))
print("== queue E tail ==")
q = io.open(os.path.join(root, "docs/self-improvement-queue.md"), encoding="utf-8", errors="ignore").read().splitlines()
for l in q[-40:]:
    print("Q:", l[:180])
