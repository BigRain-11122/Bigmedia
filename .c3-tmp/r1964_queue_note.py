# -*- coding: utf-8 -*-
import io

path = "state/queue/main.md"
with io.open(path, "r", encoding="utf-8") as f:
    text = f.read()

NOTE = " **[R1964 注记]**：A 首件批第二件=C-00025 陆海峰收官——**F-173 登记**（R1964 单轮全链：拍稿 46 verbatim 锚零 MISS→S1 10/10 一次过〔fire 10:57 GO 即发〕→TTS light 212.78s→同文本 13/13→ai_feel 0F0W→ASR 终轨 46 cues〔信条句 close 位 verbatim 全净·字位 15.0% 再外溢 1.2pp→S2 8.0 诚实扣 1.0〕→E4 8.0 同窗〔fire 11:02 GO 即发·三连 8.0〕→E8 七席 ≥9→M4→F-173=成品库第 173 件·L-音第 28 件·单轮全链=SC-005-01 三轮链压缩·fire 窗连用+turnkey 预载双教训执法兑现）；余位=第三件 C-00024 缪一〔把自己复制两份〕随轮领。"

if "[R1964 注记]" in text:
    print("NOTE-ALREADY-PRESENT skip")
else:
    lines = text.splitlines(keepends=False)
    for i, l in enumerate(lines):
        if l.startswith("14."):
            lines[i] = l.rstrip() + NOTE
            break
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")
    print("QUEUE-14-NOTED")
