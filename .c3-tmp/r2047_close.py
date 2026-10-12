# -*- coding: utf-8 -*-
# R2047 close: CEO yield-order O-20261012-1115 lane enforcement accounting. Explicit-file commit; MV session domain untouched.
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'src', 'os'))

import close_commit
import export_refresh
import group_scan

LOG = u"2026-10-12 11:3x R2047: 收令轮·O-20261012-1115 CEO 用机让路令+机队满负荷令本司份额执法（集团 orders 271→275 四新行=O-1015 反韩化重制/O-1050 剧本 v5 穿越/O-1102 拍摄语法深研 三 MV 域令【MV sprint 会话域在案·查看位零接触维持 R1745 承继】+O-1115 让路令）——①让路执法毕：pause 指纹 7/8 在役（他窗 pause 实跑回执 VRAM 曾清 1615MB）vs 本司 AIHOT 磨链残留实锚（R2046 requeue 池在磨→14b-8k 重载驻留 10.4GB=CEO 让路面被本司面撤销中）→身份实证先行（aihot_procs complete=tech#125 判据）→worker 60380 停磨（missing-worker rc1·proxy/api 留守轻足印）+ollama stop 14b-8k 卸载（VRAM 11764→1707MB=CEO 面恢复·GPU 生产者归因=全 CEO GUI 群零本司进程）；②fire 消费序律照走=fire_consume 单命令直发 no-fire rc1（reason=mv-active）F-180 flight-4+F-181 结转维持（pause 窗 GPU 队零自排·tech#121 序律执行）；③aihot-stack WARN（web TimeoutError）复验=瞬态非第五案（CEO 用机负载下 web/api HTTP 双 200+三角色 aihot_procs 全证）·tech#92 判据窗 10-13 08:00 受让路面影响=resume 早于 08:00 照读〔积累缩短 caveat〕/晚于=顺延注记（backlog #112 R2047 行）；④bookkeeping=tech#127 两步制 claim（AIHOT 栈自愈守卫·案族密度当窗实证=R2046 第四案 1.6h 盲窗+本日瞬态超时双案·交付=下轮 CPU 面）+main#21 worker 复役位入队（resume 执法行）+backlog #111 三令知悉行+探针误名 r2040→r2047 改名收口（round-debris 自因自清 R2045 同型）；⑤三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面/loop_health 3F（2 在案史实 outage+1=R2046 断轮 57min beat gap 本轮史实化）+271 WARN 折叠面（dense_fold）——收账显式列文件 commit+push。"

ow = group_scan.current_orders_watermark()
summary = close_commit.finalize_state(log_line=LOG, orders_watermark=ow)
print('finalize-tick', summary['tick'], 'orders_wm', summary.get('orders_wm_rows'),
      'tail', summary.get('orders_wm_tail'), 'log_len', summary['log_len'])

PATCH = {
    u"do": u"CEO 要用机：本司已把机上的算力活全停（雷达评分停磨、显存腾回），转入轻量值守；他机照常满负荷",
    u"live": [
        u"当前活：算力让给 CEO 用机中，本司轻量值守+准备自愈守卫件",
        u"最近实物：让路执法完成，显存从 11.7G 腾回 1.7G，雷达评分停磨，10-12 中午",
        u"下个里程碑：CEO 用机窗结束后恢复雷达评分并出重判读数，10-13 早 8 点（窗延长则顺延）",
    ],
}
export_refresh.refresh_export(os.path.join(ROOT, 'docs', 'status-export.json'), patch=PATCH)
print('export-refresh-ok')

FILES = [
    'src/os/state.json',
    'src/os/backlog.md',
    'docs/status-export.json',
    'state/queue/tech.md',
    'state/queue/main.md',
    '.c3-tmp/r2047_fastcheck.py',
    '.c3-tmp/r2047_bookkeep.py',
]
MSG = ('R2047: CEO yield-order O-20261012-1115 lane enforcement - AIHOT worker grind stopped '
       '(missing-worker, identity-proven first) + 14b-8k unloaded (VRAM 11764->1707MB CEO face '
       'restored); 3 MV-domain orders acked view-only (MV session owns); fire_consume no-fire '
       '(mv-active) F-180/F-181 carried; tech#127 claimed (AIHOT autoheal watchdog, deliver next '
       'round); worker resume row queued; next: watchdog delivery + resume-side worker restart '
       '(R2047, O-20261012-1115) [via bm-a]')
out = close_commit.run_close_commit(FILES, MSG, root=ROOT)
print('close-out', str(out)[:240].encode('ascii', 'replace'))
