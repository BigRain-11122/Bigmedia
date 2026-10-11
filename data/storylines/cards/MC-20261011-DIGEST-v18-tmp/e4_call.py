# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261011-DIGEST-v18 static digest card (non-registry seat,
# direct Ollama; v17 pattern R1536: UTF-8 stdin pipe + ANSI strip + braille strip).
# Staged as the fire_consume launcher (tech#112) for the v18 GPU tail (F-179):
# fire_consume.py dispatches THIS file the moment the card says fire.
# Material source: e4-material.md (R1986 preload, 7/7 verbatim machine-checked).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 018》'
    u'（1080×1080 方图·黑底；左上角小字「[AIGC·AI 生成内容]」；顶部大标题「城市盘点 018」）。'
    u'图上写着七行盘点正文：'
    u'「全曲冲刺日（10-11 · 单日 7 令 6 成品）」；'
    u'「mv的评审要分层级，导演是总控，专家是群审，我只是最后决定上线与否的。」——这行是老板原话引文；'
    u'「整改六令剧本四律 · 30 秒线封存转全曲」；'
    u'「导演席硬门 · 每曲独立选角 · 落地四机制」；'
    u'「剧本 v5 重写 · 十席盲评 · 定版门放生产」；'
    u'「盘燃减负三帽生效 · 判据回访窗 10-16」。'
    u'图内底部声明行「基于硅基城市真实事件（全曲冲刺日令批台账档案）」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'「城市盘点」系列是集团旗下媒体公司出品的城市档案盘点图——把集团真实发生的大事，'
    u'用数字盘点的方式做成一张方图档案，所以底部声明行写明「基于硅基城市真实事件」。'
    u'这张卡盘点的是 10 月 11 日的「全曲冲刺日」：老板看了集团音乐公司的 30 秒 MV 预览后说「有点意思了」，'
    u'随即在两小时内连下七道令，把整个集团的音乐 MV 产线推入全曲冲刺——六项整改'
    u'（掉帧插值、瑕疵帧检、调色深研、剪辑词级重核、运镜动作重摇、剧本按「写好/逻辑通顺/自然/立意高」四律重写）；'
    u'30 秒短线就此封存，全员转向完整版；新立「导演席硬门」（没有导演签章的半成品不许送到老板面前）、'
    u'「每曲独立选角」律（十首歌十张脸，不许跨歌复用同一张脸）、执行落地四机制；'
    u'最后定谳评审分层——导演总控、专家群审、老板只决定上线与否。'
    u'同一天，媒体公司自己也全速产出，登记了六件成品。'
    u'请回答三个问题，每题一段，直说不绕弯：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空话套话的地方？有的话扣几分、指出原文？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261011-DIGEST-v18 static card (cards.json + render output + e4-material.md)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding="utf-8").write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
