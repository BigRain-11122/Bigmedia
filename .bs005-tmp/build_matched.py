# -*- coding: utf-8 -*-
"""BS-005 cards-v1-matched.json builder (R192).

Loads TTS v3 baseline cards (.bs005-tmp/cards.json), attaches honest visual
declarations per footage-matching-spec: probe-evidenced biggame-cockpit for
b5/b7 only; all other beats cards-only with per-beat reasons (numbers-on-
screen mismatch rule: cockpit HUD shows 4/8/153/2min labels, using them for
8/12/10min claims would be on-screen contradiction = spec violation).
ASCII source; Chinese stays in the JSON data file (encoding law)."""
import json
import io
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE = REPO / ".bs005-tmp" / "cards.json"
OUT = REPO / "data" / "sources" / "bs005" / "cards-v1-matched.json"

CP = "data/sources/footage/biggame-cockpit-vertical.mp4"
VISUALS = {
    0: {"cards-only": True, "reason": "四不主张无画面证据：驾驶舱弹窗为集团汇报面，HUD 数字（拍板4款/行动8项）与本拍主张错位，用即声画错位；hook 纯字卡承担（footage-matching-spec §2）"},
    1: {"cards-only": True, "reason": "源池无账本/软著画面：HUD「待审 4 款」「今日 153 笔」与本拍 8 款软著数字错位，避用；账本拍纯字卡锚点 8（§2 无源注理由）"},
    2: {"cards-only": True, "reason": "设计逻辑拍无玩法/广告位画面：源池五源均为总控/日志/台账/剪辑面，无游戏内画面；逼氪→值得停留为设计声明，纯字卡（§2）"},
    3: {"cards-only": True, "reason": "零服务器选型拍无服务器/架构画面：源池无对应证据面，纯字卡（§2 无源注理由）"},
    4: {"source": CP, "req": "窗口标题「Biggame·小游戏公司总控」+弹窗「2/3机并网」=总控机与机器并网状态直接证据（探针 0-44s 全程在帧）；同源多用注记（b7 像素小镇同源·§3）"},
    5: {"cards-only": True, "reason": "驾驶舱仅见「数据 2 分钟前自动刷新」标签（节律数字与本拍 10 分钟主张错位、机制语言不同），10 分钟快照无画面证据，避用即诚实；纯字卡锚点 10 分钟（§2）"},
    6: {"source": CP, "req": "像素园区+各部门楼宇+集团驾驶舱管理弹窗=「管理游戏公司本身就是放置游戏」直接证据（探针 10 帧全程像素小镇·NPC/车辆/施工围挡经营态在帧）；同源多用注记（b5 总控同源·§3）"},
    7: {"cards-only": True, "reason": "遮羞布三连判定为修辞判断拍，源池无买量/上云/氪金对应画面；日志判定体由字幕承担，纯字卡（§2）"},
    8: {"cards-only": True, "reason": "源池无宪法/约束文本画面：园区「公告栏·8项」与本拍 12 条数字错位，避用；12 条红线纯字卡锚点（§2）"},
    9: {"cards-only": True, "reason": "本拍即「没有收入数据」的诚实声明（未上线=未测量）：任何数据画面反而与主张相反；HUD ¥0 为游戏内计数非收入证据，避用（§2+诚实律）"},
    10: {"cards-only": True, "reason": "结构结论拍无画面证据：撤遮羞布为全片论点收束，纯字卡（§2）"},
    11: {"cards-only": True, "reason": "CTA 常规拍纯字卡（footage-matching-spec §1·BS-002/BS-003/BS-004 同型先例）"},
}


def main():
    cfg = json.loads(BASE.read_text(encoding="utf-8"))
    assert len(cfg["cards"]) == 12, "expect 12 cards"
    cfg["meta"]["order"] = (
        "D-BS-06 production open: BS-005 batch-1 shipinhao piece (5th of N=6); "
        "v12 full-set default per D-BS-01; v3 beats = S1 v1.5 first real-gate "
        "10/10 PASS zero-flag (R192) + air-budget cuts v1 66.16s -> v2 61.03s "
        "-> v3 58.39s in-window (1.6s margin, mechanical L15, card anchors "
        "intact, facts 8/10/12 intact); visual declarations probe-evidenced "
        "(biggame-cockpit 10-frame multi-timepoint scan R192)")
    for i, card in enumerate(cfg["cards"]):
        v = VISUALS[i]
        if "source" in v:
            card["visual"] = {"source": v["source"], "req": v["req"]}
        else:
            card["visual"] = {"cards-only": True, "reason": v["reason"]}
    OUT.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    n_src = sum(1 for c in cfg["cards"] if "source" in c.get("visual", {}))
    print("matched cards written:", OUT.name)
    print("footage beats: %d/12 (cards-only %d)" % (n_src, 12 - n_src))
    for c in cfg["cards"]:
        print("%.2f-%.2f" % (c["start"], c["end"]),
              "SRC" if "source" in c.get("visual", {}) else "CAR",
              c["lines"][0][:14])


if __name__ == "__main__":
    main()
