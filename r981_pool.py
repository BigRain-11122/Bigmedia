# R981: dump festival bucket of all axes with consumption marks for DAILY v12 line pick
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))

# consumed (documented in build_daily_v11.py): DAILY v1-v11 + REACT-v8 same-bucket trio
consumed = {
    ("求新", 4), ("怀旧", 0), ("侠气", 5), ("烟火", 4), ("秩序", 4), ("逍遥", 3),
    ("求新", 7), ("侠气", 13), ("求新", 12), ("怀旧", 3), ("烟火", 13),
    ("逍遥", 17), ("烟火", 12), ("秩序", 14),
}
NY = [u"年味", u"过年", u"春节", u"春联", u"红包", u"拜年", u"除夕", u"年夜", u"鞭炮", u"爆竹", u"守岁", u"压岁"]

out = io.open("r981_pool.txt", "w", encoding="utf-8")
for ax in [u"求新", u"怀旧", u"侠气", u"烟火", u"秩序", u"逍遥"]:
    fest = pool["axes"][ax]["festival"]
    out.write(u"=== %s (%d lines) ===\n" % (ax, len(fest)))
    for i, ln in enumerate(fest):
        mark = u"USED" if (ax, i) in consumed else u"    "
        ny = u" [NY?" + u",".join(w for w in NY if w in ln) + u"]" if any(w in ln for w in NY) else u""
        out.write(u"%s [%2d] %s%s\n" % (mark, i, ln, ny))
out.close()
print("written r981_pool.txt")
