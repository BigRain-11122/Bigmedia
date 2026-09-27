# r512_read2.py - ASR baseline + interchat all + SC003 s7 + E8 review format + footage file check
import os, io, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r512-read2.md")
lines = []
def w(s=""):
    lines.append(str(s))

def main():
    # 0. footage source file existence (render-stale adjudication)
    p = os.path.join(ROOT, "data", "sources", "footage", "census-card-v7-vertical.mp4")
    w("## footage_source_check")
    w("exists=%s size=%s" % (os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else "-"))
    fd = os.path.join(ROOT, "data", "sources", "footage")
    w("footage_dir_listing:")
    if os.path.isdir(fd):
        for f in sorted(os.listdir(fd)):
            w("  %s" % f)

    # 1. voiceover.txt (ASR baseline)
    w("## voiceover_txt")
    with io.open(os.path.join(ROOT, ".lc001-tmp", "voiceover.txt"), "r", encoding="utf-8", errors="replace") as fh:
        w(fh.read())

    # 2. interchat all 22 records (dates + participants + text)
    w("## interchat_all22")
    il = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\interchat-ledger.jsonl"
    with io.open(il, "r", encoding="utf-8", errors="replace") as fh:
        for i, ln in enumerate([l for l in fh.read().splitlines() if l.strip()], 1):
            w("%02d| %s" % (i, ln[:300]))

    # 3. SC-003-01 script s6/s7 region
    w("## sc003_script_s6s7")
    sc = os.path.join(ROOT, "data", "storylines", "video", "SC-003-01-v1.md")
    with io.open(sc, "r", encoding="utf-8", errors="replace") as fh:
        sl = fh.read().splitlines()
    w("(total %d lines)" % len(sl))
    start = None
    for i, s in enumerate(sl):
        if s.startswith("## "):
            start = i
    # dump from second-to-last section header region: find '七' heading
    idx7 = None
    for i, s in enumerate(sl):
        if re.match(r"^#+\s*[七7]", s) or "互聊" in s:
            idx7 = i if idx7 is None else idx7
    if idx7:
        for j in range(max(0, idx7 - 2), min(len(sl), idx7 + 30)):
            w("L%d: %s" % (j + 1, sl[j][:240]))

    # 4. E8 review card format (bs004v15)
    w("## review_bs004v15_format")
    rv = os.path.join(ROOT, "docs", "reviews", "review-20260927-bs004v15-v1.md")
    with io.open(rv, "r", encoding="utf-8", errors="replace") as fh:
        rl = fh.read().splitlines()
    w("(total %d lines)" % len(rl))
    for s in rl[:75]:
        w(s[:240])

    # 5. whisper CLI args
    w("## whisper_cli_args")
    with io.open(os.path.join(ROOT, "src", "render", "whisper_to_srt.py"), "r", encoding="utf-8", errors="replace") as fh:
        wl = fh.read().splitlines()
    for i, s in enumerate(wl):
        if "add_argument" in s or "def main" in s or "usage" in s.lower():
            w("L%d: %s" % (i + 1, s.strip()[:200]))

    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("OK")

if __name__ == "__main__":
    main()
