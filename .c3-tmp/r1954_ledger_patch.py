# -*- coding: utf-8 -*-
# R1954 ledger patch: MD-0002 voice-leg-1 record into queue main#4 and the
# piece README. Idempotent: skips a line if its R1954 marker already present.
from pathlib import Path

Q = Path("state/queue/main.md")
R = Path("data/storylines/drama/md0002/README.md")

Q_ADD = ("——**[R1954 配音腿第一程 2026-10-11]**：三声部档位声直出（tech#2 定谳）+逐镜实测毕"
         "——narrator 8 镜 Yunyang 产线默认/system 2 镜 Yunjian rate-10% pitch-3Hz 机械播报克制/"
         "afeng 3 镜 Xiaoxiao rate+4% pitch+2Hz〔沪语跨语=R1785 保留面·档位声直出本程〕·"
         "空气预算律（6s 镜窗·≥0.3s 空气）12/13 fit（shot02 +15%/shot05 +8% rate bump=verbatim 保真机械窗预算·E8 听审可 A/B 回退）+"
         "shot07（04:30 主题锚句）自然语速 6.79s=extend-shot 7.1s 候选（延伸哲学=保锚句自然 delivery·+15% 压速判弃）——"
         "drama-ep 窗验证：speech 55.53s+12 gap 求解=投影 57.0-74.6s∈[60,90]（floor 面由 gap 求解器补足·ceiling 面 74.6<90 留裕）——"
         "资产=data/storylines/audio/MD-0002-voice-v1-shotNN.mp3×13+draft 预览（mp3 gitignored·charter §4 口径）+"
         "voice-v1.json=装配腿消费正源（cast/flags/时长/verdict 全量）·gen-voice-v1.py=可复跑件；"
         "T2I PACK 腿维持 tech#29 门（提示词规范 retrofit gated CEO 点头+GPU 窗）不抢跑·余链=T2I〔gated〕→装配→S2+E8→M4→F 登记")

R_ADD = """
- [R1954 配音腿第一程 2026-10-11] 三声部档位声直出（tech#2 定谳：CosyVoice3 判负→edge-tts 档位声）+逐镜时长实测——cast：narrator=zh-CN-YunyangNeural（产线默认·light 赛博纹理=装配腿整轨面）/system=zh-CN-YunjianNeural（rate-10% pitch-3Hz 机械播报克制）/afeng=zh-CN-XiaoxiaoNeural（rate+4% pitch+2Hz·上海话跨语=R1785 保留面本程未达）。空气预算律（6s 镜窗≥0.3s 空气）：12/13 fit（shot02 +15%/shot05 +8% rate bump=verbatim 保真机械窗预算·E8 听审可 A/B 回退）+shot07（04:30 主题锚句）+15% 仍超→**自然语速 6.79s=extend-shot 7.1s 候选**（延伸判决=保锚句自然 delivery·+15% 压速与延伸哲学相抵判弃）。drama-ep 窗验证：speech 55.53s+gap 求解投影 57.0-74.6s∈[60,90]（floor 面=求解器补 air 正常路径·ceiling 面 74.6<90 留裕）。资产：`data/storylines/audio/MD-0002-voice-v1-shotNN.mp3`×13+`MD-0002-voice-v1-draft.mp3` 预览（mp3 gitignored）+`voice-v1.json`（cast/flags/时长/verdict=装配腿消费正源）+`gen-voice-v1.py`（可复跑·路径修正 parents[4] 实锚在案）。T2I PACK 腿维持 tech#29 门（提示词规范 retrofit gated CEO 点头+GPU 窗）不抢跑。
"""


def patch(path, add, marker, at_line=None, append_mode=False):
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print("SKIP (marker present):", path)
        return
    lines = text.splitlines(keepends=True)
    if append_mode:
        if not text.endswith("\n"):
            text += "\n"
        text += add
    else:
        idx = at_line
        lines[idx] = lines[idx].rstrip("\n") + add + "\n"
        text = "".join(lines)
    path.write_text(text, encoding="utf-8")
    print("PATCHED:", path)


patch(Q, Q_ADD, "[R1954 配音腿第一程", at_line=7)
patch(R, R_ADD, "[R1954 配音腿第一程", append_mode=True)
