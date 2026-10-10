# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261010-DIGEST-v17 static digest card (non-registry seat,
# direct Ollama; v16 pattern R1536: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill same-round if landed,
# else next round per R1303->R1304 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 017》'
    u'（1080×1080 方图·黑底；左上角小字「[AIGC·AI 生成内容]」；顶部大标题「城市盘点 017」；'
    u'下面七行数字盘点：'
    u'「审查执法双日（10-08/09 · 令批 34 单）」'
    u'「每个子公司给我逐个审查审计，」「然后强力改善」'
    u'（引号里是老板原话：连着两天下了 34 道指令，要求把每个子公司挨个审查一遍，'
    u'查完必须强力改善）'
    u'「审查三案同窗 7/7 · 直审+逐审+工作区基线」'
    u'「自驱执法令 · 5/8 司违例 · 三队建面 7/12/12」'
    u'「三横切病根 · 物理件积压 · 正典断更 · 簿记税」'
    u'「实弹改善 5 件 · 判据预注册 · 回访 10-16」；'
    u'图内底部来源行「基于硅基城市真实事件（审查执法双日台账档案）」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'10 月 8 日和 9 日连续两天，老板下了 34 道指令，要求对每个子公司逐个审查审计、'
    u'然后强力改善。集团内部的审查委员会同窗连开三案，全部 7/7 通过：一家游戏公司直审、'
    u'九家公司逐审、机队工作区基线。随后一道自驱执法令自查出 8 个子公司里有 5 个'
    u'「不主动找活干」的违例（审查 AI 自家也在点名册里，如实记），于是给每个子公司'
    u'建了三条自驱工作队列（条数 7/12/12），当场实弹改善 5 件事，验收判据提前注册，'
    u'定下 10 月 16 日回访检验。全部数字可在集团台账溯源。这是「城市盘点」系列第十七张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261010-DIGEST-v17 static card (cards.json + render output + e4-material.md)'}
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
