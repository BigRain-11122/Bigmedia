import io, json, os, datetime, hashlib

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1368_dusk.txt", "w", encoding="utf-8")
w = out.write

pp = base + r"\life\BigLife\cognition\pools.json"
raw = io.open(pp, encoding="utf-8").read()
w("len=%s mtime=%s\n" % (len(raw), datetime.datetime.fromtimestamp(os.path.getmtime(pp)).strftime("%m-%d %H:%M:%S")))
w("sha256=%s\n" % hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16])
w("has_umbrella=%s\n" % ("修了这么多伞" in raw))
idx = raw.find("修了这么多伞")
if idx >= 0:
    w("ctx=%s\n" % raw[max(0, idx - 220):idx + 120])
else:
    # find all dusk rows to see what remains
    try:
        pj = json.loads(raw)
        keys = list(pj.keys())
        w("top_keys=%s\n" % keys[:20])
        for k in keys:
            v = pj[k]
            if isinstance(v, list):
                w("k=%s n=%s\n" % (k, len(v)))
                dusk = [x for x in v if isinstance(x, dict) and "dusk" in json.dumps(x, ensure_ascii=False)]
                if dusk:
                    w("  dusk_rows=%s\n" % json.dumps(dusk[:3], ensure_ascii=False)[:500])
            elif isinstance(v, dict):
                sub = list(v.keys())
                w("k=%s(dict) sub=%s\n" % (k, sub[:10]))
                for sk in sub:
                    sv = v[sk]
                    if isinstance(sv, list):
                        w("  k=%s.%s n=%s\n" % (k, sk, len(sv)))
                        dusk = [x for x in sv if "dusk" in json.dumps(x, ensure_ascii=False)]
                        if dusk:
                            w("  dusk_rows=%s\n" % json.dumps(dusk[:3], ensure_ascii=False)[:600])
            else:
                w("k=%s scalar=%s\n" % (k, str(v)[:60]))
    except Exception as e:
        w("parse_err=%s %s\n" % (type(e).__name__, str(e)[:200]))

# git status of BigLife worktree for the pools file (read-only)
out.close()
print("ok")
