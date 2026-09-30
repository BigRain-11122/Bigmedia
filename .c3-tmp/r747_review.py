# -*- coding: utf-8 -*-
# R747 finalize review doc: draft -> docs/reviews/review-20260930-lc019-v1.md
import io, json

A = json.load(io.open('.c3-tmp/r747_asr.json', encoding='utf-8'))
d = io.open('.c3-tmp/r747_review_draft.md', encoding='utf-8').read()

s2_row = ('ASR 事实词核验（R169 QC recipe 参数位 medium-int8+beam5+noctx·vad_filter=False 补覆盖·HF_HUB_OFFLINE=1·满载机面=他工作区 2dlive-spike 图像生成作业占核·'
          '脱壳轮间落地·asr-check-novad.srt+asr-diff-r746.txt）：' + A['pct'] + ' 字位=' + A['band'] + '〔' + A['fin_full'] + '·字幕轨=edge-tts 直出 12/12 零损兜底〕')
note_row = ('【ASR-注记行：novad 补覆盖=tool-layer finding 首档〔whisper_to_srt.py 硬编码 vad_filter=True 非 R169 recipe 文本·本件 b7-b10 稳定掉段=R711 型复发第二证·'
            'novad 通道=补读非降级（参数位 medium-int8+beam5+noctx 全同）·工具面修复候选=--no-vad CLI 选项位提案随行〕；'
            + A['note_extra'] + '；发布轨字幕=edge-tts 直出 12/12 零损】')
var_row = ('/S2 9.0（R747 ASR 终轨·novad 全覆盖补读 ' + A['pct'] + ' 字位=' + A['band'] + '·tool-layer finding 首档〔VAD 硬编码非 recipe 文本·R711 型复发第二证〕·'
           '字幕轨 edge-tts 12/12 零损兜底）')

d = d.replace('【ASR-量化行：sites/diff/ref 字位=系列带位读数·关键存活清单·实质退化清单·字幕轨=edge-tts 直出 12/12 零损兜底】', s2_row)
d = d.replace('【ASR-注记行：novad 补覆盖=tool-layer finding 首档〔whisper_to_srt.py 硬编码 vad_filter=True 非R169 recipe 文本·本件 b7-b10 稳定掉段=R711 型复发第二证·novad 通道=补读非降级（参数位 medium-int8+beam5+noctx 全同）·工具面修复候选=--no-vad CLI 选项位提案随行〕；关键正面+实质退化清单全档；发布轨字幕=edge-tts 直出 12/12 零损】', note_row)
d = d.replace('【novad 补覆盖读数】', 'novad 补覆盖 ' + A['pct'] + ' 字位=' + A['band'])
d = d.replace('【ASR-注记行', note_row if '【ASR-注记行' in d else '')  # safety no-op
assert '【' not in d, 'unfilled placeholder remains: ' + [l for l in d.splitlines() if '【' in l][0][:200]
io.open('docs/reviews/review-20260930-lc019-v1.md', 'w', encoding='utf-8').write(d)
print('REVIEW_OK')
