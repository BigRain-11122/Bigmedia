# -*- coding: utf-8 -*-
"""R2014 closing step (canonical single-writer path, tech#76):
finalize_state + export_refresh + run_close_commit (self-included
per tech#81 autodetect law)."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))
import close_commit as cc  # noqa: E402

LOG = (
 "2026-10-12 03:2x R2014: 生产轮·P2 队头消费=tech#120 楔死快败探针交付（O-20261009-1246 取活·fire 卡 no-fire 等待窗照取·两段制收账=交付段 9fd1a7f2 先行）——"
 "①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面静"
 "（decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS rows=270 tail_key='10-11 13:4x'==基线 tech#103 连窗过+HQ orders 14:00:46==R1978 消费锚）"
 "+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；"
 "②tech#106 消费律=comfy_activity 02:53:53 quiet rc0（queue 0/0+cpu delta 0.0ms·PID 58200）→fire_window_card 02:55:30 verdict=no-fire"
 "（gate 双闸败 free_min 446MB<2048 守卫+util_max 99>80·probe face=busy-contended·band 3 稳态·readings-age gate 90s vs TTL 120s tech#90 在役）"
 "→F-180 flight-3 维持挂 fire_consume 重发通道结转（R2013 指针）；"
 "③tech#120 交付=C-24 --wedge-probe 面（单一真相入 call_expert.py 非 per-launcher 手拼）：WEDGE_PROBE_MODEL qwen2.5:7b-instruct（4.7GB·ollama list 实核在册）+WEDGE_PROBE_CAP 90s 帽复用 call_model"
 "→健康席秒回 WEDGE-OK 续飞主调用（R2012 GEN-OK 7b 5.8s 实锚）／楔死席烧帽 WEDGE-FAIL rc 6 新码快败（rc 空间 0/2/3/4/5 零占用·expert_retry_loop 语义不撞）"
 "+帽律=探针帽独立于 --timeout 1500 主帽（回归锁）+审计纯度=探针先于 verdict/ledger 写路径零 expert-calls 落行（tech#120 判据③·双断言测试锁）+guard→probe→main 序"
 "+staged 发射器 sc005-07-v1-tmp/s1_call.py 接参 --wedge-probe=flight-3 受益面（flight-1/R2012+flight-2/R2013 同病结构性根治）+5 新测 TestWedgeProbeCli"
 "（timeout 快败 rc6 零主飞行烧零台账行/非零 rc 快败同面/过探续飞主调用台账行在/旗关零探针飞行/主帽 1500 下探针帽 90 独立）——e4 家族接面=显式延后腿注记"
 "（e4_call 族直呼 ollama 不走 call_expert·接面位=e4_launcher_gen 机器段·窗口=F-171 评审腿 e4 发射器迭代窗=原 scope「s1/e4 下次发射器迭代窗并入」正身·非静默缺口）；"
 "④随批真发现收口=tech#114 守卫真仓冒烟复绿：suite 首跑 1123 例 1 失败=test_loop_health AudioTmpResidueTests.test_real_repo_clean_baseline_smoke"
 "点名 sc005-07-v1-tmp 6 件 untracked（R2012/R2013 断窗轮 flight 残件收账缺口=s1-run.out/err+s1_call.py.out/err 证据件+asr_diff_r2012/e4-material/same_text_r2012 预置件）"
 "→按守卫文本「batch-commit」臂交付段批量入账（+r2013_s1_flight2_timeout_evidence.txt 收账缺口一并回补）→复跑 **1123 全回归绿 120.4s SUITE_RC=0**（1118+5·run_suite 正法）"
 "=守卫执法首抓获后收口闭环（R2012/R2013 log 预期态注记的消费面兑现）；"
 "⑤三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现 unannot=0/loop_health 例行面带内"
 "（audio-tmp-residue 复绿后零点名·两 outage 09-26/09-28 已裁定不重触发）；"
 "⑥例行件=10-12 日报在案不重跑（R2008 00:03 一份为真相）·W42 周审第 4 期在案（R2008）·GB §④ v1.3 下期 10-15 ≤7d 跳过·tech#92 雷达标定权威窗 10-12 08:00 届日即领不预扫"
 "（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）·meme V1 成片查看位零新到件（R1899 锚维持·装配腿 bm-a 会话域在飞零接触）·MD-0002 T2I gated CEO 点头维持"
 "（剧本/配音/装配 turnkey 全备）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 CPU 工程+探针只读+套件跑零本地模型产出调用·P-54⑤ 计量律）；"
 "⑦队列补货步=真无独立新种子如实注记零膨胀（tech#120=R2012 既有种子兑现·flight 残件入账=tech#114 既有判据收口·禁凑数律）——"
 "下轮=R2015 fire 卡首查（comfy_activity 消费律先行）→fire=flight-3 派发（--wedge-probe 就位：楔死窗 rc6 ≤120s 显式败退=tech#120 判据兑现窗/健康窗判词 ≥9=TTS light 续链 F-180 登记）/"
 "no-fire=等待窗声明；tech#92 08:00 权威窗届日即领。"
)

FOCUS = (
 "R2015 fire 卡首查（comfy_activity 消费律先行）→fire=flight-3 派发（--wedge-probe 就位·"
 "楔死窗 rc6 快败/健康窗判词 ≥9=TTS light 续链 F-180 登记）→tech#92 雷达标定权威窗 "
 "10-12 08:00 届日即领（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）；"
 "meme V1 成片查看位；MD-0002 T2I gated CEO 点头；tech#119 低优先在册"
)

# --- canonical state accounting (tech#76 single writer) ---
cc.finalize_state(LOG, focus=FOCUS)
print("finalize_state done")

# --- export refresh via canonical writer (tech#70/74) ---
EXP = REPO / "docs" / "status-export.json"
cur = json.loads(EXP.read_text(encoding="utf-8"))
live = list(cur.get("live", []))
live[0] = ("F-180 口述史新件剧本评审排队重发：发射器已带防卡死快败保护"
           "（最多 90 秒败退），等 GPU 真窗")
patch = {
    "do": ("F-180 口述史二季首件 S1 评审 flight-1/2 双双超时（ollama 拥塞窗"
           "烧满 25 分钟）；本轮给发射器加楔死快败探针（≤90 秒败退 rc6），"
           "flight-3 排队等下个真窗；10-12 08:00 雷达标定判读到点"),
    "live": live,
}
patch_path = REPO / ".c3-tmp" / "r2014_export_patch.json"
patch_path.write_text(json.dumps(patch, ensure_ascii=False, indent=1),
                      encoding="utf-8")
r = subprocess.run([sys.executable, "src/os/export_refresh.py",
                    "--patch", str(patch_path)],
                   cwd=str(REPO), capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
print(r.stdout.strip()[:300])
if r.returncode != 0:
    print("EXPORT-REFRESH-FAIL rc=%d %s" % (r.returncode, r.stderr[-300:]))
    sys.exit(2)
patch_path.unlink()  # intermediate consumed by the writer

# --- close commit (tech#81 autodetect self-include) ---
rc, lines = cc.run_close_commit(
    files=["src/os/state.json", "docs/status-export.json"],
    message=("R2014 close: tech#120 wedge probe delivered (call_expert "
             "--wedge-probe, flight-3 launcher wired); tech#114 smoke "
             "re-green via residue batch-commit; 1123 suite green; "
             "tick 2014; export refreshed [via bm-a]"))
print("\n".join(lines))
print("CLOSE_RC=%d" % rc)
