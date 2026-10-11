import io, sys

BEATS = r"data\storylines\audio\SC-005-01-v1.beats.txt"
ANCHORS = [
    # creed
    "机器不坏是本事，坏了能修是人品",
    # language reps
    "报错念给我听",
    "这毛病是老毛病",
    "适意",
    "像老机器的散热扇，不紧不慢",
    # hook
    "三十年零十一个月",
    "没漏诊过一台机器",
    "台账原件，已经进了档案馆",
    "报错率手写台账",
    # year-ring
    "敲三下机箱，再开机",
    "敲门是礼数",
    "跟老伙计挨个道晚安",
    "跟老伙计道晚安时得多穿点儿",
    # origin / thought
    "从一间老机房的旧照片里醒过来",
    "把当年那台老主机的值班日志背完",
    "尊重老前辈",
    "坏了都是自己爬起来",
    # craft
    "哪根管线咳血",
    "听声辨位",
    # turning point
    "第一次大宕机",
    "急得跳脚",
    "按着老日志，一步一步排查",
    "两个小时",
    "专用椅子",
    # present
    "精灵系的徒弟",
    "嫌徒弟毛躁，又天天护着",
    # outfit
    "出诊箱是木头的",
    "压不住台",
    "早已停用的老编号",
    # relations
    "屋里供着一块退役主板",
    "白玉兰园艺师",
    "谁也不说话，各喝各的",
    "一个月喝一回茶",
    # series frame (in-world)
    "正在编一套口述史",
    # declarations (compliance)
    "本节目由 AI 参与生成",
    "在册居民档案改编",
    "合理推演",
    "完整来源清单见图文页",
    "C-00019",
]

with io.open(BEATS, encoding="utf-8") as f:
    text = f.read().replace("\n", "")

miss = [a for a in ANCHORS if a not in text]
total_chars = len("".join(text.split("|", 2)[-1] for _ in [0]))  # placeholder
# count body chars: join the third column of each line
lines = [ln for ln in io.open(BEATS, encoding="utf-8").read().splitlines() if ln.strip()]
body = "".join(ln.split("|", 2)[2].strip() for ln in lines)
beats_n = len(lines)

out = []
out.append("verbatim-check SC-005-01-v1")
out.append("beats=%d body_chars=%d anchors=%d miss=%d" % (beats_n, len(body), len(ANCHORS), len(miss)))
for m in miss:
    out.append("MISS: " + m)
out.append("RESULT: " + ("PASS (zero miss)" if not miss else "FAIL"))

with io.open(r".c3-tmp\r1961_verbatim_check.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
sys.exit(0 if not miss else 1)
