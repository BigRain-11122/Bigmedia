# -*- coding: utf-8 -*-
"""R2215 close: tech#155 accounting (both faces delivered).

This close is the first production use of the tech#155 face-2 standing
law: run_close_commit(expect_tick=2215) re-reads the on-disk ledger
after the commit and VERIFY-FAILs loudly if the accounting the round
claims is not what the ledger carries (the R2214 anchor disease).
Every r{N}_close.py from here on passes expect_tick.
"""
import sys

sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os")
import close_commit  # noqa: E402

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

LOG_LINE = u"2026-10-14 04:2x R2215: tech#155 交付轮·双面执法件全落（R2214 断账实锚收口·夜窗 CPU 面实活轮）——①取活=tech#155 P2 队头：①loop_health 新 WARN 面 unaccounted-round-work=git log 扫深 12 消息头锚 R<N> 提取〔他窗无锚 commit 跳过·body 内 R 提及不计·git 失败顾问级静默〕·轮号>tick=每轮号一行 WARN 带 sha 清单+check_unaccounted_round_work 接线 main——判据双过：fixture 锚形态点名〔合成 R2214×3 commit vs tick 2213·纯核+真 git repo check-face 双测〕+真跑零误触〔live repo 探针 silent·尾 commit R2214==tick 2214 健康态〕；②close_commit verify_state_tick/read_disk_state_tick 正身+run_close_commit expect_tick 参〔默认 None=存量调用面零回归·50 存量测全绿〕+VERIFY-FAIL rc3 契约+CLI --expect-tick——判据双过：单测双态锁+全回归绿；192 loop_health+59 close_commit 全绿〔+19 新测〕；本 close 脚本首用 expect_tick=2215=face ② 生产首发（此后 r{N}_close.py 常设传参）；②F-180 接力=前实体 03:56 飞行 04:00 判定 RATE-FAIL 弹回〔seat probe 240s 超时·慢窗·s1_call.py.out 实锚〕→本轮回读后重发 fire_consume=no-fire rc1 card-no-fire gate-static-no-go〔VRAM 04:00 时窗 10673MB free→04:05 卡读 worst-case 828MB=MV 会话释放后 5 分钟内重占〕→F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16+F-184 DIGEST-v20 五件 fire-ready carried（真窗=util/VRAM 门开·fire_window_card 唯一仲裁面）；③main#32 守望=V3 成片未落位〔local release/ 10-08 旧龄+kf-demo 顶=23:57 r977 fix3 已消费·查看位零接触〕；④五查全静=own orders 锚 O-20260908-1105 mtime 10-08 12:08 维持+origin_gap_check QUIET ahead0 behind0+group_scan 六面 fresh 04:03 全静〔DECISIONS truly_new=0 水位 155+LEDGER @BigStream 5 行值守锚零新转办+ORDERS rows=382 tail '10-13 23:5x'==stored+DIGEST-SUPPLY quiet〔v20 卡覆盖 10-14〕+ORDERS-ORIGIN-DELTA delta=0〕+树=MV-lane 预期脏面零锁〔mv0001/mv001 域 MV sprint 会话件·R1745 零接触承继〕；⑤三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕+2 发现 react-v16/digest-v20 unannot=F-183/184 fire 窗登记即清预期态（R2118 裁定维持）/loop_health 3F+299W 皆在案史实（三 outage 窗=pause-让路窗族+drift 21=adjudicated 基线·dense-fold 带内 +1）；⑥例行件=10-14 日报在案不重跑（R2205 补产）·W42 周审在案（R2011）·GB §④ 下期 10-15 ≤7d 跳过+export=实活轮 canonical writer do 行刷新（tech#148 正身）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·T1 催办无超线项（账号物理件=呈现状行不催办）·tokens:local=0（探针/直读/fire 卡/测试=零本地模型产出调用·P-54⑤ 计量律）；⑦队列补货步=真无独立新种子如实注记零膨胀（本轮发现双面=tech#155 自身交付件〔face ② 常设传参约定入 done 标〕+F-180 重发=carried 工作非新种子·禁凑数律）——下轮=F-180 飞行收割/重发（fire 门开即接力 F-180→184）+08:00 tech#92/#126 权威窗读数（zhihu-hot 头部 ≥3 篇 ≥60 判据/否则 T1 60→55 fallback）+晨窗 08:00 回滚序（re-enable MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位）"

FOCUS = u"08:00 tech#92/#126 authority window reads (zhihu >=3 >=60 or T1 60->55 fallback) + F-180 flight re-fire/relay F-181..184 on util/VRAM gate open + morning rollback re-enable MiniGameOllama dual tasks (R2215)"


def main():
    summary = close_commit.finalize_state(LOG_LINE, tick=2215, focus=FOCUS)
    print("FINALIZE tick=%s ts=%s" % (summary["tick"], summary["ts"]))
    rc, lines = close_commit.run_close_commit(
        files=[r"src\os\state.json",
               r"data\pipeline\fire-consume-ledger.jsonl",
               r"data\storylines\audio\sc005-07-v1-tmp\s1_call.py.out"],
        message=("R2215: close - tech#155 accounting (tick 2215, expect_tick "
                 "readback = face-2 first production use); F-180 re-fire "
                 "no-fire receipt (VRAM re-consumed by MV session "
                 "10.6GB->828MB in 5min); flight-2 bail record (seat probe "
                 "240s RATE-FAIL); next=08:00 tech#92/#126 window + fire "
                 "relay [via bm-a]"),
        root=ROOT,
        export_do=("tech#155 guard live (unaccounted-round probe + close "
                   "readback verify); F-180 re-fire no-fire; next=08:00 "
                   "window reads"),
        expect_tick=2215,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
