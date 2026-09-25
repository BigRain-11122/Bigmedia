import io, re, sys, os

# R277 same-text checker adapted for ch.3 v3 (source change only + ch.3 anchors)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
novel = io.open(os.path.join(ROOT, "data", "storylines", "novel", "SC-001-03-v3.md"), encoding="utf-8").read()
beats_raw = io.open(os.path.join(ROOT, "data", "storylines", "audio", "SC-001-03-v3.beats.txt"), encoding="utf-8").read()

# body paragraphs = between first and second '---' (v3 layout: header/table before 1st, sources after 2nd)
parts = novel.split("\n---\n")
body = parts[1]
lines = [l.strip() for l in body.split("\n")]
paras = [l for l in lines if l and not l.startswith("#") and not l.startswith(">") and not l.startswith("|")]

# beats content = third field
beats = []
for l in beats_raw.split("\n"):
    l = l.strip()
    if not l:
        continue
    parts = l.split(" | ")
    assert len(parts) == 3, "bad beat line: %r" % l[:40]
    beats.append((parts[0], parts[1], parts[2]))

content_all = "".join(b[2] for b in beats)

miss = []
for i, p in enumerate(paras):
    p_norm = p.replace("**", "")  # markdown bold = layout, not spoken
    if p_norm.startswith("（下一章"):  # preview para = cta spokenization, checked separately
        continue
    if p_norm not in content_all:
        miss.append((i, p_norm[:30]))

# cta spokenization check: novel preview -> beats cta
m = re.search(r"（下一章(?:预告)?：(.*?)）", novel, re.S)
preview = m.group(1).strip() if m else None
cta = [b for b in beats if b[0] == "cta"][0][2]
cta_expected = "下一章：" + preview
cta_ok = (cta == cta_expected)

# hook declaration beat: cue01 triple-label presence
hook = beats[0][2]
hook_ok = ("AI 参与生成" in hook) and ("真实事件改编" in hook) and ("来源清单见图文页" in hook) and ("第三章" in hook)

# A1 hook-position check: cue01 declaration (compliance-mandated) then golden-100 opening
a1_ok = beats[1][0] == "punch" and "可能输掉一座钟" in beats[1][2]

# O-1756 x1.5 register inheritance spot-checks on same-text source (vulgar words zero + system-register markers present)
vulgar = [w for w in ["发疯", "枪毙", "卧槽", "杀疯了", "燃爆", "封神", "吊打", "炸裂"] if w in content_all]
x15_ok = (len(vulgar) == 0) and ("全城齐秒" in content_all) and ("自我更新" in content_all)

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "same-text-check-r279.txt"), "w", encoding="utf-8") as f:
    f.write("novel body paras: %d\n" % len(paras))
    f.write("beats: %d (types: %s)\n" % (len(beats), "/".join(b[0] for b in beats)))
    f.write("paras missed: %d\n" % len(miss))
    for i, p in miss:
        f.write("  MISS p%d: %s...\n" % (i, p))
    f.write("cta spokenized OK: %s\n" % cta_ok)
    f.write("cta: %s\n" % cta)
    f.write("hook triple-label OK: %s\n" % hook_ok)
    f.write("A1 hook-position OK: %s\n" % a1_ok)
    f.write("x1.5 register inheritance OK: %s (vulgar found: %s)\n" % (x15_ok, vulgar))

print("paras=%d beats=%d miss=%d cta_ok=%s hook_ok=%s a1_ok=%s x15_ok=%s" % (len(paras), len(beats), len(miss), cta_ok, hook_ok, a1_ok, x15_ok))
sys.exit(1 if (miss or not cta_ok or not hook_ok or not a1_ok or not x15_ok) else 0)
