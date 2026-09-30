# -*- coding: utf-8 -*-
# R741: LC-018 leg A - derive census-card-v6-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (12/12 source-card-as-evidence, field-level sourcing anchor C-00015)
#        (R737 build_leg_a.py adapted: C-00015 Chen Yawen / F-025 CENSUS-v6 / census 006)
#        + b9 annotation strip (trace-layer relocation, R737 b9 precedent) + pre-audit geometry (R720 law, zero-char).
import json, io, os, subprocess, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v6', 'MC-20260925-CENSUS-v6.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v6-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc018-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc018', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG
assert os.path.getsize(PNG) == 188550, 'F-025 PNG size drift: %d' % os.path.getsize(PNG)

# --- step 1: ffprobe v15 reference ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v6 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v6 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v6-vertical.mp4'
REQS = [
    u"源画面=钩子位（锚 C-00015 钩子字段 verbatim「全城唯一在拦截日志里给每单写「一句话理由」的风控官——被拦的人从没有不服的，说看完那句话像上了堂课」+钩子尾「找到了」=系列同型 LC-003~LC-017）。",
    u"源画面=居民档案位（卡题行 C-00015·陈雅雯+物种行 verbatim「碳基市民·通勤族 ｜ 女 · 42 岁」·「女」由字卡列承载=b2 卡口分工·LC-013/LC-014/LC-015/LC-016/LC-017 同型）。",
    u"源画面=城区职业位（城区行 verbatim「QUANT 城 · 风控高地」+职业行展开「风控官——风控高地的瞭望员——全城最擅长说『不』的岗位，也是最受尊敬的」=压缩分载由源卡承载·LC-008/012/013/014/015/016/017 b3 同型）。",
    u"源画面=到岗规矩位（锚 C-00015 行为字段 verbatim「红灯亮起时永远第一个到岗，绿灯常亮时反而睡不着」·beat 拍·同源多拍注记）。",
    u"源画面=转折位（锚 C-00015 经历转折字段 verbatim「那年在风控高地拦下自己师父的一单，挨了骂，第二天师父提着酒来道歉，从此她认准了「规矩面前无师徒」」·punch 拍·同源多拍注记）。",
    u"源画面=口头禅位（锚 C-00015 语言字段 verbatim「普通话干脆利落：「过」「不过」「理由三条」；从不说「应该没问题」——只有「实测没问题」」·行话「限额」「熔断」「不碰红线」不入口播由卡锚列承载=量化近域三零断言收口〔零策略推荐/零收益承诺/零投资建议·R739 选优门注记〕·turn 拍·同源多拍注记）。",
    u"源画面=性格位（锚 C-00015 性格字段 verbatim「把关（过不过就看这一眼，从不含糊）· 稳（天塌下来先把手里这步做完）· 防微杜渐（听见第一声异响就开始排查）」·类别词把关/稳/防微杜渐由卡锚列承载·LC-015/LC-016/LC-017 b7 同型·wink 拍·同源多拍注记）。",
    u"源画面=徽章与徒弟位（锚 C-00015 服装字段徽章句 verbatim「胸前别着一枚哑光徽章——是女儿画的红绿灯，她给做成了金属的」+经历现状字段 verbatim「带徒弟了，第一课永远是「先学会说不过」」=双字段同拍分载·body 拍·同源多拍注记）。",
    u"源画面=没发生的功劳位（锚 C-00015 思想字段 verbatim「她说这行最大的奖赏没人看得见：没发生的事，就是她全部的功劳。红脉冲亮起来的时候，她心里反而最平静」·现实银行双栖面=脱敏律选材排除〔R296 登记在案口径维持〕·proof 拍·同源多拍注记）。",
    u"源画面=互证位（C-00014 关系字段点名 verbatim「风控官陈雅雯是他最怕又最服的人」〔R739 选优门②注记〕+C-00015 年轮 2026-09-30 相遇句 verbatim「与 C-00014 相遇：陈雅雯：风控中心刚过，天气正好适合分析。」=第十对人物链卡面双端互证拍：C-00015×C-00014 双端在册+REACT-v6 F-067 信条收束前件直连〔R716 两日前成品件〕·proof 拍·同源多拍注记。**卡面注记剥离迁移注**=col2 内嵌生产溯源注记〔C-00014 关系字段+职业行双端互记·C-00015/C-00014 年轮 2026-09-30 相遇句双端在册〕R739 起链笔误（fleet 扫描 lc001-lc017 卡面零〔〕先例）→渲染腿迁回溯源层（本 req·beats/S1 材料零接触·卡面=锚字段 verbatim 零动）。",
    u"源画面=信条位（锚 C-00015 信条字段 verbatim「红灯是为所有人亮的，包括我。」保护行零动·close 拍·同源多拍注记）。",
    u"源画面=载体位（全档案载体=M5 公众号图文页·语境层承接位·发布锁=M5 账号物理件·CTA 句式=LC-001~LC-017 先例·非锚内事实=载体与转发位设计·cta 拍）。",
]

with io.open(SRC_CARDS, encoding='utf-8') as fh:
    j = json.load(fh)
