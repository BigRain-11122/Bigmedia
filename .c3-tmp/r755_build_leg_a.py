# -*- coding: utf-8 -*-
# R755: LC-021 leg A - derive census-card-v3-vertical.mp4 (R511 law: scale 660 + pad y=160 + zoompan <=1.04, 13s)
#        + build cards-v1-matched.json (12/12 source-card-as-evidence, field-level sourcing anchor C-00012)
#        (R745 build_leg_a.py adapted: C-00012 Shen Peilan / F-022 CENSUS-v3 / census 003)
#        + zero-bracket verification (col2 pure verbatim by design, R737/R741 strip-prevention)
#        + pre-audit geometry (R720 law standing face, per-card size fix only on intrusion).
import json, io, os, subprocess, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v3', 'MC-20260925-CENSUS-v3.png')
OUT_MP4 = os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v3-vertical.mp4')
SRC_CARDS = os.path.join(ROOT, '.lc021-tmp', 'cards.json')
DST = os.path.join(ROOT, 'data', 'sources', 'lc021', 'cards-v1-matched.json')

assert os.path.exists(PNG), 'PNG missing: ' + PNG
assert os.path.getsize(PNG) == 225299, 'F-022 PNG size drift: %d' % os.path.getsize(PNG)

# --- step 1: ffprobe v15 reference ---
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, 'data', 'sources', 'footage', 'census-card-v15-vertical.mp4')],
                    capture_output=True)
