# -*- coding: utf-8 -*-
"""R1905 accounting close (tech#71 delivery, segment-2 prep).

Does: tech.md done-mark + tech#72 seed append, capabilities v1.78,
evidence file, state.json tick/log/ts/task, scratch tmp cleanup.
Export refresh runs separately via the tech#70 canonical writer CLI.
"""
import io
import json
import os
import re
import sys
from datetime import datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ROUND = "R1905"
LOG_LINE = (
    "2026-10-10 20:0x R1905: 等待窗 P2 取活·tech#71 chips/depts 胞形契约 parity "
    "守卫交付（O-20261009-1246 取活·R1904 补货兑现·交付段先行 commit e12583d3）——"
    "①轮首五查全静（own orders mtime==R1733 锚+origin_gap_check QUIET ahead0 behind0"
    "+group_scan truly_new=0 水位 131 维持+ledger @BigStream 4 行==锚+HQ orders "
    "18:54:32==R1902 锚·树态=MV sprint 会话域在飞件零接触 R1745 承继）；"
    "②tech#71 交付=classify_export_face 增 export-chips〔[txt 2..14, live|wip] 2 胞〕"
    "+export-depts〔{n 2..24, t 2..96, s∈{0,1,2} 缺省 1}〕双胞形面——消费方契约先核"
    "（零断言纪律：MiniGame generate.ps1 v6.2 整形律 L192-225+strings.json EF 原文实读="
    "shaper 丢 n/t<2 条目+丢 txt<2 胞+静默改 class→wip/s→1+截断超帽文本·tech#71 原文 "
    "s∈{1,2} 勘正=s=0 亦原样保留·合法值 {0,1,2}〔L195〕）·守卫+writer 写前自检双消费"
    "同源（export_refresh._classify 同一纯核=一次修双面·2 拒写测盘字节零触碰）；"
    "③判据双过=锚形 fixture 复现点名（chips 7/7+depts 7/7+边界静默）+真仓实读 "
    "ZERO-FINDINGS（8 depts+14 chips 全净·.c3-tmp/r1905_t71_realrepo.txt）；"
    "④767 全回归绿 118.1s SUITE_RC=0（761+6·run_suite 正法）；⑤收账=两段制（交付段 "
    "e12583d3 先行上链）+tech#71 done 标+tech#72 补货（live 面消费方核验种子=本轮代码"
    "精读真发现：六检面 do/depts/outs/chips/results/ts 而 live 三行零检·产品优先律 §5 "
    "CEO 过程可见面正身·且 shaper 是否消费 live 未核）+capabilities v1.78+export 走 "
    "tech#70 正典写入器（新胞形守卫在写前自检内首战 dogfood）+.c3-tmp r1905 草稿件三"
    "删净证据件留一；例行件：日报 10-10 在案不重跑（Test-Path 实证）·W41 周审在案·"
    "W42 件 10-12 到窗·T1 催办线无新增·HQ-FEEDBACK 不写（无集团层新 open 问题）·"
    "tokens:local=0（纯 CPU 面·零本地模型调用·P-54⑤ 计量律如实记）；下轮=R1906 五查"
    "→tech#72（live 面消费方核验）或 GPU 窗 C-37 fresh 判定（四腿 fire-ready：MD-0002 "
    "剧本腿/DIGEST v17 M4.5·E4/F-170 S1）或 10-11 08:00 #112 城市口径判据窗验收。"
)

EVIDENCE = """tech#71 chips/depts parity facets - round R1905 evidence
=========================================================
[judgement criterion 1] anchor-shape fixture reproduction:
  guard tests: chips 7/7 bad cells named + depts 7/7 bad cells named
  (tests.test_loop_health.ExportFaceTests, 4 new cases)
  writer tests: bad chips/depts patch refused rc=2, export file
  byte-identical (tests.test_export_refresh.RefusalTests, 2 new)
  targeted run: Ran 44 tests OK (ExportFaceTests + export_refresh)
[judgement criterion 2] real-repo read (r1905_realrepo_check.py):
  tech#71 criterion-2 real-repo read: 0 export face finding(s)
  RESULT: ZERO-FINDINGS
[full regression] tools/run_suite.ps1 (tech#33 canonical runner):
  SUITE_RC=0
  SUITE_RAN=Ran 767 tests in 118.086s
  SUITE_RESULT=OK
[consumer contract source read]
  MiniGame tools/siliconwatch generate.ps1 L192-225 (v6.2 shape loop)
  MiniGame tools/siliconwatch strings.json labels.export_face EF caps
  correction: tech#71 seed text said depts s in {1,2}; shaper L195
  keeps s=0 too -> valid set {0,1,2}, missing s defaults to 1
[deliverable commit] segment-1: e12583d3 (pushed)
"""

