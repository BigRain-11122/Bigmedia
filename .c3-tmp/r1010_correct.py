# -*- coding: utf-8 -*-
"""R1010 correction pass (R981/R1006 scan-correction lineage):
1) regenerate r1010_pool.txt at face level (cards[].lines + source_quote + city-spirit),
   fixing the false USED on zhixu line1 caused by whole-cards.json meta-prose matching;
2) fix festival-remaining count 32 -> 60 (face-level truth) across queue row, state.json
   (focus + log), export (results entry + OS-loop outs row);
3) append honest correction notes (scan-lineage regression + old-count drift)."""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def W(p): return os.path.join(ROOT, p)

BASE = os.path.join(ROOT, "data", "storylines", "cards")
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
spirit = io.open(W("data/storylines/codex/city-spirit.md"), encoding="utf-8").read()
faces = []
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        try:
            c = json.load(io.open(cj, encoding="utf-8"))
        except Exception:
            continue
        for card in c.get("cards", []):
            faces.extend(card.get("lines", []))
        faces.append(c.get("meta", {}).get("source_quote", ""))
face_txt = u"\n".join(faces)

# 1) regenerate r1010_pool.txt (face level) for zhixu bucket
fest = pool["axes"][u"秩序"][u"festival"]
assert len(fest) == 18
out = [u"=== zhixu/festival bucket 18 lines (R1010 scan for DAILY v41 · REGENERATED face-level: "
       u"cards[].lines + meta.source_quote + city-spirit.md; v1 whole-cards.json matching "
       u"falsely marked line1 USED via meta-prose quoting = R981/R1006 scan-correction lineage; "
       u"line1 is truly FREE but zero-person-zero-scene slogan (R442 weakness) = content-strength "
       u"ranked below line17, selection outcome unaffected; build fleet assertion = hard gate unaffected) ==="]
for i, ln in enumerate(fest):
    used = (ln in spirit) or (ln in face_txt)
    out.append(("USED" if used else "FREE") + "  " + str(i) + "  " + ln)
io.open(W(".c3-tmp/r1010_pool.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")

corr = (u"〔**轮内修正实录**=①festival 余行计数口径修正：R1008/R1009 行 65 未随消费递减=旧口径漂移·本行起=卡面级实扫"
        u"（cards[].lines+source_quote+city-spirit）实测 60/108〔r1010_festcount.txt 逐轴实证〕"
        u"②轮前 r1010_pool.txt 首版整 cards.json 文本匹配法误标秩序 line1 USED（meta 叙述面引用假命中）→卡面级重生成="
        u"R981/R1006 扫描件修正谱系回归·line1「守规矩才能让城市更安稳」真实 FREE 但零人物零场景口号（R442 弱点正中）"
        u"内容强度弱于本行=选优结果不受影响·build fleet 断言=硬门不受影响〕")

# 2) queue row: fix count + append correction before final newline
q = io.open(W("docs/self-improvement-queue.md"), encoding="utf-8").read()
assert u"festival 居民桶余 32 行" in q
q = q.replace(u"festival 居民桶余 32 行", u"festival 居民桶余 60 行")
i = q.rfind(u"CLOUD_LINE 首测）。")
assert i >= 0
q = q[:i + len(u"CLOUD_LINE 首测）。")] + corr + q[i + len(u"CLOUD_LINE 首测）。"):]
io.open(W("docs/self-improvement-queue.md"), "w", encoding="utf-8", newline="\n").write(q)

# 3) state.json: focus + log count fix, log correction append
st = json.load(io.open(W("src/os/state.json"), encoding="utf-8"))
assert u"festival 居民桶余 32 行" in st["focus"]
st["focus"] = st["focus"].replace(u"festival 居民桶余 32 行", u"festival 居民桶余 60 行")
logline = st["log"][-1]
assert u"festival 居民桶余 32 行" in logline
logline = logline.replace(u"festival 居民桶余 32 行", u"festival 居民桶余 60 行")
anchor = u"P-54 计量纪律如实记）。"
assert anchor in logline
logline = logline.replace(anchor, anchor + corr, 1)
st["log"][-1] = logline
json.dump(st, io.open(W("src/os/state.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

# 4) export: results entry + OS-loop outs row count fix
ex = json.load(io.open(W("docs/status-export.json"), encoding="utf-8"))
for row in ex["outs"]:
    if row[0] == u"OS 循环":
        assert u"festival 余 32 行" in row[1]
        row[1] = row[1].replace(u"festival 余 32 行", u"festival 余 60 行")
r = ex["results"][-1]
assert r[0] == "1010" and u"festival 居民桶余 32 行" in r[1]
r[1] = r[1].replace(u"festival 居民桶余 32 行", u"festival 居民桶余 60 行")
json.dump(ex, io.open(W("docs/status-export.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

print("CORRECTION OK: pool regen + 32->60 in queue/state(focus+log)/export + notes appended")
