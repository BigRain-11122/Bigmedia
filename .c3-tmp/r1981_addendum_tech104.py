# -*- coding: utf-8 -*-
"""R1981 addendum: correct tech#104 (wrong gitignored premise, tracked-evidence restore record)."""
import io

PATH = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\state\queue\tech.md"

NEW_104 = (
    "104. [R1981 补货→R1981 轮末勘误收口·判负留痕] .c3-tmp 存量清账评估（**R1981 判定勘误**：R1981 落板原缺口锚基于「.c3-tmp=gitignored 会话中间件」错误前提——"
    "R1981 收账后复核查实 git ls-files .c3-tmp=400 件全 tracked=tech#81 自含律设计正身〔每轮 close 脚本/探针证据件随 close commit 入 git=清理律「删净或批量入账」的入账臂·历轮已持续满足〕→"
    "R1848-R1976 存量非「跨轮遗留复发」=committed 证据链；**R1981 ⑦段「近窗族清账」8 件 Remove-Item=tracked 证据件误删**（r1976-r1980_close×5+r1978_fmt_restore+r1979_group_scan_orders/r1979_probes×2·git status 8 行 D 实锚·r1979 证据件=R1979 committed log 行引文证据面）→"
    "**同轮 git checkout HEAD -- 8 件全恢复**（未提交前恢复=零历史影响·恢复后 git status .c3-tmp 干净实证）；"
    "候选裁=**判负收口零动作**（存量面=committed 证据链维持·清理钩执法面收窄维持 tech#81 判据原样=当轮新临时件经 close 自含律入账·untracked 遗留=tech#81 判据既有覆盖）；"
    "教训入册=**删临时件前必 git check-ignore/git ls-files 实测追踪态**（勿凭 git status 零显示推 ignored——R1981 实锚：tracked+unmodified=零显示≠ignored·新鲜验证律执法）；"
    "R1981 state log ⑦段错误宣称按「错账留痕勘误禁抹除」保留原文·本行=勘误正身；判据=本行即档·后续轮 .c3-tmp 零误删（git status 干净=执法通过））"
    "——[done 2026-10-11 R1981 轮末勘误·判负留痕收口]"
)

with io.open(PATH, encoding="utf-8") as f:
    lines = f.readlines()

out, hit = [], 0
for ln in lines:
    if ln.startswith("104. [R1981"):
        out.append(NEW_104 + "\n")
        hit += 1
    else:
        out.append(ln)

if hit != 1:
    raise SystemExit("ANCHOR-FAIL: expected exactly one '104. [R1981' line, found %d - aborting, no write" % hit)

with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.writelines(out)
print("TECH104-CORRECTED", hit)
