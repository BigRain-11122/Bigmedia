# -*- coding: utf-8 -*-
"""R1940 capabilities surgery: insert C-41 row after C-40, append v1.89 changelog."""
import io

PATH = "docs/capabilities.md"
ROW = ("| C-41 | 音频线同文本核验 CLI（same_text_check） | 工程技术部 | live | "
       "`python src/render/same_text_check.py --beats X --srt Y [--decl-check] [--out FILE]`"
       "（state/queue/tech#87·OS 循环 R1940·缺口锚=音频线同文本机械核验六代 ad-hoc 复制实录 "
       "same_text_r275→r277→r279→r281→r637→r1939 全 .c3-tmp 逐件改源复写=S1/E4 wrapper 增殖史同族"
       "〔tech#45 --timeout+tech#46 席位注册已收口的同族〕·音频线续产件每件+1 复制件）"
       "——**单一真相 CLI**：SRT cue 数 vs beats 拍数对齐（COUNT-MISMATCH）+逐 cue 逐字比对"
       "（去空格 verbatim·MISS cueNN+双侧引文行）+hook 三重标注/close 推演声明可选检"
       "（--decl-check advisory 行永不影响 rc·r1939 逻辑原样）+--out UTF-8 无 BOM 证据件；"
       "**rc 0/1/2=same-text 零 miss/MISS 在/用法坏输入**（beats 坏行=缺三列 pipe 响亮 rc2 非静默·"
       "GBK 控制台 backslashreplace 安全打印）；16 新测（CompareCore 5+DeclReport 2+CLI 6+"
       "ParityAnchor 2·r1939 报告行格式冻结锁）·**926 全回归绿 96.2s SUITE_RC=0**"
       "（910+16·run_suite 正法）·**判据双过**=①真跑 SC-004-01-v1 读数与 r1939 ad-hoc 面逐行一致"
       "（cues=17 beats=17/hook-triple-decl 全 True/close-inference-decl True/SAME-TEXT miss=0·rc0）"
       "②正身提取完成=下件音频续产零 ad-hoc 复制（六代复制线收口） |")
CHANGE = ("- 2026-10-11: v1.89 音频线同文本核验 CLI 新席 C-41（O-20261009-1246 取活·state/queue/tech#87·OS 循环 R1940）"
          "——src/render/same_text_check.py 单一真相 CLI（r1939 ad-hoc 正身提取）：同文本核验六代复制线（r275→r1939）收口；"
          "判据双过=真跑 SC-004-01 读数与 r1939 ad-hoc 面逐行一致+926 全回归绿（+16 新测·ParityAnchor 冻结 r1939 报告行格式）。")

text = io.open(PATH, encoding="utf-8").read()
assert "| C-41 |" not in text, "C-41 already present"
lines = text.splitlines()
idx = [i for i, l in enumerate(lines) if l.startswith("| C-40 ")]
assert len(idx) == 1, "C-40 row not found"
ins = idx[0] + 1
lines.insert(ins, ROW)
out = "\n".join(lines)
if not out.endswith("\n"):
    out += "\n"
out += CHANGE + "\n"
io.open(PATH, "w", encoding="utf-8", newline="\n").write(out)
print("OK: C-41 inserted after line %d, changelog appended" % ins)
