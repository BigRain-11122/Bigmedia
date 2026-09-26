# -*- coding: utf-8 -*-
# R447 ledger writes (UTF-8 via python; PS5.1 CJK-escape hazard avoided)
import io

RD = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

# ---------- 1) renders README: extend the v15 batch-declaration row + append render row
p = RD + r'\output\renders\README.md'
t = io.open(p, encoding='utf-8').read()

a1 = 'cyber light+human 42 产线默认·BGM-A 纯净]）——同性质非成品'
n1 = ('cyber light+human 42 产线默认·BGM-A 纯净]+**R447 渲染链**：'
      'build_cards_v15.py[对位表构建件=v15 TTS 基线时钟×v12-matched visuals 承继×'
      '卡面 v11 锚·line_diff 三处实证=b3/b4/b7 TTS 中间稿回退锚点]'
      '+probe-r447/[拍头 12+回环边界 12 帧+head/loop 双 tile+全分辨率抽验帧]'
      '）——同性质非成品')
assert t.count(a1) == 1, 'anchor1 count=%d' % t.count(a1)
t = t.replace(a1, n1)

a2 = '+s1-review-material-v15.md 评审材料）；'
n2 = ('+s1-review-material-v15.md 评审材料+**cards-v15-matched.json 对位表**'
      '[R447·v15 时钟 12 拍·visuals 承继 v12-matched·卡面 v11 锚]）；')
assert t.count(a2) == 1, 'anchor2 count=%d' % t.count(a2)
t = t.replace(a2, n2)

row = ('| bs-001-v15-shipinhao-60s.mp4 | **在链·重制候选（#71 重制腿③ F-001 渲染件·'
       'S2 三门全绿·E8/M4/F-001 SUPERSEDED 更账=R448 待走）** | '
       '**R-E shipinhao 12 段 11 柔转场 0 硬切**（9:16 1080×1920·'
       '**58.66s 实测=音频尾门·1.3s 余量**·cards-v15-matched 对位 10/12=0.83 承继 '
       'v12-matched·hits=[0,2,4,7] 同 v14b 原件）·**S5.5 角标常驻位产线首用**'
       '（BigStream | BS-001 EP.01 右上 H3 档灰白 60% 全片常驻·≤60s 短件 §5.5 '
       '二选一律=不用片头帧）+**§4.5 三开关首启用**（--h1-glow 克制档/'
       '--scanlines CRT 氛围 ≤8%/--sys-status 逐 cue sys.beat=NN t=MM:SS 状态行）；'
       'S2 三门 R447 循环独立执法**全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 '
       '0.220-0.558s·pacing CV 0.204·prosody 9 档 12 拍·copy CV 0.216）+层 1.8 '
       '六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 0.83+'
       'transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS'
       '（9:16+58.66s 入 30-60s 窗 1.3s 余量）；**帧验三律**：拍头 12/12 语义全中'
       '（citywatch×4/驾驶舱×3/editgrid/looplog/reviewsdoc/字卡×2）+'
       '**回环边界 12/12 全净**（citywatch b0/b1/b8/b10 拍内 4.066s 穿越点 '
       'pre/x/post·零任务管理器零编辑器零聊天窗=R197 净源链继承·素材内运镜跨回环'
       '连续无毛刺）+全分辨率帧文字完整（角标/状态行/AIGC white@0.9/字幕零截断'
       '零乱码·H1 glow 克制档暗缘读数=R445 判 CEO 目检面）；'
       '**edit_craft 七参接线随件入账**（series 四参+三开关→compose→'
       'build_render_plan·plan.series+s45_dials 证据字段=§5.5 机检判据③·'
       'help 裸 % 坑即修=R445 renderer 同型·291 全回归绿）；plan.json 入 git |\n')
t = t.rstrip('\n') + '\n' + row
io.open(p, 'w', encoding='utf-8').write(t)
print('renders README ok')

