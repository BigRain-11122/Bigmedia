# -*- coding: utf-8 -*-
"""R1900 accounting close: state.json + status-export.json refresh, then
embedded close_commit as the LAST step (tech#65 law: the accounting commit
runs inside the close script, kill window = script-internal only)."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "os"))
from close_commit import run_close_commit  # noqa: E402

NOW = datetime.now()
TS_FULL = NOW.strftime("%Y-%m-%d %H:%M:%S")
PREFIX = "2026-10-10 " + NOW.strftime("%H:%M") + " R1900: "

LOG = PREFIX + (
    "生产轮·tech#66 断轮前体残件守卫交付（O-20260909-1246 取活·R1899 种子兑现·两段制收账=交付件先行+close_commit 末步内嵌）——"
    "①轮首五查静=own orders 顶 O-20260908-1105==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+decisions dnum 内容寻址差集 NEW=[]（水位 130 维持）+ledger @BigStream 4 行==值守锚零新转办+无 index.lock"
    "+树态=mv0001/mv001/whisper v3 MV sprint 会话批域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
    "②HQ orders mtime 16:50:06 破 R1899 锚 16:11:46→尾读两新行全他域知悉 ack"
    "（O-20261010-1645 回测不停机令=@BigMoney 域+O-20261010-1650 全组合项目名收口+重新梳理令=@MiniGame 域"
    "〔内引 meme SCRIPT-FORMULA 五拍反转为方法论锚=本司 meme 线正典跨域消费证·commit 消息承载 P-51〕）·新锚 16:50:06；"
    "③12:00 GPU 窗 C-37 fresh 判读=NO-GO（pause_face 任务态指纹 8/8 Disabled=CEO 让路令在役"
    "〔vram_face 9607MB 已过守卫线=pause 单面即定〕）→四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）"
    "维持 fire-ready gated（材料 R1870/R1871/R1875 turnkey）；"
    "④#111/#115 查看位轻扫零新到件（meme outbound 止于 15:41 narration.mp3==R1899 锚·krea2 30s-reel-v1 止于 15:14 AGE-FINAL-BOARD==R1898 锚·禁重扫跳过）；"
    "⑤tech#66 交付=**round-debris 检测面全落**——loop_health 新 ROUND_DEBRIS_RE 名锚〔^r(\\d+)_〕"
    "+classify_broken_round_debris 纯核（untracked .c3-tmp/rN_* 轮号锚 N ∉ [tick,tick+1]=残件点名"
    "·**双流时序鲁棒**=探针跑在收账 tick 递增前后均不误触当轮在飞件）"
    "+check_broken_round_debris 接线（state tick 缺失/非 git 树/git 失败=静默·顾问级〔tech#22/#31/#37/#58/#60/#61/#62/#64 家族律〕）"
    "·7 新测（R1895 锚形真 git 夹具复现点名+双流时序前后流锁+tick 无效静默+非 .c3-tmp/非数字锚/界外零误触+CLI WARN 不破 FAIL+真仓只读冒烟）"
    "·**704 全回归绿 94.5s rc=0**（697+7·run_suite 正法）——判据双过=①真跑净态（残件清理后零发现+probe_capture 例行消费零 round-debris 行）"
    "②**首战真抓获**=.c3-tmp/__pycache__/r1897_close.cpython-314.pyc（R1897 断轮编译残件·N=1897 锚外·mtime 当日=tech#64 mtime 面射程外的结构性证明）"
    "当场点名→守卫忠告执行=残件删除+复验净态·C-20 v1.73+tech#66 done 标+tech#67 补货（.c3-tmp __pycache__ 生成面治理·真发现种子）；"
    "⑥三探针=probe_capture 单调消费（board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现"
    "/loop_health 2F+史实带内〔两 outage 已裁定不重触发·drift 带内·round-debris 新面净态〕·证据 .c3-tmp/r1900_probes.txt）；"
    "⑦例行件=10-10 日报在案不重跑（R1845 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ 下期 10-15 跳过"
    "·#112 城市口径判据窗 10-11 08:00 届日即领（tech#53 双新源流量首报同窗）·#99 blocked-on-channel 维持（SLA ≤10-13）"
    "·15:07 盘燃已点名毕不重扫·export 刷新（P-61·实况变化=tech#66 交付+两令 ack）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "·tokens:local=0（纯工程+套件跑零本地模型产出调用·P-54⑤ 计量律）——"
    "下轮=R1901 快速路径首查（**10-11 08:00 #112 城市口径判据窗届日即领**〔≥60 ≥2 件+failed 尾读数〕"
    "+GPU 窗 C-37 fresh 判读〔pause 指纹解除即四腿按 R-20261010-01 §5 叠加序开窗〕+tech#67 领取判断）。收账显式列文件 commit+push。"
)

TASK = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R1900: ", "", LOG)[:60]

OUTS = (
    "OS 循环 tick 1900：R1900 tech#66 断轮前体残件守卫交付（round-debris 检测面=untracked .c3-tmp/rN_* 轮号锚外点名·双流时序鲁棒·7 新测·"
    "704 全回归绿 94.5s·**首战真抓获**=R1897 pyc 残件点名+删除净态·C-20 v1.73）"
    "+HQ orders 两新行他域知悉 ack（O-20261010-1645 BigMoney 回测不停机/O-20261010-1650 MiniGame 项目名收口·anchor 16:50:06）"
    "+GPU 窗 C-37 NO-GO（pause 指纹 8/8 在役·vram 9607 过线=单面即定·四腿 fire-ready gated）——详见 state.json log R1900 行"
)

LIVE_OLD = (
    '  "当前活：R1899 断轮吸收（prior body 交付件收口·697 绿复验）+tech#65 close_commit 收账内嵌提交器交付（C-39 v1.72·交付+收账双 dogfood）+GPU 窗 C-37 NO-GO（pause 指纹在役四腿 fire-ready）",\n'
    '  "最近实物：src/os/close_commit.py+tests/test_close_commit.py（C-39 v1.72·commit ffa9fdf6 push ok）+tech.md tech#65 done 标注+tech#66 补货",\n'
    '  "下个里程碑：①10-11 08:00 #112 城市口径判据窗验收（城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报）②GPU 窗 C-37 fresh 判读随轮（pause 指纹在役期四腿 fire-ready gated）③meme-daily-v1 V1 成片到件随轮盯（#115）"'
)
LIVE_NEW = (
    '  "当前活：R1900 tech#66 断轮前体残件守卫交付（round-debris 检测面·C-20 v1.73·704 全回归绿·首战真抓获=R1897 pyc 残件点名+清理）+GPU 窗 C-37 NO-GO 维持（pause 指纹 8/8 在役·四腿 fire-ready gated）",\n'
    '  "最近实物：src/os/loop_health.py round-debris 检测面+tests/test_loop_health.py 7 新测（704 绿 94.5s）+tech.md tech#66 done/tech#67 补货+capabilities v1.73 变更行",\n'
    '  "下个里程碑：①10-11 08:00 #112 城市口径判据窗验收（城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报）②GPU 窗 C-37 fresh 判读随轮（pause 指纹解除即四腿叠加序开窗）③meme-daily-v1 V1 成片到件随轮盯（#115）"'
)

MSG = (
    "R1900: tech#66 round-debris guard delivered (C-20 v1.73: untracked .c3-tmp round-anchored middleware face, "
    "timing-robust vs tick increment, 7 new tests, 704 suite green 94.5s; first real catch = R1897 pyc leftover "
    "named+cleaned, both verdicts met); HQ orders ack O-20261010-1645 (BigMoney) + O-20261010-1650 (MiniGame, cites "
    "our meme SCRIPT-FORMULA) - zero BigStream share, anchor 16:50:06; next: 10-11 08:00 #112 city-caliber readout "
    "+ GPU window fresh check [via bm-a]"
)

FILES = [
    "src/os/loop_health.py",
    "tests/test_loop_health.py",
    "docs/capabilities.md",
    "state/queue/tech.md",
    "src/os/state.json",
    "docs/status-export.json",
    ".c3-tmp/r1900_probes.txt",
    ".c3-tmp/r1900_close.py",
]


def jd(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    # --- state.json: tick+1, log append, ts/task refresh ---
    sp = ROOT / "src" / "os" / "state.json"
    raw = sp.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    state = json.loads(raw.decode("utf-8-sig"))
    assert state["tick"] == 1899, "unexpected tick %r" % state.get("tick")
    state["tick"] = 1900
    state["log"].append(LOG)
    state["ts"] = TS_FULL
    state["task"] = TASK
    s2 = json.dumps(state, indent=1, ensure_ascii=False) + "\n"
    json.loads(s2)  # validate
    sp.write_bytes((b"\xef\xbb\xbf" if bom else b"") + s2.encode("utf-8"))
    print("state.json: tick 1899->1900, log +1, ts/task refreshed")

    # --- status-export.json: export_ts, outs/results append, live 三行 ---
    ep = ROOT / "docs" / "status-export.json"
    raw = ep.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    e = raw.decode("utf-8-sig")
    old = '\n ],\n "chips": ['
    assert e.count(old) == 1, "outs anchor not unique"
    e = e.replace(old, ",\n  " + jd(OUTS) + '\n ],\n "chips": [', 1)
    old = '\n  ]\n ],\n "live": ['
    assert e.count(old) == 1, "results anchor not unique"
    e = e.replace(
        old,
        '\n  ],\n  [\n   "1900",\n   ' + jd(LOG) + '\n  ]\n ],\n "live": [',
        1,
    )
    assert e.count(LIVE_OLD) == 1, "live block anchor not unique"
    e = e.replace(LIVE_OLD, LIVE_NEW, 1)
    old = '"export_ts": "2026-10-10 16:30:29",'
    assert e.count(old) == 1, "export_ts anchor not unique"
    e = e.replace(old, '"export_ts": ' + jd(TS_FULL) + ",", 1)
    json.loads(e)  # validate
    ep.write_bytes((b"\xef\xbb\xbf" if bom else b"") + e.encode("utf-8"))
    print("status-export.json: export_ts/outs/results/live refreshed")

    # --- embedded close commit (last step) ---
    rc, lines = run_close_commit(FILES, MSG)
    print("CLOSE_RC=%d" % rc)
    for ln in lines:
        print("  " + ln)
    return rc


if __name__ == "__main__":
    sys.exit(main())
