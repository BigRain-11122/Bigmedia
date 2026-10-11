# -*- coding: utf-8 -*-
import io
srt = io.open('data/storylines/audio/sc005-03-v1-tmp/asr-check.srt', encoding='utf-8-sig').read()
srt_n = srt.replace('\n', '')
checks = {
    '信条句-字幕慢半帧': '字幕慢半帧',
    '信条句-对说话人的辜负': '对说话人的辜负',
    'C-00024': 'C-00024',
    'H-1014': 'H-1014',
    'H 独居数字族': '1014',
    '合理推演': '合理推演',
    '缪一': '缪一',
    '谬一(同音变体)': '谬一',
    '复制了两份': '复制了两份',
    '复制了两份-变体': '复制了2份',
    '成长没有并行捷径': '成长没有并行捷径',
    '并行捷径(短串)': '并行捷径',
    '有人味': '有人味',
    '裱在': '裱在',
    '工欲善其事': '工欲善其事',
    '工欲善(短串)': '工欲善',
    '发版': '发版',
    '像素小学': '像素小学',
    '像素(短串)': '像素',
    '霸得蛮': '霸得蛮',
    '字幕君': '字幕君',
    '字幕慢(短串)': '字幕慢',
    '慢半帧(短串)': '慢半帧',
}
res = []
for k, needle in checks.items():
    res.append((k, needle in srt_n, needle))
out = io.open('.c3-tmp/r1965_asr_survival.txt', 'w', encoding='utf-8')
for k, ok, needle in res:
    out.write(('OK  ' if ok else 'XX  ') + k + ' | ' + needle + '\n')
    print(('OK ' if ok else 'XX ') + k)
out.write('cues=' + str(srt.count(' --> ')) + '\n')
out.close()