# ---------- 2) station-reviews: append S2 enforcement row
p = RD + r'\docs\reviews\station-reviews.md'
t = io.open(p, encoding='utf-8').read()
srow = ('| 2026-09-27 | **S2 三门循环独立执法+帧验三律（bs-001-v15-shipinhao='
        '#71 重制腿③ F-001 渲染件=R447·S5.5 角标常驻位+§4.5 三开关产线首用件）** | '
        'output/renders/bs-001-v15-shipinhao-60s.mp4+.plan.json+'
        '`.bs001-v15-tmp/probe-r447/`（24 帧+双 tile） | '
        '三门读数：ai_feel all-PASS 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·'
        'pacing CV 0.204·prosody 9 档 12 拍·copy CV 0.216）+层 1.8 六面 PASS'
        '（beat-align 11/11+camera 12 段全动+visual-ratio 0.83〔10/12〕+'
        'transition-share 1.00+variety 无连排+timeline 代数过）+spec 微信视频号'
        '双 PASS（9:16+58.66s∈30-60s 窗 1.3s 余量）——**R-E 链系列件/赛博层接线'
        '执法面**（edit_craft 七参贯通·plan.series+s45_dials 证据字段=§5.5 机检'
        '判据③·291 全回归绿）；帧验三律=拍头 12/12 语义全中（badge+sys.beat '
        '状态行+AIGC+扫描线全帧在位）+回环边界 12/12 全净（citywatch 4.066s '
        '穿越点·零桌面穿帮·运镜连续）+全分辨率三帧文字完整（角标逐字/'
        'sys-status 逐字/AIGC/字幕）；H1 glow 克制档暗缘读数=R445 已判 CEO 目检面'
        '如实注记；未测面如实列=ASR 终轨回听〔E8 S2 席〕+E8 终审+M4+F-001 '
        'SUPERSEDED 更账=R448 续走·受众反应面=未上线未测量 |\n')
t = t.rstrip('\n') + '\n' + srow
io.open(p, 'w', encoding='utf-8').write(t)
print('station-reviews ok')

# ---------- 3) backlog: append R447 progress note after the R446 note
p = RD + r'\src\os\backlog.md'
t = io.open(p, encoding='utf-8').read()
a3 = 'F-002~F-004 逐件随轮继]**'
n3 = ('F-002~F-004 逐件随轮继]**\n'
      '   **[R447 进展 2026-09-27：F-001 渲染腿毕（claim 沿用·#71 循环名下）——'
      '①edit_craft.py 七参接线=R-E 链系列件+赛博层贯通（--series-badge/'
      '--series-id/--series-intro/--intro-s/--h1-glow/--scanlines/--sys-status→'
      'compose→build_render_plan·plan.series+s45_dials 证据字段入 plan.json='
      '§5.5 机检判据③·--series-intro 无 id=FAIL 有牙镜像 renderer·help 裸 % 坑'
      '即修=R445 renderer 同型·291 全回归绿）；②对位表=cards-v15-matched.json'
      '（v15 TTS 基线时钟×v12-matched visuals 承继×卡面 v11 锚——build_cards_v15.py '
      'line_diff 三处实证=b3/b4/b7 TTS 中间稿回退锚点）；③R-E 渲染 '
      'bs-001-v15-shipinhao-60s.mp4=角标常驻位（BigStream | BS-001 EP.01）+§4.5 '
      '三开关首启用（≤60s 短件二选一律=不用片头帧）·9:16 1080×1920·58.66s 实测'
      '（音频尾门）1.3s 余量·hits=[0,2,4,7] 同 v14b 原件；④S2 三门循环独立执法'
      '全绿=ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·CV 0.204/0.216·'
      'prosody 9 档）+层 1.8 六面 PASS（beat-align 11/11+visual-ratio 0.83+'
      'share 1.00+代数过）+spec 微信视频号双 PASS；⑤帧验三律全过=拍头 12/12 '
      '语义全中+回环边界 12/12 全净（citywatch 4.066s 穿越点 pre/x/post·R197 '
      '净源链继承）+全分辨率文字完整（角标/sys.beat 状态行/AIGC/字幕零截断·'
      'H1 glow 克制档暗缘读数=R445 判 CEO 目检面）——**余腿=R448 E8 终审'
      '（S2 席 ASR 终轨回听+七席）→M4→finished 更账 F-001 SUPERSEDED 处置→'
      '呈 CEO 目检；F-002~F-004 逐件随轮继]**')
assert t.count(a3) == 1, 'anchor3 count=%d' % t.count(a3)
t = t.replace(a3, n3)
io.open(p, 'w', encoding='utf-8').write(t)
print('backlog ok')
