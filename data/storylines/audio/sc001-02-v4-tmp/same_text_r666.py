import io, re, sys, os

# R666 same-text check for SC-001-02-v4 (adapts same_text_r637.py to ch2 benchmark source:
# full-day scene arc; no cta preview paragraph in v4 source -> no cta beat expected;
# A1 golden-100 = pre-dawn opening beat right after declaration beat).
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
novel = io.open(os.path.join(ROOT, "data", "storylines", "novel", "SC-001-02-v4.md"), encoding="utf-8").read()
beats_raw = io.open(os.path.join(ROOT, "data", "storylines", "audio", "SC-001-02-v4.beats.txt"), encoding="utf-8").read()

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
hook_ok = ("AI 参与生成" in hook) and ("真实事件改编" in hook) and ("来源清单见图文页" in hook) and ("第二章" in hook)

# A1 hook-position: golden-100 scene opening immediately after declaration beat
a1_ok = beats[1][2].startswith("凌晨四点二十八分") and beats[1][0] in ("beat", "punch")

# x1.5 cyber register: zero vulgar words + system-log register markers present in source text
vulgar = [w for w in ["发疯", "枪毙", "卧槽", "杀疯了", "燃爆", "封神"] if w in content_all]
x15_ok = (len(vulgar) == 0) and ("检索" in content_all) and ("提交" in content_all)

# scene-arc structure check (v4 benchmark: full-day arc open->ignition->creed->ch3 hook)
arc_ok = ("四点二十八分" in content_all) and ("炉子点起来" in content_all) and ("灶上留一壶" in content_all) and ("周三" in content_all)

out = os.path.join(HERE, "same-text-check-r666.txt")
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
    f.write("scene-arc OK: %s\n" % arc_ok)
    f.write("content chars (spoken): %d\n" % len(re.sub(r"\s", "", content_all)))

print("paras=%d beats=%d miss=%d cta_ok=%s hook_ok=%s a1_ok=%s x15_ok=%s arc_ok=%s" % (
    len(paras), len(beats), len(miss), cta_ok, hook_ok, a1_ok, x15_ok, arc_ok))
sys.exit(1 if (miss or not cta_ok or not hook_ok or not a1_ok or not x15_ok or not arc_ok) else 0)
