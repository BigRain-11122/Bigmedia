# -*- coding: utf-8 -*-
# R685 new-row extraction: ledger 37->38, decisions 74->75
import io, os, re, time

LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r685_newrows.txt"

buf = []
buf.append("LEDGER mtime=%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(LED))))
with io.open(LED, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
buf.append("LEDGER total_lines=%d" % len(lines))
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线|@全公司|@all-companies")
hits = [(i + 1, l) for i, l in enumerate(lines) if pat.search(l)]
buf.append("LEDGER sixmode_hits=%d" % len(hits))
for ln, l in hits[-3:]:
    buf.append("--- LEDGER L%d ---" % ln)
    buf.append(l.rstrip()[:1500])
buf.append("=== LEDGER last 3 lines ===")
for l in lines[-3:]:
    buf.append(l.rstrip()[:1500])

buf.append("")
buf.append("DECISIONS mtime=%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(DEC))))
with io.open(DEC, "r", encoding="utf-8") as f:
    dl = [l for l in f if l.strip()]
buf.append("DECISIONS nonempty=%d" % len(dl))
for l in dl[-4:]:
    buf.append("--- DEC row ---")
    buf.append(l.rstrip()[:2000])

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(buf))
print("EXTRACT_DONE")
