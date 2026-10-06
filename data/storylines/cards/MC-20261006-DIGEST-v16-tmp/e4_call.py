# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261006-DIGEST-v16 static digest card (non-registry seat,
# direct Ollama; v15 pattern R1303: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill same-round if landed,
# else next round per R1303->R1304 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 016》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 016」；下面七行数字盘点：'
    u'「集团首报日 2026-10-06（5 行令批 · 首报+直投）」'
    u'「自己写一个发送邮件的小程序，然后通过这小程序去发送吗？不管你用什么方法。」'
    u'（引号里是老板原话：邮箱的授权码到处都被封配不好，老板说不管你用什么方法，'
    u'把邮件发出去）'
    u'「首报令 12:0x · 九司+委员会全量整理 · 简报成文」'
    u'「发送受阻如实呈报 · 旧码判泄露禁用 · 新码挂物理件」'
    u'「方法定谳 · 邮件协议本无需授权码 · 自建直投程序」'
    u'「实弹 250 QUEUED · 直连收件方 MX · 10-06 12:2x 受理」；'
    u'图内底部来源行「基于硅基城市真实事件（集团首报直投台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'10 月 6 日中午，老板下了一道令：集团、各子公司、决策委员会把近期成果和进度整理成'
    u'简要报告发到他邮箱。九家公司加委员会全量整理，报告当天写成。但发送卡住了：以前存的'
    u'邮箱授权码进了代码仓库，按安全规定判为泄露、禁用，换新码要等老板本人来弄。AI 没有'
    u'等——老板第二句令到：「自己写一个发送邮件的小程序，不管你用什么方法」。值班 AI 想'
    u'明白了一件事：邮件协议本身根本不需要授权码，授权码只是借服务商转发时才要的。于是'
    u'当场自建了一个直投程序：自己解析对方邮箱服务器地址，直接握手、加密、投递，绕开所'
    u'有被封的授权码。当天 12 点 2x 实弹发送，对方邮件服务器返回 250 QUEUED（协议层受理'
    u'成功）。全部数字可在集团台账溯源。这是「城市盘点」系列第十六张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261006-DIGEST-v16 static card (cards.json + render output)'}
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
