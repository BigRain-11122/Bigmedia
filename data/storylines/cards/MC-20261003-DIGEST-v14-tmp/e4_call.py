# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261003-DIGEST-v14 static digest card (non-registry seat,
# direct Ollama; v13 pattern R872: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill same-round if landed,
# else next round per R517->R518 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 014》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 014」；下面七行数字盘点：'
    u'「集团令批 2026-10-02（两审计令 · 5 行决策催办）」'
    u'「检查到底是什么在大量耗费token？委员会继续开展节省云端token，加强本地算力工作」'
    u'（引号里是老板原话：老板追问到底是什么在大量耗费 token，让委员会继续开展节省云端 token、'
    u'加强本地算力的工作）'
    u'「token 三面审计 7/7 通过 · 六款续执 · 回访 10-08」'
    u'「硅基城审计三厚三薄 · 问题分级 3+4+3 · 对标七作」'
    u'「一线十定律 · 里程碑 10-09 可逛切片 · 12-31 预研」'
    u'「巡检双单 34h 静默回执窗 10-05 · 假读治本标记」；'
    u'图内底部来源行「基于硅基城市真实事件（集团令批台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'10 月 1 日深夜老板下令重点审计硅基城市的问题、对标 Steam 一线城市类游戏；10 月 2 日老板又追问'
    u'到底是什么在大量耗费 token，委员会当天收口「token 三面审计」，七席记名表决 7/7 全过，'
    u'给出六款续执方案，判据 10 月 8 日回访。硅基城问题审计当天定谳「三厚三薄」：'
    u'调研厚、正典厚、机制厚，但交付薄、可玩薄、产品闸薄，问题按严重度分成 3+4+3 三级，'
    u'对标 Steam 七款一线游戏实测和十条第一线定律，里程碑排到 10 月 9 日可逛切片、'
    u'12 月 31 日 Steam 发行预研。另有集团巡检班两单：一条生产线静默 34 小时被点名，'
    u'要求 10 月 5 日前交自检回执；一条是巡检探针把过期旧数据当新读数的假读问题，'
    u'当场立了治本标记。全部数字可在集团台账溯源。这是「城市盘点」系列第十四张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261003-DIGEST-v14 static card (cards.json + render output)'}
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
