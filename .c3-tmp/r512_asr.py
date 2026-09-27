# r512_asr.py - S2 seat ASR final-track check (R169 QC recipe) + dump exact edit targets
import os, io, subprocess, time, difflib, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LT = os.path.join(ROOT, ".lc001-tmp")
OUT = os.path.join(ROOT, ".c3-tmp", "r512-report3.md")
lines = []
def w(s=""):
    lines.append(str(s))

def norm(s):
    # strip punctuation/whitespace for char-level compare
    return re.sub(r"[\s，。、：；「」『』！？,.:;!?“”\"'（）()\-—…·%]", "", s)

def main():
    # 1. run ASR (R169 QC recipe: medium + beam5 + no-context)
    t0 = time.time()
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(["python", "src/render/whisper_to_srt.py",
                        "--audio", os.path.join(LT, "audio.mp3"),
                        "--out", os.path.join(LT, "asr-check.srt"),
                        "--model", "medium", "--beam-size", "5", "--no-context"],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=900)
    w("## asr_run exit=%d elapsed=%.1fs" % (r.returncode, time.time() - t0))
    if r.returncode != 0:
        w("STDERR tail: %s" % (r.stderr or "")[-1500:])
    with io.open(os.path.join(LT, "asr-check.srt"), "r", encoding="utf-8", errors="replace") as fh:
        srt = fh.read()
    w("## asr_check_srt")
    w(srt)

    # 2. difflib char-level diff vs voiceover
    with io.open(os.path.join(LT, "voiceover.txt"), "r", encoding="utf-8", errors="replace") as fh:
        vo = fh.read()
    a, b = norm(vo), norm(srt)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ratio = sm.ratio()
    sites = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            sites.append("%s: ref[%s] asr[%s]" % (tag, a[i1:i2][:24], b[j1:j2][:24]))
    w("## asr_diff ratio=%.3f ref_chars=%d asr_chars=%d diff_sites=%d" % (ratio, len(a), len(b), len(sites)))
    for s in sites:
        w("  " + s)
    # factual-word survival check
    w("## factual_words")
    for kw in ["徐根福", "六十六", "一九八零", "1980", "K线", "公众号", "大跌", "例汤", "档案"]:
        w("  %s: in_asr=%s" % (kw, kw in b))
    # write diff archive file
    with io.open(os.path.join(LT, "asr-diff-r512.txt"), "w", encoding="utf-8") as fh:
        fh.write("LC-001 ASR final-track check R512 (R169 QC recipe medium/beam5/noctx)\n")
        fh.write("ref=%d chars asr=%d chars ratio=%.3f diff_sites=%d\n" % (len(a), len(b), ratio, len(sites)))
        for s in sites:
            fh.write(s + "\n")

    # 3. renders README: structure + v15 finished-row format + full lc-001 rows + census refs
    w("## renders_readme_structure")
    rr = os.path.join(ROOT, "output", "renders", "README.md")
    with io.open(rr, "r", encoding="utf-8", errors="replace") as fh:
        rl = fh.read().splitlines()
    for i, s in enumerate(rl, 1):
        if s.startswith("#") or s.startswith("> **") or "成品" in s[:40]:
            w("L%d: %s" % (i, s[:150]))
    w("## renders_v15_row_example")
    for i, s in enumerate(rl, 1):
        if "bs-001-v15-shipinhao" in s:
            w("L%d FULL: %s" % (i, s))
            break
    w("## renders_lc001_full_rows")
    for i, s in enumerate(rl, 1):
        if "lc-001" in s or "census-card-v7-vertical" in s:
            w("L%d FULL: %s" % (i, s))
    w("## station_reviews_census_refs")
    sr = os.path.join(ROOT, "docs", "reviews", "station-reviews.md")
    with io.open(sr, "r", encoding="utf-8", errors="replace") as fh:
        sl = fh.read().splitlines()
    for i, s in enumerate(sl, 1):
        if "census-card-v7-vertical" in s:
            w("L%d: %s" % (i, s[:200]))

    # 4. release-schedule exact regions
    w("## release_schedule_regions")
    rs = os.path.join(ROOT, "docs", "release-schedule-v1.md")
    with io.open(rs, "r", encoding="utf-8", errors="replace") as fh:
        rsl = fh.read().splitlines()
    for i, s in enumerate(rsl, 1):
        if 14 <= i <= 40 or 58 <= i <= 90:
            w("L%d: %s" % (i, s[:250]))

    # 5. SC-003 script tail (s5-s7)
    w("## sc003_script_tail")
    sc = os.path.join(ROOT, "data", "storylines", "video", "SC-003-01-v1.md")
    with io.open(sc, "r", encoding="utf-8", errors="replace") as fh:
        scl = fh.read().splitlines()
    for j in range(58, min(104, len(scl))):
        w("L%d: %s" % (j + 1, scl[j][:240]))

    # 6. e4_call.py candidates
    w("## e4_wrapper_candidates")
    for base, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
        for f in fs:
            if f == "e4_call.py":
                w("  %s" % os.path.join(base, f))

    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("OK ratio=%.3f sites=%d" % (ratio, len(sites)))

if __name__ == "__main__":
    main()
