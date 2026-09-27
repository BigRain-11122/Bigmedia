# r512_check.py - R512 five-check + three probes (write UTF-8 report, zero PS round trips)
import os, subprocess, sys, json, io, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DECISIONS = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
OUT = os.path.join(ROOT, ".c3-tmp", "r512-report.md")

lines = []
def w(s=""):
    lines.append(str(s))

def main():
    # 1. orders check
    odir = os.path.join(ROOT, "orders")
    files = [(f, os.path.getmtime(os.path.join(odir, f))) for f in os.listdir(odir) if f.endswith(".md")]
    files.sort(key=lambda x: -x[1])
    w("## orders")
    w("count=%d (anchor 35)" % len(files))
    for f, m in files[:3]:
        w("  %s mtime=%s" % (f, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(m))))
    # files edited after 12:14:30 excluding O-1050 self-append
    thr = time.mktime(time.strptime("2026-09-27 12:14:30", "%Y-%m-%d %H:%M:%S"))
    edited = [f for f, m in files if m > thr and not f.startswith("O-20260927-1050")]
    w("new_since_anchor_excl_selfappend=%s" % (edited if edited else "NONE"))
    w("o1050_mtime=%s (R511 self-append expected ~12:36)" % time.strftime("%H:%M:%S", time.localtime(files[0][1]) if files[0][0].startswith("O-20260927-1050") else 0))

    # 2. ledger five-mode count (strict @ prefix, case-sensitive; anchor 31)
    modes = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
    cnt = 0
    per = {}
    bs_lines = []
    with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as fh:
        for i, ln in enumerate(fh, 1):
            s = ln.rstrip("\n")
            hit = None
            for m in modes:
                if m in s:
                    hit = m
                    cnt += 1
                    per[m] = per.get(m, 0) + 1
            if hit == "@BigStream":
                bs_lines.append("L%d: %s" % (i, s[:160]))
    w("## ledger")
    w("five_mode_count=%d (anchor 31)" % cnt)
    w("per_mode=%s" % per)
    for b in bs_lines[-5:]:
        w("  " + b)

    # 3. decisions non-empty line count (UTF-8; anchor 56)
    with io.open(DECISIONS, "r", encoding="utf-8", errors="replace") as fh:
        dl = [l for l in fh if l.strip()]
    w("## decisions")
    w("nonempty_lines=%d (anchor 56)" % len(dl))

    # 4. state fields + index.lock
    st = json.load(open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
    w("## state")
    w("production=%s tick=%s ts=%s" % (st.get("production"), st.get("tick"), st.get("ts")))
    w("index_lock_exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

    # 5. backlog top items (first bullet lines)
    w("## backlog_top")
    with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8", errors="replace") as fh:
        bl = fh.read().splitlines()
    shown = 0
    for l in bl:
        if l.strip().startswith(("- [ ]", "- [x]", "##")):
            w("  " + l[:200])
            shown += 1
        if shown >= 8:
            break

    # 6. window items
    w("## window_items")
    anchors_dir = None
    for cand in [r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors", r"C:\Users\sjs20\Desktop\FluxGroup\BigLife\census\anchors"]:
        if os.path.isdir(cand):
            anchors_dir = cand
            break
    if anchors_dir:
        afiles = sorted(f for f in os.listdir(anchors_dir) if f.endswith(".md"))
        w("anchors_dir=%s files=%d last3=%s" % (anchors_dir, len(afiles), afiles[-3:]))
        w("C-00030_in_place=%s C-00031_in_place=%s" % ("C-00030.md" in afiles, "C-00031.md" in afiles))
    else:
        w("anchors_dir=NOT FOUND")
    # #72 BigLife interchat ledger probe
    hits = []
    bl_root = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife"
    if os.path.isdir(bl_root):
        for dirpath, dirnames, filenames in os.walk(bl_root):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for f in filenames:
                if ("互聊" in f) or ("interchat" in f.lower()):
                    hits.append(os.path.join(dirpath, f))
    w("biglife_interchat_hits=%s" % (hits if hits else "0 (pending)"))
    w("daily_0927=%s daily_0928=%s" % (
        os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")),
        os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md"))))
    w("W40_audit=%s" % os.path.exists(os.path.join(ROOT, "docs", "audits", "2026-2026-W40-self-audit.md")))

    # 7. lc001 tmp assets for S2 ASR leg
    lt = os.path.join(ROOT, ".lc001-tmp")
    w("## lc001_tmp")
    if os.path.isdir(lt):
        for f in ["audio.mp3", "subs.srt", "cards.json"]:
            p = os.path.join(lt, f)
            w("  %s exists=%s size=%s" % (f, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else "-"))
    else:
        w("  DIR NOT FOUND")

    # 8. git HEAD
    g = subprocess.run(["git", "log", "--oneline", "-2"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    w("## git")
    w(g.stdout.strip())

    # 9. probes (PYTHONIOENCODING=utf-8)
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    for name, cmd in [("board", ["python", "src/board_check.py"]),
                      ("readiness", ["python", "src/readiness.py"]),
                      ("loop_health", ["python", "src/os/loop_health.py"])]:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        w("## probe_%s exit=%d" % (name, r.returncode))
        out = (r.stdout or "") + (r.stderr or "")
        w(out[-3000:] if len(out) > 3000 else out)

    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("OK report written")

if __name__ == "__main__":
    main()
