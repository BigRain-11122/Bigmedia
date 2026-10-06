# -*- coding: utf-8 -*-
"""R1548 REACT-v10 M0/M1 selection probe (temp, cleaned at round end).

Checks:
 A) candidate reaction lines + creed are verbatim members of their sources (pools.json / anchor C-00019)
 B) R1010 card-face collision: candidates must be CLEAN vs all finished card faces
    (exact-line reuse = FAIL; longest common substring >=4 = FAIL; 2-3 char content shingles
     listed for adjudication with function-word noise filtered)
 C) hot title verbatim in daily brief 2026-10-07
"""
import io, json, os, re, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = []

CAND_LINES = [
    ("怀旧", "morning", "捡破烂也是门技术活，得眼尖手快"),
    ("侠气", "morning", "晨风一扫夜的凉，摊子开张早赚两分光"),
    ("逍遥", "morning", "早市忙，人声鼎沸"),
]
CREED_PREFIX = "引擎医生信条"
CREED = "机器不坏是本事，坏了能修是人品。"
HOT1 = "媒体称破铜烂铁、废纸壳、废塑料可能正在创造巨量财富，"
HOT2 = "这是真的吗？为啥「破烂」正在变成黄金赛道？"

# --- A) verbatim source assertions
pools = json.load(open(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json", encoding="utf-8"))
for axis, bucket, line in CAND_LINES:
    ok = line in pools["axes"].get(axis, {}).get(bucket, [])
    OUT.append("A pool-verbatim %s/%s: %s :: %s" % (axis, bucket, "OK" if ok else "FAIL", line))

anchor = open(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00019.md", encoding="utf-8").read()
creed_ok = CREED in anchor
OUT.append("A anchor-C00019-creed-verbatim: %s :: %s" % ("OK" if creed_ok else "FAIL", CREED))
# non-honorary check: anchor registered in registry index? (read registry list of anchor ids)
reg_path = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\registry"
try:
    reg_ids = [f for f in os.listdir(reg_path)]
    OUT.append("A registry dir entries: %d (anchor C-00019 = handwritten anchor, registry!=anchor per R316)" % len(reg_ids))
except Exception as e:
    OUT.append("A registry probe: %r" % e)

daily = open(os.path.join(ROOT, "data", "intel", "daily", "2026-10-07.md"), encoding="utf-8").read()
hot_full = HOT1 + HOT2
hot_ok = hot_full in daily
OUT.append("A daily-verbatim hot-title: %s" % ("OK" if hot_ok else "FAIL"))

# --- B) R1010 card-face collision scan (all finished piece dirs, self excluded)
cards_dir = os.path.join(ROOT, "data", "storylines", "cards")
face_lines = []
pieces = []
for d in sorted(os.listdir(cards_dir)):
    if not d.startswith("MC-") or d.endswith("-tmp"):
        continue
    cj = os.path.join(cards_dir, d, "cards.json")
    if os.path.exists(cj):
        try:
            c = json.load(open(cj, encoding="utf-8"))
        except Exception:
            continue
        for card in c.get("cards", []):
            for ln in card.get("lines", []):
                face_lines.append((d, ln))
        pieces.append(d)
OUT.append("B fleet pieces scanned: %d, face lines: %d" % (len(pieces), len(face_lines)))

STOP2 = set(["也是", "真的", "咱们", "这个", "就是", "的人", "起来", "上来", "开张", "日子",
             "的人", "了一", "得了", "早点", "早上", "今儿", "一天", "还得", "怎么", "什么"])

def content_shingles(s, lo=2, hi=5):
    out = set()
    for n in range(lo, hi + 1):
        for i in range(len(s) - n + 1):
            out.add(s[i:i + n])
    return out

def lcs_len(a, b):
    # longest common substring length
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                k += 1
            if k > best:
                best = k
    return best

for label, cand in [("R1", CAND_LINES[0][2]), ("R2", CAND_LINES[1][2]), ("R3", CAND_LINES[2][2]), ("CREED", CREED)]:
    exact = [(d, ln) for d, ln in face_lines if ln.strip() == cand or cand in ln]
    near = []
    sh_hits = {}
    for d, ln in face_lines:
        L = lcs_len(cand, ln)
        if L >= 4:
            near.append((d, ln, L))
        for sh in content_shingles(cand, 2, 5):
            if sh in ln and sh not in STOP2 and len(sh) >= 2:
                sh_hits.setdefault(sh, []).append((d, ln))
    OUT.append("--- %s :: %s" % (label, cand))
    OUT.append("  exact/near4: exact=%d near>=4=%d" % (len(exact), len(near)))
    for d, ln, L in near[:6]:
        OUT.append("    NEAR %d %s :: %s" % (L, d, ln))
    # adjudication list: content-bearing 2-3 char shingle hits (deduped, capped)
    listed = 0
    for sh in sorted(sh_hits, key=lambda x: -len(x)):
        if listed >= 8:
            OUT.append("    ... more shingle hits (%d total shingles)" % len(sh_hits))
            break
        ex = sh_hits[sh][0]
        OUT.append("    SHINGLE %r -> %s :: %s" % (sh, ex[0], ex[1]))
        listed += 1
    if not sh_hits:
        OUT.append("  shingle-hits: NONE (CLEAN)")

print("\n".join(OUT))

# --- C) fresh-bucket mapping scan evidence (for bucket-reuse honest note + M0 reasons)
C_OUT = ["", "=== C) fresh-bucket / topic-domain mapping scan (r1548) ==="]
pools2 = pools
RECYCLE_KW = ["破烂", "旧货", "旧物", "捡", "收废", "废", "宝贝", "赚", "买卖", "寻宝", "财", "生意", "开张"]
FRAUD_KW = ["骗", "诈", "贼", "抓捕", "覆灭", "正义", "审判", "警察", "反诈", "罪犯", "落网", "窝点"]
for b in ["dusk", "typhoon", "coldsnap", "ceo_order"]:
    hits = []
    for axis, bk in pools2["axes"].items():
        for ln in bk.get(b, []):
            if any(k in ln for k in RECYCLE_KW):
                hits.append("%s: %s" % (axis, ln))
    C_OUT.append("C fresh-bucket %s recycle-domain hits: %d" % (b, len(hits)))
    for h in hits:
        C_OUT.append("   " + h)
# fraud-domain scan across WHOLE pool (pre-indicated candidate exclusion evidence)
fraud_hits = []
for axis, bk in pools2["axes"].items():
    for b, lines in bk.items():
        for ln in lines:
            if any(k in ln for k in FRAUD_KW):
                fraud_hits.append("%s/%s: %s" % (axis, b, ln))
for b, lines in pools2.get("sprite", {}).items():
    for ln in lines:
        if any(k in ln for k in FRAUD_KW):
            fraud_hits.append("sprite/%s: %s" % (b, ln))
C_OUT.append("C fraud-domain whole-pool hits: %d" % len(fraud_hits))
for h in fraud_hits:
    C_OUT.append("   " + h)
# morning bucket v6-reuse evidence
v6 = open(os.path.join(cards_dir, "MC-20260930-REACT-v6", "cards.json"), encoding="utf-8").read()
C_OUT.append("C v6 used morning bucket: %s" % ("morning" in v6))
open(os.path.join(ROOT, ".c3-tmp", "r1548_react_probe.txt"), "a", encoding="utf-8").write("\n" + "\n".join(C_OUT) + "\n")
print("\n".join(C_OUT))
