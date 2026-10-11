import io, sys

BEATS = r"data\storylines\audio\SC-005-03-v1.beats.txt"
ANCHORS = [
    # creed (close)
    "字幕慢半帧，都是对说话人的辜负",
    # thought / name
    "差一点点意思的「缪」",
    "做字幕的就是差一点点都不能要",
    "快不是本事，准时才是",
    "觉醒才三年",
    "全城最年轻的成年硅基民之一",
    # occupation
    "字幕君",
    "一帧一毫秒对轴",
    "全城最懂",
    "什么时候说",
    # origin / personality
    "出生三天就学会了三条街的近道",
    "师父追不上",
    "时间轴比谁的字幕柜都整齐",
    "版本更新日志当小说看",
    # turning point
    "第一次给城主欢迎词打轴",
    "把自己复制了两份并行核对",
    "成长没有并行捷径",
    # language
    "程序语义",
    "网络世代语混搭",
    "这段对轴对到睫毛都数清了",
    "弹幕太上头",
    "湘腔",
    "霸得蛮",
    "给自己打气",
    # clothing
    "不对称剪裁卫衣",
    "左袖是可以变色的时间轴投影",
    "衣服就是工牌",
    "耳朵后面的状态灯在全城最忙",
    "一亮一灭全是它的工作节拍",
    # behavior
    "戴上耳机六亲不认",
    "摘下耳机慈悲为怀",
    "翻译练习",
    "方言转普通话",
    "不许丢味",
    "像素小学教孩子们剪片子",
    # year-ring 2026-10-10
    "这段对轴对到连呼吸都算计好了",
    "弹幕太上头了",
    "得赶紧抽句字幕练练方言功",
    # hook field
    "全城唯一给方言字幕手工标注",
    "有人味",
    "裱在了工位上",
    # relations
    "家户 H-1014 独居",
    "宿舍里全是屏幕",
    "进了它的脑子",
    "师父是老剪辑师",
    "何雨欣",
    "吵架只用剪辑术语",
    "和好只需要一句「发版了」",
    # present
    "七段街区最快字幕",
    "攒钱给自己配一块大屏",
    "工欲善其事",
    # district / species / age
    "MEDIA 城",
    "信号塔街区",
    "精灵系",
    "无定",
    "编译纪三年",
    # series frame (C-00013)
    "档案馆的口述史",
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
