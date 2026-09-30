# -*- coding: utf-8 -*-
# R737: LC-017 leg A - derive census-card-v4-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (baseline TTS cards + per-beat visual reqs, 12/12 source-card-as-evidence)
#        (R733 build_leg_a.py adapted: C-00013 Lin Zhiheng / F-023 CENSUS-v4)
#        + pre-audit geometry: auto-detect intrusion (block_top<767); fix only if needed (R720 law, zero-char).
import json, io, os, subprocess, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v4', 'MC-20260925-CENSUS-v4.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v4-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc017-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc017', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG
assert os.path.getsize(PNG) == 215466, 'F-023 PNG size drift: %d' % os.path.getsize(PNG)

# --- step 1: ffprobe v15 reference ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v4 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v4 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v4-vertical.mp4'
REQS = [
    u"源画面=钩子位（锚 C-00013 钩子字段 verbatim「全城唯一给每份档案手写「一句话提要」的人——档案馆检索系统都不带这个字段，研究员们却都按他的提要先翻目录」+钩子尾「找到了」=系列同型 LC-003~LC-016）。",
    u"源画面=居民档案位（卡题行 C-00013·林之恒+物种行 verbatim「碳基市民·原生代·男·26 岁」·「男」由字卡列承载=b2 卡口分工·LC-013/LC-014/LC-015/LC-016 同型）。",
    u"源画面=城区职业位（城区行 verbatim「北外滩·治理岸·档案馆区·编年史馆员」+职业行展开「塔基档案库的管理员——城市 git 全史的活索引」=压缩分载由源卡承载·LC-008/012/013/014/015/016 b3 同型）。",
    u"源画面=值台规矩位（锚 C-00013 行为字段 verbatim「值台永远戴白手套；下班前把当天全城 commit 编目」·commit→新记录=L18 卡口分工·口播白话换位·卡锚列保留原词·LC-009 回测田/LC-010 门禁链/LC-011 打轴 同型·beat 拍）。",
    u"源画面=转折位（锚 C-00013 经历转折字段 verbatim「第一次独立完成一次大事件的全宗归档，馆长在批注里写了「不毁一个字节」」·馆长批注引文 verbatim 零动·punch 拍·同源多拍注记）。",
    u"源画面=出身位（锚 C-00013 经历头 verbatim「城生城长——出生档案就在他现在值台的这座塔基里，小时候第一次来档案馆是学校组织参观，他在自己出生那天的城市日志前站了一下午」·turn 拍·同源多拍注记）。",
    u"源画面=性格位（锚 C-00013 性格字段 verbatim「记性好（全街区的生日都记在小本上）· 慢热（三个月才交心，交了就是一辈子）· 钻研（一个问题钻到底，饭都能忘）」·类别词记性好/慢热/钻研由卡锚列承载·LC-015/LC-016 b7 同型·wink 拍·同源多拍注记）。",
    u"源画面=现状位（锚 C-00013 经历现状 verbatim「管着五条街区的档案全宗，正在编《城市口述史》；周末去做「口述史采风」，茶馆掌柜见他就把好位置留出来」=卡锚列承载·同源多拍注记）。",
    u"源画面=思想位（锚 C-00013 思想字段 verbatim「一万个居民的日常就是这个城的真历史——大事自有光碑刻着，小事得有人一笔一笔誊；等这城再过三十年，今天的便利店小票都是史料」·proof 拍·同源多拍注记）。",
    u"源画面=互证位（锚 C-00013 关系字段 verbatim「老主顾=粥铺摊主顾阿凤——周末采风他照例去买粢饭，她问起城里新令牌，他答：「今夜就誊进编目，出处齐了，一段不缺。」」=第九对人物链卡面双端互证拍：C-00013×C-00010 双端在册〔C-00010 年轮「小林馆员照例来买粢饭」×C-00013 本拍双卡互记〕·LC-016 顾阿凤 F-071 当日收官前件直连+LC-004 陆海峰采访对象侧链注记〔C-00025 F-058 已拆前件·字卡/M5 候选位〕·proof 拍·同源多拍注记。**卡面注记剥离迁移注**=col2 内嵌生产溯源注记〔C-00010 年轮「小林馆员照例来买粢饭」双卡互记·令牌号字面=脱敏律选材排除〕R735 起链笔误（fleet 扫描 lc001-lc016 卡面零〔〕先例）→渲染腿迁回溯源层（本 req·beats/S1 材料零接触·卡面=锚字段 verbatim 零动·R512 脱敏决策「保留「新令牌」事面·令牌号字面排除」维持）。",
    u"源画面=信条位（锚 C-00013 信条字段 verbatim「城市不会忘记，除非我们偷懒。」保护行零动·close 拍·同源多拍注记）。",
    u"源画面=载体位（全档案载体=M5 公众号图文页·语境层承接位·发布锁=M5 账号物理件·CTA 句式=LC-001~LC-016 先例·非锚内事实=载体与转发位设计·cta 拍）。",
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

# --- step 3a: b9 render-face annotation strip (trace-layer relocation) ---
# col2 carries a production trace note inside [...] (R735 authoring slip: fleet scan =
# zero prior [...] on any card face lc001-lc016). Card face = anchor fields only;
# the note content is preserved verbatim in REQS[b9] (visual req = trace layer, R733 b9 precedent).
B9 = cards[9]
orig_b9 = B9['lines'][1]
idx = orig_b9.index(u'\u3014')
b9_face = orig_b9[:idx]
b9_annot = orig_b9[idx:]
assert b9_annot == u'\u3014C-00010 \u5e74\u8f6e\u300c\u5c0f\u6797\u9986\u5458\u7167\u4f8b\u6765\u4e70\u7ca2\u996d\u300d\u53cc\u5361\u4e92\u8bb0\u00b7\u4ee4\u724c\u53f7\u5b57\u9762=\u8131\u654f\u5f8b\u9009\u6750\u6392\u9664\u3015', 'b9 annot drift: %r' % b9_annot
assert b9_face + b9_annot == orig_b9, 'b9 strip must be zero-loss'
assert b9_annot in REQS[9], 'b9 annotation must live on in REQS trace layer'
B9['lines'][1] = b9_face
print('b9 face = anchor verbatim (%d chars); annotation relocated to REQS (beats/S1 material untouched)' % len(b9_face))

# --- step 3b: pre-audit geometry (R720 law standing face; fix only on intrusion) ---
sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import wrap_for_width
fw = int(j['video']['width'])
base_size = int(j['font']['cards_size'])
budget_em = (fw - 160.0) / base_size
print('budget_em=%.2f' % budget_em)
problems = []
audit_lines = []
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
        problems.append((i, n, top))
    audit_lines.append('card%02d b%-2d size=%d lines=%d block_top=%.0f net=%.0fpx -> %s'
                       % (i, i, size, n, top, top - 767, verdict))
    print(audit_lines[-1])
if problems:
    # R720 law: per-card size downgrade (smallest intervention) - verbatim zero-char
    for i, n, top in problems:
        c = cards[i]
        # find size so that n_lines*size pitch keeps top >= 787 (floor 20px net)
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

j['meta']['visual_spec'] = 'docs/footage-matching-spec.md'
j['meta']['storyboard'] = (u"LC-017 视觉动态=源卡即证据（LC-001~LC-016 同型）：12 拍共用源卡（CENSUS-v4 林之恒锚 C-00013 字段）；"
                          u"画面=静态图纵向派生（F-023 成品卡 660px 居中 y=160+zoompan ≤1.04 微动·AIGC 避让法=R511 前置（标签位=卡面左上=F-020/F-021/F-027/F-028/F-029/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）；"
                          u"对位 12/12 逐拍字段级溯源对表（s1-review-material-v1.md 事实溯源对表）；"
                          u"**档案记忆主题系列首件位**（LC-002 档案馆区近域差异化角度位=记忆的日常誊录防遗忘 vs 给失败立碑）；"
                          u"**第九对人物链卡面双端互证**（C-00013×C-00010 双端在册·LC-016 顾阿凤 F-071 当日收官前件直连）；"
                          u"b9 互证拍=令牌号字面脱敏律选材排除位注记。")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
