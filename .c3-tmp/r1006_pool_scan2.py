# -*- coding: utf-8 -*-
# R1006 pool scan v2: hardcoded consumed (axis,idx) pairs per R981 method (build-script documented face)
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))

# consumed festival picks: DAILY v1-v37 + REACT-v8 trio + city-spirit v1.2 trio
consumed = {
    ("求新", 4), ("怀旧", 0), ("侠气", 5), ("烟火", 4), ("秩序", 4), ("逍遥", 3),   # v1-v6
    ("求新", 7), ("侠气", 13), ("求新", 12), ("怀旧", 3), ("烟火", 13), ("逍遥", 15),  # v7-v12
    ("侠气", 2), ("求新", 3), ("求新", 11), ("怀旧", 1), ("秩序", 12), ("逍遥", 1),   # v13-v18
    ("烟火", 3), ("侠气", 1), ("秩序", 6), ("怀旧", 12), ("求新", 13), ("烟火", 2),   # v19-v24
    ("怀旧", 17), ("侠气", 10), ("烟火", 7), ("秩序", 9), ("逍遥", 2), ("秩序", 2),   # v25-v30
    ("逍遥", 4), ("烟火", 10), ("怀旧", 4), ("侠气", 9), ("秩序", 11), ("逍遥", 16),   # v31-v36
    ("求新", 5),                                                                       # v37
    ("逍遥", 17), ("烟火", 12), ("秩序", 14),   # REACT-v8 source_facts trio
    ("秩序", 16), ("求新", 14), ("侠气", 0),    # city-spirit v1.2 festival trio
}
labels = {}
dl = {("求新", 4): "DAILY-v1", ("怀旧", 0): "DAILY-v2", ("侠气", 5): "DAILY-v3", ("烟火", 4): "DAILY-v4",
      ("秩序", 4): "DAILY-v5", ("逍遥", 3): "DAILY-v6", ("求新", 7): "DAILY-v7", ("侠气", 13): "DAILY-v8",
      ("求新", 12): "DAILY-v9", ("怀旧", 3): "DAILY-v10", ("烟火", 13): "DAILY-v11", ("逍遥", 15): "DAILY-v12",
      ("侠气", 2): "DAILY-v13", ("求新", 3): "DAILY-v14", ("求新", 11): "DAILY-v15", ("怀旧", 1): "DAILY-v16",
      ("秩序", 12): "DAILY-v17", ("逍遥", 1): "DAILY-v18", ("烟火", 3): "DAILY-v19", ("侠气", 1): "DAILY-v20",
      ("秩序", 6): "DAILY-v21", ("怀旧", 12): "DAILY-v22", ("求新", 13): "DAILY-v23", ("烟火", 2): "DAILY-v24",
      ("怀旧", 17): "DAILY-v25", ("侠气", 10): "DAILY-v26", ("烟火", 7): "DAILY-v27", ("秩序", 9): "DAILY-v28",
      ("逍遥", 2): "DAILY-v29", ("秩序", 2): "DAILY-v30", ("逍遥", 4): "DAILY-v31", ("烟火", 10): "DAILY-v32",
      ("怀旧", 4): "DAILY-v33", ("侠气", 9): "DAILY-v34", ("秩序", 11): "DAILY-v35", ("逍遥", 16): "DAILY-v36",
      ("求新", 5): "DAILY-v37", ("逍遥", 17): "REACT-v8", ("烟火", 12): "REACT-v8", ("秩序", 14): "REACT-v8",
      ("秩序", 16): "spirit", ("求新", 14): "spirit", ("侠气", 0): "spirit"}

out = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1006_pool_scan.txt", "w", encoding="utf-8")
free_total = 0
for ax in [u"求新", u"怀旧", u"侠气", u"烟火", u"秩序", u"逍遥"]:
    fest = pool["axes"][ax][u"festival"]
    out.write(u"== %s festival ==\n" % ax)
    for i, ln in enumerate(fest):
        if (ax, i) in consumed:
            mark = u"USED(%s)" % dl[(ax, i)]
        elif u"年味" in ln:
            mark = u"AVOID(年味)"
        else:
            mark = u"FREE"
            free_total += 1
        out.write(u"[%d] %s %s\n" % (i, mark, ln))
out.write(u"\nROTATION DAILY counts post-v37: 求新 7 / 怀旧 6 / 侠气 6 / 烟火 6 / 秩序 6 / 逍遥 6\n")
out.write(u"FREE total=%d (USED 43 + AVOID 18 + FREE = 108)\n" % free_total)
out.close()
print("pool scan v2 written, FREE=%d" % free_total)
