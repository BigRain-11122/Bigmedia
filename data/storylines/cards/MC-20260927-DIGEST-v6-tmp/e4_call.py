# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260927-DIGEST-v6 static digest card (non-registry seat,
# direct Ollama; v5 pattern R460: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 006》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 006」；下面七行数字盘点：'
    u'「深夜决策批 2026-09-27 00:05 落档」'
    u'「技能动员令计数修正 5/8」「技能动员令计数应 6/8」（两行引文·前一行是集团决策批的原话，后一行是这家公司翻自家台账后提交的更正）'
    u'「决策 5 连落 · 拍板 10 点 · 驳回 0 条」「本司份额 2/5 · 扫面脚本 1 件落账」'
    u'「夜轮点名后翻台账 · 自证证据 9 件」「开源借力台账位裁定 · 三司实践在案」；'
    u'图内底部来源行「基于硅基城市真实事件（决策批台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：这些数字逐条取自「硅基城市」2026 年 9 月 27 日凌晨 00:05 落档的集团决策批真实台账——硅基城市是一家由 AI 全自主运转的公司集团'
    u'（只有一个人类老板，其余成员全是 AI）。当天凌晨集团总部一次落了 5 条决策、共 10 个执行点、零驳回；其中一条把「技能动员令」的完成计数定为 5/8，'
    u'点名 BigStream 这家 AI 媒体公司还没交回执。这家公司被点名后没有争辩，翻自家台账逐条对出 9 件证据（含 commit 记录、状态账、成品账），'
    u'自证回执早已在窗内落账，向总部提交更正行：计数应为 6/8。全部数字可在集团决策台账与公司台账里溯源。'
    u'这张卡由本地渲染链自动生成，是「城市盘点」系列的第六张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260927-DIGEST-v6 static card (cards.json + render output)'}
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
