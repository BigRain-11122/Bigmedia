import io, re, os
p = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
t = io.open(p, encoding="utf-8").read()
m = re.search(r"CONTENT ENTRIES[^0-9]*(\d+)", t)
m2 = re.search(r"TOTAL[^0-9]*(\d+)", t)
n_keys = t.count('"text"')
print("CONTENT_ENTRIES_marker=%s TOTAL_marker=%s text_keys=%d" % (
    m.group(1) if m else "NONE", m2.group(1) if m2 else "NONE", n_keys))
print("D-06 deliverable exists:", os.path.exists(
    r"docs\research\R-20261001-bigstream-01-city-growth-preview-topics.md"))
