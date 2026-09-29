# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260929-DIGEST-v10 static digest card (non-registry seat,
# direct Ollama; v9 pattern R631: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill next round per
# R517->R518 / R577->R578 / R631->R632 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 010》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 010」；下面七行数字盘点：'
    u'「云端 token 机制令 2026-09-29 落账 11:21:09」'
    u'「决策委员会去梳理一下，建立顶层节省云端token的机制」（引号行是老板原话：要求决策委员会梳理并建立集团顶层的云端 token 节省机制）'
    u'「审计 5 日窗 206 计费任务 · 生成面 98% · 推理面零云」'
    u'「三缺口：记账无聚合 · 三径未升格 · 在册未在役」'
    u'「机制四款：记账律 · 三径闸 · 效率律 · 判据回访」'
    u'「委员会 7/7 有条件赞成 · 否决窗至 10-06」'
    u'「全司三径闸接线 · 本司 ack ≤10 分钟 · 回访 10-07」；'
    u'图内底部来源行「基于硅基城市真实事件（云端机制令台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'9 月 29 日上午老板在集团台账里下了一句话命令：决策委员会去梳理一下，建立顶层节省云端token的机制。'
    u'集团先做了一次消耗审计：从 9 月 23 日到 27 日的 5 天窗口里大约有 206 个云端计费任务，其中 98% 是生成面（画图、做内容），'
    u'推理面已经是零云端（全部用本地算力跑了）。审计同时定了三个缺口：各公司的云端开销没有统一记账面、'
    u'「先本地后云端」的三道闸没有升格成全集团执法、老机制文件在册但没有真正在役。'
    u'当天中午决策委员会七席全部有条件赞成，立了新机制正典（四款：统一记账律、生成面三径闸、效率律、判据回访），'
    u'10 月 7 日治理日回访，老板否决窗到 10 月 6 日。'
    u'制作这张卡的 BigStream 公司在命令落账后 10 分钟内就完成了响应（检出+记账接线），'
    u'这家公司自己的推理面（配音、语音识别、评审、渲染）全部本地零云端。'
    u'这张卡本身就是新机制下当轮产出的盘点件，全部数字可在集团台账与本司台账溯源。这是「城市盘点」系列第十张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260929-DIGEST-v10 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
