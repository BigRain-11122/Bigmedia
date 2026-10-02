# -*- coding: utf-8 -*-
"""R982 pool sprite top-level key structure check (leaf 1440 baseline accounting)."""
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))

out = []
sp = pool.get("sprite")
out.append(u"sprite type=%s" % type(sp).__name__)
if isinstance(sp, dict):
    tot = 0
    for k, v in sorted(sp.items()):
        if isinstance(v, list):
            out.append(u"sprite.%s list=%d" % (k, len(v)))
            tot += len(v)
        elif isinstance(v, dict):
            for k2, v2 in sorted(v.items()):
                if isinstance(v2, list):
                    out.append(u"sprite.%s.%s list=%d" % (k, k2, len(v2)))
                    tot += len(v2)
                else:
                    out.append(u"sprite.%s.%s type=%s" % (k, k2, type(v2).__name__))
        else:
            out.append(u"sprite.%s type=%s val=%s" % (k, type(v).__name__, json.dumps(v, ensure_ascii=False)[:200]))
    out.append(u"sprite total leaves=%d" % tot)
    axes_total = 1296
    out.append(u"grand total = %d + %d = %d (baseline 1440)" % (axes_total, tot, axes_total + tot))

# axes key names (write UTF-8 for reliable read)
axes_names = sorted(pool.get("axes", {}).keys())
out.append(u"axes names: %s" % u", ".join(axes_names))
# sprite axes names if dict-of-axes style
if isinstance(sp, dict):
    out.append(u"sprite keys: %s" % u", ".join(sorted(sp.keys())))

io.open(os.path.join(BS, ".c3-tmp", "r982_sprite.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("SPRITE-OK")
