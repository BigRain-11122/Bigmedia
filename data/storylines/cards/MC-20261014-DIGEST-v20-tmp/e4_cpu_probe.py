# -*- coding: utf-8 -*-
# tech#164 E4 CPU-lane viability probe (single call, CPU-only).
# Pre-registered judging questions (state/queue/tech.md #164):
#   Q1 latency <= 600s (10 min) = CPU lane viable
#   Q2 GPU zero-touch (num_gpu=0 forced + nvidia-smi before/after snapshots)
#   Q3 verdict format consistency vs GPU-era E4 readings (same model+prompt)
# Mirrors e4_call.py (MC-20261014-DIGEST-v20) model + prompt verbatim for a
# comparable reading; API /api/generate route instead of CLI stdin pipe
# (CLI has no num_gpu/num_thread flags; API is the same backend).
# Detached-safe: self-contained file log (2026-10-14 detached-batch law),
# hard client cap 1200s, result json written next to this file.
import io, json, os, subprocess, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'e4_cpu_probe.out')
RESULT = os.path.join(HERE, 'e4_cpu_result.json')
MODEL = 'qwen2.5:14b'
CAP_S = 1200        # hard client cap: 20 min (Q1 line is 600s; headroom so a
                    # slow-but-completing call still yields a Q3 reading)
Q1_LINE_S = 600
THREADS = 4         # CEO 10% CPU reserve law compliant face (tech#164 seed)

PROMPT = ('你是一名刷公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 020》\n'
          '（1080×1080 方图·黑底；左上角小字「[AIGC·AI 生成内容]」；顶部大标题「城市盘点 020」）。\n'
          '图上写着：\n'
          '「死线冲刺日（10-13·43 行台账 18 道 CEO 令）」——这行是城市台账数字盘点：10-13 单日 43 行令批台账，其中 18 道是老板亲颁的令；\n'
          '「应该说 每个块面都要是全球一流的，」；\n'
          '「不要出来垃圾玩艺」——这两行是老板当天的原话；\n'
          '「每块全球一流律 · 闸 > 死线 · 产线母法」——公司把这句原话立成产线母法：质量闸比死线大，产出不达基准禁出厂；\n'
          '「复评 60 分 · 整改九项 · 90 分入片库门槛」——旗舰音乐片当天被老板复评 60 分，连颁九项整改令，入片库门槛提到 90 分；\n'
          '「全席调研 9/9 归笼 · 四专 41 曲全量重制立项」——九组专家调研当天全部归笼，四张早期专辑 41 首经典歌曲全量 AI 重制立项；\n'
          '「全本地验证 · CPU 常开 · 云端放开」——同日三道资源令收尾。\n'
          '图内底部声明行「基于硅基城市真实事件（死线冲刺日令批台账档案）」。\n'
          '背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。\n'
          '「城市盘点」系列是集团旗下媒体公司出品的数字盘点卡——把城市自己台账里的真实事件与数字原样盘点出来，不虚构不加工。\n'
          '本卡的背景是：10-13 是死线冲刺日——凌晨赶片到死线、迟到后手工收口、老板复评只给 60 分；\n'
          '然后一整天连颁 18 道令：整改、调研、立项；而当天最高的一道令是「每块全球一流律」——\n'
          '赶死线的日子，最高令反而是质量闸比死线大。\n'
          '请回答三个问题，每题一段，直说不委婉：\n'
          '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
          '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
          '3) 最弱的一项是什么？')


def log(msg):
    with io.open(LOG, 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + str(msg) + '\n')


def gpu_snap():
    try:
        p = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.free',
                            '--format=csv,noheader,nounits'], capture_output=True, timeout=15)
        line = p.stdout.decode('utf-8', 'replace').strip().splitlines()[0]
        parts = [x.strip() for x in line.split(',')[:3]]
        return {'util_pct': int(parts[0]), 'used_mb': int(parts[1]), 'free_mb': int(parts[2])}
    except Exception as exc:
        return {'error': repr(exc)}


log('PROBE start tech#164 E4 CPU-lane single call (model=%s num_gpu=0 num_thread=%d cap=%ds)'
    % (MODEL, THREADS, CAP_S))
gpu_before = gpu_snap()
log('GPU-BEFORE %s' % json.dumps(gpu_before))

payload = json.dumps({
    'model': MODEL,
    'prompt': PROMPT,
    'stream': False,
    'options': {'num_gpu': 0, 'num_thread': THREADS, 'num_ctx': 8192},
}).encode('utf-8')
req = urllib.request.Request('http://localhost:11434/api/generate', data=payload,
                             headers={'Content-Type': 'application/json'})

verdict = None
api_metrics = {}
error = None
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=CAP_S) as resp:
        body = json.loads(resp.read().decode('utf-8'))
    verdict = (body.get('response') or '').strip()
    for k in ('total_duration', 'load_duration', 'prompt_eval_count',
              'prompt_eval_duration', 'eval_count', 'eval_duration', 'done'):
        if k in body:
            api_metrics[k] = body[k]
except Exception as exc:
    error = repr(exc)
elapsed = int(round(time.time() - t0))

gpu_after = gpu_snap()
log('GPU-AFTER %s' % json.dumps(gpu_after))

q1 = (error is None and elapsed <= Q1_LINE_S)
q2 = ('error' not in gpu_before and 'error' not in gpu_after
      and gpu_before.get('used_mb') == gpu_after.get('used_mb'))
q3 = None
if verdict:
    has_score = any(ch.isdigit() for ch in verdict[:400])
    has_three = ('1' in verdict and '2' in verdict and '3' in verdict)
    q3 = {'len_chars': len(verdict), 'score_digit_seen': has_score,
          'numbered_answers_seen': has_three}

result = {
    'ts': time.strftime('%Y-%m-%d %H:%M:%S'),
    'probe': 'tech#164 E4 CPU-lane viability (single call)',
    'model': MODEL,
    'options': {'num_gpu': 0, 'num_thread': THREADS, 'num_ctx': 8192},
    'latency_s': elapsed,
    'q1_latency_viable': q1,
    'q1_line_s': Q1_LINE_S,
    'q2_gpu_zero_touch': q2,
    'gpu_before': gpu_before,
    'gpu_after': gpu_after,
    'q3_format_check': q3,
    'api_metrics': api_metrics,
    'error': error,
    'verdict': verdict,
}
io.open(RESULT, 'w', encoding='utf-8').write(json.dumps(result, ensure_ascii=False, indent=2))
log('DONE latency=%ds q1=%s q2=%s q3=%s error=%s -> %s'
    % (elapsed, q1, q2, q3 is not None, error, os.path.basename(RESULT)))
