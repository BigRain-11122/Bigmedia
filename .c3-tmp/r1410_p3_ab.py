# -*- coding: utf-8 -*-
# r1410 P-3 pilot A/B measurement leg (queue P-3: faster-whisper initial_prompt
# proper-noun preload A/B on in-case ASR terminal tracks BS-003/BS-004).
# A = R169 QC recipe (medium-int8 + beam5 + no-context), B = same + --initial-prompt.
# Chinese strings live in r1410_p3_terms.json (data file) per the encoding law.
import io, os, re, json, subprocess, sys
from difflib import SequenceMatcher

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
cfg = json.load(io.open(repo + r"\.c3-tmp\r1410_p3_terms.json", encoding="utf-8"))
out = io.open(repo + r"\.c3-tmp\r1410_p3_ab.txt", "w", encoding="utf-8")
w = out.write
env = dict(os.environ)
env["HF_HUB_OFFLINE"] = "1"
env["PYTHONIOENCODING"] = "utf-8"

CUE_TS = re.compile(r"-->")

def parse_srt(path):
    """Return list of cue text strings."""
    cues = []
    cur = []
    for line in io.open(path, encoding="utf-8-sig").read().split("\n"):
        s = line.strip()
        if not s:
            if cur:
                cues.append("".join(cur)); cur = []
            continue
        if s.isdigit() or CUE_TS.search(s):
            continue
        cur.append(s)
    if cur:
        cues.append("".join(cur))
    return cues

def norm(t):
    """Keep CJK chars + ascii alnum only."""
    return "".join(ch for ch in t if ("\u4e00" <= ch <= "\u9fff") or ch.isalnum())

def run_track(tag, spec):
    w("== %s ==\n" % tag)
    audio = os.path.join(repo, spec["audio"])
    ref_cues = parse_srt(os.path.join(repo, spec["ref"]))
    refn = [norm(c) for c in ref_cues]
    ref_concat = "".join(refn)
    a_out = repo + r"\.c3-tmp\r1410_p3_%s_A.srt" % tag
    b_out = repo + r"\.c3-tmp\r1410_p3_%s_B.srt" % tag
    runs = [("A", a_out, []), ("B", b_out, ["--initial-prompt", spec["prompt"]])]
    hyp = {}
    for label, outp, extra in runs:
        if os.path.exists(outp) and os.path.getsize(outp) > 0:
            w("[%s] cached=%s (prior run output reused)\n" % (label, outp))
            hyp[label] = parse_srt(outp)
            continue
        cmd = [sys.executable, r"src\render\whisper_to_srt.py", "--audio", audio,
               "--out", outp, "--model", "medium", "--beam-size", "5", "--no-context"] + extra
        p = subprocess.run(cmd, cwd=repo, capture_output=True, timeout=900, env=env)
        ok = p.returncode == 0
        line = (p.stdout or b"").decode("utf-8", "replace").strip()
        w("[%s] rc=%s %s\n" % (label, p.returncode, line))
        if not ok:
            w("[%s] STDERR: %s\n" % (label, (p.stderr or b"").decode("utf-8", "replace")[-400:]))
        hyp[label] = parse_srt(outp) if ok else []
    a_cues = hyp.get("A", [])
    b_cues = hyp.get("B", [])
    a_concat = norm("".join(a_cues))
    b_concat = norm("".join(b_cues))

    # determinism check: fresh A vs archived R169-recipe output
    arch = os.path.join(repo, spec["baseline_archive"])
    if os.path.exists(arch):
        archn = norm("".join(parse_srt(arch)))
        same = archn == a_concat
        ratio = SequenceMatcher(None, archn, a_concat).ratio()
        w("A_vs_archive identical=%s ratio=%.4f (determinism/recipe match)\n" % (same, ratio))

    # proper-noun degradation sites (count-based proxy, clamped)
    w("%-8s %5s %5s %5s %6s %6s\n" % ("term", "ref", "A", "B", "degA", "degB"))
    deg_a = deg_b = leak_b = 0
    for t in spec["terms"]:
        tn = norm(t)
        rc = ref_concat.count(tn)
        ac = a_concat.count(tn)
        bc = b_concat.count(tn)
        da = max(0, rc - ac); db = max(0, rc - bc)
        lb = max(0, bc - rc)
        deg_a += da; deg_b += db; leak_b += lb
        if rc or ac or bc:
            w("%-8s %5d %5d %5d %6d %6d%s\n" % (t, rc, ac, bc, da, db, " LEAK+%d" % lb if lb else ""))
    w("proper_noun_degraded_sites A=%d B=%d leaked_B=%d\n" % (deg_a, deg_b, leak_b))

    # whole-text char mismatch rate (homophone noise proxy, includes number-form diffs equally on both sides)
    def mm(ref, hyp):
        sm = SequenceMatcher(None, ref, hyp)
        bad = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "replace":
                bad += max(i2 - i1, j2 - j1)
            elif tag == "delete":
                bad += i2 - i1
            elif tag == "insert":
                bad += j2 - j1
        return bad
    m_a = mm(ref_concat, a_concat); m_b = mm(ref_concat, b_concat)
    w("char_mismatch A=%d B=%d (ref_len=%d) rateA=%.4f rateB=%.4f\n" % (m_a, m_b, len(ref_concat), m_a / len(ref_concat), m_b / len(ref_concat)))
    w("cue_counts ref=%d A=%d B=%d\n\n" % (len(ref_cues), len(a_cues), len(b_cues)))
    return dict(deg_a=deg_a, deg_b=deg_b, leak=leak_b, m_a=m_a, m_b=m_b, ref_len=len(ref_concat))

res = {}
for tag, spec in cfg.items():
    res[tag] = run_track(tag, spec)

w("== P-3 criteria (registered: 1) proper-noun degradation reduction >=50%  2) prompt-leak hallucination sites = 0  3) whole-char noise rate not higher) ==\n")
tot_a = tot_b = tot_leak = 0
for tag, r in res.items():
    red = 100.0 * (r["deg_a"] - r["deg_b"]) / r["deg_a"] if r["deg_a"] else None
    c1 = "N/A (A already clean)" if r["deg_a"] == 0 else ("PASS" if red is not None and red >= 50 else "FAIL")
    c2 = "PASS" if r["leak"] == 0 else "FAIL"
    c3 = "PASS" if r["m_b"] <= r["m_a"] else "FAIL"
    w("%s: degA=%d degB=%d reduction=%s%% leakB=%d mismatchA=%d mismatchB=%d -> c1=%s c2=%s c3=%s\n"
      % (tag, r["deg_a"], r["deg_b"], ("%.0f" % red) if red is not None else "n/a", r["leak"], r["m_a"], r["m_b"], c1, c2, c3))
    tot_a += r["deg_a"]; tot_b += r["deg_b"]; tot_leak += r["leak"]
red_tot = 100.0 * (tot_a - tot_b) / tot_a if tot_a else None
w("TOTAL: degA=%d degB=%d reduction=%s%% leak=%d\n" % (tot_a, tot_b, ("%.0f" % red_tot) if red_tot is not None else "n/a", tot_leak))
out.close()
print("done")