print('[v15 ref]', pr.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 2: derive v3 vertical ---
fc = ("[0:v]scale=660:660,"
      "zoompan=z='min(1+0.04*on/390,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=390:s=660x660:fps=30,"
      "pad=1080:1920:(ow-iw)/2:160:color=black,format=yuv420p")
cmd = ['ffmpeg', '-y', '-v', 'error', '-i', PNG, '-filter_complex', fc,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-t', '13', '-r', '30', OUT_MP4]
subprocess.run(cmd, check=True)
pr2 = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                      '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                      '-of', 'default=nw=1', OUT_MP4], capture_output=True)
print('[v3 out]', pr2.stdout.decode('utf-8', 'replace').replace('\n', ' | ').strip())

# --- step 3: build matched cards ---
CARD_SRC = 'data/sources/footage/census-card-v3-vertical.mp4'
REQS = [
    u"源画面=钩子位（锚 C-00012 钩子字段 verbatim「全城唯一能靠光带节奏认出每个队员心气的人——谁今天状态不对，她放的音乐都会慢半拍」·hook 三重标注位=系统日志体·系列同型 LC-003~LC-019）。",
    u"源画面=居民档案位（卡题行 C-00012·沈佩兰+物种行 verbatim「碳基市民 · 弄堂派」+性别年龄行「女 · 58 岁」（58→五十八=口播数字读法全拼·「女」由字卡列承载=b1 卡口分工·LC-013~LC-019 b2 同型）。",
    u"源画面=城区职业位（城区行 verbatim「北外滩 · 治理岸 · 脑环广场街区」+职业行展开 verbatim「晨操领队——广场舞的光带版——舞步踏出的是晨光涟漪」=破折号展开段归卡锚列承载·LC-013~LC-019 b3 同型）。",
    u"源画面=带队规矩位（锚 C-00012 行为字段 verbatim「比太阳起得早；光带音响永远只开三分贝（「吵醒上夜班的缺德」）；每逢单日带队绕外环走一段，说是替城「活动筋骨」」·缺德句/单日绕外环段归卡锚列承载·beat 拍·同源多拍注记）。",
    u"源画面=转折位（锚 C-00012 经历转折字段 verbatim「那年广场舞队散伙又重组，她挨家挨户把老姐妹一个个请回来，从此明白了队伍散了人心不能散」+经历现状段 verbatim「队里从七人带到四十三人，年轻教练想接棒，她嘴上不说，心里已经点头」=现状段归卡锚列承载·本件情绪峰=人心不能散·punch 拍·同源多拍注记）。",
    u"源画面=沪语位（锚 C-00012 语言字段 verbatim「上海话底色：「结棍」「灵光」「帮帮忙」；口令简短干脆：「对齐——起步——」；训人从不带脏字，一句「侬说啥物事」比红脉冲还管用」·沪语词段「结棍」「灵光」「帮帮忙」归卡锚列承载〔口播只取口令句+侬说啥物事〕·turn 拍·同源多拍注记）。",
    u"源画面=性格位（锚 C-00012 性格字段 verbatim「攒劲（认准的目标一口一口啃到底）·端水（一碗水端得比谁都平）·唠嗑（三句话聊成老街坊）」·类别词攒劲/端水/唠嗑由卡锚列承载·三词标签族 E4 弱位避让=口播取最生动两面〔啃到底+端水平〕·LC-018/LC-019 b7 同型·wink 拍·同源多拍注记）。",
    u"源画面=玫红与三块糖位（锚 C-00012 服装字段 verbatim「玫红运动服（她挑的降饱和色，说是「亮的让给塔顶白光」），腰间别着光带控制器，包里永远有一卷备用光带和三块糖——低血糖的队员比坏设备常见」·玫红/降饱和/光带控制器/备用光带段归卡锚列承载·三块糖=口播承载位·body 拍·同源多拍注记）。",
    u"源画面=大家都还在位（锚 C-00012 思想字段 verbatim「带队十九年，看明白一件事：晨操跳的不是舞，是「大家都还在」。光带音响一响，老街坊一个个从楼里出来，她在队首回头数人头，一个不落，这一天就算开了张」=本件主轴=「大家都还在」·尾段归卡锚列承载·proof 拍·同源多拍注记）。",
    u"源画面=互证位（锚 C-00012 关系字段 verbatim「家户 H-1003 夫妻带娃（孙女在像素小学，跳房子全弄堂第一）；老对头兼老姐妹=街区调解阿姨（俩人一年吵三回，回回和好）；半个队员都喊她「沈老师」」·家户段/孙女像素小学段归卡锚列承载〔孙女像素小学=LC-008 王多多同校邻域注记·零身份断言·禁虚构〕·proof 拍·同源多拍注记）。",
    u"源画面=信条位（锚 C-00012 信条字段 verbatim「队形不能乱，人心更不能散。」保护行零动·close 拍·同源多拍注记）。",
    u"源画面=载体位（领队全档案载体=M5 公众号图文页·语境层承接位·发布锁=M5 账号物理件·CTA 句式=LC-001~LC-019 先例·分享对象具明「转给起得比太阳早的人」=b3 比太阳起得早+信条队形人心受众侧对位设计·cta 拍）。",
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

# --- step 3a: zero-bracket verification (strip-prevention by design; R737/R741 precedent family) ---
for i, c in enumerate(cards):
    for ln in c['lines']:
        assert u'\u3014' not in ln and u'\u3015' not in ln, 'b%d col2 contains bracket annotation (design violation): %r' % (i, ln)
print('zero-bracket check: 12/12 col2 lines pure verbatim, no strip needed (R743/R751 design)')

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
def block_top(lines, size):
    n = 0
    for x in lines:
        n += len(wrap_for_width(str(x), size, fw).split('\n'))
    return (1920 - n * (size * 1.2 + 14)) / 2.0, n

def split_at(text, seps):
    segs, cur = [], u''
    for ch in text:
        cur += ch
        if ch in seps:
            segs.append(cur)
            cur = u''
    if cur:
        segs.append(cur)
    assert u''.join(segs) == text
    return segs

if problems:
    # R720 law: two-phase minimal intervention, verbatim zero-char (R719/R725/R745 dot-split family)
    for i in problems:
        c = cards[i]
        # phase 1: per-card size ladder on original lines
        for size_try in (56, 54, 52, 50, 48, 46):
            t2, nn = block_top(c['lines'], size_try)
            if t2 >= 787:
                c['size'] = size_try
                print('FIX b%d: per-card size=%d -> %d lines top=%.0f net=%.0f (zero-char)' % (i, size_try, nn, t2, t2 - 767))
                break
        else:
            # phase 2: semantic dot-split (sentence-level first, then comma-level) + ladder extension below 46
            text = u''.join(c['lines'][1:])
            fixed = False
            for label, seps, sizes in (('sentence-split', u'\u3002\uff1b', (56, 54, 52, 50, 48, 46, 42, 38, 36)),
                                       ('comma-split', u'\u3002\uff1b\uff0c', (56, 54, 52, 50, 48, 46, 42, 38, 36))):
                segs = split_at(text, seps)
                for size_try in sizes:
                    cand = [c['lines'][0]] + segs
                    t2, nn = block_top(cand, size_try)
                    if t2 >= 787:
                        c['lines'] = cand
                        c['size'] = size_try
                        print('FIX b%d: %s %d segs + per-card size=%d -> %d lines top=%.0f net=%.0f (zero-char join-verified)'
                              % (i, label, len(segs), size_try, nn, t2, t2 - 767))
                        fixed = True
                        break
                if fixed:
                    break
            if not fixed:
                raise SystemExit('b%d cannot fix by dot-split ladder alone' % i)
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
j['meta']['storyboard'] = (u"LC-021 视觉动态=源卡即证据（LC-001~LC-019 同型）：12 拍共用源卡（CENSUS-v3 沈佩兰锚 C-00012 字段）；"
                          u"画面=静态图纵向派生（F-022 成品卡 660px 居中 y=160+zoompan ≤1.04 微动·AIGC 避让法=R511 前置〔标签位=卡面左上=同位族多模态实证〕）；"
                          u"对位 12/12 逐拍字段级溯源对表（s1-review-material-v1.md 事实溯源对表）；"
                          u"**拆条系列 20 卡全覆盖收官件**（锚池 20 手写展示锚 C-00010~C-00029 全拆位·E21 出池后补池义务=BS-007 稿集件/新锚卡 supply-gated 随选优轮评估）；"
                          u"孙女像素小学=LC-008 王多多同校邻域注记（零身份断言·禁虚构）；b9 互证拍=关系字段三联直引。")
with io.open(DST, 'w', encoding='utf-8') as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print('written ->', DST)
