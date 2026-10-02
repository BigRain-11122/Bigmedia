# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261002-DAILY-v1 static daily-sign card (non-registry
# seat, direct Ollama qwen2.5:14b; v13 pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (detached, 1500s window; backfill same-round if landed, else next
# round per R517->R518 / R870->R871 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 001》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 001」；日期行「2026-10-02 · 国庆假期」；'
    u'中间引文两行「直播间的观众都说，我家的灯笼最独特。」；署名行「——硅基城市台词池 · 求新轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。这句引文是国庆假期里一位做灯笼的师傅在直播间说的城市台词'
    u'（台词池池级署名·无具体姓名）。今天是国庆假期第二天。'
    u'这是「城市日签」系列第一张（与「城市语录」「城市图鉴」「城市盘点」「城市速报」平行的新系列）。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-DAILY-v1 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[⠀-⣿]', '', cleaned)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
