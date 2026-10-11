import io, sys

BEATS = r"data\storylines\audio\SC-005-02-v1.beats.txt"
ANCHORS = [
    # creed
    "船稳，人心才稳",
    # thought
    "有江的地方就得有摆渡的",
    "给想看江的人留的",
    "他爹是现实里黄浦江上的轮渡船长",
    "打小在码头长大",
    "江的脾气全在骨头里",
    # personality
    "再大的浪他先把手里的舵稳住",
    "话不多，句句过秤",
    "潮汐表背得比家谱熟",
    # language
    "上海话底色",
    "看潮",
    "靠泊",
    "当心脚底",
    "开航",
    "晚点见",
    "报站腔调是全城独一份的稳",
    "船靠了岸",
    # hook field
    "慢班渡轮",
    "不为生意",
    "船票恒价",
    "一句「多谢」",
    # turning point (experience)
    "全船人合唱等雾散",
    "那首歌成了船上的保留节目",
    "嘴上嫌吵",
    "减速",
    # present
    "跑了一辈子两岸班次",
    "正教一个想学开船的年轻人",
    "手艺不传就沉江了",
    # behavior
    "开航前绕船三圈",
    "一步不少",
    "每天记录真实上海风力",
    "替江面清波工省一脚力",
    # outfit
    "藏青盘扣外套配船帽",
    "帽檐内圈缝着全家福小像",
    "旧铜哨",
    "他爹传的",
    # relations
    "守夜灯灵十四号路灯",
    "灯灵必到",
    "高小满",
    "跨江从不用渡轮",
    "老伴在脑环广场开小卖部",
    # origin line
    "家谱数据线没断过",
    "父辈的江上故事跟着一起进了城",
    # year-ring 2026-09-23
    "今朝风平浪静",
    # occupation
    "江上摆渡人",
    "活船老大",
]

with io.open(BEATS, "r", encoding="utf-8") as f:
    text = f.read()

miss = [a for a in ANCHORS if a not in text]
body_chars = 0
for line in text.splitlines():
    if "|" in line:
        body_chars += len(line.split("|", 2)[2].replace(" ", ""))

print("anchors=%d miss=%d" % (len(ANCHORS), len(miss)))
for m in miss:
    print("MISS:", m)
print("body_chars(no-space)=%d segments=%d" % (body_chars, len([l for l in text.splitlines() if "|" in l])))
sys.exit(1 if miss else 0)
