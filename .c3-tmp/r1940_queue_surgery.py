# -*- coding: utf-8 -*-
"""R1940 queue surgery: mark tech#87 done with delivery note."""
import io

PATH = "state/queue/tech.md"
ANCHOR = "——按认领制随轮领做（CPU 面·轻量）"
# only the tech#87 row ends with this exact anchor after its paren block
DONE = ("——[done 2026-10-11 R1940] ——已交付：**src/render/same_text_check.py 单一真相 CLI 全落（C-41 v1.89）**"
        "——r1939 ad-hoc 正身提取：SRT cue 数 vs beats 拍数对齐（COUNT-MISMATCH）+逐 cue 去空格 verbatim 比对"
        "（MISS cueNN+双侧引文行）+--decl-check advisory（hook 三重标注/close 推演声明·r1939 逻辑原样·永不影响 rc）"
        "+--out UTF-8 无 BOM 证据件+rc 0/1/2（same-text 零 miss/MISS 在/用法坏输入——beats 缺三列行响亮 rc2 非静默）；"
        "16 新测（CompareCore 5+DeclReport 2+CLI 6+ParityAnchor 2=r1939 报告行格式冻结锁）·"
        "**926 全回归绿 96.2s SUITE_RC=0**（910+16·run_suite 正法）·"
        "**判据双过**：①CLI 真跑 SC-004-01-v1 读数与 r1939 ad-hoc 面逐行一致"
        "（cues=17 beats=17/hook-triple-decl 全 True/close-inference-decl True/SAME-TEXT miss=0·rc0）"
        "②正身提取完成=下件音频续产走本 CLI 零 ad-hoc 复制（六代复制线 r275→r1939 收口）")

text = io.open(PATH, encoding="utf-8").read()
pos = text.find("87. [R1939 补货")
assert pos >= 0, "tech#87 row not found"
seg = text[pos:]
a = seg.find(ANCHOR)
assert a >= 0, "anchor not found in tech#87 row"
end = a + len(ANCHOR)
text = text[:pos] + seg[:end].replace(ANCHOR, DONE, 1) + seg[end:]
io.open(PATH, "w", encoding="utf-8", newline="\n").write(text)
print("OK: tech#87 marked done")
