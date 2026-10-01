import io, os, re, json

GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(GRP, "media", "BigStream")
OUT = []

p = os.path.join(GRP, "life", "BigLife", "cognition", "interchat-ledger.jsonl")
OUT.append("exists=%s" % os.path.exists(p))
if os.path.exists(p):
    import datetime
    OUT.append("mtime=%s size=%d" % (datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"), os.path.getsize(p)))
    entries = []
    for ln in io.open(p, "r", encoding="utf-8"):
        ln = ln.strip()
        if ln:
            try:
                entries.append(json.loads(ln))
            except Exception:
                pass
    OUT.append("entries=%d" % len(entries))
    if entries:
        OUT.append("keys: " + str(list(entries[0].keys())))
        for i, e in enumerate(entries):
            OUT.append("--- #%d ts=%s ---" % (i, str(e.get("ts") or e.get("time") or "")[:19]))
            OUT.append(json.dumps(e, ensure_ascii=False)[:600])

with io.open(os.path.join(BS, ".c3-tmp", "r912_ic.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("lines:", len(OUT))
