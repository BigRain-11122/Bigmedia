import io, re, sys, os

# R637 same-text check for SC-001-01-v4 (adapts same_text_r275.py to v4 layout:
# header block (# / >) directly precedes body; single '---' separates sources;
# no cta preview paragraph in v4 source -> no cta beat expected).
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
novel = io.open(os.path.join(ROOT, "data", "storylines", "novel", "SC-001-01-v4.md"), encoding="utf-8").read()
beats_raw = io.open(os.path.join(ROOT, "data", "storylines", "audio", "SC-001-01-v4.beats.txt"), encoding="utf-8").read()

# body = everything before the sources separator; drop header (# / >) lines
pre = novel.split("\n---\n")[0]
paras = []
for l in pre.split("\n"):
    l = l.strip()
    if not l or l.startswith("#") or l.startswith(">") or l.startswith("|"):
        continue
    paras.append(l)

VALID = {"hook", "punch", "body", "wink", "turn", "beat", "proof", "close", "cta"}
beats = []
for l in beats_raw.split("\n"):
    l = l.strip()
    if not l:
        continue
    parts = l.split(" | ")
    assert len(parts) == 3, "bad beat line: %r" % l[:40]
    assert parts[0] in VALID, "bad beat type: %r" % parts[0]
    beats.append((parts[0], parts[1], parts[2]))

content_all = "".join(b[2] for b in beats)

miss = []
for i, p in enumerate(paras):
    p_norm = p.replace("**", "")  # markdown bold = layout, not spoken
    if p_norm not in content_all:
        miss.append((i, p_norm[:30]))

# v4 source has no chapter-preview paragraph -> no cta beat; spokenization check = N/A
has_preview = bool(re.search(r"（下一章", novel))
cta_beats = [b for b in beats if b[0] == "cta"]
cta_ok = (not has_preview) and (len(cta_beats) == 0)

# hook declaration beat: cue01 triple-label presence (charter S2)
hook = beats[0][2]
hook_ok = ("AI 参与生成" in hook) and ("真实事件改编" in hook) and ("来源清单见图文页" in hook) and ("第一章" in hook)

# A1 hook-position: golden-100 opening immediately after declaration beat
a1_ok = beats[1][0] == "punch" and "「开一家媒体公司。」" in beats[1][2]

# x1.5 cyber register: zero vulgar words + system-log register markers present in source text
vulgar = [w for w in ["发疯", "枪毙", "卧槽", "杀疯了", "燃爆", "封神"] if w in content_all]
x15_ok = (len(vulgar) == 0) and ("系统日志" in content_all) and ("提交记录" in content_all)

# dual-strand structure check (v4 TOP1: cold city log x morning scene)
strand_ok = ("员工数：零" in content_all) and ("蒸笼开始发光" in content_all) and ("口味" in content_all)

out = os.path.join(HERE, "same-text-check-r637.txt")
with io.open(out, "w", encoding="utf-8") as f:
    f.write("novel body paras: %d\n" % len(paras))
    f.write("beats: %d (types: %s)\n" % (len(beats), "/".join(b[0] for b in beats)))
    f.write("paras missed: %d\n" % len(miss))
    for i, p in miss:
        f.write("  MISS p%d: %s...\n" % (i, p))
    f.write("cta N/A (no preview in source) OK: %s\n" % cta_ok)
    f.write("hook triple-label OK: %s\n" % hook_ok)
    f.write("A1 hook-position OK: %s\n" % a1_ok)
    f.write("x1.5 register OK: %s (vulgar found: %s)\n" % (x15_ok, vulgar))
    f.write("dual-strand OK: %s\n" % strand_ok)
    f.write("content chars (spoken): %d\n" % len(re.sub(r"\s", "", content_all)))

print("paras=%d beats=%d miss=%d cta_ok=%s hook_ok=%s a1_ok=%s x15_ok=%s strand_ok=%s" % (
    len(paras), len(beats), len(miss), cta_ok, hook_ok, a1_ok, x15_ok, strand_ok))
sys.exit(1 if (miss or not cta_ok or not hook_ok or not a1_ok or not x15_ok or not strand_ok) else 0)
