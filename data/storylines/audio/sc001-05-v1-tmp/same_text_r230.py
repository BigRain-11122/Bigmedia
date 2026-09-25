import io, re, sys

import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
novel = io.open(os.path.join(ROOT, "data", "storylines", "novel", "SC-001-05-v1.md"), encoding="utf-8").read()
beats_raw = io.open(os.path.join(ROOT, "data", "storylines", "audio", "SC-001-05-v1.beats.txt"), encoding="utf-8").read()

# body paragraphs = between header blockquote and '---'
body = novel.split("\n---\n")[0]
lines = [l.strip() for l in body.split("\n")]
paras = [l for l in lines if l and not l.startswith("#") and not l.startswith(">")]
# drop the title-ish first line if any remaining
paras = [p for p in paras if not p.startswith("硅基城市·第五章")]

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
    if p not in content_all:
        miss.append((i, p[:30]))

# cta spokenization check: novel preview -> beats cta
m = re.search(r"（下一章预告：(.*?)）", novel, re.S)
preview = m.group(1).strip() if m else None
cta = [b for b in beats if b[0] == "cta"][0][2]
cta_expected = "下一章：" + preview
cta_ok = (cta == cta_expected)

# hook declaration beat: cue01 triple-label presence
hook = beats[0][2]
hook_ok = ("AI 参与生成" in hook) and ("真实事件改编" in hook) and ("来源清单见图文页" in hook) and ("第五章" in hook)

with io.open(r"same-text-check-r230.txt", "w", encoding="utf-8") as f:
    f.write("novel body paras: %d\n" % len(paras))
    f.write("beats: %d (types: %s)\n" % (len(beats), "/".join(b[0] for b in beats)))
    f.write("paras missed: %d\n" % len(miss))
    for i, p in miss:
        f.write("  MISS p%d: %s...\n" % (i, p))
    f.write("cta spokenized OK: %s\n" % cta_ok)
    f.write("cta: %s\n" % cta)
    f.write("hook triple-label OK: %s\n" % hook_ok)

print("paras=%d beats=%d miss=%d cta_ok=%s hook_ok=%s" % (len(paras), len(beats), len(miss), cta_ok, hook_ok))
sys.exit(1 if (miss or not cta_ok or not hook_ok) else 0)
