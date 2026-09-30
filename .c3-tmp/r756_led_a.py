# -*- coding: utf-8 -*-
# R756 ledger leg A: append E4-audience row to expert-calls.md (E4 landed 15:16:27, same-window with ASR in flight)
import io
ROW = ("| 2026-09-30 15:16 | E4-audience | E4 直觉观众（参考仪·非拦截席） | "
       r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc021-tmp\subs.srt"
       " | 1 | full text=expert-verdicts/20260930-151627-E4-audience.md / **8.0 三意愿两明一条件**"
       "（会看完明说+「如果内容真实且故事感人，我可能会点赞并转发给朋友」可能式·「温暖和人情味」「创意和叙述方式新颖」正面定性"
       "=拆条带 8.0×12 回稳位·旗①=hook「全城唯一能靠光带节奏认出队员心气的人」+wink「一口一口啃到底，一碗水端得比谁都平」"
       "被旗夸张缺场景扣 1-2=MC-003 语境门槛族 hook/wink 位变体〔皆锚 C-00012 verbatim 卡锚不可改写·吸收位=M5 图文页语境+系列语境〕"
       "·最弱=故事现实性落地性〔60s 固有+信条句语境门槛同族=M6 校准位〕） | e4_call.py 脱壳与 ASR 并飞同窗（LC-021 收官腿 R756） |")
p = r"docs/reviews/expert-calls.md"
old = io.open(p, encoding='utf-8').read()
if '20260930-151627' in old:
    print('ALREADY-PRESENT')
else:
    io.open(p, 'a', encoding='utf-8').write('\n' + ROW + '\n')
    print('APPENDED')