TECH_HEAD_OLD = "71. [R1904 补货·tech#70 交付面真发现] chips/depts 胞形契约 parity 守卫候选（缺口锚="
TECH_HEAD_NEW = "71. [done 2026-10-10 R1905] chips/depts 胞形契约 parity 守卫（R1904 补货·tech#70 交付面真发现·缺口锚="
TECH_TAIL_OLD = ("〔守卫+writer 自检双消费同源=一次修双面〕·判据=锚形 fixture 复现点名+真仓零发现"
                 "·判负留痕合法）——按认领制随轮领做（CPU 面）")
TECH_TAIL_NEW = ("〔守卫+writer 自检双消费同源=一次修双面〕·判据=锚形 fixture 复现点名+真仓零发现"
                 "·判负留痕合法）——已交付：**export-chips+export-depts 双胞形面落位（commit "
                 "e12583d3）**——①消费方契约先核（零断言纪律：MiniGame generate.ps1 v6.2 整形律"
                 "L192-225+strings.json labels.export_face EF 原文实读——shaper 丢 n/t 缺失或 <2 的 "
                 "depts 条目+丢 txt<2 的 chips 胞+静默改 class→'wip'/s→1+截断超帽文本·**tech#71 原文"
                 " s∈{1,2} 勘正=s=0 亦原样保留·合法值 {0,1,2}〔generate.ps1 L195〕**）；"
                 "②classify_export_face 增 export-chips〔[txt 2..14, live|wip] 2 胞〕+export-depts"
                 "〔{n 2..24, t 2..96, s∈{0,1,2} 缺省 1}〕——守卫+writer 写前自检双消费同源"
                 "（export_refresh._classify 同一纯核·2 拒写测文件字节零触碰）；③判据双过=锚形 "
                 "fixture 复现点名（chips 7/7+depts 7/7+边界静默）+真仓实读 ZERO-FINDINGS"
                 "（8 depts+14 chips 全净·.c3-tmp/r1905_t71_realrepo.txt）；④**767 全回归绿 "
                 "118.1s SUITE_RC=0**（761+6·run_suite 正法）；⑤下位发现=tech#72（live 面消费方"
                 "核验种子）")

TECH_72 = ("72. [R1905 补货·tech#71 交付面真发现] live 面消费方核验+守卫候选评估"
           "（缺口锚=R1905 代码精读实测：classify_export_face 六检面=do/depts/outs/chips/"
           "results/ts 而 **live 三行全面不检**——产品优先律 §5 明文「本司对外实况面 "
           "docs/status-export.json 必含三行（当前活/最近实物/下个里程碑）」=live 是 CEO "
           "过程可见面正身·且 tech#70 写入器白名单含 live 键；同时 MiniGame generate.ps1 "
           "v6.2 整形循环只读 do/depts/outs/chips/results 五键 **live 是否被硅基窗 shaper "
           "消费未核**〔L161-245 实读未见·canonical.html 及其他消费面未扫〕——本件=先核"
           "消费方〔generate.ps1 全文+canonical.html+数据件消费面扫〕再定守卫形态候选"
           "〔存在性+3 行形态+行帽·守卫锚形 fixture 复现+真仓零发现〕·消费方不消费=守卫"
           "降级为 writer 白名单形态注记收口·判负留痕合法）——按认领制随轮领做（CPU 面）")

CAPS_LINE = ("- 2026-10-10: v1.78 chips/depts 胞形守卫批（O-20261009-1246 取活·state/queue/"
             "tech#71·OS 循环 R1905）——C-20 升级：**export-chips+export-depts 胞形面**"
             "（缺口锚=R1904 交付面代码精读真发现：classify_export_face 只检 chips 条目帽"
             "〔≤14〕不检胞形·depts 全面不检——坏条目过 writer 写前自检+例行探针双面皆静默"
             "·消费方 v6.2 shaper 逐字段整形律静默回退=CEO 看板条目级陈腐面敞口〔R1901 面"
             "族的 chips/depts 残余位〕）——loop_health 新 `_export_chip_cell_ok`〔[txt 2..14, "
             "live|wip] 2 胞·shaper 丢 txt<2 胞+静默改 class→'wip'=mislabel 可见化〕+"
             "`_export_dept_cell_ok`〔{n 2..24, t 2..96, s∈{0,1,2} 缺省 1} 对象·shaper 丢 "
             "n/t<2 条目+静默 s→1+截断超帽〕+classify_export_face 增两 facet〔一 WARN 一面·"
             "家族律顾问级〕——**消费方契约先核**（零断言纪律：generate.ps1 L192-225+strings.json "
             "EF 原文·tech#71 种子文 s∈{1,2} 勘正={0,1,2}）·**守卫+writer 写前自检双消费同源**"
             "（export_refresh._classify 同一纯核=一次修双面·tech#70 写入器拒写路径自动覆盖）"
             "·6 新测（守卫 4：chips 七坏形 7/7 点名+边界静默+depts 七坏形 7/7 点名+边界静默"
             "〔s 缺省=shaper 同语义〕/writer 2：坏 chips/depts patch 拒写 rc2+文件字节零触碰）"
             "·**767 全回归绿 118.1s rc=0**（761+6·run_suite 正法）——判据双过=①锚形 fixture "
             "复现点名（单测锁）②真仓实读 ZERO-FINDINGS（8 depts+14 chips 全净·"
             ".c3-tmp/r1905_t71_realrepo.txt·新面首战静默 PASS）；下位发现=tech#72（live 面六检"
             "缺位·消费方核验先行）。现 live×34 / in-dev×1 / blocked×2 / planned×1（存量探针"
             "升级非新席）。")


