# r512_check2.py - anomaly resolution: new order file / +3 ledger lines / render-stale source / backlog top / interchat ledger
import os, io, time, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
OUT = os.path.join(ROOT, ".c3-tmp", "r512-report2.md")
lines = []
def w(s=""):
    lines.append(str(s))

def main():
    # 1. full orders listing with mtime
    odir = os.path.join(ROOT, "orders")
    files = sorted([(f, os.path.getmtime(os.path.join(odir, f))) for f in os.listdir(odir) if f.endswith(".md")])
    w("## orders_all_36")
    for f, m in files:
        w("  %s | %s" % (time.strftime("%m-%d %H:%M", time.localtime(m)), f))

    # 2. ledger: all five-mode lines with numbers + git log of ledger file
    modes = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
    with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as fh:
        all_lines = fh.read().splitlines()
    w("## ledger_matched_34")
    for i, s in enumerate(all_lines, 1):
        if any(m in s for m in modes):
            w("L%d: %s" % (i, s[:220]))
    # tail rows (last 8 non-empty) to see newest entries
    w("## ledger_tail8")
    ne = [(i, s) for i, s in enumerate(all_lines, 1) if s.strip()]
    for i, s in ne[-8:]:
        w("L%d: %s" % (i, s[:220]))

    # 3. census-card-v7-vertical.mp4 where?
    w("## census_card_v7_vertical_search")
    for base in [os.path.join(ROOT, "output", "renders"), os.path.join(ROOT, ".lc001-tmp"), os.path.join(ROOT, "data", "sources", "lc001")]:
        if os.path.isdir(base):
            for f in os.listdir(base):
                if "census" in f.lower():
                    p = os.path.join(base, f)
                    w("  %s | %s | %d bytes" % (p, time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(p))), os.path.getsize(p)))
    # grep renders README for the row
    rr = os.path.join(ROOT, "output", "renders", "README.md")
    with io.open(rr, "r", encoding="utf-8", errors="replace") as fh:
        rl = fh.read().splitlines()
    w("## renders_readme_census_rows")
    for i, s in enumerate(rl, 1):
        if "census-card" in s or "lc-001" in s:
            w("L%d: %s" % (i, s[:240]))

    # 4. backlog top (first 40 raw lines)
    w("## backlog_head40")
    with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8", errors="replace") as fh:
        bl = fh.read().splitlines()
    for s in bl[:40]:
        w(s[:220])

    # 5. interchat ledger inspect
    il = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\interchat-ledger.jsonl"
    w("## interchat_ledger")
    w("mtime=%s size=%d" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(il))), os.path.getsize(il)))
    with io.open(il, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    jl = [l for l in content.splitlines() if l.strip()]
    w("jsonl_records=%d" % len(jl))
    if jl:
        w("first_record=%s" % jl[0][:400])
        w("last_record=%s" % jl[-1][:400])

    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("OK")

if __name__ == "__main__":
    main()
