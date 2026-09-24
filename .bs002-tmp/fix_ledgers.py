# -*- coding: utf-8 -*-
"""One-shot repair for PS backtick-escape corruption in two ledger lines (R173).
Removes duplicated/mangled lines and rewrites the intended content literally."""
import io

P1 = "output/renders/README.md"
P2 = "docs/reviews/station-reviews.md"

NOTE = ("> BS-002 生产件批（D-BS-06 量产线批次① 第二件·2026-09-24）：中间件 `.bs002-tmp/`"
        "（分句段+间隙/呼吸件+赛博链前后音轨+cards 基线+subs+抽帧探针 tile/裁片）"
        "——同性质非成品·不入本表（R21 声明）；拍稿链 `voiceover-v4/v5.beats.txt`"
        "=窗预算裁口两道（S1 判词存档不回炉）；对位表=`data/sources/bs002/cards-v1-matched.json`"
        "（**入 git**）+`bs-002-v1-shipinhao-60s.mp4.plan.json`（**入 git**）。")

ROW = ("| 2026-09-24 | M2/M3 生产（S2 三门循环独立执法+抽帧验图+脱敏探针） | "
       "bs-002-v1-shipinhao-60s | S2 配音听审+E8 机检面+S3 对位面（循环·R173） | "
       "—（机检档·E8 终审待下轮） | 空气预算律两道裁口（63.20→58.00s 音频·S1 过门稿纯机械窗预算裁"
       "·语义零改·卡片行零动·v4/v5 留档）；对位率 10/12=83%（looplog×6/citywatch×3/reviewsdoc×1"
       "+cards-only×2 注理由·同源多用注记）；三门读数=ai_feel 0 FAIL 0 WARN（gaps 11 处 "
       "0.220-0.558s·CV 0.193/0.197）+层 1.8 六面 PASS+spec 微信视频号双 PASS"
       "（9:16+58.02s 入 30-60s·2.0s 余量）；抽帧验图 4 拍语义全中+脱敏过"
       "（tokens:local=0=技术字段非账单）；AIGC 常驻复核=cards-only 拍低对比度水印在帧可读"
       "（#23 必修项同引擎同缺陷如实注记） | **PASS（S2 三门面·进链生产件）**"
       "——E8 终审+M4+成品库登记=下轮；发布锁=M5 账号物理件+#23 对比度整改批前置 | "
       "本轮三门跑录+`.bs002-tmp/probe-tile.png` 验图件+`bs-002-v1-shipinhao-60s.mp4.plan.json`"
       "（入 git） |")

# --- renders README: drop every line containing 0x08 or the mangled dup, then
#     find the truncated original (ends with 拍稿链 ) and replace with NOTE ---
lines = io.open(P1, encoding="utf-8").read().splitlines()
bad = [i for i, l in enumerate(lines) if ("\x08" in l or "\x0b" in l
        or l.startswith("> BS-002 ") and "\\." in l)]
trunc = [i for i, l in enumerate(lines) if l.endswith("拍稿链 ")]
assert len(trunc) == 1, trunc
lines[trunc[0]] = NOTE
for i in sorted(set(bad) - {trunc[0]}, reverse=True):
    del lines[i]
assert not any("\x08" in l or "\x0b" in l for l in lines)
io.open(P1, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

# --- station-reviews: last table row was mangled/doubled; rewrite it ---
lines2 = io.open(P2, encoding="utf-8").read().splitlines()
assert "\x08" in lines2[-1] or "bs002-tmp" in lines2[-1]
lines2[-1] = ROW
io.open(P2, "w", encoding="utf-8", newline="\n").write("\n".join(lines2) + "\n")

for p in (P1, P2):
    b = open(p, "rb").read()
    assert b.count(b"\x08") == 0 and b.count(b"\x0b") == 0, p
print("repaired OK; renders lines:", len(lines), "| station-reviews lines:", len(lines2))
