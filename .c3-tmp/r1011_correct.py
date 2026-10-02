# -*- coding: utf-8 -*-
"""R1011 correction pass (R1010 r1010_correct.py lineage direct inheritance):
r1011_ledgers.py section-0 was copied from the COMMITTED r1010_ledgers.py = the
PRE-correction whole-cards.json membership face (R1010 already fixed 32->60 in-round via
r1010_correct.py but the committed ledgers script still carries the old section - copy
trap). Whole-file membership false-excludes festival lines quoted as full text inside
recent metas' candidate-strength notes (v38-v41 weakness-note quoting) = 23 false count.
Fix to face-level truth (cards[].lines + meta.source_quote + city-spirit):
1) face-level festival remaining count (post-v42 consumption) + per-axis tally artifact;
2) fix 23 -> face truth across queue row, state.json (focus + log), export (results + outs);
3) append honest correction note (lineage + copy-trap root cause)."""
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

# 1) face-level per-axis tally + total (post-v42: v42 faces now in face_txt)
tally = []
free_total = 0
for ax in pool["axes"]:
    fest = pool["axes"][ax].get("festival", [])
    used_idx = []
    for i, ln in enumerate(fest):
        if (ln in spirit) or (ln in face_txt):
            used_idx.append(i)
    free_total += len(fest) - len(used_idx)
    tally.append(u"%s: USED %s (n=%d) FREE %d" % (ax, ",".join(str(i) for i in used_idx), len(used_idx), len(fest) - len(used_idx)))
FEST_TRUE = free_total
tally.append(u"TOTAL FREE = %d / 108" % FEST_TRUE)
io.open(W(".c3-tmp/r1011_festcount.txt"), "w", encoding="utf-8").write("\n".join(tally) + "\n")

# regenerate r1011_pool.txt at face level (post-consumption; pre-selection scan was index-based
# with line13 FREE = honest pre-selection state preserved in git history of this artifact family)
fest = pool["axes"][u"逍遥"][u"festival"]
assert len(fest) == 18
out = [u"=== xiaoyao/festival bucket 18 lines (R1011 scan for DAILY v42 · FACE-LEVEL regenerated "
       u"post-consumption: cards[].lines + meta.source_quote + city-spirit.md; pre-selection "
       u"version was index-list-based with line13 FREE = honest pre-selection state; v42 now "
       u"consumes line13; whole-cards.json membership would false-exclude 36 extra lines via "
       u"v38-v41 meta candidate-note full-text quoting = R1010 correction lineage) ==="]
for i, ln in enumerate(fest):
    used = (ln in spirit) or (ln in face_txt)
    out.append(("USED" if used else "FREE") + "  " + str(i) + "  " + ln)
io.open(W(".c3-tmp/r1011_pool.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")

corr = (u"〔**轮内修正实录（R1010 r1010_correct.py 谱系直承）**=①festival 余行计数口径修正：r1011_ledgers.py section-0 "
        u"复制自已提交 r1010_ledgers.py=**修正前旧整 cards.json 文本匹配面**（R1010 已轮内 32→60 修正但已提交台账脚本"
        u"未回写修正版=复刻陷阱首案）→整文匹配把近批件 meta 候选弱项注记全文引用（v38-v41）误判为消费=23 假计数·"
        u"本修正=卡面级实扫（cards[].lines+source_quote+city-spirit）实测 %d/108〔r1011_festcount.txt 逐轴实证·"
        u"R1010 60 基线-v42 消费 1 行=60-1 数值对合零漂移〕②r1011_pool.txt 面级重生成（line13 USED 后态·选优时点版=索引法 "
        u"line13 FREE=选优前真态保留）·build fleet 断言=硬门不受影响（源断言以整文匹配跑于 v42 建立前=v42 未入集合"
        u"且 line13 全文零命中实证通过）〕" % FEST_TRUE)

# 2) queue row: fix count + append correction before final newline
q = io.open(W("docs/self-improvement-queue.md"), encoding="utf-8").read()
assert u"festival 居民桶余 23 行" in q
q = q.replace(u"festival 居民桶余 23 行", u"festival 居民桶余 %d 行" % FEST_TRUE)
i = q.rfind(u"W41 周轮件（10-05：周报+自驱提案窗+CLOUD_LINE 首测）。")
assert i >= 0
anchor = u"W41 周轮件（10-05：周报+自驱提案窗+CLOUD_LINE 首测）。"
q = q[:i + len(anchor)] + corr + q[i + len(anchor):]
io.open(W("docs/self-improvement-queue.md"), "w", encoding="utf-8", newline="\n").write(q)

# 3) state.json: focus + log count fix, log correction append
st = json.load(io.open(W("src/os/state.json"), encoding="utf-8"))
assert u"festival 居民桶余 23 行" in st["focus"]
st["focus"] = st["focus"].replace(u"festival 居民桶余 23 行", u"festival 居民桶余 %d 行" % FEST_TRUE)
logline = st["log"][-1]
assert u"festival 居民桶余 23 行" in logline
logline = logline.replace(u"festival 居民桶余 23 行", u"festival 居民桶余 %d 行" % FEST_TRUE)
anc = u"P-54 计量纪律如实记）。"
assert anc in logline
logline = logline.replace(anc, anc + corr, 1)
st["log"][-1] = logline
json.dump(st, io.open(W("src/os/state.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

# 4) export: results entry + OS-loop outs row count fix
ex = json.load(io.open(W("docs/status-export.json"), encoding="utf-8"))
for row in ex["outs"]:
    if row[0] == u"OS 循环":
        assert u"festival 余 23 行" in row[1]
        row[1] = row[1].replace(u"festival 余 23 行", u"festival 余 %d 行" % FEST_TRUE)
r = ex["results"][-1]
assert r[0] == "1011" and u"festival 居民桶余 23 行" in r[1]
r[1] = r[1].replace(u"festival 居民桶余 23 行", u"festival 居民桶余 %d 行" % FEST_TRUE)
json.dump(ex, io.open(W("docs/status-export.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

print("CORRECTION OK: pool regen + festcount + 23->%d in queue/state(focus+log)/export + notes appended" % FEST_TRUE)
