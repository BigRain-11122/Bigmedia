# -*- coding: utf-8 -*-
# R2047 bookkeeping: yield-order ack notes + tech#127 two-step claim + main#21 resume row + probe rename
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def edit(path, old, new, expect=1):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    n = t.count(old)
    assert n == expect, "anchor %r count=%d expect=%d in %s" % (old[:60], n, expect, path)
    t = t.replace(old, new)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(t)
    print("EDIT-OK", os.path.basename(path), old[:40].replace("\n", "|"))

B = os.path.join(ROOT, "src", "os", "backlog.md")

# --- backlog #111: three MV-domain orders ack (insert before "112." row line)
note111 = u"   **[R2047 知悉 2026-10-12]**：集团 orders 10-12 上午三新 MV 域令消费=MV sprint 会话域在案（O-20261012-1015 男女主反韩化重制令〔男主 jman LoRA 全曲线挂载+女主台湾 2000s 年代候选批〕+O-20261012-1050 剧本 v5 穿越-定稿令〔「写不出的开头→穿越去刻→回来写出」因果引擎〕+O-20261012-1102 年代 MV 拍摄语法深研令〔七律正典 ERA-MV-GRAMMAR-v1〕）——本循环=查看位零接触维持（R1745 承继·执行面其窗在执·令行落点节全在案）。\n"
edit(B, u"\n112. **雷达日报（AIHOT 自托管 PoC 转产品线）运维位**",
     u"\n" + note111 + u"112. **雷达日报（AIHOT 自托管 PoC 转产品线）运维位**")

# --- backlog #112: yield-order enforcement note (insert before "113." row line)
note112 = u"   **[R2047 让路执法 2026-10-12]**：O-20261012-1115 CEO 用机让路令本司份额执法毕——pause 指纹 7/8 在役（他窗实跑回执 VRAM 曾清 1615MB）vs 本司 AIHOT 磨链残留实锚（requeue 池在磨+14b-8k 重载驻留 10.4GB）→身份实证先行（aihot_procs complete=tech#125 判据）→worker 60380 停磨（missing-worker rc1·proxy/api 留守轻足印）+ollama stop 14b-8k（VRAM 11764→1707MB=CEO 面恢复）——**tech#92 判据窗 10-13 08:00 受让路面影响注记**：resume 早于 08:00=照读（窗内积累缩短 caveat 如实）·resume 晚于 08:00=顺延 resume 后首个 08:00 compose 窗；复役位=main#21（worker-restart.bat）·watchdog 自动化=tech#127 下轮交付。\n"
edit(B, u"\n113. **全司逐审+强力改善令 O-20261009-1227 BigStream 被审配合位**",
     u"\n" + note112 + u"113. **全司逐审+强力改善令 O-20261009-1227 BigStream 被审配合位**")

# --- tech.md: tech#127 two-step claim (insert after #127 entry line)
T = os.path.join(ROOT, "state", "queue", "tech.md")
with open(T, encoding="utf-8") as f:
    tt = f.read()
anchor127 = u"127. [R2046 新种子·断轮承接真发现]"
assert tt.count(anchor127) == 1, "tech#127 head not unique"
claim = u"   **[R2047 claim 2026-10-12]**：两步制先落防撞——claim=R2047（CPU 面）·live 佐证窗=案族密度当窗实证（R2046 第四案 ~1.6h 盲窗+本日 web 瞬态超时误读=探针面 TimeoutError vs 全灭不可分均待守卫收敛）·交付=下轮（watchdog 脚本+注册件+单测·CEO 让路窗 CPU 面合法位）·随行=resume 复役面 worker-restart.bat（main#21 承载）。\n"
idx = tt.index(anchor127)
end = tt.index("\n", idx) + 1
tt2 = tt[:end] + claim + tt[end:]
with open(T, "w", encoding="utf-8", newline="") as f:
    f.write(tt2)
print("EDIT-OK tech.md tech#127 claim inserted")

# --- main.md: append resume row 21
M = os.path.join(ROOT, "state", "queue", "main.md")
with open(M, encoding="utf-8") as f:
    mt = f.read()
row21 = u"21. [R2047 补货] AIHOT worker CEO 窗停磨·复役位（O-20261012-1115 让路执法面：R2047 停 worker 60380+卸载 14b-8k〔VRAM 11764→1707MB〕）——**resume 执法**（machine-state resume/全面开工令轮）=worker-restart.bat 重启（data/assets/aihot-poc/）+磨链续跑 requeue 池+tech#92 判据窗顺延注记照 backlog #112 R2047 行——gated resume 令\n"
assert "21. [R2047 补货]" not in mt, "row21 already present"
with open(M, "w", encoding="utf-8", newline="") as f:
    f.write(mt.rstrip("\n") + "\n" + row21)
print("EDIT-OK main.md row21 appended")

# --- rename probe r2040 -> r2047 (round-debris self-clean, R2045 precedent)
src = os.path.join(ROOT, ".c3-tmp", "r2040_fastcheck.py")
dst = os.path.join(ROOT, ".c3-tmp", "r2047_fastcheck.py")
if os.path.exists(src):
    os.rename(src, dst)
    print("RENAME-OK r2040_fastcheck.py -> r2047_fastcheck.py")
else:
    print("RENAME-SKIP src absent")

# --- verify all edits landed
with open(B, encoding="utf-8") as f:
    b2 = f.read()
for probe in (u"[R2047 知悉 2026-10-12]", u"[R2047 让路执法 2026-10-12]"):
    assert b2.count(probe) == 1, probe
with open(T, encoding="utf-8") as f:
    assert f.read().count(u"[R2047 claim 2026-10-12]") == 1
with open(M, encoding="utf-8") as f:
    assert u"21. [R2047 补货]" in f.read()
print("VERIFY-ALL-OK")
