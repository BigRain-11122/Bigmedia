# -*- coding: utf-8 -*-
# read full L177/L181 ledger rows + P-20260929-04 detail + check runbook.md existence
import io, re, os
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
out = []
with io.open(LED, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
out.append("=== L177 ===\n" + lines[176])
out.append("=== L181 ===\n" + lines[180])
# check state/runbook.md
rb = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\state\runbook.md"
out.append("runbook_exists=%s" % os.path.exists(rb))
# any reference to runbook in cph4 orders/docs
import glob
for pat in [r"C:\Users\sjs20\Desktop\FluxGroup\cph4\*.md"]:
    for fp in glob.glob(pat):
        try:
            t = io.open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"[^\n]*runbook[^\n]*", t):
                s = m.group(0).strip()
                if len(s) > 10:
                    out.append("%s :: %s" % (os.path.basename(fp), s[:300]))
        except Exception:
            pass
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r681_l177_l181.txt"), "w", encoding="utf-8").write("\n\n".join(out))
print("written", len("\n\n".join(out)))
