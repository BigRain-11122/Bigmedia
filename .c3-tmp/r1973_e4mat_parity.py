# -*- coding: utf-8 -*-
# r1973: e4-material transcript parity check (SC-005-04/05/06 vs beats spoken column)
import io

base = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\audio"
pairs = [("SC-005-04-v1", "sc005-04-v1-tmp"), ("SC-005-05-v1", "sc005-05-v1-tmp"), ("SC-005-06-v1", "sc005-06-v1-tmp")]
MARKER = u"\u5168\u6587\u7a3f\uff08\u53e3\u64ad\u5168\u6587\u6458\u5f55\uff0c\u4f9b\u5bf9\u4f4d\uff09\uff1a"  # 全文稿（口播全文摘录，供对位）：
ok_all = True
for stem, tmp in pairs:
    beats = io.open(base + "\\" + stem + ".beats.txt", encoding="utf-8").read().splitlines()
    spoken = [ln.split("|")[2].strip() for ln in beats if ln.strip() and not ln.startswith("#") and ln.count("|") >= 2]
    mat = io.open(base + "\\" + tmp + "\\e4-material.md", encoding="utf-8").read()
    head, sep, tail = mat.partition(MARKER)
    if not sep:
        print(stem + ": MARKER-MISSING"); ok_all = False; continue
    mat_lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
    miss = 0
    for i, sp in enumerate(spoken):
        if i < len(mat_lines) and sp == mat_lines[i]:
            continue
        miss += 1
        print(stem + " cue" + str(i + 1) + ": MISS")
        if i < len(mat_lines):
            print("  beats :", sp[:60])
            print("  mat   :", mat_lines[i][:60])
    extra = len(mat_lines) - len(spoken)
    verdict = "PARITY-OK" if miss == 0 and extra == 0 else "FAIL"
    print("%s: beats_spoken=%d mat_lines=%d miss=%d extra=%d %s" % (stem, len(spoken), len(mat_lines), miss, extra, verdict))
    ok_all = ok_all and miss == 0 and extra == 0
print("ALL:", "GREEN" if ok_all else "FAIL")
