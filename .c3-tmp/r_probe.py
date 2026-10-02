import json, re, os, io, glob

BASE = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(BASE, "media", "BigStream")
OUT = os.path.join(BS, ".c3-tmp", "r_probe_out.txt")

def w(f, s):
    f.write(s + "\n")

with io.open(OUT, "w", encoding="utf-8") as f:
    # 1. state.json key fields
    p = os.path.join(BS, "src", "os", "state.json")
    st = json.load(io.open(p, encoding="utf-8"))
    w(f, "== state.json ==")
    for k in ["tick", "ts", "task", "production"]:
        w(f, f"{k} = {st.get(k)}")
    w(f, f"keys = {sorted(st.keys())}")
    wm = st.get("decisions_watermark", {})
    w(f, f"watermark keys = {sorted(wm.keys()) if isinstance(wm, dict) else wm}")
    if isinstance(wm, dict):
        dn = wm.get("dnums", [])
        w(f, f"dnums n={len(dn)} last10={sorted(dn)[-10:]}")
    log = st.get("log", [])
    w(f, f"log n={len(log)}")
    w(f, "== last 3 log lines ==")
    for line in log[-3:]:
        w(f, line)
    # 2. orders dir latest
    w(f, "== orders dir (last 8 by mtime) ==")
    od = os.path.join(BS, "orders")
    files = glob.glob(os.path.join(od, "*"))
    files.sort(key=lambda x: os.path.getmtime(x))
    for x in files[-8:]:
        w(f, f"{os.path.getmtime(x):.0f} {os.path.basename(x)}")
    # 3. evolution-ledger scan
    w(f, "== evolution-ledger @lines ==")
    el = os.path.join(BASE, "cph4", "evolution-ledger.md")
    if os.path.exists(el):
        txt = io.open(el, encoding="utf-8", errors="replace").read().splitlines()
        pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
        hits = [(i+1, l) for i, l in enumerate(txt) if any(p in l for p in pats)]
        w(f, f"total hits = {len(hits)}")
        pn = re.findall(r"P-\d{8}-\d{2}", "\n".join(h[1] for h in hits))
        w(f, f"P-numbers n={len(pn)} last8={pn[-8:]}")
        for i, l in hits[-3:]:
            w(f, f"L{i}: {l[:220]}")
    else:
        w(f, "evolution-ledger MISSING")
    # 4. decisions.md D/C regex diff
    w(f, "== group decisions.md ==")
    dc = os.path.join(BASE, "docs", "decisions.md")
    dnums_file = set()
    if os.path.exists(dc):
        txt = io.open(dc, encoding="utf-8", errors="replace").read()
        found = re.findall(r"[DC]-\d{8}-\d{2}", txt)
        dnums_file = set(found)
        w(f, f"file D/C set n={len(dnums_file)}")
        if isinstance(wm, dict):
            known = set(wm.get("dnums", []))
            new = sorted(dnums_file - known)
            w(f, f"NEW vs watermark n={len(new)}: {new[:30]}")
        # top dispatch board block
        lines = txt.splitlines()
        w(f, "== decisions.md top 25 lines ==")
        for l in lines[:25]:
            if l.strip():
                w(f, l[:200])
        # tail for latest additions
        w(f, "== decisions.md tail 12 non-empty lines ==")
        ne = [l for l in lines if l.strip()]
        for l in ne[-12:]:
            w(f, l[:200])
    else:
        w(f, "decisions.md MISSING")
    # 5. group orders.md CEO physical items + latest O lines
    w(f, "== group orders.md ==")
    go = os.path.join(BASE, "docs", "orders.md")
    if os.path.exists(go):
        txt = io.open(go, encoding="utf-8", errors="replace").read()
        lines = txt.splitlines()
        ne = [l for l in lines if l.strip()]
        w(f, f"non-empty n={len(ne)}")
        for l in ne[-6:]:
            w(f, l[:200])
    # 6. BS daily intel + W40 audit + benchmarks date
    w(f, "== routine checks ==")
    d102 = os.path.join(BS, "data", "intel", "daily", "2026-10-02.md")
    w(f, f"daily 2026-10-02 exists = {os.path.exists(d102)}")
    w40 = os.path.join(BS, "docs", "audits", "2026-W40-self-audit.md")
    w(f, f"W40 self-audit exists = {os.path.exists(w40)}")
    gb = os.path.join(BS, "docs", "global-benchmarks.md")
    if os.path.exists(gb):
        gt = io.open(gb, encoding="utf-8", errors="replace").read()
        m4 = re.search(r"更新记录[^\n]*", gt)
        sec4 = re.search(r"##\s*④[^\n]*\n", gt)
        # first date after section 4 header
        idx = gt.find("④")
        seg = gt[idx:idx+800] if idx >= 0 else ""
        dts = re.findall(r"\d{4}-\d{2}-\d{2}", seg)
        w(f, f"global-benchmarks sec4 dates first={dts[:3]}")
        dts2 = re.findall(r"\d{4}-\d{2}-\d{2}", gt[:2000])
        w(f, f"global-benchmarks head dates={dts2[:3]}")
    # 7. finished.md tail (latest F numbers)
    w(f, "== finished.md last F-numbers ==")
    fm = os.path.join(BS, "output", "finished.md")
    if os.path.exists(fm):
        t = io.open(fm, encoding="utf-8", errors="replace").read()
        fs = re.findall(r"F-\d{3}", t)
        w(f, f"F numbers n={len(fs)} max={max(set(fs)) if fs else None} last5={fs[-5:]}")
    # 8. lock check
    lk = os.path.join(BS, "logs", "iteration-loop", "round.lock")
    w(f, f"round.lock exists = {os.path.exists(lk)}")
    idx_lock = os.path.join(BS, ".git", "index.lock")
    w(f, f"git index.lock exists = {os.path.exists(idx_lock)}")
print("OK")