def read_text(path):
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def write_text(path, text):
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def replace_once(text, old, new, label):
    """Idempotent single replace: apply, or skip if already applied."""
    n = text.count(old)
    if n == 1:
        return text.replace(old, new, 1)
    if n == 0 and text.count(new) == 1:
        return text  # already applied by a prior partial run
    raise AssertionError("%s: expected 1 occurrence, found %d" % (label, n))


def main():
    steps = []

    # --- 1. tech.md: done-mark #71 + append #72 ---
    tech_path = os.path.join(REPO, "state", "queue", "tech.md")
    tech = read_text(tech_path)
    eol = "\r\n" if "\r\n" in tech else "\n"
    tech = replace_once(tech, TECH_HEAD_OLD, TECH_HEAD_NEW, "tech head")
    tech = replace_once(tech, TECH_TAIL_OLD, TECH_TAIL_NEW, "tech tail")
    if not tech.endswith(("\n", "\r\n")):
        tech += eol
    if "72. [R1905" not in tech:
        tech += TECH_72 + eol
    assert tech.count(eol + "72. [R1905") == 1, "queue-glue guard: 72 head must be line-anchored once"
    write_text(tech_path, tech)
    steps.append("tech.md: #71 done-mark + #72 seed appended (eol=%r)" % eol)

    # --- 2. capabilities.md: v1.78 ---
    caps_path = os.path.join(REPO, "docs", "capabilities.md")
    caps = read_text(caps_path)
    eol = "\r\n" if "\r\n" in caps else "\n"
    if "v1.78" not in caps:
        if not caps.endswith(("\n", "\r\n")):
            caps += eol
        caps += CAPS_LINE + eol
        write_text(caps_path, caps)
    steps.append("capabilities.md: v1.78 ensured")

    # --- 3. evidence file ---
    ev_path = os.path.join(REPO, ".c3-tmp", "r1905_t71_realrepo.txt")
    write_text(ev_path, EVIDENCE)
    steps.append("evidence: .c3-tmp/r1905_t71_realrepo.txt written")

    # --- 4. state.json: tick/log/ts/task ---
    state_path = os.path.join(REPO, "src", "os", "state.json")
    with io.open(state_path, "r", encoding="utf-8", newline="") as fh:
        state = json.load(fh)
    if state.get("tick") == 1905:
        steps.append("state.json: already at tick 1905 (prior run)")
    else:
        assert state["tick"] == 1904, "expected tick 1904, got %s" % state["tick"]
        state["tick"] = 1905
        state["log"].append(LOG_LINE)
        state["ts"] = NOW
        m = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{1,2}x? R\d+: (.*)$", LOG_LINE)
        assert m, "log line prefix shape"
        state["task"] = m.group(1)[:60]
        with io.open(state_path, "w", encoding="utf-8", newline="") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        steps.append("state.json: tick=1905, log+1, ts=%s, task=%s..."
                     % (NOW, state["task"][:24]))

    # --- 5. scratch cleanup (keep evidence file only) ---
    removed = []
    for name in ("r1905_tech_list.py", "r1905_t71.txt", "r1905_realrepo_check.py"):
        p = os.path.join(REPO, ".c3-tmp", name)
        if os.path.isfile(p):
            os.unlink(p)
            removed.append(name)
    steps.append("scratch removed: %s" % ", ".join(removed))

    for s in steps:
        print("OK", s.encode("ascii", "replace").decode("ascii"))
    print("CLOSE-PREP-DONE ts=%s" % NOW)
    return 0


if __name__ == "__main__":
    sys.exit(main())
