# -*- coding: utf-8 -*-
"""R982 pools.json content diff: leaf 1440->1296, locate the change (axes/buckets/lines)."""
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))

out = []
total = 0
for ax, buckets in sorted(pool.get("axes", {}).items()):
    axn = 0
    bparts = []
    for b, lines in sorted(buckets.items()):
        axn += len(lines)
        bparts.append(u"%s=%d" % (b, len(lines)))
    total += axn
    out.append(u"axis %s: %d  [%s]" % (ax, axn, u", ".join(bparts)))
out.append(u"TOTAL leaf=%d (baseline 1440, delta %d)" % (total, total - 1440))

# festival bucket full lines (for DAILY lane continuity check)
fest = pool.get("axes", {}).get("festival", {})
out.append(u"festival buckets: %s" % u", ".join(u"%s=%d" % (b, len(v)) for b, v in sorted(fest.items())))

# check the 12 DAILY lines consumed v1-v12 still present?
daily_used = {
 u"v1": u"直播间的观众都说，我家的灯笼最独特",
 u"v2": u"挂上这些灯，这老破小也亮堂了",
 u"v3": u"灯下兄弟把酒言，江湖义气不言钱",
 u"v4": u"节日的灯多了，家里的笑声也多",
 u"v5": u"校准好每盏灯，心里才踏实",
 u"v6": u"闲来垂钓乐悠悠，喜见灯火映高楼",
 u"v7": u"这灯笼真好看，像极了小时候的记忆",
 u"v8": u"快把那笑声再大些，灯也跟着亮",
 u"v9": u"晚上出来走走，满眼都是光啊",
 u"v10": u"档案馆里藏着的，这灯也是当年的样式",
 u"v11": u"街上的灯可真多，照亮了每个人的笑脸",
 u"v12": u"灯挂得真高，看得见星星了",
}
all_lines = []
for ax, buckets in pool.get("axes", {}).items():
    for b, lines in buckets.items():
        all_lines.extend(lines)
missing = []
for v, frag in sorted(daily_used.items()):
    hit = any(frag in ln for ln in all_lines)
    if not hit:
        missing.append(v)
out.append(u"DAILY v1-v12 used-line presence: missing=%s" % (missing if missing else u"NONE all in pool"))

# axes keys overview / any non-axes content
out.append(u"top-level keys: %s" % u", ".join(pool.keys()))
if u"meta" in pool:
    m = pool[u"meta"]
    out.append(u"meta: %s" % json.dumps(m, ensure_ascii=False)[:800])

io.open(os.path.join(BS, ".c3-tmp", "r982_pool_diff.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print(u"POOL-DIFF-OK total=%d missing_daily=%d" % (total, len(missing)))
print(u"\n".join(out[:16]))
