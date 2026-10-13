# -*- coding: utf-8 -*-
"""R2197 accounting close: consume HQ orders rows 375-377 (CEO full-local order ack)."""
import sys, io
sys.path.insert(0, 'src/os')
sys.path.insert(0, 'src')
from close_commit import finalize_state
from group_scan import current_orders_watermark

log_line = (
    "2026-10-13 21:3x R2197: 收令轮·集团 ORDERS rows 374→377 三新行消费（group_scan fresh 21:33 检出·D-13 SLA 带内）"
    "——row 375（V3 五席帧审回执汇总+导演席签章·白名单 v1.4 落档）+row 376（W1 星晴烧制包+选角案 v1 checkout 恢复判例留痕）"
    "=MV sprint 会话域自执件·查看位验真=FRAME-GATE-WHITELIST-v1.4.md 4894B 21:28:40+星晴-SHOTLIST-v3.md 12210B 21:24:39"
    "+星晴-KF-PACK-A-v1.md 3839B 21:28:22 三件盘上在位新到件确证（新鲜验证律）·本循环零接触承继（R1745）；"
    "row 377=CEO 全本地验证令 O-20261013-2200（原话「你这次全按照本地化的能力去生产…尽量不要去云端了，我主要是要验证本地的能力」"
    "→V3 成片切全本地源·云端例外面今晚关闭·过闸判据=装配前 asm_preflight 云引用计数 0·执行单 @bm-c 修复批+云槽位重产批+@bm-b 备援"
    "+bm-a=MV 会话域监管/装配/调度在役）——本 OS 循环零点名执行份额·查看位零接触维持；"
    "本司产线对照=推理面零云在册（edge-tts/faster-whisper/Ollama/FFmpeg 全本地链）与 10-12 资源总纲「机队为上云端为否」同源"
    "=无操作变化零新立法；ack=本行+commit 含令号+R2197+下一动作（P-51 双载体）；"
    "五查余面静=own orders 锚 O-20260908-1105 维持+origin_gap_check QUIET ahead0 behind0+DECISIONS truly_new=0 水位 154 维持"
    "+LEDGER @BigStream 5 行守锚零新转办+DIGEST-SUPPLY advisory 1 row-date 10-13 age0d 已裁决面维持〔F-182 staged+夜窗 DIGEST-v20〕"
    "+树=MV-lane 预期脏面 14 件零锁；三探针带内=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面"
    "+1 发现 react-v16 unannot=F-183 夜窗登记即清（R2118 裁定维持）/loop_health 3F+290W 皆在案史实；"
    "fire_consume no-fire rc1 workday-hours（CEO 21:33 仍在下令=用机让路面正确侧）→F-180 SC-005-07 flight-4+F-181 REACT-v15"
    "+F-182 DIGEST-v19+F-183 REACT-v16 四件 fire-ready carried·真窗=10-14 00:00 夜窗；"
    "例行件=日报在案不重跑·W42 周审在案·GB §④ 下期 10-15 ≤7d 跳过·export=skip <24h（台账面变化非成品态变化·tech#148 强制律下"
    "skip=零写入安全态·live 三行核读仍准）·HQ-FEEDBACK 不写（三行=MV 会话域自执件非集团层新 open 问题零膨胀）·T1 无超线项"
    "·tokens:local=0（探针/直读/验真=档案读写零本地模型调用·P-54⑤）；队列补货步=真无独立新种子如实注记零膨胀"
    "（CEO 验证令=MV 域执行件其会话承载·本司产线全本地在册无操作面·禁凑数律）·临时件清理钩=.c3-tmp/r2197_groupscan.txt 轮末删净"
    "·tech#103 水位消费 rows=377——下轮=等待态续（等待对象同上不重扫）·10-14 00:00 夜窗开窗即转收口三连"
    "（撤 AIHOT pause 旗+main#21 重启+fire 接力+tech#126 校准冒烟+DIGEST-v20 产线）·tech#92/#126 权威窗 10-14 08:00"
)

ow = current_orders_watermark()
print('orders_watermark to store:', ow)
res = finalize_state(log_line, orders_watermark=ow)
buf = io.StringIO()
for k in sorted(res):
    buf.write('%s=%r\n' % (k, res[k]))
print(buf.getvalue().encode('unicode_escape').decode('ascii'))