cards = j['cards']
assert len(cards) == 12, 'expect 12 beats, got %d' % len(cards)
durs = []
for i, c in enumerate(cards):
    durs.append((i, round(c['end'] - c['start'], 2)))
    c['visual'] = {'source': CARD_SRC, 'req': REQS[i]}
print('beat_durations', durs)
print('max_dur', max(d for _, d in durs))

# --- step 3a: b9 annotation strip (trace-layer relocation, R737 b9 precedent) ---
B9 = cards[9]
assert len(B9['lines']) == 3, 'b9 expected 3 lines (face + annotation split), got %d' % len(B9['lines'])
l1, l2 = B9['lines'][1], B9['lines'][2]
idx = l1.index(u'\u3014')  # 〔
b9_face = l1[:idx]
annot_part1 = l1[idx:]
assert annot_part1 == u'\u3014C-00014 \u5173\u7cfb\u5b57\u6bb5+\u804c\u4e1a\u884c\u53cc\u7aef\u4e92\u8bb0\u00b7C-00015', 'b9 annot p1 drift: %r' % annot_part1
assert l2 == u'C-00014 \u5e74\u8f6e 2026-09-30 \u76f8\u9047\u53e5\u53cc\u7aef\u5728\u518c\u3015', 'b9 annot p2 drift: %r' % l2
b9_annot_full = annot_part1 + '/' + l2  # '/' lost at the TTS cards split point - restored (zero-loss)
assert b9_face + b9_annot_full == l1 + '/' + l2, 'b9 strip must be zero-loss'
assert b9_annot_full in REQS[9], 'b9 annotation must live on in REQS trace layer'
B9['lines'][1] = b9_face
del B9['lines'][2]
print('b9 face = anchor verbatim (%d chars); annotation relocated to REQS (beats/S1 material untouched)' % len(b9_face))

# --- step 3b: pre-audit geometry (R720 law standing face; fix only on intrusion) ---
sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import wrap_for_width
fw = int(j['video']['width'])
base_size = int(j['font']['cards_size'])
budget_em = (fw - 160.0) / base_size
print('budget_em=%.2f' % budget_em)
problems = []
for i, c in enumerate(cards):
    size = int(c.get('size', base_size))
    n = 0
    for x in c['lines']:
        n += len(wrap_for_width(str(x), size, fw).split('\n'))
    pitch = size * 1.2 + 14
    text_h = n * pitch
    top = (1920 - text_h) / 2.0
    verdict = 'INTRUDES' if top < 767 else ('thin' if top < 787 else 'clean')
    if top < 767:
        problems.append(i)
    print('card%02d b%-2d size=%d lines=%d block_top=%.0f net=%.0fpx -> %s'
          % (i, i, size, n, top, top - 767, verdict))
if problems:
    # R720 law: per-card size downgrade (smallest intervention) - verbatim zero-char
    for i in problems:
        c = cards[i]
        for size_try in (56, 54, 52, 50, 48, 46):
            nn = 0
            for x in c['lines']:
                nn += len(wrap_for_width(str(x), size_try, fw).split('\n'))
            pitch = size_try * 1.2 + 14
            t2 = (1920 - nn * pitch) / 2.0
            if t2 >= 787:
                c['size'] = size_try
                print('FIX b%d: per-card size=%d -> %d lines top=%.0f net=%.0f (zero-char)' % (i, size_try, nn, t2, t2 - 767))
                break
        else:
            raise SystemExit('b%d cannot fix by size alone - needs dot-split' % i)
else:
    print('pre-audit: NO intrusion - no fix needed (R720 pre-emptive law not triggered)')

# --- final audit re-run (must be problems=NONE) ---
final_problems = []
for i, c in enumerate(cards):
    size = int(c.get('size', base_size))
    n = 0
    for x in c['lines']:
        n += len(wrap_for_width(str(x), size, fw).split('\n'))
    top = (1920 - n * (size * 1.2 + 14)) / 2.0
    if top < 767:
        final_problems.append((i, n, top))
print('FINAL_AUDIT problems=%s' % (final_problems if final_problems else 'NONE'))
assert not final_problems, 'post-fix audit still has intrusions'

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-018 视觉动态=源卡即证据（LC-001~LC-017 同型）：12 拍共用源卡（CENSUS-v6 陈雅雯锚 C-00015 字段）；"
                          u"画面=静态图纵向派生（F-025 成品卡 660px 居中 y=160+zoompan ≤1.04 微动·AIGC 避让法=R511 前置（标签位=卡面左上=F-020/F-021/F-023/F-027/F-028/F-029/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12 逐拍字段级溯源对表（s1-review-material-v1.md 事实溯源对表）；"
                          u"**规则治理主题系列首件位**（量化近域三零断言收口=零策略推荐/零收益承诺/零投资建议·熔断/限额/不碰红线行话不入口播由卡锚列承载·M5 简介层合规位预留〔R739 选优门注记·BS-004 三落先例〕）；"
                          u"**第十对人物链卡面双端互证**（C-00015×C-00014 双端在册·REACT-v6 F-067 信条收束前件直连〔R716〕+LC-017 F-072 当日收官前件直连第二位）；"
                          u"b9 互证拍=年轮相遇句双端在册位注记。")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
